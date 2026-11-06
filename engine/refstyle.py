"""STYLE='ref' 편 도우미 — 기준 영상(남자가 한 명뿐이라면) 형식, 내레이션 없음 (11-06 오너).

편 파일의 LINES 각 줄: d=길이(초), sub=아래 자막(두 줄까지 '\\n').
GROUPS=[dict(at="줄 이름", badge="D-DAY", label=, title=, big=, big_color=...)] — 묶음은 at 줄부터 다음 묶음 전까지
위 칩·제목이 그대로 있고, 아래 자막만 줄마다 바뀐다.
"""
from .common import Beat

KEYS = ("badge", "title", "label", "big", "label_color", "big_color", "title_size", "big_size", "note", "note_color")


def starts_of(lines):
    """줄 길이(d)를 이어 붙인 시작 시각들과 전체 길이."""
    out, t = [], 0.0
    for ln in lines:
        out.append(round(t, 3))
        t += ln["d"]
    return out, round(t, 3)


def heads_of(groups, ln):
    """묶음이 시작하는 줄 번호들 (0번 줄부터, 같은 줄에 둘 금지)."""
    s = sorted(ln[g["at"]] for g in groups)
    assert s[0] == 0 and len(set(s)) == len(s), s
    return s


def beats_of(lines, starts, dur, groups, ln):
    """줄마다 Beat 하나(아래 자막) — 위 칩·제목은 그 줄이 속한 묶음 것."""
    heads_of(groups, ln)
    gs = sorted(((ln[g["at"]], g) for g in groups), key=lambda x: x[0])
    out = []
    for k, line in enumerate(lines):
        g = [g for i, g in gs if i <= k][-1]
        t1 = starts[k + 1] if k + 1 < len(starts) else dur
        out.append(Beat(starts[k], t1, sub=line.get("sub", ""), **{x: g[x] for x in KEYS if x in g}))
    return out


def sfx_of(starts, groups, ln, extra=()):
    """효과음 시각 [초, 종류, 세기(, 길이)]: 0초·묶음이 바뀌는 줄은 '찰싹'(hit), 나머지 줄 바뀜은 '휙'(whoosh)."""
    heads = set(heads_of(groups, ln))
    ev = [[0.0, "hit", 1.0]] + [[s, "hit" if k in heads else "whoosh", 1.0] for k, s in enumerate(starts) if k > 0]
    return sorted(ev + [list(e) for e in extra])


if __name__ == "__main__":   # 자체 점검
    ln_ = {"a": 0, "b": 1, "c": 2}
    lines_ = [dict(d=2.0, sub="가"), dict(d=3.0, sub="나"), dict(d=1.5, sub="다")]
    st_, du_ = starts_of(lines_)
    assert st_ == [0.0, 2.0, 5.0] and du_ == 6.5
    gr_ = [dict(at="a", badge="D-DAY", big="1명"), dict(at="c", badge="반전")]
    bs = beats_of(lines_, st_, du_, gr_, ln_)
    assert [b.badge for b in bs] == ["D-DAY", "D-DAY", "반전"] and bs[1].big == "1명" and bs[2].t1 == 6.5
    assert sfx_of(st_, gr_, ln_) == [[0.0, "hit", 1.0], [2.0, "whoosh", 1.0], [5.0, "hit", 1.0]]
    print("refstyle ok")
