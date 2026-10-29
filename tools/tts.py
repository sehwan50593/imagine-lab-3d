"""내레이션 만들기 (로컬, edge-tts 무료 음성): 편의 LINES를 줄마다 읽어 시간표와 하나로 이은 음성을 저장.

사용: python tools/tts.py ep19_nosleep
결과: assets/voice/<ep>/timeline.json ({"lines": [[시작초, 끝초, 글], ...], "dur": 전체초}), narration.m4a
편 파일은 timeline.json으로 자막·장면 시간을 맞추고, 합칠 때(tools/finish.py) narration.m4a를 음악 위에 얹음.
"""
import asyncio
import importlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import edge_tts

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def dur_of(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                 str(p)], capture_output=True, text=True, check=True).stdout)


async def speak(text, out, voice, rate):
    await edge_tts.Communicate(text, voice, rate=rate).save(str(out))


def main(ep_name):
    ep = importlib.import_module("episodes." + ep_name)
    voice, rate = getattr(ep, "VOICE", ("ko-KR-SunHiNeural", "+10%"))
    lead, gap, tail = getattr(ep, "VOICE_PAD", (0.35, 0.18, 1.6))
    dst = ROOT / "assets" / "voice" / ep_name
    dst.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp(prefix="tts_"))
    t = lead
    lines, parts = [], []
    for i, ln in enumerate(ep.LINES):
        text = ln["say"]
        mp3 = tmp / f"{i:02d}.mp3"
        asyncio.run(speak(text, mp3, voice, rate))
        # 앞뒤 무음을 잘라 줄 사이 간격을 일정하게
        wav = tmp / f"{i:02d}.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(mp3), "-af",
                        "silenceremove=start_periods=1:start_threshold=-45dB,areverse,"
                        "silenceremove=start_periods=1:start_threshold=-45dB,areverse",
                        "-ar", "48000", "-ac", "1", str(wav)], check=True)
        d = dur_of(wav)
        lines.append([round(t, 3), round(t + d, 3), text])
        parts.append((t, wav))
        t += d + ln.get("gap", gap)
    total = round(t - gap + tail, 2)
    # 줄마다 시작 시각에 맞춰 섞기 (adelay)
    cmd = ["ffmpeg", "-v", "error", "-y"]
    for _, w in parts:
        cmd += ["-i", str(w)]
    fl = "".join(f"[{k}]adelay={int(s * 1000)}|{int(s * 1000)}[a{k}];" for k, (s, _) in enumerate(parts))
    fl += "".join(f"[a{k}]" for k in range(len(parts))) + f"amix=inputs={len(parts)}:normalize=0,apad," \
          f"atrim=0:{total},loudnorm=I=-16:TP=-1.5[o]"
    cmd += ["-filter_complex", fl, "-map", "[o]", "-ar", "48000", "-c:a", "aac", "-b:a", "160k",
            str(dst / "narration.m4a")]
    subprocess.run(cmd, check=True)
    json.dump({"voice": voice, "rate": rate, "dur": total, "lines": lines}, open(dst / "timeline.json", "w",
              encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{ep_name}: {len(lines)}줄, {total}s → {dst}")


if __name__ == "__main__":
    main(sys.argv[1])
