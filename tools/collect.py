"""GitHub Actions 결과(final-epXX) 내려받아 완성 폴더에 한글 이름으로 저장.

사용: python tools/collect.py <run_id> <완성 폴더>
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

NAMES = {"ep01_cats": "01_고양이만_남는다면", "ep02_minecraft": "02_마인크래프트_세상이라면",
         "ep03_nolaw": "03_법이_사라진다면", "ep04_ice": "04_남극북극_얼음이_다_녹는다면",
         "ep05_war": "05_남북전쟁이_일어난다면", "ep06_onenation": "06_전세계가_하나의_나라가_된다면",
         "ep07_nohouse": "07_모든_집이_사라진다면", "ep08_sun": "08_태양이_1초_꺼진다면",
         "ep09_ai": "09_AI가_세상을_지배한다면", "ep10_mochi": "10_고디바모찌_세계열풍이라면"}
run, out = sys.argv[1], Path(sys.argv[2])
tmp = Path(tempfile.mkdtemp(prefix="whatif_dl_"))
subprocess.run(["gh", "run", "download", run, "--repo", "sehwan50593/imagine-lab-3d", "--pattern", "final-*",
                "--dir", str(tmp)], check=True)
for mp4 in tmp.rglob("*.mp4"):
    ep = mp4.stem
    dst = out / f"{NAMES.get(ep, ep)}.mp4"
    shutil.copy2(mp4, dst)
    print("saved", dst)
