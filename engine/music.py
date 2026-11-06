"""잔잔한 피아노 배경음 자동 작곡 (가사 없음, 매번 새로 만든 원곡).

MIDI를 직접 쓰고 FluidSynth + FluidR3_GM(MIT 라이선스) 사운드폰트로 렌더한 뒤 ffmpeg로 마스터링.
"""
import struct
import subprocess
from pathlib import Path

import numpy as np

PPQ = 480
SCALE = {"major": [0, 2, 4, 5, 7, 9, 11], "lydian": [0, 2, 4, 6, 7, 9, 11]}
KEYS = {"C": 60, "Db": 61, "D": 62, "Eb": 63, "E": 64, "F": 65, "Gb": 66, "G": 67, "Ab": 68,
        "A": 69, "Bb": 70, "B": 71}
PROGRESSIONS = [
    [1, 5, 6, 4], [4, 1, 5, 6], [1, 6, 4, 5], [6, 4, 1, 5], [1, 4, 6, 5], [1, 3, 4, 4],
]
SOUNDFONTS = ["/usr/share/sounds/sf2/FluidR3_GM.sf2", "/usr/share/soundfonts/FluidR3_GM.sf2"]


def vlq(n):
    out = [n & 0x7F]
    n >>= 7
    while n:
        out.append((n & 0x7F) | 0x80)
        n >>= 7
    return bytes(reversed(out))


def track(events):
    """events=[(tick, bytes)] → MTrk 청크."""
    events = sorted(events, key=lambda e: (e[0], e[2] if len(e) > 2 else 0))
    data, last = bytearray(), 0
    for ev in events:
        tick, msg = ev[0], ev[1]
        data += vlq(max(0, tick - last)) + msg
        last = tick
    data += vlq(0) + b"\xff\x2f\x00"
    return b"MTrk" + struct.pack(">I", len(data)) + bytes(data)


