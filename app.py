import streamlit as st
import google.generativeai as genai
import time
import re
from datetime import datetime

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI YouTube Script Generator",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main { background-color: #0a0a0f; }

    .hero {
        background: linear-gradient(135deg, #1a0533 0%, #0d0d1a 50%, #001a33 100%);
        border: 1px solid #2a1a4a;
        border-radius: 16px;
        padding: 36px 40px;
        margin-bottom: 28px;
        text-align: center;
    }
    .hero h1 { font-size: 42px; font-weight: 700; margin: 0 0 8px; color: #ffffff; }
    .hero p  { color: #8892b0; font-size: 16px; margin: 0; }

    .section-card {
        background: #0f0f1a;
        border: 1px solid #1e1e3a;
        border-radius: 12px;
        padding: 24px 28px;
        margin-bottom: 20px;
    }
    .section-title {
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #a855f7;
        margin-bottom: 16px;
    }

    .script-block {
        background: #080810;
        border: 1px solid #1e1e3a;
        border-left: 4px solid #a855f7;
        border-radius: 10px;
        padding: 20px 24px;
        font-size: 15px;
        line-height: 1.85;
        color: #d4d4f0;
        white-space: pre-wrap;
        font-family: 'Georgia', serif;
    }

    .tag-chip {
        display: inline-block;
        background: #1a0a2e;
        border: 1px solid #4a1a8a;
        color: #c084fc;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin: 3px;
    }

    .stat-box {
        background: linear-gradient(135deg, #12002a, #001020);
        border: 1px solid #2a1a4a;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
    }
    .stat-val   { font-size: 26px; font-weight: 700; color: #a855f7; }
    .stat-label { font-size: 11px; color: #6b7280; text-transform: uppercase; letter-spacing: 1px; margin-top: 4px; }

    .tip-box {
        background: #0a1a0a;
        border-left: 3px solid #22c55e;
        border-radius: 8px;
        padding: 12px 16px;
        font-size: 13px;
        color: #86efac;
        margin: 6px 0;
    }

    div.stButton > button {
        background: linear-gradient(135deg, #7c3aed, #a855f7);
        color: white;
        font-weight: 700;
        border: none;
        border-radius: 10px;
        padding: 14px 28px;
        font-size: 16px;
        width: 100%;
        letter-spacing: 0.5px;
        transition: opacity 0.2s;
    }
    div.stButton > button:hover { opacity: 0.85; }

    .stTextInput input, .stTextArea textarea, .stSelectbox div {
        background: #0f0f1a !important;
        border-color: #2a2a4a !important;
        color: #e2e8f0 !important;
    }
    .stSlider .stSlider { color: #a855f7; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎬 Script Generator")
    st.markdown("---")

    st.markdown("### 🔑 Gemini API Key")
    api_key = st.text_input(
        "Free Gemini API Key",
        type="password",
        placeholder="AIza...",
        help="Get FREE at https://aistudio.google.com"
    )
    if not api_key:
        st.info("🆓 Get a **free** Gemini API key at [aistudio.google.com](https://aistudio.google.com) — no credit card needed!")

    st.markdown("---")
    st.markdown("### 🎯 Script Types")
    st.markdown("""
- **Tutorial** — Step-by-step how-to
- **Listicle** — Top N countdown
- **Explainer** — Deep-dive educational  
- **Storytime** — Personal narrative
- **Review** — Product/service critique
- **Motivational** — Inspire & energize
    """)
    st.markdown("---")
    st.markdown("### 📊 What You Get")
    st.markdown("""
✅ Full script with timestamps  
✅ Hook & strong CTA  
✅ SEO title suggestions  
✅ Description + hashtags  
✅ Thumbnail idea  
✅ Word count & read time  
    """)

# ── Helpers ────────────────────────────────────────────────────────────────────
TONE_OPTIONS = {
    "🎓 Educational":    "educational, clear, and authoritative — like a knowledgeable teacher",
    "😄 Entertaining":   "fun, energetic, and entertaining — like a popular entertainer",
    "💼 Professional":   "professional, polished, and credible — like a business presenter",
    "😂 Humorous":       "humorous, witty, and light-hearted — with jokes and playful language",
    "🔥 Motivational":   "high-energy, motivational, and inspiring — like a life coach",
    "🤫 Conversational": "casual, conversational, and relatable — like talking to a friend",
}

NICHE_OPTIONS = [
    "Technology & AI", "Personal Finance", "Health & Fitness", "Self Improvement",
    "Travel & Adventure", "Food & Cooking", "Gaming", "Science & Education",
    "Business & Entrepreneurship", "Beauty & Fashion", "Parenting", "Sports",
    "Politics & News", "Environment", "Art & Design", "Music", "Other",
]

DURATION_MAP = {
    "Short (3–5 min)":   ("3–5 minute", 500,  750),
    "Medium (8–12 min)": ("8–12 minute", 1200, 1800),
    "Long (15–20 min)":  ("15–20 minute", 2000, 3000),
}

def count_words(text: str) -> int:
    return len(text.split())

def estimate_read_time(word_count: int) -> str:
    minutes = word_count / 130  # avg speaking pace
    if minutes < 1:
        return "< 1 min"
    return f"{minutes:.1f} min"

def build_prompt(topic, tone_key, niche, duration_key, audience, extra_notes, include_broll, include_timestamps) -> str:
    tone_desc = TONE_OPTIONS[tone_key]
    dur_label, _, _ = DURATION_MAP[duration_key]

    broll_instruction = ""
    if include_broll:
        broll_instruction = "\n- Add [B-ROLL: description] notes throughout suggesting relevant footage to show on screen."

    timestamp_instruction = ""
    if include_timestamps:
        timestamp_instruction = "\n- Add approximate timestamps like [0:00], [0:45], [2:30] at the start of each section."

    return f"""You are an expert YouTube scriptwriter with 10+ years of experience creating viral content.

Write a complete, ready-to-record YouTube script for the following:

**TOPIC:** {topic}
**NICHE:** {niche}
**TARGET AUDIENCE:** {audience if audience else "general YouTube audience"}
**TONE:** {tone_desc}
**VIDEO LENGTH:** {dur_label} video
**EXTRA NOTES:** {extra_notes if extra_notes else "none"}

SCRIPT REQUIREMENTS:
- Start with a powerful HOOK (first 15 seconds must grab attention — use a shocking fact, bold claim, or intriguing question)
- Include a clear INTRO where you tell viewers what they'll learn
- Divide content into 3–5 clear SECTIONS with smooth transitions
- End with a strong CALL TO ACTION (subscribe, comment, like)
- Write exactly as it should be SPOKEN — natural, engaging, no bullet points in the script itself{broll_instruction}{timestamp_instruction}

AFTER THE SCRIPT, provide:

---
## 📌 SEO PACKAGE

**3 Title Options:**
1. [title option 1]
2. [title option 2]  
3. [title option 3]

**YouTube Description (150 words):**
[write the full description]

**Tags (15 tags):**
[tag1, tag2, tag3, ...]

**Thumbnail Concept:**
[describe a compelling thumbnail idea with text overlay and visual elements]

**Best Time to Post:**
[suggest best day/time based on the niche]
---

Make the script feel human, passionate, and authentic. This should be publishable immediately."""

def generate_script(prompt: str, api_key: str) -> str:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        "gemini-1.5-flash",
        generation_config={"temperature": 0.85, "max_output_tokens": 4096},
    )
    response = model.generate_content(prompt)
    return response.text

def extract_script_only(full_output: str) -> str:
    """Extract just the script portion (before the SEO package)."""
    split = re.split(r"---\s*##\s*📌\s*SEO", full_output, flags=re.IGNORECASE)
    return split[0].strip() if split else full_output

def extract_seo_only(full_output: str) -> str:
    """Extract just the SEO package."""
    split = re.split(r"---\s*##\s*📌\s*SEO", full_output, flags=re.IGNORECASE)
    return "## 📌 SEO PACKAGE\n\n" + split[1].strip() if len(split) > 1 else ""

# ── Main UI ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>🎬 AI YouTube Script Generator</h1>
  <p>Enter your topic → Get a full, ready-to-record script + SEO package in seconds</p>
</div>
""", unsafe_allow_html=True)

# ── Input form ─────────────────────────────────────────────────────────────────
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">◈ Video Details</div>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])
with col1:
    topic = st.text_input(
        "📌 Video Topic *",
        placeholder="e.g.  5 AI tools that will replace your entire workflow in 2025",
        help="Be specific — the more detail you give, the better the script"
    )
with col2:
    niche = st.selectbox("🎯 Channel Niche", NICHE_OPTIONS)

col3, col4, col5 = st.columns(3)
with col3:
    tone_key  = st.selectbox("🎭 Tone & Style", list(TONE_OPTIONS.keys()))
with col4:
    duration_key = st.selectbox("⏱️ Video Length", list(DURATION_MAP.keys()))
with col5:
    audience = st.text_input("👥 Target Audience", placeholder="e.g. beginners, developers, moms...")

col6, col7 = st.columns([2, 1])
with col6:
    extra_notes = st.text_area(
        "📝 Extra Notes (optional)",
        placeholder="e.g. Mention my sponsor XYZ, start with a personal story, avoid politics...",
        height=80,
    )
with col7:
    st.markdown("<br>", unsafe_allow_html=True)
    include_timestamps = st.checkbox("⏰ Add Timestamps", value=True)
    include_broll      = st.checkbox("🎥 Add B-Roll Notes", value=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── Generate button ────────────────────────────────────────────────────────────
generate_clicked = st.button("🚀 Generate My Script")

# ── Output ─────────────────────────────────────────────────────────────────────
if generate_clicked:
    if not api_key:
        st.error("⚠️ Please add your free Gemini API key in the sidebar first.")
    elif not topic.strip():
        st.error("⚠️ Please enter a video topic.")
    else:
        prompt = build_prompt(topic, tone_key, niche, duration_key, audience, extra_notes, include_broll, include_timestamps)

        with st.spinner("✍️ Writing your script... (takes 10–20 seconds)"):
            try:
                full_output  = generate_script(prompt, api_key)
                script_only  = extract_script_only(full_output)
                seo_only     = extract_seo_only(full_output)
                word_count   = count_words(script_only)
                read_time    = estimate_read_time(word_count)

                st.success("✅ Script generated successfully!")

                # Stats row
                st.markdown("<br>", unsafe_allow_html=True)
                s1, s2, s3, s4 = st.columns(4)
                with s1:
                    st.markdown(f'<div class="stat-box"><div class="stat-val">{word_count:,}</div><div class="stat-label">Words</div></div>', unsafe_allow_html=True)
                with s2:
                    st.markdown(f'<div class="stat-box"><div class="stat-val">{read_time}</div><div class="stat-label">Read Time</div></div>', unsafe_allow_html=True)
                with s3:
                    st.markdown(f'<div class="stat-box"><div class="stat-val">{duration_key.split()[0]}</div><div class="stat-label">Target Length</div></div>', unsafe_allow_html=True)
                with s4:
                    st.markdown(f'<div class="stat-box"><div class="stat-val">{tone_key.split()[0]}</div><div class="stat-label">Tone</div></div>', unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                # Tabs for script vs SEO
                tab1, tab2, tab3 = st.tabs(["📜 Full Script", "📌 SEO Package", "📋 Copy-Ready"])

                with tab1:
                    st.markdown('<div class="section-title">◈ Your Script</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="script-block">{script_only}</div>', unsafe_allow_html=True)

                with tab2:
                    if seo_only:
                        st.markdown(seo_only)
                    else:
                        st.markdown(full_output)

                with tab3:
                    st.markdown("**Copy the entire script below:**")
                    st.text_area(
                        label="Full script (select all → copy)",
                        value=script_only,
                        height=500,
                        label_visibility="collapsed",
                    )
                    st.download_button(
                        label="⬇️ Download Script as .txt",
                        data=full_output,
                        file_name=f"script_{topic[:30].replace(' ','_')}_{datetime.now().strftime('%Y%m%d')}.txt",
                        mime="text/plain",
                    )

                # Tips
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown('<div class="section-title">◈ Pro Tips</div>', unsafe_allow_html=True)
                for tip in [
                    "🎤 Read the script out loud before recording — edit anything that feels unnatural",
                    "⏱️ Record yourself and compare actual duration to the estimate",
                    "✂️ Cut the first 10 seconds and see if it still hooks — most intros are too slow",
                    "🔁 Re-generate with a different tone to see alternate versions",
                ]:
                    st.markdown(f'<div class="tip-box">{tip}</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Generation failed: {str(e)}\n\nCheck your API key is valid at https://aistudio.google.com")

else:
    # Empty state
    st.markdown("""
<div style="text-align:center; padding: 50px 20px; color: #4a5568;">
  <div style="font-size: 60px; margin-bottom: 16px;">🎬</div>
  <h3 style="color: #6b7280;">Fill in the details above and click Generate</h3>
  <p style="font-size: 14px;">You'll get a full script + SEO title, description, tags & thumbnail idea</p>
</div>
""", unsafe_allow_html=True)

    # Example topics
    st.markdown('<div class="section-title" style="margin-top:20px;">◈ Example Topics to Try</div>', unsafe_allow_html=True)
    examples = [
        "10 Python tricks that make you look like a pro",
        "How I saved ₹1 lakh in 6 months on a normal salary",
        "The truth about AI taking over jobs in 2025",
        "5 morning habits that changed my life completely",
        "Best budget smartphones under ₹15,000 in 2025",
    ]
    cols = st.columns(len(examples))
    for i, ex in enumerate(examples):
        with cols[i]:
            st.markdown(f'<div class="tag-chip" style="display:block;text-align:center;padding:8px 10px;font-size:11px;">{ex}</div>', unsafe_allow_html=True)
