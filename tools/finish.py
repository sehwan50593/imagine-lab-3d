"""CI 조각(full-epXX-N)과 음악(music-all)을 내려받아 로컬에서 합쳐 완성 폴더에 저장.

렌더는 CI에서, 합치기(ffmpeg 복사)만 로컬. 같은 조각이 여러 실행에 있으면 뒤 실행이 덮어씀.
사용: python tools/finish.py <music_run> <완성 폴더> ep03_nolaw=run1,run2 ep13_dog_alone=run3 ...
"""
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from engine.run import BUILD, load_ep  # noqa: E402
from names import NAMES  # noqa: E402

REPO = "sehwan50593/imagine-lab-3d"


def download(run, pattern, dst):
    subprocess.run(["gh", "run", "download", str(run), "--repo", REPO, "--pattern", pattern, "--dir", str(dst)],
                   check=True)


music_run, out = sys.argv[1], Path(sys.argv[2])
tmp = Path(tempfile.mkdtemp(prefix="whatif_fin_"))
download(music_run, "music-all", tmp / "music")
for arg in sys.argv[3:]:
    ep, runs = arg.split("=")
    parts = {}
    for run in runs.split(","):
        d = tmp / ep / run
        download(run, f"full-{ep}-*", d)
        for mp4 in d.rglob(f"{ep}_*.mp4"):
            parts[int(re.search(r"_(\d+)$", mp4.stem).group(1))] = mp4
    n = len(parts)
    if sorted(parts) != list(range(n)):
        print(f"[{ep}] 조각 빠짐: {sorted(parts)}")
        continue
    bd = BUILD / ep
    bd.mkdir(parents=True, exist_ok=True)
    shutil.copy2(next((tmp / "music").rglob(f"{ep}.m4a")), bd / "music.m4a")
    dst = out / f"{NAMES.get(ep, ep)}.mp4"
    subprocess.run([sys.executable, "-m", "engine.run", "assemble", ep, "--chunks",
                    *[str(parts[i]) for i in range(n)], "--out", str(dst)], check=True, cwd=ROOT)
    print(f"[{ep}] 저장 {dst} ({n}조각, {load_ep(ep).META['duration']}s)")
