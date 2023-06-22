# skończone
import time


def naive_find(S, W):
    m = 0
    i = 0
    results_idx = []
    count = 0
    while m != len(S):
        count += 1
        idx = m
        if S[m] == W[i]:
            m += 1
            i += 1
            while S[m] == W[i]:
                count += 1
                if i == len(W) - 1:
                    results_idx.append(idx)
                    break
                else:
                    i += 1
                    m += 1
            count += 1
            i = 0
        else:
            m = idx + 1
    return len(results_idx), count


def hash(word, d, q, W):
    hw = 0
    for i in range(len(W)):
        hw = (hw*d + ord(word[i])) % q
    return hw


def RabinKarp(S, W, do_rolling=False):
    d = 256
    q = 101
    count = 0
    results_idx = []
    hW = hash(W, d, q, W)
    conflicts = 0
    if do_rolling:
        h = 1
        for i in range(len(W) - 1):
            h = (h * d) % q
        hS = hash(S[0:len(W)], d, q, W)
        for m in range(0, len(S) - len(W) + 1):
            if m:
                hS = (d * (hS - ord(S[m - 1]) * h) + ord(S[m + len(W) - 1])) % q
                if hS < 0:
                    hS += q
            count += 1
            if hS == hW:
                if S[m:m+len(W)] == W:
                    results_idx.append(m)
                else:
                    conflicts += 1
    else:
        for m in range(0, len(S) - len(W)+1):
            hS = hash(S[m:m+len(W)], d, q, W)
            count += 1
            if hS == hW:
                if S[m:m + len(W)] == W:
                    results_idx.append(m)
                else:
                    conflicts += 1

    return len(results_idx), count, conflicts


def kmp_search(S, W):
    m, i = 0, 0
    results_idx = []
    count = 0
    T = kmp_table(W)
    while m < len(S):
        count += 1
        if W[i] == S[m]:
            m += 1
            i += 1
            if i == len(W):
                results_idx.append(m-i)
                i = T[i]
        else:
            i = T[i]
            if i < 0:
                m += 1
                i += 1
    return len(results_idx), count


def kmp_table(W):
    T = [-1] * (len(W) + 1)
    pos = 1
    cnd = 0
    while pos < len(W):
        if W[pos] == W[cnd]:
            T[pos] = T[cnd]
        else:
            T[pos] = cnd
            while cnd >= 0 and W[pos] != W[cnd]:
                cnd = T[cnd]

        pos += 1
        cnd += 1
    T[pos] = cnd
    return T


def main():
    with open("lotr.txt", encoding='utf-8') as f:
        text = f.readlines()

    S = ' '.join(text).lower()

    t_start = time.perf_counter()
    result1 = naive_find(S=S, W="time.")
    print(f"{result1[0]};{result1[1]}")
    t_stop = time.perf_counter()
    print("Czas obliczeń (naiwna):", "{:.7f}".format(t_stop - t_start))

    t_start = time.perf_counter()
    result2 = RabinKarp(S=S, W="time.", do_rolling=True)
    print(f"{result2[0]};{result2[1]};{result2[2]}")
    t_stop = time.perf_counter()
    print("Czas obliczeń (Rabin  rolling-hash):", "{:.7f}".format(t_stop - t_start))

    t_start = time.perf_counter()
    result3 = kmp_search(S=S, W="time.")
    print(f"{result3[0]};{result3[1]}")
    t_stop = time.perf_counter()
    print("Czas obliczeń (KMP):", "{:.7f}".format(t_stop - t_start))


if __name__ == '__main__':
    main()
