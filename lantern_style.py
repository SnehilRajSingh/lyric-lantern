import streamlit as st

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Almendra:wght@400;700&family=Caveat:wght@500;700&family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Jost:wght@400;500&family=Josefin+Sans:wght@300;400;500&family=Lora:ital,wght@0,400;0,600;1,400&family=Playfair+Display:wght@400;500;600&family=Special+Elite&display=swap');

.stApp {
  background-color: #f6dcb0;
  background-image:
    radial-gradient(ellipse 70% 50% at 50% -5%, rgba(255,238,196,0.95), transparent 70%),
    linear-gradient(160deg, #fbe6c2 0%, #f5d3a2 55%, #eebf8c 100%);
  background-attachment: fixed;
  color: #3b2a20;
  font-family: 'Lora', serif;
}
#MainMenu, header, footer {visibility: hidden;}
.block-container {
  max-width: none !important; padding: 1rem 2.5rem 4rem 2.5rem !important;
  transition: padding 0.35s ease;
}

.hero {text-align: center; padding: 0.5rem 0 1.4rem; position: relative;}
.hero::before {
  content: ""; position: absolute; left: 50%; top: -20px; width: 480px; height: 320px;
  transform: translateX(-50%); pointer-events: none;
  background: radial-gradient(ellipse, rgba(255,205,120,0.65), transparent 70%);
}
.hero > * {position: relative;}
.lantern {
  font-size: 6.5rem; line-height: 1.1; display: inline-block; transform-origin: top center;
  animation: sway 4.5s ease-in-out infinite;
  filter: drop-shadow(0 12px 16px rgba(181,80,47,0.35));
}
@keyframes sway {
  0%, 100% {transform: rotate(-6deg);}
  50% {transform: rotate(6deg);}
}
.stApp .title {
  font-family: 'Papyrus', 'Almendra', 'Cormorant Garamond', fantasy; font-weight: 700;
  font-size: 4.8rem; line-height: 1.05; margin: 0.1rem 0 0; padding: 0; color: #3b2a20;
  letter-spacing: 0.08em; text-shadow: 1px 2px 0 rgba(217,164,65,0.55);
}
.stApp .title::after {
  content: ""; display: block; height: 7px; width: min(460px, 62%); margin: 0.5rem auto 0;
  background:
    linear-gradient(90deg, transparent, #7a4a2e 12%, #7a4a2e 88%, transparent) top / 100% 1.5px no-repeat,
    linear-gradient(90deg, transparent, #7a4a2e 12%, #7a4a2e 88%, transparent) bottom / 100% 1.5px no-repeat;
}
.stApp .tagline {
  font-family: 'Cormorant Garamond', serif; font-style: italic; font-weight: 600;
  font-size: 1.35rem; color: #6b4a35; margin-top: 0.7rem;
}

.st-key-toolbar {
  position: fixed; top: 0; left: 0; bottom: 0; width: min(290px, 82vw); height: 100vh; z-index: 1000;
  overflow-y: auto; box-sizing: border-box; padding: 1.4rem 0 6rem;
  background: linear-gradient(180deg, rgba(122,80,52,0.95), rgba(90,57,37,0.95));
  box-shadow: 0 0 34px rgba(60,35,20,0.28); transition: transform 0.35s ease;
}
.st-key-toolbar::before {
  content: "Toolbox"; display: block; font-size: 2.1rem; color: #f3d9a0;
  font-family: 'Papyrus', 'Almendra', 'Cormorant Garamond', fantasy;
  margin: 0 1.5rem 0.8rem; padding-bottom: 0.5rem; border-bottom: 1px solid rgba(255,238,205,0.2);
}
.stApp .st-key-toolbar [data-testid="stElementContainer"],
.stApp .st-key-toolbar .stButton {width: 100% !important;}
.stApp .st-key-toolbar .stButton > button {
  width: 100%; justify-content: flex-start; text-align: left;
  background: transparent !important; border: none !important;
  border-bottom: 1px solid rgba(255,238,205,0.14) !important; border-radius: 0 !important;
  box-shadow: none !important; transform: none !important; padding: 0.7rem 1.5rem !important;
  transition: background 0.2s, padding-left 0.2s;
}
.stApp .st-key-toolbar .stButton > button div {width: 100%; text-align: left;}
.stApp .st-key-toolbar .stButton > button p {
  font-family: 'The Seasons', 'Playfair Display', 'Bodoni Moda', serif !important;
  font-weight: 400 !important; font-size: 1.25rem !important; letter-spacing: 0.01em;
  color: #f8e9cc !important; margin: 0; text-align: left;
}
.stApp .st-key-toolbar .stButton > button:hover {
  background: rgba(255,238,205,0.12) !important; padding-left: 1.9rem !important;
  transform: none !important; box-shadow: none !important;
}
.stApp .st-key-toolbar .stButton > button:active {transform: none !important; box-shadow: none !important;}

.st-key-tbhandle {
  position: fixed; top: 1.1rem; left: 0; z-index: 1100; width: auto; transition: left 0.35s ease;
}
.stApp .st-key-tbhandle .stButton > button {
  background: #d9a441; border: 2px solid #3b2a20; border-left: none;
  border-radius: 0 12px 12px 0; padding: 0.45rem 1rem 0.45rem 0.8rem;
  box-shadow: 3px 3px 0 rgba(59,42,32,0.55);
}
.stApp .st-key-tbhandle .stButton > button p {
  font-family: 'Playfair Display', serif !important; font-weight: 500 !important;
  font-size: 1.05rem !important; color: #3b2a20 !important;
}

.stApp [class*="st-key-page_"] {
  background-color: rgba(255,249,238,0.72);
  border: 1.5px solid #3b2a20; border-radius: 8px 14px 9px 12px;
  box-shadow: 5px 6px 0 rgba(59,42,32,0.55); padding: 1.8rem 1.8rem 2rem;
  animation: pageIn 0.45s ease both;
}
@keyframes pageIn {
  from {opacity: 0; transform: translateY(10px);}
  to {opacity: 1; transform: none;}
}
.stApp [class*="st-key-page_"] [data-testid="stMarkdownContainer"] p,
.stApp [class*="st-key-page_"] [data-testid="stMarkdownContainer"] li {
  font-family: 'Cormorant Garamond', serif; font-weight: 600; font-size: 1.25rem;
  line-height: 1.55; color: #3b2a20;
}
.stApp [data-testid="stCaptionContainer"] {
  font-family: 'Lora', serif; font-style: italic; color: #6b4a35;
}

.stApp .card {
  position: relative; background: #fff0c2; border: 1.5px solid #3b2a20;
  border-radius: 3px 7px 4px 8px; padding: 0.9rem 1.2rem 1rem; margin: 0.4rem 0 1rem;
  box-shadow: 3px 4px 0 rgba(59,42,32,0.8); transform: rotate(-0.8deg);
}
.stApp .card.glow {background: #f9d9c2; transform: rotate(0.7deg);}
.stApp .card::before, .stApp .step::before {
  content: ""; position: absolute; top: -11px; left: calc(50% - 40px); width: 80px; height: 20px;
  background: rgba(125,143,105,0.55); transform: rotate(-3deg);
}
.stApp .card h3 {
  font-family: 'Papyrus', 'Almendra', 'Cormorant Garamond', fantasy; font-weight: 700;
  font-size: 1.6rem; color: #b5502f; margin: 0 0 0.15rem; padding: 0; line-height: 1.15;
}
.stApp [class*="st-key-page_"] .card p {
  font-family: 'Lora', serif; font-weight: 400; font-style: italic; font-size: 0.95rem;
  line-height: 1.5; margin: 0; color: #4d3727;
}

.stApp .home-title {
  font-family: 'Papyrus', 'Almendra', 'Cormorant Garamond', fantasy; font-weight: 700;
  font-size: 2.4rem; margin: 0; padding: 0; color: #3b2a20; line-height: 1.1;
}
.stApp [class*="st-key-page_"] p.home-sub {
  font-family: 'Caveat', cursive; font-weight: 700; font-size: 1.4rem; color: #b5502f; margin: 0.2rem 0 0;
}
.stApp [class*="st-key-page_"] p.home-text {
  font-family: 'Cormorant Garamond', serif; font-weight: 600; font-size: 1.15rem; margin-top: 0.9rem;
}
.stApp .steps {display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.3rem; margin: 1.5rem 0 1.1rem;}
.stApp .step {
  position: relative; background: #fff0c2; border: 1.5px solid #3b2a20;
  border-radius: 3px 7px 4px 8px; padding: 0.9rem 1.1rem; box-shadow: 3px 4px 0 rgba(59,42,32,0.8);
}
.stApp .step.s1 {transform: rotate(-1.2deg);}
.stApp .step.s2 {background: #f9d9c2; transform: rotate(0.8deg);}
.stApp .step.s3 {background: #e6e9cf; transform: rotate(-0.6deg);}
.stApp .step h4 {
  font-family: 'Papyrus', 'Almendra', 'Cormorant Garamond', fantasy; font-weight: 700;
  font-size: 1.15rem; margin: 0 0 0.2rem; padding: 0; color: #b5502f;
}
.stApp [class*="st-key-page_"] .step p {
  font-family: 'Lora', serif; font-weight: 400; font-style: italic; font-size: 0.88rem; margin: 0; line-height: 1.5;
}
.stApp [class*="st-key-page_"] p.promise {
  font-family: 'Caveat', cursive; font-weight: 700; font-size: 1.3rem; color: #5a3b27;
  border-top: 1.5px dashed rgba(59,42,32,0.4); padding-top: 0.7rem; margin-top: 0.5rem;
}

.stApp div[data-baseweb="textarea"], .stApp div[data-baseweb="input"] {
  background: #fff6df !important; border: 1.5px solid #3b2a20 !important;
  border-radius: 5px 9px 6px 10px !important;
}
.stApp textarea, .stApp input[type="text"] {
  background: transparent !important; color: #3b2a20 !important;
  font-family: 'Caveat', 'Lora', serif !important; font-size: 1.4rem !important;
}
.stApp [data-testid="stWidgetLabel"] p {
  font-family: 'Special Elite', monospace !important; font-size: 0.85rem !important;
  color: #6b4a35 !important; letter-spacing: 0.04em;
}
.stApp [class*="st-key-page_"] .stRadio label p,
.stApp [class*="st-key-page_"] .stSlider label p {color: #3b2a20 !important;}

.stApp .stButton > button, .stApp .stDownloadButton > button {
  background: #d9a441; color: #3b2a20; border: 2px solid #3b2a20;
  border-radius: 4px 9px 5px 10px; padding: 0.4rem 1.4rem; box-shadow: 3px 3px 0 #3b2a20;
  transition: transform 0.08s, box-shadow 0.08s;
}
.stApp .stButton > button p, .stApp .stDownloadButton > button p {
  font-family: 'Cormorant Garamond', serif !important; font-weight: 700 !important;
  font-size: 1.2rem !important; color: #3b2a20 !important; margin: 0;
}
.stApp .stButton > button:hover, .stApp .stDownloadButton > button:hover {
  background: #e3b255; transform: translate(-1px, -1px); box-shadow: 4px 4px 0 #3b2a20;
}
.stApp .stButton > button:active, .stApp .stDownloadButton > button:active {
  transform: translate(2px, 2px); box-shadow: 1px 1px 0 #3b2a20;
}

.stApp .paper {
  background: #fff6df !important; border: 1.5px solid #3b2a20 !important;
  border-radius: 4px 9px 5px 10px !important; box-shadow: 4px 5px 0 rgba(59,42,32,0.85) !important;
  color: #3b2a20 !important; font-family: 'Caveat', 'Lora', serif !important;
  font-size: 1.6rem !important; line-height: 1.5 !important; padding: 0.9rem 1.4rem !important;
}
.stApp .stage {
  background: #2a1d17 !important; color: #fff1d6 !important; border: 3px solid #3b2a20 !important;
  border-radius: 8px 14px 9px 13px !important; box-shadow: 7px 8px 0 rgba(59,42,32,0.6) !important;
  font-family: 'Caveat', 'Lora', serif !important;
}
.stApp .stage .chord {
  color: #e8b24a !important; font-family: 'Special Elite', monospace !important;
}

#lantern-audio-box {
  top: auto !important; right: auto !important; left: 18px !important; bottom: 18px !important;
  background: #fff6df !important; border: 2px solid #3b2a20 !important;
  border-radius: 5px 10px 6px 11px !important; box-shadow: 3px 3px 0 #2f1f15 !important;
}
#lantern-music-btn {
  background: #d9a441 !important; color: #3b2a20 !important; border: 2px solid #3b2a20 !important;
  border-radius: 4px 8px 5px 9px !important; font-family: 'Cormorant Garamond', serif !important;
  font-weight: 700 !important; font-size: 1.05rem !important;
}

@media (max-width: 900px) {
  .block-container {padding: 1rem 1rem 4rem !important;}
  .stApp .steps {grid-template-columns: 1fr;}
}
.stApp .title {
  font-family: 'NT Lamore', 'Jost', 'Outfit', sans-serif; font-weight: 500;
  font-size: 4.2rem; letter-spacing: 0.14em;
}
.stApp .st-key-toolbar .stButton > button p {
  font-family: 'Chaste', 'Josefin Sans', sans-serif !important; font-weight: 400 !important;
  font-size: 1.15rem !important; letter-spacing: 0.05em;
}
.stApp textarea, .stApp input[type="text"] {
  font-family: 'Mapalie', 'Cormorant Garamond', serif !important; font-style: italic;
  font-synthesis: none; font-weight: 600; font-size: 1.5rem !important;
}
html {font-size: 17px !important;}
.block-container {padding-top: 0.5rem !important; padding-bottom: 2rem !important;}

.hero {padding: 0.1rem 0 0.6rem;}
.hero::before {
  width: 380px; height: 240px; top: -20px; animation: haloPulse 3s ease-in-out infinite;
}
@keyframes haloPulse {
  0%, 100% {opacity: 0.65;}
  50% {opacity: 1;}
}
.lantern {
  font-size: 5.6rem; line-height: 1.1;
  animation: sway 4.5s ease-in-out infinite, lanternGlow 3s ease-in-out infinite;
}
@keyframes lanternGlow {
  0%, 100% {filter: drop-shadow(0 0 8px rgba(255,166,60,0.55)) drop-shadow(0 0 22px rgba(255,140,40,0.35));}
  50% {filter: drop-shadow(0 0 18px rgba(255,196,90,0.95)) drop-shadow(0 0 48px rgba(255,150,40,0.7));}
}
.stApp .title {font-size: 3.1rem; margin: 0;}
.stApp .title::after {margin-top: 0.35rem;}
.stApp .tagline {font-size: 1.1rem; margin-top: 0.35rem;}

.notes {position: fixed; inset: 0; overflow: hidden; pointer-events: none; z-index: 0; opacity: 0.13;}
.notes span {
  position: absolute; bottom: -70px; color: #6b4630; font-family: 'Cormorant Garamond', serif;
  animation-name: noteRise; animation-timing-function: linear; animation-iteration-count: infinite;
}
@keyframes noteRise {
  0% {transform: translate(0, 0) rotate(-12deg); opacity: 0;}
  8% {opacity: 1;}
  50% {transform: translate(22px, -55vh) rotate(8deg);}
  92% {opacity: 1;}
  100% {transform: translate(-14px, -120vh) rotate(16deg); opacity: 0;}
}
@media (prefers-reduced-motion: reduce) {
  .notes span, .lantern, .hero::before {animation: none;}
}

.st-key-toolbar::before {font-size: 1.7rem; margin-bottom: 0.5rem;}
.stApp .st-key-toolbar .stButton > button {padding: 0.5rem 1.4rem !important;}
.stApp .st-key-toolbar .stButton > button p {font-size: 1.05rem !important;}
.stApp .st-key-tbhandle .stButton > button p {font-size: 0.95rem !important;}

.stApp [class*="st-key-page_"] {padding: 1.1rem 1.4rem 1.3rem; gap: 0.55rem;}
.stApp [class*="st-key-page_"] [data-testid="stVerticalBlock"] {gap: 0.5rem;}
.stApp [class*="st-key-page_"] [data-testid="stHorizontalBlock"] {gap: 1.2rem;}
.stApp [class*="st-key-page_"] [data-testid="stMarkdownContainer"] p,
.stApp [class*="st-key-page_"] [data-testid="stMarkdownContainer"] li {font-size: 1.08rem; line-height: 1.42;}

.stApp .card {padding: 0.6rem 1rem 0.7rem; margin: 0.3rem 0 0.6rem;}
.stApp .card h3 {font-size: 1.35rem;}
.stApp [class*="st-key-page_"] .card p {font-size: 0.85rem; line-height: 1.4;}

.stApp .home-title {font-size: 1.9rem;}
.stApp [class*="st-key-page_"] p.home-sub {font-size: 1.15rem;}
.stApp [class*="st-key-page_"] p.home-text {font-size: 1rem; margin-top: 0.5rem;}
.stApp .steps {margin: 1rem 0 0.8rem; gap: 1rem;}
.stApp .step {padding: 0.65rem 0.9rem;}
.stApp .step h4 {font-size: 1rem;}
.stApp [class*="st-key-page_"] .step p {font-size: 0.8rem;}
.stApp [class*="st-key-page_"] p.promise {font-size: 1.1rem; padding-top: 0.5rem;}

.stApp [data-testid="stWidgetLabel"] p {font-size: 0.75rem !important;}
.stApp textarea, .stApp input[type="text"] {font-size: 1.25rem !important;}
.stApp .stButton > button, .stApp .stDownloadButton > button {padding: 0.3rem 1.1rem;}
.stApp .stButton > button p, .stApp .stDownloadButton > button p {font-size: 1rem !important;}
.stApp .paper {font-size: 1.3rem !important; line-height: 1.35 !important; padding: 0.6rem 1.1rem !important;}

#lantern-music-btn {font-size: 0.95rem !important; padding: 5px 12px !important;}
"""

HERO = """
<div class="hero">
<div class="lantern">🏮</div>
<h1 class="title">LYRIC LANTERN</h1>
<p class="tagline">You write the heart. AI helps with the craft.</p>
</div>
<div class="notes"><span style="left:3%;font-size:2.0rem;animation-delay:-12s;animation-duration:26s">♪</span><span style="left:9%;font-size:1.5rem;animation-delay:-7s;animation-duration:30s">♫</span><span style="left:16%;font-size:2.6rem;animation-delay:-14s;animation-duration:28s">♩</span><span style="left:24%;font-size:1.8rem;animation-delay:-3s;animation-duration:32s">♬</span><span style="left:33%;font-size:2.2rem;animation-delay:-11s;animation-duration:27s">♪</span><span style="left:41%;font-size:1.6rem;animation-delay:-19s;animation-duration:31s">♫</span><span style="left:50%;font-size:2.4rem;animation-delay:-5s;animation-duration:29s">♬</span><span style="left:58%;font-size:1.7rem;animation-delay:-16s;animation-duration:33s">♩</span><span style="left:66%;font-size:2.1rem;animation-delay:-9s;animation-duration:26s">♪</span><span style="left:74%;font-size:1.5rem;animation-delay:-22s;animation-duration:30s">♫</span><span style="left:81%;font-size:2.5rem;animation-delay:-2s;animation-duration:28s">♬</span><span style="left:88%;font-size:1.9rem;animation-delay:-13s;animation-duration:32s">♩</span><span style="left:94%;font-size:2.2rem;animation-delay:-6s;animation-duration:27s">♪</span><span style="left:46%;font-size:1.4rem;animation-delay:-25s;animation-duration:34s">♫</span></div>
"""

HOME = """
<div class="home">
<h2 class="home-title">Welcome in</h2>
<p class="home-sub">Pull up a chair. The lantern is lit.</p>
<p class="home-text">Lyric Lantern is a quiet corner for songwriters who get stuck between a spark and a finished song. You bring the heart of the song. The lantern helps with rhythm, rhyme, stuck moments and more.</p>
<div class="steps">
<div class="step s1"><h4>Pick a tool</h4><p>Open the toolbox on the left.</p></div>
<div class="step s2"><h4>Write your lines</h4><p>A line, a verse, a photo or a hum.</p></div>
<div class="step s3"><h4>Light the lantern</h4><p>Ideas come back. You decide what stays.</p></div>
</div>
<p class="promise">AI suggests, the artist decides. We never copy existing songs or imitate a living writer's lyrics.</p>
</div>
"""


def apply():
    st.markdown("<style>" + CSS + "</style>", unsafe_allow_html=True)
    st.markdown(HERO, unsafe_allow_html=True)


def _pick(i):
    st.session_state["tool_idx"] = i
    st.session_state["tb_open"] = (i == 0)


def _toggle():
    st.session_state["tb_open"] = not st.session_state["tb_open"]


def pages(names):
    labels = ["Home"] + list(names)
    st.session_state.setdefault("tool_idx", 0)
    st.session_state.setdefault("tb_open", True)
    idx = st.session_state["tool_idx"]
    is_open = st.session_state["tb_open"]

    css = ",".join(".st-key-page_" + str(i) for i in range(len(labels)) if i != idx)
    css += "{display:none !important;}"
    css += ".stApp .st-key-tool_" + str(idx) + " .stButton > button{background:rgba(217,164,65,0.92) !important;border-bottom-color:transparent !important;padding-left:1.9rem !important;}"
    css += ".stApp .st-key-tool_" + str(idx) + " .stButton > button p{color:#2f1f15 !important;font-weight:500 !important;}"
    if is_open:
        css += ".st-key-tbhandle{left:min(290px,82vw);}"
        css += "@media (min-width:901px){.block-container{padding-left:330px !important;}}"
    else:
        css += ".st-key-toolbar{transform:translateX(-105%);pointer-events:none;box-shadow:none;}"
        css += ".st-key-tbhandle{left:0;}"

    with st.container(key="tbhandle"):
        st.button("Hide" if is_open else "Tools", key="tb_toggle", on_click=_toggle)
    with st.container(key="toolbar"):
        for i, label in enumerate(labels):
            st.button(label, key="tool_" + str(i), on_click=_pick, args=(i,))
        st.markdown("<style>" + css + "</style>", unsafe_allow_html=True)
    boxes = [st.container(key="page_" + str(i)) for i in range(len(labels))]
    with boxes[0]:
        st.markdown(HOME, unsafe_allow_html=True)
        st.button("Start with " + names[0], key="home_go", on_click=_pick, args=(1,))
    return boxes[1:]