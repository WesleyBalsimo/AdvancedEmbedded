#using micropython as a calculator for a current division problem

def parallel(a, b):
    ans = (a*b) / (a+b)
    return ans

I = 10

R3 = 30
R2 = parallel(R3, 15) + 3
R1 = 20

I1 = I * (R2 / (R1 + R2))
print("Current through R1:", I1)

I2_1 = 10 - I1
I2 = I2_1 * (R3 / (R3 + 15))
print("Current through R2:", I2)

I3 = I2_1 - I2
print("Current through R3:", I3)