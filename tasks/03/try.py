def c(a, b):
    try:
        a.remove(6)
        b.remove(6)
    except KeyError as e:
        print(e)


a = {1, 2, 3}
b = {1, 2, 3}
c(a, b)
print(a)
print(b)
