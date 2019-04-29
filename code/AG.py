
# coding: utf-8

# Classe produto

# In[29]:


from random import random
class Produto():
    def __init__(self, nome, espaco, valor):
        self.nome = nome
        self.espaco = espaco
        self.valor = valor


# In[30]:


class Individuo():
    def __init__(self, espacos, valores, limite_espacos, geracao=0):
        self.espacos = espacos
        self.valores = valores
        self.limite_espacos = limite_espacos
        self.geracao = geracao
        self.nota_avaliacao = 0
        self.espaco_usado = 0
        self.cromossomo = []
        
        for i in range(len(espacos)):
            if random() < 0.5:
                self.cromossomo.append("0")
            else:
                self.cromossomo.append("1")
        
        self.fitness()
    def __str__(self):
        return str("Cromossomo {}\nFitness: {}\nEspaço Usado: {}"
                   .format(self.cromossomo, self.nota_avaliacao, self.espaco_usado))
                
    def fitness(self):
        nota = 0
        soma_espacos = 0
        
        for i in range(len(self.cromossomo)):
            if self.cromossomo[i] == '1':
                nota += self.valores[i]
                soma_espacos += self.espacos[i]
        if soma_espacos > self.limite_espacos:
            nota = 1
        self.nota_avaliacao = nota
        self.espaco_usado = soma_espacos
    
    def crossover(self, outro_individuo):
        corte = round(random() * len(self.cromossomo))
        
        filho1 = outro_individuo.cromossomo[0:corte] + self.cromossomo[corte::]
        filho2 = self.cromossomo[0:corte] + outro_individuo.cromossomo[corte::]
        
        filhos = [Individuo(self.espacos, self.valores, self.limite_espacos, self.geracao + 1),
                 Individuo(self.espacos, self.valores, self.limite_espacos, self.geracao + 1)]
        
        filhos[0].cromossomo = filho1
        filhos[1].cromossomo = filho2
        
        return filhos
    
    def mutacao(self, taxa_mutacao=0.05):
        #print("\nAntes: {}".format(self.cromossomo))
        for i in range(len(self.cromossomo)):
            if random() <= taxa_mutacao:
                if self.cromossomo[i] == '1':
                    self.cromossomo[i] = '0'
                else:
                    self.cromossomo[i] = '1'
        #print("\nDepos: {}".format(self.cromossomo))
        return self
                    
        


# In[43]:


class AlgoritmoGenetico():
    def __init__(self, tamanho_pop):
        self.tamanho_pop = tamanho_pop
        self.populacao = []
        self.geracao = 0
        self.melhor_solucao = 0
        
    def __str__(self):
        return str("Geracao: {}\nFitness: {}\nEspaco: {}\n Cromossomo{}\n"
    .format(self.populacao[0].geracao, self.populacao[0].nota_avaliacao, 
           self.populacao[0].espaco_usado, self.populacao[0].cromossomo))
        
    def init_pop(self, espacos, valores, limite_espacos):
        for i in range(self.tamanho_pop):
            self.populacao.append(Individuo(espacos, valores, limite_espacos))
                
        self.melhor_solucao = self.populacao[0]
    
    def ordena_pop(self):
        self.populacao = sorted(self.populacao, key = lambda populacao: populacao.nota_avaliacao, reverse = True)
    
    def melhor_individuo(self, individuo):
        if individuo.nota_avaliacao > self.melhor_solucao.nota_avaliacao:
            self.melhor_solucao = individuo
    
    def soma_avaliacoes(self):
        soma = 0
        for individuo in self.populacao:
            soma += individuo.nota_avaliacao
        return soma
    
    def seleciona_pai(self, soma_avaliacao):
        pai = -1
        valor_sorteado = random() * soma_avaliacao
        soma = 0
        i  = 0
        while i < len(self.populacao) and soma < valor_sorteado:
            soma += self.populacao[i].nota_avaliacao
            pai+=1
            i+=1
        
        return pai
    
    def resolver(self, espacos, valores, limite_espacos, taxa_mutacao, numero_geracoes):
        self.init_pop(espacos, valores, limite_espacos)
        
        self.ordena_pop()
        print(self)
        
        for geracao in range(numero_geracoes):
            soma_avaliacao = self.soma_avaliacoes()
            nova_pop = []
            
            for individuos_gerados in range(0, self.tamanho_pop, 2):
                pai1 = self.seleciona_pai(soma_avaliacao)
                pai2 = self.seleciona_pai(soma_avaliacao)
        
                filhos = self.populacao[pai1].crossover(self.populacao[pai2])
                nova_pop.append(filhos[0].mutacao(taxa_mutacao))
                nova_pop.append(filhos[1].mutacao(taxa_mutacao))
            
            self.populacao = list(nova_pop)
            
            self.ordena_pop()
            print(self)
            self.melhor_individuo(self.populacao[0])
        
        print("\n***Melhor solução***\n")
        print("Geracao: {}\nFitness: {}\nEspaco: {}\n Cromossomo{}\n"
        .format(self.melhor_solucao.geracao, self.melhor_solucao.nota_avaliacao, 
           self.melhor_solucao.espaco_usado, self.melhor_solucao.cromossomo))
        
        return self.melhor_solucao.cromossomo        
    


# In[48]:


if __name__ == '__main__':
    lista_produtos = []
    lista_produtos.append(Produto("Geladeira", 0.751, 999.90))
    lista_produtos.append(Produto("Microondas", 0.0456, 200.00))
    lista_produtos.append(Produto("Celular Caro", 0.00456, 5999.90))
    lista_produtos.append(Produto("Notebook Bom", 0.0163, 6955.90))
    lista_produtos.append(Produto("Fogao", 0.651, 699.90))
    lista_produtos.append(Produto("Guarda Roupa", 1.2, 4999.90))
    lista_produtos.append(Produto("Chinelo", 0.00002, 29.90))
    lista_produtos.append(Produto("Tv 55' ", 0.400, 2999.90))
    lista_produtos.append(Produto("Monitor 22' ", 0.152, 2550.90))
    lista_produtos.append(Produto("Computador", 0.455, 8000.90))
    
    espacos = []
    valores = []
    nomes = []
    
    limite = 2.2
    tam_pop = 20
    nova_pop = []
    taxa_mutacao = 0.05
    n_geracoes = 100
    
    for produto in lista_produtos:
        espacos.append(produto.espaco)
        valores.append(produto.valor)
        nomes.append(produto.nome)
        
    ag = AlgoritmoGenetico(tam_pop)
    solucao = ag.resolver(espacos, valores, limite, taxa_mutacao, n_geracoes)
    
    for i in range(len(lista_produtos)):
        if solucao[i] == '1':
            print("\n***Produto {}***\nNome: {}\nValor"
                  .format(i, lista_produtos[i].nome, lista_produtos[i].valor))
    
            

