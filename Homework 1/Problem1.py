#Advanced Embedded
#homework 1

def parallel(a, b):
    ans = (a*b) / (a+b)
    return ans

r1 = 75
r2 = 200 + 150
r12 = parallel(r1, r2)

r3 = 250
r4 = 300
r34 = parallel(r3, r4)

r5 = 50 + r34
r6 = 150
r56 = parallel(r5, r6)

rtop = r12 + r56

rbottom = 350
rab = parallel(rtop, rbottom)

print("Total resistance:", rab)