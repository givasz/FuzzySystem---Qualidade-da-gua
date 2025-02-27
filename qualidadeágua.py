# -*- coding: utf-8 -*-
"""QualidadeÁgua.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1l5YhPhw18BIGoulrGFWoR-koakU1-iWs

**A Lógica Fuzzy** é baseada na teoria dos conjuntos
fuzzy.

   - Tradicionalmente, uma proposição lógica tem dois
extremos: ou é completamente verdadeiro ou é
completamente falso. Entretanto, na lógica Fuzzy, uma premissa varia em
grau de verdade de 0 a 1, o que leva a ser
parcialmente verdadeira ou parcialmente falsa.

>O presente notebook colab, escrito por Givanildo Barbosa, João Eduardo, Luiz Felipe e Wender Alves. A codificação foi baseada na biblioteca scikit fuzzy e no exemplo fornecido pelo professor Alison Zille Lopes{1}.
---
{1} LOPES, Alison Zille. Exemplo de Sistema Fuzzy. Disponível em: https://colab.research.google.com/drive/1fQCvZ6w-3q5ZPDy-iDRabAnR7vmq8Dqr?usp=sharing#scrollTo=W1qC1Jz7R5aq. Acesso em: 04 out. 2024.
"""

!pip install scikit-fuzzy

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

"""**Sistemas Fuzzy**

> Sistemas são desenvolvidos para resolver problemas. Assim, precisamos do problema que pretendemos resolver através de um Sistema Fuzzy, o qual pode ser visto abaixo.

> Baseado no artigo de Sergio Luís de Castro Junior et al. (2022) {1}, o objetivo do sistema fuzzy é diagnosticar a qualidade da água para o cultivo de tilápias-do-Nilo, considerando variáveis como temperatura e pH da água. A qualidade da água influencia diretamente a saúde e o desempenho produtivo dos peixes.

---
{1} CASTRO JUNIOR, S. L.; LAMARCA, D. S. F.; KRAETZER, T. L.; BALTHAZAR, G. R.; CANEPPELE, F. L. *Sistema baseado na lógica fuzzy para diagnóstico da qualidade da água para o cultivo de tilápia-do-Nilo*. *Research, Society and Development*, v. 11, n. 4, e3211426933, 2022. Disponível em: <http://dx.doi.org/10.33448/rsd-v11i4.26933>. Acesso em: 27 set. 2024.

**Fuzzificação**

Nesta etapa vamos definir as variáveis linguísticas e funções de pertinência.

> Nas funções de pertinência foram usados as trapezoidais, como no artigo.

> Com o artigo usado como base, foi feito um sistema para avaliação de qualidade da água para tilápias-do-Nilo, gerando a qualidade atráves da comparação entre Temperatura e pHagua. A temperatura é um valor entre 8 e 40 ºC, o pH fica entre 0 e 14.

**Váriaveis de Entrada:**

Temperatura:
- Universo (intervalo de valores): [8, 40]
- Conjuntos Fuzzy/Funções de Pertinência: baixa, média, alta

pHagua:
- Universo (intervalo de valores): [0, 14]
- Conjuntos Fuzzy/Funções de Pertinência: baixo, médio, alto


**Váriaveis de Saída:**

Qualidade:
- Universo (intervalo de valores): [0, 1]
- Conjuntos Fuzzy/Funções de Pertinência: ruim, moderada, boa/ideal
"""

temperatura = ctrl.Antecedent(np.arange(8, 41, 1), 'temperatura')
pHagua = ctrl.Antecedent(np.arange(0, 15, 1), 'pHagua')

qualidade = ctrl.Consequent(np.arange(0, 1.01, 0.01), 'qualidade')

temperatura['baixa'] = fuzz.trapmf(temperatura.universe, [8, 8, 20, 27])
temperatura['média'] = fuzz.trapmf(temperatura.universe, [21, 27, 28, 32])
temperatura['alta'] = fuzz.trapmf(temperatura.universe, [28, 32, 40, 40])

pHagua['baixo'] = fuzz.trapmf(pHagua.universe, [0, 0, 4.5, 6])
pHagua['médio'] = fuzz.trapmf(pHagua.universe, [4.5, 6, 9, 10])
pHagua['alto'] = fuzz.trapmf(pHagua.universe, [9, 10, 14, 14])

qualidade['ruim'] = fuzz.trapmf(qualidade.universe, [0, 0, 0.3, 0.4])
qualidade['moderada'] = fuzz.trapmf(qualidade.universe, [0.3, 0.4, 0.6, 0.7])
qualidade['boa/ideal'] = fuzz.trapmf(qualidade.universe, [0.6, 0.7, 1, 1])


temperatura.view()
pHagua.view()
qualidade.view()

