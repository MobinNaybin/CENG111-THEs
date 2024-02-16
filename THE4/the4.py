def brothers(T, pname):
    chldrn = []
    if type(T) == str:
        return []
    if len(T) <= 1:
        return []
    if T[0] == pname:
        return []

    for i in T[1:]:
        if type(i) == list:
            chldrn.append(i[0])
        else:
            chldrn.append(i)
    if pname in chldrn:
        boyslst = []
        for i in chldrn:
            if i[0].islower() and i != pname:
                boyslst.append(i)
        return boyslst
    for i in T[1:]:
        result = brothers(i, pname)
        if result:
            return result
    return []


def sisters(T, pname):
    chldrn = []
    if type(T) == str:
        return []
    if len(T) <= 1:
        return []
    if T[0] == pname:
        return []

    for i in T[1:]:
        if type(i) == list:
            chldrn.append(i[0])
        else:
            chldrn.append(i)
    if pname in chldrn:
        girlslst = []
        for i in chldrn:
            if i[0].isupper() and i != pname:
                girlslst.append(i)
        return girlslst
    for i in T[1:]:
        result = sisters(i, pname)
        if result:
            return result
    return []


def siblings(T, pname):
    chldrn = []
    if type(T) == str:
        return []
    if len(T) <= 1:
        return []
    if T[0] == pname:
        return []

    for i in T[1:]:
        if type(i) == list:
            chldrn.append(i[0])
        else:
            chldrn.append(i)
    if pname in chldrn:
        siblingslst = []
        for i in chldrn:
            if i != pname:
                siblingslst.append(i)
        return siblingslst
    for i in T[1:]:
        result = siblings(i, pname)
        if result:
            return result
    return []


def parent(T, pname):
    if type(T) == str:
        return []
    if len(T) <= 1:
        return []
    if T[0] == pname:
        return []
    for i in T[1:]:
        if type(i) == list and i[0] == pname:
            return T[0]
        if type(i) == str and i == pname:
            return T[0]
    for i in T[1:]:
        result = parent(i, pname)
        if result:
            return result
    return []


def uncles(T, pname):
    p = parent(T, pname)
    if not p:
        return []
    return brothers(T, p)


def aunts(T, pname):
    p = parent(T, pname)
    if not p:
        return []
    return sisters(T, p)


def children(T, pname):
    if type(T) == str:
        return []
    if len(T) <= 1:
        return []
    chldrnlist = []
    if T[0] == pname:
        for i in T[1:]:
            if type(i) == list:
                chldrnlist.append(i[0])
            else:
                chldrnlist.append(i)
        return chldrnlist
    for i in T[1:]:
        result = children(i, pname)
        if result:
            return result
    return []


def cousins(T, pname):
    p = parent(T, pname)
    uncle = brothers(T, p)
    aunt = sisters(T, p)
    cousinslst = []
    for i in uncle + aunt:
        cousinslst.extend(children(T, i))
    return cousinslst
