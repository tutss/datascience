import numpy as np
from scipy.stats import poisson, norm
from scipy.optimize import root_scalar
import matplotlib.pyplot as plt

# Parametros
N = 1000  # N simulacoes
n = 100   # Amostra
theta0 = 4  # theta verdadeiro
thetahat = np.zeros(N)  # valores estimados de theta

for j in range(N):
    z = np.random.poisson(theta0, size=n)
    sample_mean = np.mean(1 / (1 + z))
    
    # Un(theta)
    def Un(theta):
        return sample_mean - (1 - np.exp(-theta)) / theta
    
    try:
        result = root_scalar(Un, bracket=[1e-6, 20], method='brentq')
        thetahat[j] = result.root
    except:
        thetahat[j] = np.nan

thetahat = thetahat[~np.isnan(thetahat)]

# Lambda(theta), I(theta), e V(theta)
def Lambda(theta):
    z_vals = np.arange(0, 1001)
    dpois_values = poisson.pmf(z_vals, theta)
    E = np.sum((1 / (1 + z_vals))**2 * dpois_values)
    return E - ((1 - np.exp(-theta))**2) / theta**2

def I(theta):
    return (1 - np.exp(-theta)) / theta**2 - np.exp(-theta) / theta

def V(theta):
    return Lambda(theta) / I(theta)**2

Vtheta0 = V(theta0)

Z0 = np.sqrt(n) * (thetahat - theta0) / np.sqrt(Vtheta0)

# Plot histogram of Z0 and overlay standard normal density
plt.hist(Z0, bins=50, density=True, alpha=0.6, color='skyblue', edgecolor='black')
x = np.linspace(-4, 4, 100)
plt.plot(x, norm.pdf(x), 'r-', lw=2, label='Standard Normal Density')
plt.title('Histogram of Z0 with Standard Normal Density')
plt.xlabel('Z0')
plt.ylabel('Density')
plt.legend()
plt.show()

# Plot histogram of thetahat and overlay normal density with mean=theta0 and variance=V(theta0)/n
plt.hist(thetahat, bins=50, density=True, alpha=0.6, color='lightgreen', edgecolor='black')
mean = theta0
sd = np.sqrt(Vtheta0 / n)
x = np.linspace(min(thetahat), max(thetahat), 100)
plt.plot(x, norm.pdf(x, mean, sd), 'r-', lw=2, label='Normal Density')
plt.title('Histogram of Estimated Theta with Normal Density')
plt.xlabel('Estimated Theta')
plt.ylabel('Density')
plt.legend()
plt.show()

# Print the true theta value
print(f"True theta value: {theta0}")