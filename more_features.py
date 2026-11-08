import html
import io
import json
import re
import wave
from collections import Counter

import numpy as np
import streamlit as st

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
ROOTS = {"C": 0, "C#": 1, "DB": 1, "D": 2, "D#": 3, "EB": 3, "E": 4, "F": 5, "F#": 6,
         "GB": 6, "G": 7, "G#": 8, "AB": 8, "A": 9, "A#": 10, "BB": 10, "B": 11}
STOP = set("the a an and or but of to in on at is it i you me my we your with for that this be are was so as".split())


def parse_json(text):
    m = re.search(r"\{.*\}", text or "", re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except Exception:
        return None


def chord_notes(name):
    m = re.match(r"^([A-Ga-g][#b]?)(.*)$", str(name).strip())
    if not m:
        return [48, 52, 55]
    root = ROOTS.get(m.group(1).upper(), 0)
    q = m.group(2).lower()
    if q.startswith("dim"):
        iv = [0, 3, 6]
    elif q.startswith("sus"):
        iv = [0, 5, 7]
    elif q.startswith("maj"):
        iv = [0, 4, 7, 11]
    elif q.startswith("m"):
        iv = [0, 3, 7] + ([10] if "7" in q else [])
    elif "7" in q:
        iv = [0, 4, 7, 10]
    else:
        iv = [0, 4, 7]
    return [48 + root + i for i in iv]


def vlq(n):
    out = [n & 0x7F]
    n >>= 7
    while n:
        out.append((n & 0x7F) | 0x80)
        n >>= 7
    return bytes(reversed(out))


def make_midi(steps, bpm=80, velocity=80):
    tpq = 480
    track = bytearray()
    tempo = int(60000000 / max(int(bpm), 20))
    track += b"\x00\xff\x51\x03" + tempo.to_bytes(3, "big")
    pending = 0
    for notes, dur in steps:
        notes = [min(127, max(0, int(n))) for n in notes]
        if not notes:
            pending += dur
            continue
        for i, n in enumerate(notes):
            track += vlq(pending if i == 0 else 0) + bytes([0x90, n, velocity])
        pending = 0
        for i, n in enumerate(notes):
            track += vlq(dur if i == 0 else 0) + bytes([0x80, n, 0])
    track += vlq(pending) + b"\xff\x2f\x00"
    head = (b"MThd" + (6).to_bytes(4, "big") + (0).to_bytes(2, "big")
            + (1).to_bytes(2, "big") + tpq.to_bytes(2, "big"))
    return head + b"MTrk" + len(track).to_bytes(4, "big") + bytes(track)


def read_wav(data):
    with wave.open(io.BytesIO(data), "rb") as w:
        sr = w.getframerate()
        ch = w.getnchannels()
        width = w.getsampwidth()
        raw = w.readframes(w.getnframes())
    if width == 2:
        x = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    elif width == 4:
        x = np.frombuffer(raw, dtype=np.int32).astype(np.float32) / 2147483648.0
    else:
        x = (np.frombuffer(raw, dtype=np.uint8).astype(np.float32) - 128) / 128.0
    if ch > 1:
        x = x[: len(x) // ch * ch].reshape(-1, ch).mean(axis=1)
    return x, sr


def frame_pitch(frame, sr, fmin=80, fmax=800):
    frame = frame - frame.mean()
    if np.sqrt(np.mean(frame ** 2)) < 0.01:
        return None
    n = len(frame)
    spec = np.fft.rfft(frame, 2 * n)
    ac = np.fft.irfft(spec * np.conj(spec))[:n]
    if ac[0] <= 0:
        return None
    ac = ac / ac[0]
    lo = int(sr / fmax)
    hi = min(int(sr / fmin), n - 1)
    if hi <= lo:
        return None
    lag = lo + int(np.argmax(ac[lo:hi]))
    if ac[lag] < 0.5:
        return None
    return sr / lag


def hum_to_notes(x, sr):
    n = int(sr * 0.04)
    hop = max(1, n // 2)
    midis = []
    for i in range(0, len(x) - n, hop):
        f = frame_pitch(x[i:i + n], sr)
        midis.append(None if f is None else int(round(69 + 12 * np.log2(f / 440.0))))
    for i in range(1, len(midis) - 1):
        if midis[i - 1] == midis[i + 1] and midis[i] != midis[i - 1]:
            midis[i] = midis[i - 1]

    def merge(seq):
        segs = []
        for m in seq:
            if segs and segs[-1][0] == m:
                segs[-1][1] += 1
            else:
                segs.append([m, 1])
        return segs

    sec = hop / sr
    segs = merge(midis)
    segs = [[None if (m is not None and c * sec < 0.1) else m, c] for m, c in segs]
    segs = merge([m for m, c in segs for _ in range(c)])
    notes = [(m, c * sec) for m, c in segs]
    while notes and notes[0][0] is None:
        notes.pop(0)
    while notes and notes[-1][0] is None:
        notes.pop()
    return notes[:60]


def note_name(m):
    return NOTE_NAMES[m % 12] + str(m // 12 - 1)


@st.cache_resource
def shared_rooms():
    return {}


@st.fragment(run_every=3)
def live_view(room):
    box = shared_rooms().setdefault(room, {"text": "", "comments": []})
    st.markdown('<div class="card glow"><h3>Live song</h3><p>Updates every few seconds.</p></div>', unsafe_allow_html=True)
    if box["text"].strip():
        st.markdown('<div class="paper">' + html.escape(box["text"]).replace("\n", "<br>") + '</div>', unsafe_allow_html=True)
    else:
        st.caption("Nothing saved yet.")
    st.markdown("**Feedback**")
    if not box["comments"]:
        st.caption("No feedback yet.")
    for c in box["comments"][-10:]:
        st.markdown("- " + html.escape(c))


def card(title, text, glow=True):
    cls = "card glow" if glow else "card"
    st.markdown('<div class="' + cls + '"><h3>' + title + '</h3><p>' + text + '</p></div>', unsafe_allow_html=True)


def add_more(tabs, ask_ai, client, types, model, RULES):
    def ask_media(prompt, data, mime):
        last = ""
        for _ in range(2):
            try:
                r = client.models.generate_content(
                    model=model,
                    contents=[types.Part.from_bytes(data=data, mime_type=mime), prompt],
                )
                return r.text
            except Exception as e:
                last = str(e)[:120]
        return "The lantern flickered. Please try again. (" + last + ")"

    # ---------- Feature 8: Photo-to-Mood ----------
    with tabs[0]:
        left, right = st.columns(2, gap="large")
        with left:
            card("Photo to Mood", "Upload a photo and get lyric imagery, moods and a song idea.", glow=False)
            img = st.file_uploader("Your photo", type=["jpg", "jpeg", "png"], key="photo_up")
            if img is not None:
                st.image(img, width=360)
            go = st.button("Read the mood", key="photo_go")
        with right:
            card("Lantern glow", "Imagery and ideas from your photo.")
            if go:
                if img is not None:
                    with st.spinner("The lantern is looking at your photo..."):
                        out = ask_media(
                            "You are a songwriting co-writer. Look at this photo and give: 1) three moods it carries, "
                            "2) five fresh lyric images drawn from what you see, 3) one song idea with a working title "
                            "and a one-line hook concept. Keep it short." + RULES,
                            img.getvalue(), img.type or "image/jpeg")
                    st.markdown(out)
                else:
                    st.info("Upload a photo first.")
            else:
                st.caption("Your suggestions will appear here.")

    


    # ---------- Feature 10: Chord and Melody Sketch ----------
    with tabs[1]:
        left, right = st.columns(2, gap="large")
        with left:
            card("Chords and MIDI", "Pick a mood and genre. Get a chord progression and MIDI files for any music app.", glow=False)
            mood = st.text_input("Mood", value="cozy rainy night", key="ch_mood")
            genre = st.selectbox("Genre", ["Lo-fi", "Pop", "Folk", "Baul folk", "Rock", "Jazz", "Ballad"], key="ch_genre")
            go = st.button("Sketch the chords", key="ch_go")
        with right:
            card("Lantern glow", "Your chord sketch.")
            if go:
                with st.spinner("The lantern is humming chords..."):
                    raw = ask_ai('Suggest a chord progression for a ' + genre + ' song with this mood: ' + mood +
                                 '. Reply with ONLY JSON like {"key": "A minor", "bpm": 78, "chords": ["Am", "F", "C", "G"], '
                                 '"why": "one short sentence"}. Use 4 to 8 chords with simple names such as Am, F, Cmaj7, G7, Dm7.')
                data = parse_json(raw)
                if data and data.get("chords"):
                    st.session_state["ch_result"] = data
                else:
                    st.session_state.pop("ch_result", None)
                    st.warning("The lantern could not read that answer. Please try again.")
            res = st.session_state.get("ch_result")
            if res:
                chords = [str(c) for c in res.get("chords", [])][:8]
                try:
                    bpm = int(res.get("bpm", 80))
                except Exception:
                    bpm = 80
                st.markdown("**Key:** " + html.escape(str(res.get("key", "-"))) + "  |  **Tempo:** " + str(bpm) + " BPM")
                st.markdown('<div class="paper" style="text-align:center;font-size:1.6rem">' +
                            "  &rarr;  ".join(html.escape(c) for c in chords) + '</div>', unsafe_allow_html=True)
                st.caption(str(res.get("why", "")))
                chord_steps = [(chord_notes(c), 1920) for c in chords]
                melody_steps = []
                for c in chords:
                    nt = chord_notes(c)
                    for idx in [0, 1, 2, 1]:
                        melody_steps.append(([nt[idx] + 12], 480))
                st.download_button("Download chords (.mid)", make_midi(chord_steps, bpm),
                                   file_name="lyric-lantern-chords.mid", mime="audio/midi", key="dl_chords")
                st.download_button("Download melody sketch (.mid)", make_midi(melody_steps, bpm),
                                   file_name="lyric-lantern-melody.mid", mime="audio/midi", key="dl_melody")
            elif not go:
                st.caption("Your chords will appear here.")

    # ---------- Feature 11: Hum-to-Melody ----------
    with tabs[2]:
        left, right = st.columns(2, gap="large")
        with left:
            card("Hum to Melody", "Hum a tune into the mic. I will write it out as notes and a MIDI file.", glow=False)
            if hasattr(st, "audio_input"):
                audio = st.audio_input("Hum for 3 to 10 seconds, one note at a time works best", key="hum_audio")
            else:
                audio = None
                st.warning("This version of Streamlit has no microphone input. Update streamlit to use this feature.")
        with right:
            card("Lantern glow", "Your hum, written out.")
            if audio is not None:
                try:
                    x, sr = read_wav(audio.getvalue())
                    notes = hum_to_notes(x, sr)
                except Exception:
                    notes = None
                    st.warning("I could not read that recording. Please try again.")
                if notes is not None:
                    if not notes:
                        st.info("I could not hear a clear tune. Hum louder, closer to the mic, in a quiet room.")
                    else:
                        names = [("rest" if m is None else note_name(m)) for m, d in notes]
                        st.markdown('<div class="paper">' + " &middot; ".join(names) + '</div>', unsafe_allow_html=True)
                        st.caption(str(len(notes)) + " notes found. Rough pitch only, so tidy it in your music app.")
                        steps = [([] if m is None else [m], max(60, int(d * 960))) for m, d in notes]
                        st.download_button("Download melody (.mid)", make_midi(steps, 120),
                                           file_name="lyric-lantern-hum.mid", mime="audio/midi", key="dl_hum")
            else:
                st.caption("Record your hum on the left.")

    # ---------- Feature 12: Real-time Collaboration ----------
    with tabs[3]:
        left, right = st.columns(2, gap="large")
        with left:
            card("Co-write together", "Use the same room code as your co-writer. Save your lines and leave feedback.", glow=False)
            room = st.text_input("Room code", value="lantern", key="collab_room").strip().lower() or "lantern"
            me = st.text_input("Your name", value="Writer", key="collab_name")
            box = shared_rooms().setdefault(room, {"text": "", "comments": []})
            mine = st.text_area("Edit the shared song", value=box["text"], height=200, key="collab_text_" + room)
            if st.button("Save to shared song", key="collab_save"):
                box["text"] = mine
                st.success("Saved. Your co-writer sees it in a few seconds.")
            note = st.text_input("Leave feedback", key="collab_note")
            if st.button("Send feedback", key="collab_send"):
                if note.strip():
                    box["comments"].append(me + ": " + note.strip())
                    st.success("Feedback sent.")
                else:
                    st.info("Write your feedback first.")
        with right:
            live_view(room)