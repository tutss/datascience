import numpy as np
import matplotlib.pyplot as plt

# Parâmetros da distribuição Normal verdadeira
mu_true = 0       # Média verdadeira
sigma_true = 1    # Desvio padrão verdadeiro (raiz quadrada da variância)

# Parâmetros da simulação
num_simulations = 10000   # Número de simulações de Monte Carlo
sample_size = 30          # Tamanho da amostra em cada simulação

# Lista para armazenar as estimativas da variância
variance_estimates = []

# Loop de simulação de Monte Carlo
for _ in range(num_simulations):
    # Gerar uma amostra aleatória de tamanho 'sample_size' da distribuição Normal
    sample = np.random.normal(loc=mu_true, scale=sigma_true, size=sample_size)
    
    # Estimar a variância a partir da amostra (utilizando o estimador não viciado)
    variance_estimate = np.var(sample, ddof=1)  # ddof=1 para obter o estimador não viciado
    
    # Armazenar a estimativa da variância
    variance_estimates.append(variance_estimate)

# Converter a lista em um array numpy para facilitar os cálculos
variance_estimates = np.array(variance_estimates)

# Calcular a média das estimativas de variância
mean_variance_estimate = np.mean(variance_estimates)

# Exibir o resultado
print(f"Estimativa média da variância: {mean_variance_estimate:.4f}")
print(f"Valor verdadeiro da variância: {sigma_true**2:.4f}")

# Plotar o histograma das estimativas de variância
plt.hist(variance_estimates, bins=50, edgecolor='black', alpha=0.7)
plt.axvline(sigma_true**2, color='red', linestyle='dashed', linewidth=2, label='Variância Verdadeira')
plt.title('Distribuição das Estimativas de Variância')
plt.xlabel('Estimativa de Variância')
plt.ylabel('Frequência')
plt.legend()
plt.show()