import numpy as np
import random
import matplotlib.pyplot as plt
from pynput import keyboard
from matplotlib.colors import ListedColormap



TAMANHO_FLORESTA = 200  #A floresta será uma matriz quadrada de lado TAMANHO_FLORESTA
CHUVA = False           #CHUVA influencia fatores como espalahamento do fogo, além de adicionar uma chance aleatória de o fogo apagar espontaneamente

CHANCE_ARVORE_PEGAR_FOGO = 0.1 #representa a chance de uma ARVORE virar FOGO. Cada vizinho FOGO aumenta a chance
CHANCE_ARVORE_NASCER = 0.01     #representa a chance de uma CINZA virar ARVORE. Cada vizinho ARVORE aumenta a chance

DURACAO_PADRAO_FOGO = 4     #quantas geracoes dura FOGO antes de virar CINZA


class CINZAS():
    """Classe que representa as cinzas"""
    n = 0   #valor utilizado no color map
    
    def calcula_proxima_geracao(self,floresta,i,j):
        #Condições iniciais
        chance = CHANCE_ARVORE_NASCER
        if CHUVA:
            chance = chance*2
        
        #contando quantos vizinhos arvore existem
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
        r = random.random()
        if (1-chance)**contador<r:
            return ARVORE()
        return self


class ARVORE():
    """Classe que representa as arvores"""
    n = 1
    def calcula_proxima_geracao(self,floresta,i,j):
        #Condições iniciais
        chance = CHANCE_ARVORE_PEGAR_FOGO
        if CHUVA:
            chance = chance/2
        
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
        r = random.random()
        if (1-chance)**contador<r:
            return FOGO()
        return self


class AGUA():
    """Classe que representa a água"""
    n=2
    def calcula_proxima_geracao(self,floresta = None,i=None,j=None):
        return self

class PEDRA():
    """Classe que representa Pedras, usada para definir as bordas da floresta"""
    n=3
    def calcula_proxima_geracao(self,floresta = None,i = None,j = None):
        return self

class FOGO():
    """Classe que representa o fogo, tendo o contador como o numero de estagios que o fogo dura"""
    n=4
    def __init__(self,estagio=0,duracao = DURACAO_PADRAO_FOGO) -> None:
        self.estagio = estagio
        self.duracao = duracao
    def calcula_proxima_geracao(self,floresta = None,i = None,j = None):
        self.estagio = self.estagio + 1
        if self.estagio >= self.duracao:
            return CINZAS()
        return self


N_ESTADOS = 5

colors = {CINZAS.n: 'gray',ARVORE.n: 'green',AGUA.n: 'blue',PEDRA.n: 'black', FOGO.n: 'yellow'}
CMAP  = ListedColormap([colors[i] for i in sorted(colors.keys())])

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
            if isinstance(floresta[i][j],CINZAS):
                continue
            copia[i][j] = floresta[i][j].calcula_proxima_geracao(floresta,i,j)
    return copia

