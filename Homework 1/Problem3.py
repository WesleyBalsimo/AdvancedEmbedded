#using micropython for voltage division problem

def parallel(a, b):
    ans = (a*b) / (a+b)
    return ans

#equvalent resistance at each node
R3 = 22
R2 = parallel((R3 + 3), 16)
R1 = parallel((R2 + 8), 12)
R0 = R1 + 5

#input voltage
V0 = 10
V1 = V0 * (R1 / R0)
V2 = V1 * (R2 / (R2 + 8))
V3 = V2 * (R3 / (R3 + 3))

print("Voltage across R0:", V0)
print("Voltage across R1:", V1)
print("Voltage across R2:", V2)
print("Voltage across R3:", V3)
