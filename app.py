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
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11 = st.tabs(["✍️ Co-Write", "🥁 Rhythm", "🎵 Rhyme", "🧹 Cliché", "🧱 Block Breaker", "🔄 Voice Switch", "🎤 Stage Mode", "📷 Photo Mood", "🎹 Chords", "🎙️ Hum", "🤝 Collab"])

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
    import html
import re
import streamlit.components.v1 as components

st.markdown("""
<style>
.paper {background: rgba(255, 236, 200, 0.10); border: 1px solid rgba(255,179,71,0.45); border-radius: 18px; padding: 1.2rem 1.6rem; margin-top: 0.8rem; line-height: 1.8; font-size: 1.1rem; box-shadow: 0 0 35px rgba(255,157,46,0.2);}
.stage {background: #0e0705; border: 2px solid rgba(255,179,71,0.5); border-radius: 22px; padding: 2rem; text-align: center; line-height: 1.5; color: #fff1d6; font-family: 'Playfair Display', serif; margin-top: 1rem; box-shadow: 0 0 60px rgba(255,157,46,0.25);}
.chord {color: #ffb347; font-family: 'Quicksand', sans-serif; font-weight: 700; font-size: 0.6em; display: block; letter-spacing: 0.1em;}
.stRadio label p, .stSlider label p {color: #fbe9d0 !important;}
</style>
""", unsafe_allow_html=True)

with tab6:
    st.markdown('<div class="card glow"><h3>Voice Switch</h3><p>Paste a verse, pick a new angle, and hear it in a new voice.</p></div>', unsafe_allow_html=True)
    vs_text = st.text_area("Your verse", height=160, key="vs_text")
    vs_mode = st.radio("Choose the new angle", ["Sad to hopeful", "Hopeful to sad", "First person to second person", "Second person to first person"], horizontal=True, key="vs_mode")
    if st.button("Switch the voice", key="vs_btn"):
        if vs_text.strip():
            with st.spinner("The lantern is changing its voice..."):
                out = ask_ai("Rewrite this verse with this change: " + vs_mode + ". Keep the same number of lines and a similar rhythm, and keep the writer's own imagery where possible. Return only the rewritten verse." + RULES + "\n\nVerse:\n" + vs_text)
            st.caption("The new voice")
            st.markdown('<div class="paper">' + html.escape(out).replace("\n", "<br>") + '</div>', unsafe_allow_html=True)
        else:
            st.info("Paste a verse first.")

with tab7:
    st.markdown('<div class="card glow"><h3>Stage Mode</h3><p>Paste your finished song. Put chords in brackets like [Am], then perform from the big screen.</p></div>', unsafe_allow_html=True)
    song = st.text_area("Your finished song", height=200, key="stage_text")
    size = st.slider("Text size", 24, 80, 44, key="stage_size")
    if song.strip():
        safe = html.escape(song)
        safe = re.sub(r"\[(.*?)\]", r'<span class="chord">\1</span>', safe)
        safe = safe.replace("\n", "<br>")
        st.markdown('<div class="stage" style="font-size:' + str(size) + 'px">' + safe + '</div>', unsafe_allow_html=True)
    else:
        st.caption("Your stage view will appear here.")

components.html("""
<script>
function boot() {
  if (document.getElementById('lantern-music-btn')) { return; }
  var ctx = null, master = null, on = false, timer = null, idx = 0;
  var chords = [[220, 261.63, 329.63], [174.61, 261.63, 349.23], [196, 261.63, 329.63], [196, 246.94, 293.66]];
  function ensure() {
    if (!ctx) {
      var AC = window.AudioContext || window.webkitAudioContext;
      ctx = new AC();
      master = ctx.createGain();
      master.gain.value = 0.9;
      master.connect(ctx.destination);
    }
    if (ctx.state === 'suspended') { ctx.resume(); }
  }
  function pad(freq, t, dur) {
    var o = ctx.createOscillator(), g = ctx.createGain(), f = ctx.createBiquadFilter();
    o.type = 'sine'; o.frequency.value = freq;
    f.type = 'lowpass'; f.frequency.value = 900;
    g.gain.setValueAtTime(0.0001, t);
    g.gain.linearRampToValueAtTime(0.03, t + 2);
    g.gain.linearRampToValueAtTime(0.0001, t + dur);
    o.connect(f); f.connect(g); g.connect(master);
    o.start(t); o.stop(t + dur + 0.1);
  }
  function chord() {
    var t = ctx.currentTime + 0.05, c = chords[idx % chords.length];
    idx++;
    for (var k = 0; k < c.length; k++) {
      pad(c[k], t, 7); pad(c[k] * 1.003, t, 7); pad(c[k] / 2, t, 7);
    }
  }
  function sparkle() {
    ensure();
    var notes = [1318.5, 1568, 2093, 2637], t = ctx.currentTime;
    for (var k = 0; k < notes.length; k++) {
      var o = ctx.createOscillator(), g = ctx.createGain(), s = t + k * 0.07;
      o.type = 'sine'; o.frequency.value = notes[k];
      g.gain.setValueAtTime(0.0001, s);
      g.gain.exponentialRampToValueAtTime(0.12, s + 0.01);
      g.gain.exponentialRampToValueAtTime(0.0001, s + 0.45);
      o.connect(g); g.connect(master);
      o.start(s); o.stop(s + 0.5);
    }
  }
  var btn = document.createElement('button');
  btn.id = 'lantern-music-btn';
  btn.textContent = '🔈 Music off';
  btn.style.cssText = 'position:fixed;top:14px;right:18px;z-index:99999;background:#ff9d2e;color:#2b1510;border:none;border-radius:999px;padding:8px 16px;font-weight:600;cursor:pointer;box-shadow:0 0 18px rgba(255,157,46,0.5);';
  btn.onclick = function (e) {
    e.stopPropagation();
    ensure();
    on = !on;
    if (on) {
      master.gain.setTargetAtTime(0.9, ctx.currentTime, 0.2);
      chord();
      timer = setInterval(chord, 6000);
      btn.textContent = '🔊 Music on';
    } else {
      clearInterval(timer);
      master.gain.setTargetAtTime(0.0001, ctx.currentTime, 0.5);
      btn.textContent = '🔈 Music off';
    }
    sparkle();
  };
  document.body.appendChild(btn);
  document.addEventListener('click', function (e) {
    var b = e.target.closest ? e.target.closest('button') : null;
    if (!b || b.id === 'lantern-music-btn') { return; }
    if (b.closest('[data-testid="stButton"]') || b.closest('.stButton')) { sparkle(); }
  }, true);
}
var P = window.parent;
if (!P.document.getElementById('lantern-audio-js')) {
  var s = P.document.createElement('script');
  s.id = 'lantern-audio-js';
  s.textContent = '(' + boot.toString() + ')();';
  P.document.head.appendChild(s);
}
</script>
""", height=0)
import more_features
more_features.add_more([tab8, tab9, tab10, tab11], ask_ai, client, types, MODEL, RULES)