"""GitHub Actions 결과(final-epXX) 내려받아 완성 폴더에 한글 이름으로 저장.

사용: python tools/collect.py <run_id> <완성 폴더>
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from names import NAMES
run, out = sys.argv[1], Path(sys.argv[2])
tmp = Path(tempfile.mkdtemp(prefix="whatif_dl_"))
subprocess.run(["gh", "run", "download", run, "--repo", "sehwan50593/imagine-lab-3d", "--pattern", "final-*",
                "--dir", str(tmp)], check=True)
for mp4 in tmp.rglob("*.mp4"):
    ep = mp4.stem
    dst = out / f"{NAMES.get(ep, ep)}.mp4"
    shutil.copy2(mp4, dst)
    print("saved", dst)
