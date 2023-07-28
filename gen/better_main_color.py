import copy


def get_cluster_dis(c1, c2, p):
    n_c1 = len(c1)
    n_c2 = len(c2)
    s_c1c2 = 0
    for i in range(p):
        avr_c1 = sum([e[i] for e in c1]) / n_c1
        avr_c2 = sum([e[i] for e in c2]) / n_c2
        s_c1c2 += (avr_c1 - avr_c2) ** 2

    return s_c1c2 * ((n_c1 * n_c2) / (n_c1 + n_c2))


def clustering(d, i, t, count):
    if len(d) == 1 or i == len(d):
        print(f'count: {count}')
        return d
    c1 = d[i]
    min_dis_c1c2 = 196608
    last_cluster = None
    for j in range(i + 1, len(d)):
        c2 = d[j]
        dis_c1c2 = get_cluster_dis(c1, c2, 3)
        if dis_c1c2 > t:
            continue
        if dis_c1c2 < min_dis_c1c2:
            min_dis_c1c2 = dis_c1c2
            last_cluster = c2

    if last_cluster is None:
        return clustering(d, i + 1, t, count + 1)
    else:
        dst = list(copy.deepcopy(d))
        dst.remove(last_cluster)
        dst.pop(i)
        dst.append(c1 + last_cluster)
        return clustering(dst, 0, t, count + 1)

