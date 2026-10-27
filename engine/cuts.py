"""카메라 키: 장면 사이 짧은 휙 돌리기(0.6초 이하)를 컷으로 (10-27 오너: 너무 빠름 → 깜빡임 전환)."""


def snap(keys, gap=0.6):
    out = list(keys)
    for i in range(len(out) - 1):
        ta, tb = out[i][0], out[i + 1][0]
        if 0 < tb - ta <= gap:
            m = (ta + tb) / 2
            out[i] = (m - 0.01, *out[i][1:])
            out[i + 1] = (m + 0.01, *out[i + 1][1:])
    return out