def chord_tones(tonic, scale, degree, kind="add9"):
    def deg(d):
        d0 = d - 1
        return tonic + scale[d0 % 7] + 12 * (d0 // 7)
    r = degree
    tones = [deg(r), deg(r + 2), deg(r + 4)]
    if kind in ("add9", "7add9"):
        tones.append(deg(r + 8))
    if kind in ("7", "7add9"):
        tones.append(deg(r + 6))
    return tones


def compose(duration, key="C", mode="major", bpm=72, seed=1, twist_at=None, out_mid="music.mid"):
    rs = np.random.default_rng(seed)
    tonic = KEYS[key] - 12 if KEYS[key] > 64 else KEYS[key]   # 중간 C 근처
    scale = SCALE[mode]
    beat = PPQ
    bar = beat * 4
    sec_per_beat = 60.0 / bpm
    total_beats = duration / sec_per_beat
    n_bars = int(np.ceil(total_beats / 4)) + 1
    prog = PROGRESSIONS[int(rs.integers(len(PROGRESSIONS)))]
    piano, pad, bell = [], [], []
    tempo = int(60_000_000 / bpm)
    meta = [(0, b"\xff\x51\x03" + tempo.to_bytes(3, "big")),
            (0, b"\xff\x58\x04\x04\x02\x18\x08")]
    # 프로그램/볼륨/리버브 (ch0 피아노, ch1 패드, ch2 벨)
    piano += [(0, bytes([0xC0, 0])), (0, bytes([0xB0, 7, 108])), (0, bytes([0xB0, 91, 96])),
              (0, bytes([0xB0, 93, 20]))]
    pad += [(0, bytes([0xC1, 89])), (0, bytes([0xB1, 7, 44])), (0, bytes([0xB1, 91, 120]))]
    bell += [(0, bytes([0xC2, 10])), (0, bytes([0xB2, 7, 52])), (0, bytes([0xB2, 91, 127]))]

    def note(lst, ch, t, p, dur, vel):
        t = int(max(0, t + rs.normal(0, 8)))
        vel = int(np.clip(vel + rs.normal(0, 4), 18, 110))
        lst.append((t, bytes([0x90 | ch, int(p), vel]), 1))
        lst.append((t + int(dur), bytes([0x80 | ch, int(p), 0]), 0))

    twist_bar = int(twist_at / sec_per_beat / 4) if twist_at else None
    motif = None
    prev_mel = tonic + 12 + scale[2]
    for b in range(n_bars):
        ci = (b // 2) % len(prog)
        deg = prog[ci]
        if twist_bar is not None and b >= twist_bar:
            deg = [6, 4, 1, 5][((b - twist_bar) // 2) % 4]  # 반전부: 단조 느낌의 6도 진행
        kind = "7add9" if rs.random() < 0.35 else "add9"
        tones = chord_tones(tonic, scale, deg, kind)
        t0 = b * bar
        is_last = b == n_bars - 1
        energy = 0.55 + 0.45 * min(1.0, b / 6.0)
        if twist_bar is not None and twist_bar <= b < twist_bar + 2:
            energy = 0.5
        # 서스테인 페달
        piano.append((t0 + 10, bytes([0xB0, 64, 0]), 0))
        piano.append((t0 + 30, bytes([0xB0, 64, 100]), 1))
        # 왼손: 낮은 근음 + 천천히 펼친 화음
        root = tones[0] - 24
        while root < 36:
            root += 12
        lh = [root, root + 7, tones[1] - 12 if tones[1] - 12 > root + 7 else tones[1],
              root + 12 + (2 if rs.random() < 0.5 else 0)]
        pattern = [(0, 0, 3.8), (1.5, 1, 2.5), (2, 2, 2.0), (3, 3, 1.0)]
        if b % 2 == 1:
            pattern = [(0, 0, 3.8), (2, 1, 1.9), (2.5, 2, 1.5)]
        if is_last:
            pattern = [(0, 0, 8), (0.5, 1, 8), (1, 2, 8)]
        for bt, idx, dur in pattern:
            note(piano, 0, t0 + bt * beat, lh[idx % len(lh)], dur * beat, 46 * energy + 10)
        # 패드: 화음 길게
        if b % 2 == 0 or is_last:
            for p in tones[:3]:
                note(pad, 1, t0, p - 12, bar * 2 - 60, 30 + 10 * energy)
        # 오른손 멜로디: 2마디 모티프를 반복·변형
        if b == 0:
            continue
        if motif is None or (b % 4 == 0 and rs.random() < 0.6):
            k = int(rs.integers(3, 6))
            motif = sorted(set(float(x) for x in rs.choice([0, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5, 6, 6.5],
                                                           size=k, replace=False)))
        hi = [p + 12 for p in tones] + [tonic + 12 + s for s in scale] + [tonic + 24 + s for s in scale[:5]]
        for bt in motif:
            if bt >= 4 and (b % 2 == 1 or is_last):
                continue
            if bt >= 4:
                tt = t0 + bt * beat
            else:
                tt = t0 + bt * beat
            cands = np.array(sorted(set(hi)))
            weights = np.exp(-np.abs(cands - prev_mel) / 3.0)
            weights[np.isin(cands, [p + 12 for p in tones])] *= 2.2
            weights /= weights.sum()
            p = int(rs.choice(cands, p=weights))
            prev_mel = p
            note(piano, 0, tt, p, beat * float(rs.choice([1.5, 2, 3])), 52 * energy + 12)
        # 가끔 반짝이는 오르골 소리
        if rs.random() < 0.25 and not is_last:
            note(bell, 2, t0 + beat * float(rs.choice([0.5, 2.5])), tones[int(rs.integers(len(tones)))] + 24,
                 beat * 2, 34)
    piano.append((n_bars * bar + bar, bytes([0xB0, 64, 0]), 0))
    hdr = b"MThd" + struct.pack(">IHHH", 6, 1, 4, PPQ)
    Path(out_mid).write_bytes(hdr + track(meta) + track(piano) + track(pad) + track(bell))
    return out_mid


def render(mid, wav, sf2=None):
    sf2 = sf2 or next((s for s in SOUNDFONTS if Path(s).exists()), None)
    if not sf2:
        raise RuntimeError("FluidR3_GM.sf2 없음 (apt install fluid-soundfont-gm)")
    cmd = ["fluidsynth", "-ni", "-q", "-g", "0.45", "-r", "44100", "-R", "1", "-C", "0",
           "-o", "synth.reverb.room-size=0.45", "-o", "synth.reverb.damp=0.6",
           "-o", "synth.reverb.width=0.8", "-o", "synth.reverb.level=0.3",
           "-F", str(wav), sf2, str(mid)]
    subprocess.run(cmd, check=True)


def master(wav, out, duration):
    """out이 .f32면 효과음과 섞을 원시 파형(44.1kHz 스테레오 float32)으로."""
    fo = max(0.0, duration - 3.2)
    af = (f"highpass=f=45,atrim=0:{duration:.3f},afade=t=in:st=0:d=1.0,"
          f"afade=t=out:st={fo:.3f}:d=3.2,loudnorm=I=-23:TP=-1.5:LRA=9")
    enc = ["-f", "f32le"] if str(out).endswith(".f32") else ["-c:a", "aac", "-b:a", "192k"]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(wav), "-af", af, "-ar", str(SR),
                    "-ac", "2", *enc, str(out)], check=True)


# ── 효과음 (11-06 오너: 배경음은 낮추고 더 찰싹하게) — CI 음악 잡엔 numpy만 있어서 FFT로 거름 ──
SR = 44100
SFX_GAIN = {"whoosh": 0.10, "hit": 0.30, "thud": 0.45, "buzz": 0.08, "ding": 0.11, "rumble": 0.30}
SFX_LEAD = {"whoosh": 0.24}   # 휙은 컷 순간에 가장 크게 (그만큼 먼저 시작)


def _band(x, lo, hi):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X[(f < lo) | (f > hi)] = 0
    return np.fft.irfft(X, len(x))


def _tone(f0, f1, sec, decay):
    t = np.arange(int(sec * SR)) / SR
    return np.sin(2 * np.pi * np.cumsum(f0 + (f1 - f0) * t / sec) / SR) * np.exp(-t * decay)


def _peak1(x):
    return x / max(1e-9, float(np.abs(x).max()))


def sfx_clip(kind, rs, sec=None):
    """효과음 하나(모노, 최대 1). whoosh 컷 휙 · hit 묶음 바뀜 찰싹 · thud 착지 쿵 · buzz 모기 앵 · ding 띵 · rumble 우르릉."""
    if kind == "whoosh":
        n = int(0.34 * SR)
        u = np.linspace(0, 1, n)
        x = rs.normal(0, 1, n)
        y = _band(x, 300, 1400) * (1 - u) + _band(x, 1800, 7500) * u
        return _peak1(y * np.sin(np.pi * u ** 0.75) ** 2)
    if kind == "hit":
        n = int(0.42 * SR)
        t = np.arange(n) / SR
        slap = _peak1(_band(rs.normal(0, 1, n), 1200, 9000) * np.exp(-t * 55))
        return _peak1(0.9 * slap + 0.55 * _tone(190, 70, 0.42, 20) + 0.5 * _tone(62, 42, 0.42, 7))
    if kind == "thud":
        n = int(0.8 * SR)
        t = np.arange(n) / SR
        return _peak1(_tone(78, 36, 0.8, 6) + 0.7 * _peak1(_band(rs.normal(0, 1, n), 40, 260)) * np.exp(-t * 14))
    if kind == "buzz":
        sec = sec or 1.6
        t = np.arange(int(sec * SR)) / SR
        f = 610 + 30 * np.sin(2 * np.pi * 6.0 * t) + 12 * np.sin(2 * np.pi * 1.3 * t)
        ph = np.cumsum(f) / SR
        saw = 2 * (ph % 1.0) - 1
        am = (0.75 + 0.25 * np.sin(2 * np.pi * 9 * t)) * np.minimum(1, np.minimum(t / 0.15, (sec - t) / 0.3))
        return _peak1(_band(saw, 400, 5000) * am)
    if kind == "ding":
        t = np.arange(int(1.4 * SR)) / SR
        return _peak1((np.sin(2 * np.pi * 1318.5 * t) + 0.35 * np.sin(2 * np.pi * 2637 * t)) * np.exp(-t * 3.2))
    if kind == "rumble":
        sec = sec or 2.0
        n = int(sec * SR)
        t = np.arange(n) / SR
        am = (0.7 + 0.3 * np.sin(2 * np.pi * 3.1 * t)) * np.minimum(1, np.minimum(t / 0.2, (sec - t) / 0.6))
        return _peak1(_band(rs.normal(0, 1, n), 28, 190) * am)
    raise ValueError(kind)


def sfx_track(events, n, seed=1):
    """events=[[초, 종류, 세기(, 길이)]] → n샘플 스테레오 (휙·찰싹은 좌우로 조금씩 흩음)."""
    rs = np.random.default_rng(seed + 7)
    out = np.zeros((n, 2))
    for ev in events:
        t, kind, g = ev[0], ev[1], ev[2]
        x = sfx_clip(kind, rs, ev[3] if len(ev) > 3 else None) * SFX_GAIN[kind] * g
        i = max(0, int((t - SFX_LEAD.get(kind, 0.0)) * SR))
        x = x[:max(0, n - i)]
        pan = float(rs.uniform(-0.25, 0.25)) if kind in ("whoosh", "hit") else 0.0
        out[i:i + len(x), 0] += x * min(1.0, 1 - pan)
        out[i:i + len(x), 1] += x * min(1.0, 1 + pan)
    return out


def make(meta, duration, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    m = meta.get("music", {})
    mid = compose(duration + 4, key=m.get("key", "C"), mode=m.get("mode", "major"),
                  bpm=m.get("bpm", 72), seed=m.get("seed", 1), twist_at=m.get("twist_at"),
                  out_mid=out_dir / "music.mid")
    render(mid, out_dir / "music.wav")
    if not m.get("sfx"):
        master(out_dir / "music.wav", out_dir / "music.m4a", duration)
        return out_dir / "music.m4a"
    raw = out_dir / "music_bed.f32"
    master(out_dir / "music.wav", raw, duration)       # 배경음만 -23 LUFS
    bed = np.fromfile(raw, np.float32).reshape(-1, 2).astype(np.float64)
    mix = (bed + sfx_track(m["sfx"], len(bed), m.get("seed", 1))).astype(np.float32)
    mix.tofile(raw)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", str(raw),
                    "-af", "alimiter=limit=0.89", "-c:a", "aac", "-b:a", "192k", str(out_dir / "music.m4a")], check=True)
    return out_dir / "music.m4a"


if __name__ == "__main__":   # 효과음 자체 점검 (fluidsynth 없이)
    _rs = np.random.default_rng(0)
    for _k in SFX_GAIN:
        _c = sfx_clip(_k, _rs)
        assert _c.ndim == 1 and len(_c) > 1000 and abs(float(np.abs(_c).max()) - 1.0) < 1e-6, _k
    _tr = sfx_track([[0.0, "hit", 1.0], [1.0, "whoosh", 1.0], [2.9, "thud", 1.0]], 3 * SR)
    assert _tr.shape == (3 * SR, 2) and 0.05 < float(np.abs(_tr).max()) < 1.0
    print("sfx ok")
