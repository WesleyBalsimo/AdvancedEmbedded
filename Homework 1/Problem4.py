#calculate the impedence from a to b

def parallel(a, b):
    ans = (a*b) / (a+b)
    return ans

r1 = parallel(250, -1j*300)
r2 = r1 + 1j*30
r3 = parallel(r2, 1j*150)

r4 = parallel(1j*200 + 150, 75)
r5 = r4 + r3

rtotal = parallel(r5, 350)

print("Total impedance:", rtotal)

