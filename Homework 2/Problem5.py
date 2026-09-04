#calculate the impedence from a to b

def parallel(a, b):
    ans = (a*b) / (a+b)
    return ans

def series(a, b):
    return a + b

r1 = parallel(250, -1j*300)
r2 = series(r1, 1j*30)
r3 = parallel(r2, 1j*150)

r4 = parallel(series(1j*200, 150), 75)
r5 = series(r4, r3)

rtotal = parallel(r5, 350)

print("Total impedance:", rtotal)
