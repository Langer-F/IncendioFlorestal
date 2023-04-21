import numpy as np
import random
import matplotlib.pyplot as plt
from pynput import keyboard
from matplotlib.colors import ListedColormap



TAMANHO_FLORESTA = 200  #A floresta será uma matriz quadrada de lado TAMANHO_FLORESTA
CHUVA = True            #CHUVA influencia fatores como espalahamento do fogo, além de adicionar uma chance aleatória de o fogo apagar espontaneamente

CHANCE_ARVORE_PEGAR_FOGO = 0.1 #representa a chance de uma ARVORE virar FOGO. Cada vizinho FOGO aumenta a chance
CHANCE_ARVORE_NASCER = 0.01     #representa a chance de uma CINZA virar ARVORE. Cada vizinho ARVORE aumenta a chance

DURACAO_PADRAO_FOGO = 4     #quantas geracoes dura FOGO antes de virar CINZA


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
        floresta[linha][coluna] = FOGO()
    return floresta
        
def calculaProximaGeracaoQueimada(floresta):
    """Dada uma floresta, calcula a próxima geração de acordo com as regras:
    Se uma arvore tem algum vizinho fogo, tem uma chance de ela virar fogo
    O fogo avança para o proximo estagio, e caso ja esteja no ultimo, ele vira cinzas"""
    copia = floresta.copy()
    n = len(floresta)
    for i in range(n):
        for j in range(n):
            if isinstance(floresta[i][j],ARVORE):
                x = contaVizinhosFOGO(floresta,i,j)
                r = random.random()
                if (1-CHANCE_ARVORE_PEGAR_FOGO)**x < r:
                    copia[i][j] = FOGO()
            elif isinstance(floresta[i][j],FOGO):
                copia[i][j].passa_proximo_estagio()
                if (copia[i][j].ultimo_estagio()):
                    copia[i][j] = CINZAS()
            
    return copia

def calculaProximaGeracaoReflorestamento(floresta):
    """dada uma floresta, calcula a proxima geração
    uma cinza que tem vizinhos arvores pode virar uma arvore"""
    copia = floresta.copy()
    n = len(floresta)
    for i in range(n):
        for j in range(n):
            if isinstance(floresta[i][j],CINZAS):
                x = contaVizinhosARVORE(floresta,i,j)
                r = random.random()
                if (1-CHANCE_ARVORE_NASCER)**x < r:
                    copia[i][j] = ARVORE()
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
    global PAUSED
    global NEXT_ESTAGIO
    global INICIAR
    listener.start()
    
    floresta = cria_floresta(TAMANHO_FLORESTA)
    #floresta[9] = np.full(TAMANHO_FLORESTA,AGUA())                 # cria um rio na linha 9
    #floresta[TAMANHO_FLORESTA//2][TAMANHO_FLORESTA//2] = FOGO()    #Adiciona uma celula em fogo no meio da floresta
    floresta = colocaFogoAleatorio(floresta, 5)
    fig,ax = plt.subplots(figsize = (25,25),layout = 'constrained') #tamanho do grafico
    ax.set_title("Estado Inicial")
    im =ax.imshow(matriz_de_cores(floresta),cmap=CMAP,vmin = 0, vmax = N_ESTADOS-1)
    plt.text(-100,1,"P para Pausar",fontsize = 18,ha='left', wrap = True)
    plt.text(-100,6,"N para Proxima Etapa",fontsize = 18,ha='left', wrap = True)
    plt.text(-100,11,"I para iniciar",fontsize = 18,ha='left', wrap = True)
    plt.show(block = False)
    plt.pause(1)
    
    while True:
        if INICIAR:
            break
    i=0
    while True:
        if not PAUSED:
            i = i+1
            floresta = calculaProximaGeracaoQueimada(floresta)
            im.set_data(matriz_de_cores(floresta))
            ax.set_title(f"Geração {i} Estagio Queimada")
            plt.draw()
            plt.pause(.01)
        if NEXT_ESTAGIO:
            NEXT_ESTAGIO = False
            break
    i = 0
    while True:
        if not PAUSED:
            i = i+1
            floresta = calculaProximaGeracaoReflorestamento(floresta)
            im.set_data(matriz_de_cores(floresta))
            ax.set_title(f"Geracao {i} Reflorestamento")
            plt.draw()
            plt.pause(.01)
        if NEXT_ESTAGIO:
            break
    
#Adicionando Keylistener para facilitar o controle do programa
def on_press(key):
    global PAUSED
    global NEXT_ESTAGIO
    global INICIAR
    try:
        if key.char=='p':
            PAUSED = not PAUSED
        elif key.char == 'n':
            NEXT_ESTAGIO = True
        elif key.char == 'i':
            INICIAR = True
    except:
        pass

def on_release(key):
    pass

listener = keyboard.Listener(on_press=on_press)
PAUSED = False
NEXT_ESTAGIO = False
INICIAR = False

if __name__ == '__main__':
    main()