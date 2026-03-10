# 🎬 AI YouTube Script Generator

<div align="center">

![Banner](https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=17,20,24&height=200&section=header&text=AI%20YouTube%20Script%20Generator&fontSize=40&fontColor=fff&animation=twinkling&fontAlignY=35&desc=Full%20Scripts%20%2B%20SEO%20Package%20in%20Seconds%20%7C%20Powered%20by%20Gemini%20AI&descAlignY=55&descSize=15)

<p>
  <img src="https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Streamlit-1.35-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/Gemini%201.5%20Flash-Free%20API-4285F4?style=for-the-badge&logo=google&logoColor=white"/>
  <img src="https://img.shields.io/badge/YouTube-Script%20%2B%20SEO-FF0000?style=for-the-badge&logo=youtube&logoColor=white"/>
  <img src="https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge"/>
</p>

<p>
  <b>Enter a topic → Get a full, ready-to-record YouTube script + complete SEO package in under 20 seconds.</b><br/>
  Hooks, transitions, CTA, timestamps, B-roll notes, titles, description, tags & thumbnail concept — all included.
</p>

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [How It Works](#-how-it-works) • [FAQ](#-faq)

</div>

---

## 🌟 Why This Project?

Writing YouTube scripts is one of the most time-consuming parts of content creation. Most creators either:
- ❌ Wing it and ramble on camera
- ❌ Spend hours writing and rewriting
- ❌ Pay expensive ghostwriters

This tool generates a **broadcast-quality, ready-to-record script** in 20 seconds — complete with a hook, structured sections, smooth transitions, and a strong CTA. Plus a full SEO package so your video actually gets found.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📜 **Full Script Generation** | Complete word-for-word scripts written to be spoken, not read |
| 🎣 **Attention-Grabbing Hook** | First 15 seconds engineered to stop the scroll |
| ⏰ **Timestamps** | Auto-generated section timestamps like `[0:00]`, `[2:30]` |
| 🎥 **B-Roll Notes** | `[B-ROLL: show X]` suggestions throughout the script |
| 🎭 **6 Tones** | Educational, Entertaining, Professional, Humorous, Motivational, Conversational |
| ⏱️ **3 Lengths** | Short (3–5 min), Medium (8–12 min), Long (15–20 min) |
| 📌 **Full SEO Package** | 3 title options, 150-word description, 15 tags, thumbnail concept, best posting time |
| 📊 **Script Stats** | Word count, estimated read/record time |
| ⬇️ **Download as .txt** | Save your script instantly |
| 🔁 **Re-generate** | Tweak tone or length and regenerate until perfect |

---

## 🖥️ Demo

```
╔══════════════════════════════════════════════════════════════════════╗
║  🎬 AI YouTube Script Generator                                      ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  Topic: "5 AI tools that will replace your workflow in 2025"        ║
║  Tone: 🔥 Motivational   Length: Medium (8-12 min)   Niche: Tech   ║
║                                                                      ║
║  ─────────────────────────────────────────────────────────────────  ║
║  📜 SCRIPT                                                          ║
║                                                                      ║
║  [0:00] HOOK                                                        ║
║  "What if I told you that 5 free tools could completely replace     ║
║  the way you work — and 90% of people have never even heard of     ║
║  them? In the next 10 minutes, I'm going to show you exactly..."   ║
║                                                                      ║
║  [B-ROLL: Show a split screen of old workflow vs. AI workflow]      ║
║                                                                      ║
║  [1:20] SECTION 1 — Tool #1: ...                                    ║
║  ...                                                                 ║
║  ─────────────────────────────────────────────────────────────────  ║
║  📌 SEO PACKAGE                                                     ║
║  Title 1: "5 AI Tools That ACTUALLY Replace Your Work (2025)"      ║
║  Tags: ai tools, productivity, automation, ...                      ║
║  Thumbnail: Bold red text "REPLACE YOUR JOB?" + shocked face       ║
╚══════════════════════════════════════════════════════════════════════╝
```

---

## 📦 Installation

### Prerequisites
- Python 3.9+ → [Download](https://www.python.org/downloads/)
- Free Gemini API key → [Get here](https://aistudio.google.com) *(no credit card)*

### Step 1 — Clone
```bash
git clone https://github.com/YOUR_USERNAME/ai-youtube-script-generator.git
cd ai-youtube-script-generator
```

### Step 2 — Virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3 — Install
```bash
pip install -r requirements.txt
```

### Step 4 — Run
```bash
streamlit run app.py
```

Opens at **http://localhost:8501** 🎉

---

## 🚀 Deploy Free (Share a Live Link)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo → click **Deploy**
4. Add your Gemini API key under **Settings → Secrets**:
```toml
GEMINI_API_KEY = "AIza..."
```

Your app is now live with a public URL — share it with anyone!

---

## 🧠 How It Works

```
┌──────────────────────────────────────────────────────┐
│  User Input                                          │
│  Topic + Tone + Length + Niche + Audience + Notes    │
└─────────────────────┬────────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────────────┐
│  Prompt Engineering Layer                            │
│  Builds a detailed system prompt with:              │
│  - Hook requirement (first 15 sec)                  │
│  - Structure: Intro → Sections → CTA               │
│  - Tone injection                                   │
│  - B-roll & timestamp instructions                  │
│  - SEO package request                              │
└─────────────────────┬────────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────────────┐
│  Gemini 1.5 Flash API                               │
│  Temperature: 0.85 (creative but coherent)          │
│  Max tokens: 4096                                   │
└─────────────────────┬────────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────────────┐
│  Output Parser                                      │
│  Splits: Script ↔ SEO Package                      │
│  Calculates: Word count, read time                  │
└──────────────────────────────────────────────────────┘
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
    📜 Script    📌 SEO Pack  📋 Copy+Download
```

---

## 🎭 Available Tones

| Tone | Best For |
|---|---|
| 🎓 Educational | Tutorials, explainers, how-tos |
| 😄 Entertaining | Vlogs, reaction videos, entertainment |
| 💼 Professional | Business, finance, career content |
| 😂 Humorous | Comedy, skits, relatable content |
| 🔥 Motivational | Self-improvement, fitness, mindset |
| 🤫 Conversational | Storytimes, opinions, podcasts |

---

## 📁 Project Structure

```
ai-youtube-script-generator/
│
├── app.py              # 🧠 Main Streamlit app — all logic
├── requirements.txt    # 📦 Just 2 dependencies
├── .gitignore          # 🚫 Excluded files
├── LICENSE             # 📄 MIT License
└── README.md           # 📖 You are here
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| [Streamlit](https://streamlit.io) | Web UI — zero frontend code needed |
| [Google Gemini 1.5 Flash](https://aistudio.google.com) | AI script generation — free tier |
| [Python re](https://docs.python.org/3/library/re.html) | Output parsing (script vs SEO split) |

Only **2 pip dependencies** — the lightest AI app stack possible.

---

## 🤔 FAQ

**Q: How good are the scripts?**
> Very good for a first draft. Gemini 1.5 Flash writes natural, spoken-style content. Most users edit 10–20% before recording.

**Q: Is the Gemini API really free?**
> Yes — 15 requests/minute and 1 million tokens/day on the free tier. That's hundreds of scripts per day at zero cost.

**Q: Can I use this for any language?**
> Technically yes — just ask in your topic/notes: "Write this script in Hindi" or "Spanish script". Gemini handles 40+ languages.

**Q: Can I remove the API key requirement?**
> Yes — replace the Gemini call with any other LLM (Ollama for fully local, or OpenAI). The prompt structure stays the same.

**Q: What niches work best?**
> Tech, Finance, Self-Improvement, and How-To channels get the best output. Very niche-specific content may need manual editing.

---

## 🗺️ Roadmap

- [ ] 🎙️ Text-to-Speech preview — hear the script read aloud before recording
- [ ] 📑 Export as formatted PDF with sections
- [ ] 🔢 Chapter markers auto-generated for YouTube
- [ ] 🌍 Multi-language script support
- [ ] 📊 Viral score estimator based on hook strength
- [ ] 🤝 Team mode — comment and edit scripts collaboratively
- [ ] 💾 Script history — save and revisit past generations

---

## 🤝 Contributing

1. Fork this repo
2. Create a branch: `git checkout -b feature/your-idea`
3. Commit: `git commit -m 'feat: your feature'`
4. Push & open a Pull Request

---

## 📄 License

MIT License — free to use, modify, and build on. See [LICENSE](LICENSE).

---

<div align="center">

**⭐ If this saved you time, star the repo — it means a lot!**

Made with ❤️ and Python

![Footer](https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=17,20,24&height=100&section=footer)

</div>
