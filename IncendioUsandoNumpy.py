import numpy as np
import random
import matplotlib.pyplot as plt
import time
from matplotlib.colors import ListedColormap



TAMANHO_FLORESTA = 50
CHANCE_ARVORE_PEGAR_FOGO = 0.3
CHANCE_ARVORE_NASCER = 0.01

#Este codigo só funciona para florestas quadradas.
CINZAS = 0
ARVORE = CINZAS + 1
AGUA = ARVORE + 1
FOGO1 = AGUA+1
FOGO2 = FOGO1 + 1
FOGO3 = FOGO1 + 1

colors = {CINZAS: 'gray',ARVORE: 'green',AGUA: 'blue', FOGO1: 'red', FOGO2: 'orange', FOGO3: 'yellow'}
CMAP  = ListedColormap([colors[i] for i in sorted(colors.keys())])

N_ESTADOS = 6

def contaVizinhosFOGO(floresta,i,j):
    """Conta o numero de vizinhos que estao pegando fogo para uma determinada celula na posição Linha i Coluna j"""
    contador = 0
    n = len(floresta)
    if floresta[(i+1)%n][(j+1)%n]>=FOGO1:
        contador += 1
    if floresta[(i+1)%n][(j)%n]>=FOGO1:
        contador += 1
    if floresta[(i+1)%n][(j-1)%n]>=FOGO1:
        contador += 1
    if floresta[(i)%n][(j+1)%n]>=FOGO1:
        contador += 1
    if floresta[(i)%n][(j-1)%n]>=FOGO1:
        contador += 1
    if floresta[(i-1)%n][(j+1)%n]>=FOGO1:
        contador += 1
    if floresta[(i-1)%n][(j)%n]>=FOGO1:
        contador += 1
    if floresta[(i-1)%n][(j-1)%n]>=FOGO1:
        contador += 1
    return contador

def contaVizinhosARVORE(floresta,i,j):
    """Conta o numero de vizinhos que sao arvores para uma determinada celula na posição Linha i Coluna j"""
    contador = 0
    n = len(floresta)
    if floresta[(i+1)%n][(j+1)%n]==ARVORE:
        contador += 1
    if floresta[(i+1)%n][(j)%n]==ARVORE:
        contador += 1
    if floresta[(i+1)%n][(j-1)%n]==ARVORE:
        contador += 1
    if floresta[(i)%n][(j+1)%n]==ARVORE:
        contador += 1
    if floresta[(i)%n][(j-1)%n]==ARVORE:
        contador += 1
    if floresta[(i-1)%n][(j+1)%n]==ARVORE:
        contador += 1
    if floresta[(i-1)%n][(j)%n]==ARVORE:
        contador += 1
    if floresta[(i-1)%n][(j-1)%n]==ARVORE:
        contador += 1
    return contador

def colocaFogoAleatorio(floresta,n):
    """Coloca n Celulas da floresta no estado FOGO1
    A escolha das Celulas é aleatória"""
    t = len(floresta)-1
    for i in range(n):
        linha = random.randint(0,t)
        coluna = random.randint(0,t)
        while (floresta[linha][coluna]!=ARVORE):
            linha = random.randint(0,t)
            coluna = random.randint(0,t)
        floresta[linha][coluna] = FOGO1
    return floresta
        
def calculaProximaGeracao(floresta):
    """Dada uma floresta, calcula a próxima geração de acordo com as regras:
    Se uma arvore tem algum vizinho fogo, tem uma chance de ela virar fogo
    O fogo no seu ultimo estagio vira cinza
    uma celula cinza com vizinho arvore pode virar uma arvore"""
    copia = floresta.copy()
    n = len(floresta)
    for i in range(n):
        for j in range(n):
            if floresta[i][j] == ARVORE:
                x = contaVizinhosFOGO(floresta,i,j)
                r = random.random()
                if (1-CHANCE_ARVORE_PEGAR_FOGO)**x < r:
                    copia[i][j] = FOGO1
            elif floresta[i][j] >=FOGO1:
                copia[i][j] = (floresta[i][j] + 1)%N_ESTADOS
            elif floresta[i][j] == CINZAS:
                x = contaVizinhosARVORE(floresta,i,j)
                r = random.random()
                if (1-CHANCE_ARVORE_NASCER)**x < r:
                    copia[i][j]= ARVORE
    return copia

def main():
    
    floresta = np.ones((TAMANHO_FLORESTA, TAMANHO_FLORESTA), dtype= int) * ARVORE
    #floresta = colocaFogoAleatorio(floresta,4)
    floresta[25][25] = FOGO1
    floresta[9] = np.ones(TAMANHO_FLORESTA)*AGUA
    fig,ax = plt.subplots()
    im =ax.imshow(floresta,cmap=CMAP,vmin = 0, vmax = N_ESTADOS-1)
    plt.show(block = False)
    plt.pause(1)
    for i in range(50):
        floresta = calculaProximaGeracao(floresta)
        im.set_data(floresta)
        plt.draw()
        plt.pause(.5)
    
        

if __name__ == '__main__':
    main()