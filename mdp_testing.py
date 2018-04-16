c1 = "c1"
c2 = "c2"
c3 = "c3"
b1 = "b1"
b2 = "b2"
b3 = "b3"
a1 = "a1"
a2 = "a2"
a3 = "a3"

actions = {
    c3: [c2, c1, b3, a3],
    c2: [c3, c1, b2, a2],
    c1: [c2, c3, b1, a1],
    b3: [c3, a3, b2, b1],
    b2: [b3, b1, c2, a1],
    b1: [a1, c1, b2, b3],
    a3: [b3, c3, a2, a1],
    a2: [b2, c2, a1, a3],
    a1: [b1, c1, a2, a3]
    }

print("Possible actions:")
for item in actions:
    for i in actions[item]:
        print(" {f} -> {t}".format(f=item, t=i))