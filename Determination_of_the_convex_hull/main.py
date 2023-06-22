# skończone

def direction(p, q, r):
    if (q[1] - p[1]) * (r[0] - q[0]) - (r[1] - q[1]) * (q[0] - p[0]) > 0:
        return "right"
    elif (q[1] - p[1]) * (r[0] - q[0]) - (r[1] - q[1]) * (q[0] - p[0]) < 0:
        return "left"
    else:
        return 'linear'


def Jarvis(points, do_linear_check=False):
    max_left = (float('inf'), float('inf'))
    for point in points:
        if point[0] < max_left[0]:
            max_left = point
            continue
        elif point[0] == max_left[0]:
            if point[1] < max_left[1]:
                max_left = point
                continue
    p = max_left
    result = [p]
    q = points[points.index(p) + 1]
    while q != max_left:
        if points.index(p) != len(points) - 1:
            q = points[points.index(p) + 1]
        else:
            q = points[0]
        for r in points:
            if r != p and r != q:
                if do_linear_check:
                    if direction(p, q, r) == 'right':
                        q = r
                    elif direction(p, q, r) == 'linear' and \
                            ((p[0] < q[0] < r[0] or p[0] > q[0] > r[0]) or (p[1] < q[1] < r[1] or p[1] > q[1] > r[1])):
                        q = r
                else:
                    if direction(p, q, r) == 'right':
                        q = r

        if q not in result:
            result.append(q)
        p = q
    return result


def main():
    points = [(2, 2), (4, 3), (5, 4), (0, 3), (0, 2), (0, 0), (2, 1), (2, 0), (4, 0)]

    print(Jarvis(points))
    print(Jarvis(points, True))


if __name__ == '__main__':
    main()

