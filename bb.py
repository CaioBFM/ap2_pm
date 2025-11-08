'''
PROGRAMACAO MATEMATICA
LINEAR AND INTEGER PROGRAMMING

Atividade Pratica 2
2025/02

Prof. Mayron Moreira

Caio Bueno Finocchio Martins
Tobias Maugus Bueno Cougo

'''

from queue import PriorityQueue

pesos = [2, 5, 3, 4]
valores = [6, 20, 12, 15]
capacidade = 10
n = len(pesos)

class No:
    def __init__(self, nivel, valor, peso, limite, itens):
        self.nivel = nivel
        self.valor = valor
        self.peso = peso
        self.limite = limite
        self.itens = itens
    def __lt__(self, outro):
        return self.limite > outro.limite

# mochila fracionaria
def limite(no):
    if no.peso >= capacidade:
        return 0
    valor_limite = no.valor
    peso_total = no.peso
    j = no.nivel + 1
    while j < n and peso_total + pesos[j] <= capacidade:
        peso_total += pesos[j]
        valor_limite += valores[j]
        j += 1
    if j < n:
        valor_limite += (capacidade - peso_total) * valores[j] / pesos[j]
    return valor_limite # ub

def branch_and_bound():
    fila = PriorityQueue()
    no_raiz = No(-1, 0, 0, 0, [])
    no_raiz.limite = limite(no_raiz)
    fila.put(no_raiz)
    melhor_valor = 0
    melhor_itens = []
    passo = 1
    print("=== Inicio do Branch and Bound ===\n")
    while not fila.empty():
        no = fila.get()
        print(f"\nPasso {passo}:")
        print(f"  Nivel: {no.nivel}")
        print(f"  Valor atual: {no.valor}")
        print(f"  Peso atual: {no.peso}")
        print(f"  Limite estimado: {no.limite:.2f}")
        print(f"  Itens escolhidos: {[i+1 for i in no.itens]}")
        passo += 1
        prox = no.nivel + 1

        # Condicao para poda por qualidade
        if no.limite < melhor_valor:
            print(f"  [PODADO POR QUALIDADE] limite={no.limite:.2f} < melhor={melhor_valor})")
            continue

        # Condicao para poda por otimalidade
        if prox >= n:
            if no.valor > melhor_valor:
                melhor_valor = no.valor
                melhor_itens = no.itens.copy()
                print(f" [NOVO MELHOR - OTIMALIDADE] Valor={melhor_valor} com itens {[i+1 for i in melhor_itens]}")
            else:
                print(f" [PODADO POR OTIMALIDADE] solucao inteira encontrada, mas sem melhorias")
            continue

        # Caso base
        peso_incl = no.peso + pesos[prox]
        valor_incl = no.valor + valores[prox]
        if peso_incl <= capacidade:
            if valor_incl > melhor_valor:
                melhor_valor = valor_incl
                melhor_itens = no.itens + [prox]
                print(f"  [NOVO MELHOR] Valor={melhor_valor} com itens {[i+1 for i in melhor_itens]}")
            no_incl = No(prox, valor_incl, peso_incl, 0, no.itens + [prox])
            no_incl.limite = limite(no_incl)
            print(f"  [+] No com item {prox+1}: val={valor_incl}, peso={peso_incl}, limite={no_incl.limite:.2f}")
            fila.put(no_incl)
        else:
            print(f"  [DESCARTADO] Item {prox+1} nao cabe (peso {peso_incl})")
        no_excl = No(prox, no.valor, no.peso, 0, no.itens)
        no_excl.limite = limite(no_excl)
        print(f"  [-] No sem item {prox+1}: val={no.valor}, peso={no.peso}, limite={no_excl.limite:.2f}")
        fila.put(no_excl)
    print("\n=== Fim da execucao ===")
    print(f"\nMelhor valor encontrado: {melhor_valor}")
    print(f"Itens escolhidos: {[i+1 for i in melhor_itens]}")

branch_and_bound()
