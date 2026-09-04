#Advanced Embedded
#homework 1

def parallel(a, b):
    ans = (a*b) / (a+b)
    return ans

def series(a, b):
    return a + b

r1 = 75
r2 = series(200, 150)
r12 = parallel(r1, r2)

r3 = 250
r4 = 300
r34 = parallel(r3, r4)

r5 = series(50, r34)
r6 = 150
r56 = parallel(r5, r6)

rtop = series(r12, r56)

rbottom = 350
rab = parallel(rtop, rbottom)

print("Total resistance:", rab)