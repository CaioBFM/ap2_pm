'''
PROGRAMACAO MATEMATICA
LINEAR AND INTEGER PROGRAMMING

Atividade Pratica 2
2025/02

Prof. Mayron Moreira



Caio Bueno Finocchio Martins
Tobias Maugus Bueno Cougo


'''

from gurobipy import Model, GRB, quicksum

def resolve_puzzle(dimensao_puzzle, termometros, quantidade_preenchida_linhas, quantidade_preenchida_colunas, verbose=True):
    m = Model("termometro_puzzle")

    # Desativa saída se verbose=False
    if not verbose:
        m.Params.OutputFlag = 0
    # vars
    y = m.addVars(dimensao_puzzle,dimensao_puzzle, vtype=GRB.BINARY, name="esta preenchida")

    # constraints

    # termometro é preenchido de baixo para cima

    


    # Objetivo neutro (problema de viabilidade)
    m.setObjective(0, GRB.MINIMIZE)

    # Otimiza
    m.optimize()

    if m.status == GRB.OPTIMAL:
        # sol = (TODO: obtem os valores das variaveis e determina sol como a matriz com os valores das variaveis (resposta do puzzle))

        if verbose:
            print("\nSolução encontrada (1 = mercúrio, 0 = vazio):")
            for r in range(1, dimensao_puzzle+1):
                print(" ".join(str(sol[r-1][c-1]) for c in range(1, dimensao_puzzle+1)))

            print("\nSoma por linha:", [sum(sol[r-1]) for r in range(1, dimensao_puzzle+1)])
            print("Soma por coluna:", [sum(sol[r-1][c-1] for r in range(1, dimensao_puzzle+1)) for c in range(1, dimensao_puzzle+1)])
        return sol
    else:
        if verbose:
            print("Nenhuma solução encontrada.")
        return None

if __name__ == "__main__":
    dimensao_puzzle = 8

    quantidade_preenchida_colunas = [4, 6, 4, 6, 4, 6, 7, 2]
    quantidade_preenchida_linhas= [6, 5, 4, 3, 6, 3, 7, 5]

    # --- TERMOMETROS ---
    # Aqui você DEVE preencher a lista `thermometers` com os termômetros reais do puzzle.
    # Cada termômetro é uma lista de células (r,c) ordenada do fundo (bottom) para o topo.
    # Exemplo de termômetro vertical com fundo em (1,2) e topo em (3,2):
    #   [(1,2), (2,2), (3,2)]
    termometros = [
        [(1,2), (2,2), (3,2)],
        [(1,3), (2,3), (3,3)],
        [(1,4), (2,4), (3,4), (4,4)],
        [(1,5), (1,6), (1,7)],
        [(2,6), (3,6), (4,6)],
        [(4,1), (3,1), (2,1), (1,1)],
        [(4,3), (4,2)],
        [(4,5), (3,5), (2,5)],
        [(4,7), (3,7), (2,7)],
        [(5,2), (5,3), (5,4), (5,5), (5,6), (5,7)],
        [(6,2), (6,3), (6,4), (6,5), (6,6), (6,7)],
        [(7,1), (6,1), (5,1)],
        [(7,3), (7,2)],
        [(7,7), (7,6), (7,5), (7,4)],
        [(8,1), (8,2), (8,3), (8,4)],
        [(8,7), (8,6), (8,5)],
        [(8,8), (7,8), (6,8), (5,8), (4,8), (3,8), (2,8), (1,8)]
    ]

    sol = resolve_puzzle(dimensao_puzzle, termometros, quantidade_preenchida_linhas, quantidade_preenchida_colunas, verbose=True)
    if sol is None:
        print("Sem solução com os termômetros fornecidos. Verifique a lista de termômetros.")
    else:
        print("Solução encontrada com os termômetros fornecidos.")

