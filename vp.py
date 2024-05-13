def vp(s):
    bn = 0
    for i in s:
        if i == "<":
            bn += 1
        elif i == ">":
            bn -= 1
        if bn < 0:
            return False
    return bn == 0


# with open("index.html", "r") as index:
#     html = index.read()
#     print(vp(html))

v = vp("<<>")
print(v)
