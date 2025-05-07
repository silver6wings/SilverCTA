import numpy as np
import pandas as pd


def SIN(S):     return np.sin(S)  # 求S的正弦值（弧度)


def COS(S):     return np.cos(S)  # 求S的余弦值（弧度)


def TAN(S):     return np.tan(S)  # 求S的正切值（弧度)


def ASIN(S):     return np.arcsin(S)  # 求S的反正弦值 [-1, 1]


def ACOS(S):     return np.arccos(S)  # 求S的反余弦值 [-1, 1]


def ATAN(S):     return np.arctan(S)  # 求S的反正切值 (-∞, +∞)


def CEILINE(S):  return np.ceil(S)  # 求S的向上取整


def FLOOR(S):    return np.floor(S)  # 求S的向下取整


def NOT(S):                 return ~S


def INTPART(S: pd.Series):  return S.astype(int)


def CROSS_PLUS(S1, S2):
    S1 = pd.Series(S1)
    S2 = pd.Series(S2)
    return (S1 > S2) & (S1.shift(1) < S2)


def COUNT_PLUS(S, N):
    res = np.repeat(np.nan, len(S))
    for i in range(len(S)):
        if (not np.isnan(N[i])):
            if 0 < N[i] <= i + 1:
                res[i] = np.sum(S[max(0, i + 1 - N[i]):i + 1])
            if N[i] == 0:
                res[i] = 0
    return res.astype(int)


def REF_PLUS(S, N):
    result = np.repeat(np.nan, len(S))

    nCount = len(N)
    for i in range(len(S)):
        if i >= nCount:
            continue

        value = N[i]

        value = int(value)
        if value >= 0 and value <= i:
            result[i] = S[i - value]
        elif i:
            result[i] = result[i - 1]
        else:
            result[i] = S[i]

    return result