"""**Interferência Fuzzy**

Nesta etapa vamos definir a base de conhecimento/regras:

- **SE** temperatura é baixa **E** pHagua é baixo **ENTÃO** a qualidade é ruim
- **SE** temperatura é baixa **E** pHagua é médio **ENTÃO** a qualidade é moderada
- **SE** temperatura é baixa **E** pHagua é alto **ENTÃO** a qualidade é ruim
- **SE** temperatura é média **E** pHagua é baixo **ENTÃO** a qualidade é moderada
- **SE** temperatura é média **E** pHagua é médio **ENTÃO** a qualidade é boa/ideal
- **SE** temperatura é média **E** pHagua é alto **ENTÃO** a qualidade é moderada
- **SE** temperatura é alta **E** pHagua é baixo **ENTÃO** a qualidade é ruim
- **SE** temperatura é alta **E** pHagua é médio **ENTÃO** a qualidade é moderada
- **SE** temperatura é alta **E** pHagua é alto **ENTÃO** a qualidade é ruim

Para validar a eficácia do modelo em relação à lógica tradicional (booleano), utilizamos dois parâmetros de entrada específicos: temperatura da água e pH da água, conforme descrito no artigo de referência. A divergência entre os dois modelos é ilustrada com o seguinte exemplo:

> Temperatura da água: 26.8°C

> pH da água: 7.0 (dentro da faixa ótima de 6 a 8.5)

De acordo com o modelo booleano, a temperatura de 26.8°C, apesar de estar muito próxima do valor ideal (27°C), classificaria a qualidade da água como "Moderada", devido à rigidez dos seus limites. Entretanto, o modelo fuzzy, que é capaz de lidar com pequenas variações, classifica essa mesma condição como "Ideal".

Essa diferença destaca uma das principais vantagens do modelo fuzzy: sua capacidade de capturar nuances nos dados de entrada, proporcionando uma avaliação mais flexível e contínua, em vez de alterações bruscas entre as classificações. Para este exemplo, o valor de saída gerado pelo processo de defuzzificação do modelo fuzzy demonstra que, apesar da leve variação na temperatura, a qualidade da água ainda é considerada "Ideal", comprovando a veracidade e a robustez do código quanto ao artigo de origem.
"""

rule1 = ctrl.Rule(temperatura['baixa'] & pHagua['baixo'], qualidade['ruim'])
rule2 = ctrl.Rule(temperatura['baixa'] & pHagua['médio'], qualidade['moderada'])
rule3 = ctrl.Rule(temperatura['baixa'] & pHagua['alto'], qualidade['ruim'])
rule4 = ctrl.Rule(temperatura['média'] & pHagua['baixo'], qualidade['moderada'])
rule5 = ctrl.Rule(temperatura['média'] & pHagua['médio'], qualidade['boa/ideal'])
rule6 = ctrl.Rule(temperatura['média'] & pHagua['alto'], qualidade['moderada'])
rule7 = ctrl.Rule(temperatura['alta'] & pHagua['baixo'], qualidade['ruim'])
rule8 = ctrl.Rule(temperatura['alta'] & pHagua['médio'], qualidade['moderada'])
rule9 = ctrl.Rule(temperatura['alta'] & pHagua['alto'], qualidade['ruim'])

qualidade_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
qualidade_simulator = ctrl.ControlSystemSimulation(qualidade_ctrl)

while True:
  temp = float(input('Digite a temperatura(celsius):'))
  if(temp<8 or temp >40):
    print('A temperatura deve estar no intervalo [8, 40]')
    continue
  qualidade_simulator.input['temperatura'] = temp
  break

while True:
  ph = float(input('Digite o pH da água: '))
  if(ph<0 or ph >14):
    print('O pH da água deve estar no intervalo [0, 14]')
    continue
  qualidade_simulator.input['pHagua'] = ph
  break

"""**Defuzzificação**

> Esta etapa corresponde ao processo de defuzzificação, no qual a saída fuzzy da qualidade é convertida para um valor numérico exato. Este valor defuzzificado, indica a qualidade da água em uma escala contínua.

> O valor obtido é então interpretado em uma categoria: "ruim", "moderada", ou "boa/ideal", dependendo do intervalo em que ele se encontra, permitindo uma melhor compreensão do resultado final do sistema fuzzy.

"""

qualidade_simulator.compute()
resultado_qualidade = qualidade_simulator.output['qualidade']

print(f'A qualidade é de {resultado_qualidade:.1f}')

#Forma fácil de resolver quando retornar o valor de saída, que não precise olhar qual parâmetro se encaixa.
if 0 <= resultado_qualidade <= 0.4:
    qualidade_str = "ruim"
elif 0.4 < resultado_qualidade <= 0.7:
    qualidade_str = "moderada"
else:
    qualidade_str = "boa/ideal"

print(f"Ou seja a qualidade da água é: {qualidade_str}")

temperatura.view(sim=qualidade_simulator)
pHagua.view(sim=qualidade_simulator)
qualidade.view(sim=qualidade_simulator)

"""**SUPERFICÍE DE RESPOSTA**

> A superfície de resposta no sistema fuzzy é uma representação gráfica tridimensional que mostra como as variáveis de entrada — neste caso, temperatura e pH da água — interagem para determinar o valor da qualidade da água, a variável de saída. O gráfico é gerado a partir das regras fuzzy previamente estabelecidas, e visualiza de maneira clara como diferentes combinações de entradas influenciam o resultado final.
"""

x_temp = np.linspace(8, 40, 100)
y_ph = np.linspace(0, 14, 100)
X, Y = np.meshgrid(x_temp, y_ph)
Z = np.zeros_like(X)

for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        qualidade_simulator.input['temperatura'] = X[i, j]
        qualidade_simulator.input['pHagua'] = Y[i, j]
        qualidade_simulator.compute()
        Z[i, j] = qualidade_simulator.output['qualidade']

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
colors = [(0, 'blue'), (0.5, '#003366'), (1, 'yellow')]
custom_cmap = LinearSegmentedColormap.from_list('CustomCoolwarm', colors)
surf = ax.plot_surface(X, Y, Z, cmap=custom_cmap, edgecolor='none')
ax.set_xlabel('Temperatura (ºC)')
ax.set_ylabel('pH')
ax.set_zlabel('Qualidade da Água')

fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)

plt.show()