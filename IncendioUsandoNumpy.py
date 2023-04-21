import numpy as np
import random
import matplotlib.pyplot as plt
import time
from matplotlib.colors import ListedColormap


TAMANHO_FLORESTA = 50
CHANCE_ARVORE_PEGAR_FOGO = 0.1
CHANCE_ARVORE_NASCER = 0.05
DURACAO_PADRAO_FOGO = 3
NUMERO_ESTAGIOS = 100

#Este codigo só funciona para florestas quadradas.
class CINZAS():
    """Classe que representa as cinzas"""
    n = 0   #valor utilizado no color map

class ARVORE():
    """Classe que representa as arvores"""
    n = 1

class AGUA():
    """Classe que representa a água"""
    n=2

class PEDRA():
    """Classe que representa Pedras, usada para definir as bordas da floresta"""
    n=3

class FOGO():
    """Classe que representa o fogo, tendo o contador como o numero de estagios que o fogo dura"""
    n=4
    def __init__(self,estagio=0,duracao = DURACAO_PADRAO_FOGO) -> None:
        self.estagio = estagio
        self.duracao = duracao
    def passa_proximo_estagio(self):
        self.estagio = self.estagio+1

    def ultimo_estagio(self)->bool:
        if (self.estagio == self.duracao):
            return True
        return False
    

N_ESTADOS = 6

colors = {CINZAS.n: 'gray',ARVORE.n: 'green',AGUA.n: 'blue',PEDRA.n: 'black', FOGO.n: 'yellow'}
CMAP  = ListedColormap([colors[i] for i in sorted(colors.keys())])

def contaVizinhosFOGO(floresta,i,j):
    """Conta o numero de vizinhos que estao pegando fogo para uma determinada celula na posição Linha i Coluna j"""
    contador = 0
    if isinstance(floresta[(i+1)][(j+1)],FOGO):
        contador += 1
    if isinstance(floresta[(i+1)][(j)],FOGO):
        contador += 1
    if isinstance(floresta[(i+1)][(j-1)],FOGO):
        contador += 1
    if isinstance(floresta[(i)][(j+1)],FOGO):
        contador += 1
    if isinstance(floresta[(i)][(j-1)],FOGO):
        contador += 1
    if isinstance(floresta[(i-1)][(j+1)],FOGO):
        contador += 1
    if isinstance(floresta[(i-1)][(j)],FOGO):
        contador += 1
    if isinstance(floresta[(i-1)][(j-1)],FOGO):
        contador += 1
    return contador

def contaVizinhosARVORE(floresta,i,j):
    """Conta o numero de vizinhos que sao arvores para uma determinada celula na posição Linha i Coluna j"""
    contador = 0
    if isinstance(floresta[(i+1)][(j+1)],ARVORE):
        contador += 1
    if isinstance(floresta[(i+1)][(j)],ARVORE):
        contador += 1
    if isinstance(floresta[(i+1)][(j-1)],ARVORE):
        contador += 1
    if isinstance(floresta[(i)][(j+1)],ARVORE):
        contador += 1
    if isinstance(floresta[(i)][(j-1)],ARVORE):
        contador += 1
    if isinstance(floresta[(i-1)][(j+1)],ARVORE):
        contador += 1
    if isinstance(floresta[(i-1)][(j)],ARVORE):
        contador += 1
    if isinstance(floresta[(i-1)][(j-1)],ARVORE):
        contador += 1
    return contador

def colocaFogoAleatorio(floresta,n):
    """Coloca n Celulas da floresta no estado FOGO)
    A escolha das Celulas é aleatória"""
    t = len(floresta)-1
    for i in range(n):
        linha = random.randint(0,t)
        coluna = random.randint(0,t)
        while ((isinstance(floresta[linha][coluna],ARVORE))==False):
            linha = random.randint(0,t)
            coluna = random.randint(0,t)
        type(floresta[linha][coluna] ,FOGO)
    return floresta
        
def calculaProximaGeracao(floresta):
    """Dada uma floresta, calcula a próxima geração de acordo com as regras:
    Se uma arvore tem algum vizinho fogo, tem uma chance de ela virar fogo
    O fogo avança para o proximo estagio, e caso ja esteja no ultimo, ele vira cinzas
    Uma celula cinza com vizinho arvore pode virar uma arvore"""
    copia = floresta.copy()
    n = len(floresta)
    for i in range(n):
        for j in range(n):
            if isinstance(floresta[i][j],ARVORE):
                x = contaVizinhosFOGO(floresta,i,j)
                r = random.random()
                if (1-CHANCE_ARVORE_PEGAR_FOGO)**x < r:
                    copia[i][j] = FOGO()
            elif isinstance(floresta[i][j],AGUA) or (isinstance(floresta[i][j], PEDRA)):
                pass
            elif isinstance(floresta[i][j],FOGO):
                copia[i][j].passa_proximo_estagio()
                if (copia[i][j].ultimo_estagio()):
                    copia[i][j] = CINZAS()
            
    return copia

def matriz_de_cores(floresta):
    """Recebe uma floresta, que é uma matriz de objetos, e retorna uma matriz com os valores n usados para desenhar a floresta"""
    n_linhas = len(floresta)
    n_colunas = len(floresta[0])
    matriz = np.zeros((n_linhas,n_colunas),dtype=int)
    for i in range(n_linhas):
        for j in range(n_colunas):
            matriz[i][j]=floresta[i][j].n
    return matriz

def cria_floresta(n):
    floresta = np.full((n,n),ARVORE())
    floresta[0] = np.full(n,PEDRA())
    floresta[n-1] = np.full(n,PEDRA())
    floresta[:,0] = PEDRA()
    floresta[:,(n-1)] = PEDRA()
    return floresta

def main():
    floresta = cria_floresta(TAMANHO_FLORESTA)
    
    floresta[9] = np.full(TAMANHO_FLORESTA,AGUA())
    floresta[TAMANHO_FLORESTA//2][TAMANHO_FLORESTA//2] = FOGO()
    fig,ax = plt.subplots()
    im =ax.imshow(matriz_de_cores(floresta),cmap=CMAP,vmin = 0, vmax = N_ESTADOS-1)
    plt.show(block = False)
    plt.pause(1)

    for i in range(NUMERO_ESTAGIOS):
        floresta = calculaProximaGeracao(floresta)
        im.set_data(matriz_de_cores(floresta))
        plt.draw()
        plt.pause(.5)   
    

if __name__ == '__main__':
    main()