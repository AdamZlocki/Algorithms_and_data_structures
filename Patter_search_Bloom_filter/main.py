# skończone
import time

import numpy as np


def hash(word, N):
    d = 256
    q = 503
    hw = 0
    for i in range(N):
        hw = (hw * d + ord(word[i])) % q
    return hw


def hash2(word, N):
    d = 256
    q = 541
    hw = 0
    for i in range(N):
        hw = (hw * d + ord(word[i])) % q
    return hw


def RabinKarp(S, W, N):
    P = 0.001
    n = 20
    b = int((-n * np.log(P) / np.log(2) ** 2) * 1.5)
    k = int(b * np.log(2) / n)
    Bloom = [0 for _ in range(b)]
    d = 256
    q = 503
    h = d ** (N - 1) % q
    for wzor in W:
        for i in range(k):
            idx = (hash(wzor, N) + i * hash2(wzor, N)) % b
            Bloom[idx] = 1

    results_idx = []
    false_detections = []

    for m in range(0, len(S) - N + 1):
        is_possible = True
        for i in range(k):
            hS = (hash(S[m:N + m], N) + i * hash2(S[m:N + m], N)) % b
            if not Bloom[hS]:
                is_possible = False
                break
        if is_possible:
            if S[m:m + N] in W:
                results_idx.append(m)
            else:
                false_detections.append(S[m:m + N])
    return len(results_idx), false_detections, len(false_detections)


def main():
    with open("lotr.txt", encoding='utf-8') as f:
        text = f.readlines()

    S = ' '.join(text).lower()

    W = ['gandalf']

    t_start = time.perf_counter()
    result = RabinKarp(S=S, W=W, N=7)
    print(f"{result[0]};{result[1]};{result[2]}")
    t_stop = time.perf_counter()
    print("Czas obliczeń:", "{:.7f}\n".format(t_stop - t_start))

    W = ['gandalf', 'looking', 'blocked', 'comment', 'pouring', 'finally', 'hundred', 'hobbits', 'however', 'popular',
         'nothing', 'enjoyed', 'stuffed', 'relaxed', 'himself', 'present', 'deliver', 'welcome', 'baggins', 'further']

    t_start = time.perf_counter()
    result = RabinKarp(S=S, W=W, N=7)
    print(f"{result[0]};{result[1]};{result[2]}")
    t_stop = time.perf_counter()
    print("Czas obliczeń:", "{:.7f}".format(t_stop - t_start))


if __name__ == '__main__':
    main()
