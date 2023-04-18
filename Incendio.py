import random
import numpy as np
import matplotlib

#dsakljdjalsdlkjaskljdakljasd
class Elemento:
    """
        tipo:   0 Arvore
                1 Agua
                2 Fogo1
                3 Fogo2
                4 Fogo3
                5 Cinza
        """
    def __init__(self,tipo) -> None:
        self.tipo = tipo
        if tipo == 0:   #arvore
            self.chance = 0.5
        elif tipo == 1: #agua
            self.chance = 0
        else:
            self.chance = 0
    
    def isEmChama(self):
        if self.tipo == 2 or self.tipo == 3 or self.tipo == 4:
            return True
        return False




class Floresta:
    """Floresta composta por Elementos, contem a matriz(grid) que será utilizada para desenhar a floresta na aplicação grafica"""
    def __init__(self,n) -> None:
        self.grid = []
        for i in range(n):
            self.grid.append([])
            for j in range(n):
                x = Elemento(0)
                self.grid[i].append(x)

    def getElemento(self,linha,coluna)->Elemento:
        return self.grid[linha][coluna]
    
    def setElemento(self,linha,coluna,tipo):
        self.grid[linha][coluna] = Elemento(tipo)
    
    def imprimeGrid(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                print(f"{self.grid[i][j].tipo}",end = " ")
            print("")
    
    def calculaProximaGeracao(self):
        mat = []
        for i in range(len(self.grid)):
            mat.append([])
            for j in range(len(self.grid[i])):
                x = self.grid[i][j]
                if x.tipo == 0 :
                    r = random.random()
                    sobrevivencia = (1- x.chance) ** self.contaVizinhosEmChamas(i,j)
                    if r > sobrevivencia:
                        mat[i].append(Elemento(2))
                    else:
                        mat[i].append(Elemento(0))
                elif x.tipo == 1 :
                    mat[i].append(Elemento(1))
                elif x.tipo == 2 or x.tipo == 3 or x.tipo == 4:
                    mat[i].append(Elemento(x.tipo + 1))
                elif x.tipo == 5:
                    mat[i].append(Elemento(5))
        self.grid = mat


    def contaVizinhosEmChamas(self,i,j):
        contador = 0
        nl = len(self.grid)
        nc = len(self.grid[0])
        if self.grid[(i+1)%nl][(j+1)%nc].isEmChama():
            contador = contador +1
        if self.grid[(i+1)%nl][(j)].isEmChama():
            contador = contador +1
        if self.grid[(i+1)%nl][(j-1)%nc].isEmChama():
            contador = contador +1
        if self.grid[(i)][(j+1)%nc].isEmChama():
            contador = contador +1
        if self.grid[(i)][(j-1)%nc].isEmChama():
            contador = contador +1
        if self.grid[(i-1)%nl][(j+1)%nc].isEmChama():
            contador = contador +1
        if self.grid[(i-1)%nl][(j)].isEmChama():
            contador = contador +1
        if self.grid[(i-1)%nl][(j-1)%nc].isEmChama():
            contador = contador +1
        return contador





def imprimeMatriz(mat):
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            print(f"{mat[i][j]}",end = " ")
        print("\n")


def main():
    f = Floresta(20)
    f.setElemento(10,10, 2)
    for _ in range(4):
        f.calculaProximaGeracao()
    f.imprimeGrid()

if __name__ == '__main__':
    main()