def calculaProximaGeracaoReflorestamento(floresta):
    """dada uma floresta, calcula a proxima geração
    uma cinza que tem vizinhos arvores pode virar uma arvore"""
    copia = floresta.copy()
    n = len(floresta)
    for i in range(n):
        for j in range(n):
            copia[i][j] = floresta[i][j].calcula_proxima_geracao(floresta,i,j)
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
    
    #criação da floresta
    floresta = cria_floresta(TAMANHO_FLORESTA)
    #floresta[TAMANHO_FLORESTA//2][TAMANHO_FLORESTA//2] = FOGO()    #Adiciona uma celula em fogo no meio da floresta
    floresta = colocaFogoAleatorio(floresta, 1)
    
    #parte da interface grafica
    dpi = 100
    tamanho_grid_x100 = 20
    fig,ax = plt.subplots(figsize = (tamanho_grid_x100,tamanho_grid_x100),dpi = dpi) #tamanho do grafico
    ax.set_title("Estado Inicial")
    im =ax.imshow(matriz_de_cores(floresta),cmap=CMAP,vmin = 0, vmax = N_ESTADOS)
    
    #textos da esquerda
    distancia_texto_vertical = 6
    t1 = ax.text(-1.5*dpi,0,"P para Pausar",fontsize = 16,ha='left', wrap = True)
    t2 = ax.text(-1.5*dpi,distancia_texto_vertical,"N para Proxima Etapa",fontsize = 16,ha='left', wrap = True)
    t3 = ax.text(-1.5*dpi,distancia_texto_vertical*2,"I para iniciar",fontsize = 16,ha='left', wrap = True)
    t4 = ax.text(-1.5*dpi,distancia_texto_vertical*3,"C para alterar CHUVA",fontsize = 16,ha='left', wrap = True)
    t5 = ax.text(-1.5*dpi,distancia_texto_vertical*4,"upArrow para aumentar CHANCE FOGO",fontsize = 16,ha='left', wrap = True)
    t6 = ax.text(-1.5*dpi,distancia_texto_vertical*5,"dowmArrow para diminuir CHANCE FOGO",fontsize = 16,ha='left', wrap = True)
    t7 = ax.text(-1.5*dpi,distancia_texto_vertical*6,"rightArrow para aumentar CHANCE NASCER",fontsize = 16,ha='left', wrap = True)
    t8 = ax.text(-1.5*dpi,distancia_texto_vertical*7,"leftArrow para diminuir CHANCE NASCER",fontsize = 16,ha='left', wrap = True)
    
    
    #textos da direita
    texto_chuva = ax.text(dpi*2,0,f"Chuva {CHUVA}", fontsize = 16)
    tfogo = ax.text(dpi*2,distancia_texto_vertical,f"CHANCE_ARVORE_PEGAR_FOGO = {CHANCE_ARVORE_PEGAR_FOGO}",fontsize = 16,ha='left', wrap = True)
    tnasc = ax.text(dpi*2,distancia_texto_vertical*2,f"CHANCE_ARVORE_NASCER = {CHANCE_ARVORE_NASCER}",fontsize = 16,ha='left', wrap = True)
    tEstFogo = ax.text(dpi*2,distancia_texto_vertical*3,f"Numero de estagio do fogo= {DURACAO_PADRAO_FOGO}",fontsize = 16,ha='left', wrap = True)

    plt.show(block = False)
    plt.pause(1)
    
    #loop inicial esperando o input "i" para iniciar
    while True:
        texto_chuva.set_text(f"Chuva = {CHUVA}")
        tfogo.set_text(f"CHANCE_ARVORE_PEGAR_FOGO = {CHANCE_ARVORE_PEGAR_FOGO}")
        tnasc.set_text(f"CHANCE_ARVORE_NASCER = {CHANCE_ARVORE_NASCER}")
        plt.draw()
        plt.pause(0.1)
        if INICIAR:
            break
    
    i=0     #contador das gerações

    #loop do primeiro estágio, o estágio da queimada
    while True:
        while PAUSED:
            texto_chuva.set_text(f"Chuva = {CHUVA}")
            tfogo.set_text(f"CHANCE_ARVORE_PEGAR_FOGO = {CHANCE_ARVORE_PEGAR_FOGO}")
            tnasc.set_text(f"CHANCE_ARVORE_NASCER = {CHANCE_ARVORE_NASCER}")
            plt.draw()
            plt.pause(.1)

        
        texto_chuva.set_text(f"Chuva = {CHUVA}")
        tfogo.set_text(f"CHANCE_ARVORE_PEGAR_FOGO = {CHANCE_ARVORE_PEGAR_FOGO}")
        tnasc.set_text(f"CHANCE_ARVORE_NASCER = {CHANCE_ARVORE_NASCER}")
        i = i+1
        floresta = calculaProximaGeracaoQueimada(floresta)
        im.set_data(matriz_de_cores(floresta))
        ax.set_title(f"Geração {i} Estagio Queimada")
        plt.draw()
        plt.pause(.01)
        if NEXT_ESTAGIO:
            NEXT_ESTAGIO = False
            break
    
    #Estágio de reflorestamento
        #Apagando o fogo
    for i in range(TAMANHO_FLORESTA):
        for j in range(TAMANHO_FLORESTA):
            if isinstance(floresta[i][j],FOGO):
                floresta[i][j] = CINZAS()
    i = 0
    while True:
        while PAUSED:
            texto_chuva.set_text(f"Chuva = {CHUVA}")
            tfogo.set_text(f"CHANCE_ARVORE_PEGAR_FOGO = {CHANCE_ARVORE_PEGAR_FOGO}")
            tnasc.set_text(f"CHANCE_ARVORE_NASCER = {CHANCE_ARVORE_NASCER}")
            plt.draw()
            plt.pause(.1)
        

        i = i+1
        texto_chuva.set_text(f"Chuva = {CHUVA}")
        tfogo.set_text(f"CHANCE_ARVORE_PEGAR_FOGO = {CHANCE_ARVORE_PEGAR_FOGO}")
        tnasc.set_text(f"CHANCE_ARVORE_NASCER = {CHANCE_ARVORE_NASCER}")
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
    global CHUVA
    global CHANCE_ARVORE_PEGAR_FOGO
    global CHANCE_ARVORE_NASCER
    try:
        if key.char == 'p':
            PAUSED = not PAUSED
        elif key.char == 'n':
            NEXT_ESTAGIO = True
        elif key.char == 'i':
            INICIAR = True
        elif key.char == 'c':
            CHUVA = not CHUVA
    except:
        try:
            if key == keyboard.Key.down:
                if CHANCE_ARVORE_PEGAR_FOGO > 0.01:
                    CHANCE_ARVORE_PEGAR_FOGO = CHANCE_ARVORE_PEGAR_FOGO - 0.01
                    CHANCE_ARVORE_PEGAR_FOGO = round(CHANCE_ARVORE_PEGAR_FOGO,2)
            elif key == keyboard.Key.up:
                if CHANCE_ARVORE_PEGAR_FOGO < 0.99:
                    CHANCE_ARVORE_PEGAR_FOGO = CHANCE_ARVORE_PEGAR_FOGO + 0.01
                    CHANCE_ARVORE_PEGAR_FOGO = round(CHANCE_ARVORE_PEGAR_FOGO,2)
            elif key == keyboard.Key.left:
                if CHANCE_ARVORE_NASCER > 0.01:
                    CHANCE_ARVORE_NASCER = CHANCE_ARVORE_NASCER - 0.01
                    CHANCE_ARVORE_NASCER = round(CHANCE_ARVORE_NASCER,2)
            elif key == keyboard.Key.right:
                if CHANCE_ARVORE_NASCER < 0.99:
                    CHANCE_ARVORE_NASCER = CHANCE_ARVORE_NASCER + 0.01
                    CHANCE_ARVORE_NASCER = round(CHANCE_ARVORE_NASCER,2)
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