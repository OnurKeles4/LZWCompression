from scipy import integrate

def f(x):
    return ((x-2)**2023 * (x+5)**2023)/10**250

result, error = integrate.quad(f, 0, 1)

print("Sonuç:", result)
print("Hata:", error)