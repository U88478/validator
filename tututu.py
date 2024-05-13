def empiler(P, e):
    P.append(e)
    return P


def depiler(P):
    if est_vide(P):
        return []
    else:
        P.pop()
    return P


def est_vide(P):
    return P == []
