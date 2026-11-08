import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options=types.HttpOptions(timeout=45000),
)
MODEL = "gemini-3.5-flash-lite"

def ask_ai(prompt):
    last_error = ""
    for attempt in range(3):
        try:
            return client.models.generate_content(model=MODEL, contents=prompt).text
        except Exception as e:
            last_error = str(e)[:120]
    return "The lantern flickered. Please try again in a moment. (" + last_error + ")"

st.set_page_config(page_title="Lyric Lantern", page_icon="🏮", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Quicksand:wght@400;600&display=swap');

.stApp {
    background: radial-gradient(circle at 20% 10%, #5a2e1a 0%, #2b1510 45%, #130a08 100%);
    color: #fbe9d0;
    font-family: 'Quicksand', sans-serif;
}
#MainMenu, header, footer {visibility: hidden;}
.block-container {max-width: 1400px; padding-top: 1.2rem;}

.hero {text-align: center; padding: 1rem 0 0.5rem;}
.lantern {
    font-size: 4.5rem; display: inline-block;
    transform-origin: top center;
    animation: sway 4s ease-in-out infinite;
    filter: drop-shadow(0 0 25px #ffb347);
}
@keyframes sway {
    0%, 100% {transform: rotate(-6deg);}
    50% {transform: rotate(6deg);}
}
.title {
    font-family: 'Playfair Display', serif; font-weight: 900;
    font-size: 4.5rem; letter-spacing: 0.18em; margin: 0;
    color: #ffd89b;
    animation: glow 3s ease-in-out infinite alternate;
}
@keyframes glow {
    from {text-shadow: 0 0 12px #ff9d2e, 0 0 30px #ff7a00;}
    to {text-shadow: 0 0 28px #ffc46b, 0 0 70px #ff8c1a;}
}
.tagline {font-style: italic; opacity: 0.85; letter-spacing: 0.08em;}

.note {
    position: fixed; bottom: -40px; font-size: 1.8rem; opacity: 0.35;
    animation: floatup 14s linear infinite; pointer-events: none;
}
@keyframes floatup {
    to {transform: translateY(-115vh) rotate(25deg); opacity: 0;}
}

.card {
    background: rgba(255, 214, 153, 0.07);
    border: 1px solid rgba(255, 179, 71, 0.3);
    border-radius: 18px; padding: 1rem 1.4rem; margin-bottom: 0.8rem;
}
.glow {box-shadow: 0 0 35px rgba(255, 157, 46, 0.25);}
.card h3 {color: #ffd89b; margin: 0 0 0.3rem 0;}
.card p {margin: 0; opacity: 0.85;}

.stTabs [data-baseweb="tab"] {color: #fbe9d0; font-size: 1.05rem;}
.stTextArea label p {color: #ffd89b !important;}
.stTextArea textarea {background: #2b1a14; color: #fbe9d0; border-radius: 12px;}
.stButton > button {
    background: #ff9d2e; color: #2b1510; border: none;
    font-weight: 600; border-radius: 999px; padding: 0.5rem 1.6rem;
}
</style>

<div class="note" style="left:8%; animation-delay:0s;">🎵</div>
<div class="note" style="left:25%; animation-delay:4s;">🎶</div>
<div class="note" style="left:45%; animation-delay:8s;">🎵</div>
<div class="note" style="left:65%; animation-delay:2s;">🎶</div>
<div class="note" style="left:82%; animation-delay:6s;">🎵</div>
<div class="note" style="left:93%; animation-delay:10s;">🎶</div>

<div class="hero">
    <div class="lantern">🏮</div>
    <h1 class="title">LYRIC LANTERN</h1>
    <p class="tagline">You write the heart. AI helps with the craft.</p>
</div>
""", unsafe_allow_html=True)


def desk(name, hint, instruction, label):
    left, right = st.columns(2, gap="large")
    with left:
        st.markdown(f'<div class="card"><h3>Writing desk</h3><p>{hint}</p></div>', unsafe_allow_html=True)
        text = st.text_area(label, height=180, key=name)
        go = st.button("Light the lantern", key=name + "_btn")
    with right:
        st.markdown('<div class="card glow"><h3>Lantern glow</h3></div>', unsafe_allow_html=True)
        if go:
            if text.strip():
                with st.spinner("The lantern is glowing..."):
                    result = ask_ai(instruction + "\n\nWriter's text:\n" + text)
                st.markdown(result)
            else:
                st.info("Write something first.")
        else:
            st.caption("Your suggestions will appear here.")


RULES = " Keep it short and clear. Never copy existing songs or imitate a living writer's lyrics."
tab1, tab2, tab3, tab4, tab5 = st.tabs(["✍️ Co-Write", "🥁 Rhythm", "🎵 Rhyme", "🧹 Cliché", "🧱 Block Breaker"])
with tab1:
    desk("cowrite", "Write one line. I'll offer 3 ways to continue it.",
         "You are a songwriting co-writer. The writer gave one line. Offer 3 different directions to continue it (one emotional, one imagery-based, one with a twist), 2 lines each. Label them Direction 1, 2, 3." + RULES,
         "Your line")
with tab2:
    desk("rhythm", "Paste your verse. I'll count the syllables.",
         "Count the syllables in each line of this verse. Show every line with its count. Flag lines where the flow breaks (count very different from neighbours) and suggest a small fix." + RULES,
         "Your verse")
with tab3:
    desk("rhyme", "Type a word or line ending. I'll find rhymes.",
         "Give perfect rhymes and slant rhymes for this word or line ending, grouped by sound, with a short note on the meaning or mood of each group." + RULES,
         "Your word")
with tab4:
    desk("cliche", "Paste your lyrics. I'll spot overused phrases.",
         "Find overused or cliché phrases in these lyrics. Show each one in bold, say briefly why it is overused, and suggest a fresher image to replace it." + RULES,
         "Your lyrics")
with tab5:
    desk("block", "Stuck? Tell me where, and I'll give you a fun challenge.",
         "You are a playful songwriting coach. The writer is stuck. Give 3 fun creative constraints they can use to write a verse (for example: write a verse using only smells, or only words a child would say). Each one gets a title and a one-line example idea. Do not write the verse for them." + RULES,
         "Where are you stuck?")
    