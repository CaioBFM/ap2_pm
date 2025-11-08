'''
PROGRAMACAO MATEMATICA
LINEAR AND INTEGER PROGRAMMING

Atividade Pratica 2
2025/02

Prof. Mayron Moreira

Caio Bueno Finocchio Martins
Tobias Maugus Bueno Cougo

'''
#import pulp
from gurobipy import Model, GRB
from collections import defaultdict

# ----------------------------
# 1) Dados básicos / instância
# ----------------------------
familias = list(range(1, 11))        
dias = list(range(1, 31))    

# obtem dia da semana (1 a 7)
def dia_semana(d):
    return ((d - 1) % 7) + 1

dia_da_semana_dict = {1: "Seg", 2: "Ter", 3: "Qua", 4: "Qui", 5: "Sex", 6: "Sab", 7: "Dom"}

# remover sábado e domingo -> dias de aula T
dias_validos = [d for d in dias if dia_semana(d) not in (6, 7)]
dias_validos.sort()

preferencias_por_familia_dict = {
    1: ["Seg", "Qua", "Sex"],
    2: ["Ter", "Qui", "Seg"],
    3: ["Qua", "Ter", "Sex"],
    4: ["Seg", "Ter", "Qui"],
    5: ["Qui", "Sex", "Seg"],
    6: ["Ter", "Qua", "Qui"],
    7: ["Sex", "Qua", "Ter"],
    8: ["Seg", "Qui", "Sex"],
    9: ["Qua", "Seg", "Ter"],
    10: ["Ter", "Sex", "Qui"],
}

peso_pref = {1: 100, 2: 10, 3: 1}
dias_semana_unicos = ["Seg", "Ter", "Qua", "Qui", "Sex"]

matriz_preferencias = {(f, w): 0 for f in familias for w in dias_semana_unicos}
for f in familias:
    prefs = preferencias_por_familia_dict[f]
    for i, w in enumerate(prefs, start=1):
        matriz_preferencias[(f, w)] = peso_pref[i]

pesos_para_cada_dia = {}
for f in familias:
    for d in dias_validos:
        w = dia_da_semana_dict[dia_semana(d)]
        pesos_para_cada_dia[(f, d)] = matriz_preferencias.get((f, w), 0)

intervalo_minimo_dias = 10

# ----------------------------
# 2) Modelo Matemático: escreva seu modelo PuLP ou Gurobipy
# ----------------------------

model = Model("Merenda_Revezamento")

# ----------------------------
# 2.1) Declaração de Variáveis
# ----------------------------
y = model.addVars(familias, dias_validos, vtype=GRB.BINARY, name="y")


model.update()

# ----------------------------
# 2.2) Função Objetivo
# ----------------------------
model.setObjective(sum(pesos_para_cada_dia[(i, d)] * y[i, d] for i in familias for d in dias_validos), GRB.MAXIMIZE)

# ----------------------------
# 2.3) Restrições
# ----------------------------
for d in dias_validos:
    model.addConstr(sum(y[i,d] for i in familias) == 1)

for i in familias:
    for d1 in dias_validos:
        for d2 in dias_validos:
            if abs(d2 - d1) < intervalo_minimo_dias and d2 > d1:
                model.addConstr(y[i, d1] + y[i, d2] <= 1, name="intervalo min")

model.optimize()

# ----------------------------
# 3) Resultados / impressão
# ----------------------------
if model.status == GRB.OPTIMAL:
    objval = model.objVal
    print(f"\nObjetivo (pontuacao total): {objval}\n")
    for i in familias:
        dias_atendidos = [d for d in dias_validos if y[i, d].X == 1]
        dias_atendidos_resposta = '-'.join(str(d) for d in dias_atendidos)
        print(f"Familia {i} - Dias atendidos: {dias_atendidos_resposta}")

else:
    print("\nModelo não foi resolvido para uma solução ótima.")


