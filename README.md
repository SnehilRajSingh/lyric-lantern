## • LYRIC LANTERN

**An AI songwriting companion that helps you write, polish, and perform your own lyrics, without writing the song for you.**

Built for **GeNarrative Clash 2026** (Phase 2: 50% MVP submission).

- **Demo video:** `<PASTE YOUR VIDEO URL HERE>`
- **Team:** **Algo-rythm**: Adrija Adhikary, Samadrita Ghosh, Snehil Raj Singh, Shivam Jain
- **Live app :** ` https://lyric-lantern-app.streamlit.app/ `

---

## • The Problem

Most AI lyric tools generate a whole song and take the creative work away from the writer. Songwriters actually get stuck on small things: a line that won't flow, a clichéd phrase, a word that won't rhyme, or a blank page. Lyric Lantern is a **co-writer, not a ghostwriter**. It nudges, critiques, and sparks ideas, while the song stays yours.

## • Features (what's built in this MVP)

| ◉ | FEATURE | What it does |
|---|---------|--------------|
| 1 | **Co-Write** | Give one line, get 3 directions to continue (emotional, imagery, twist) |
| 2 | **Rhythm** | Syllable count per line, flags where the flow breaks, suggests small fixes |
| 3 | **Rhyme** | Perfect and slant rhymes grouped by sound, with mood notes |
| 4 | **Cliché Detector** | Spots overused phrases and suggests fresher imagery |
| 5 | **Block Breaker** | Three playful creative constraints when you're stuck (never writes the verse for you) |
| 6 | **Voice Switch** | Rewrites a verse: sad↔hopeful, first↔second person |
| 7 | **Stage Mode** | Big-screen performance view with `[Am]`-style chords shown above lyrics and adjustable text size |
| 8 | **Photo to Mood** | Upload a photo and get moods, lyric imagery, and a song idea (multimodal) |
| 9 | **Chords + MIDI** | Mood and genre produce a chord progression, with downloadable chord and melody-sketch `.mid` files |
| 10 | **Hum to Melody** | Hum into the mic; pitch detection (autocorrelation, NumPy) turns it into notes and a MIDI file |
| 11 | **Collab** | Shared room code for co-writers, with live-refreshing song view and feedback |

Extras: a warm lantern-themed UI, ambient pad music toggle (Web Audio API), and sparkle sounds on button clicks.

## • Responsible-AI choices

- Every prompt tells the model **never to copy existing songs or imitate a living writer's lyrics**.
- Features are designed to **assist, not replace** the writer (e.g. Block Breaker explicitly does not write the verse).
- User text is HTML-escaped before being rendered back on the page.

## • Tech Stack

- **Frontend / App:** [Streamlit](https://streamlit.io) with custom CSS
- **AI:** Google Gemini (`gemini-3.5-flash-lite`) via the `google-genai` SDK (text and image input)
- **Audio / music:** NumPy (pitch detection), hand-built MIDI writer, Web Audio API (ambient sound)
- **Config:** `python-dotenv`

## • Project Structure

```
lyric-lantern/
├── app.py              # Main app: Gemini client, tabs 1-7, ambient audio
├── more_features.py    # Tabs 8-11: Photo Mood, Chords/MIDI, Hum, Collab
├── lantern_style.py    # Theme, CSS, sidebar "toolbox" navigation
├── requirements.txt
├── .env.example        # Template for your API key
└── .streamlit/config.toml
```

## •  Run Locally

**Requirements:** Python 3.10+ and a free [Gemini API key](https://aistudio.google.com/apikey).

```bash
git clone https://github.com/<your_username>/lyric-lantern.git
cd lyric-lantern

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env            # Windows: copy .env.example .env
# open .env and set GEMINI_API_KEY=your_real_key

streamlit run app.py
```

Then open http://localhost:8501.



## • Deploy (Streamlit Community Cloud)

1. Push the repo to GitHub (public).
2. Go to [share.streamlit.io](https://share.streamlit.io), click **New app**, and select the repo with `app.py` as the entry file.
3. Under **Advanced settings → Secrets**, add: `GEMINI_API_KEY = "your_key"`.

## ∆ Known Limitations (MVP)

- **Collab** rooms live in server memory, so they reset on restart and work on a single instance only.
- **Hum to Melody** is a rough monophonic pitch tracker. Best in a quiet room, one note at a time.
- AI replies depend on Gemini API availability and free-tier rate limits.

## • Roadmap: Finale Build (remaining 50%)

Planned for the 6-hour live building sprint at the TIU Campus finale. Each one follows the same pattern as the existing tabs: a short prompt, the Gemini call, and a rendered result.

| ◉ | PLANNED FEATURE | Idea |
|---|-----------------|------|
| 1 | **Memory-to-Song** | Describe a personal memory and get a song concept: title, mood, imagery, and a first-verse direction drawn from your own details |
| 2 | **Genre Blender** | Pick two genres (for example Baul folk and Lo-fi) and get a blended style guide covering rhythm, instruments, lyric tone, and chord ideas |
| 3 | **Bengali, Hindi and Hinglish support** | Run the writing tools (rhyme, rhythm, clichés, co-write) on lyrics in Bengali, Hindi, or mixed Hinglish, not just English |
| 4 | **Emotion Arc Map** | Paste a song and see how its emotion changes verse by verse, shown as a chart, with notes on where the arc flattens |
| 5 | **Hook Vault** | Save catchy lines and hook ideas in one place so they can be reused later |

*Beyond the finale, we would also like persistent saved songs, real multi-user collaboration with accounts, and PDF export of lyrics with chords.*

## • Team Algo-rythm

| Name | Contribution |
|------|--------------|
| **Adrija Adhikary** (Team Lead) | Project idea, Devfolio registration, team host |
| **Samadrita Ghosh** | Coding, project structure, Streamlit app development |
| **Snehil Raj Singh** | UI description and design direction, demo video voice-over |
| **Shivam Jain** | Feature suggestions, screen recording of the demo |


