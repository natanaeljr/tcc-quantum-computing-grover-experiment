#!/usr/bin/env python

# graph2cnf.py
# Gera o SAT para X-coloração de um grafo qualquer.
#
# Entrada: arquivo do grafo descrito por arestas:
# c cores vertices arestas
# p 3 10 15
# e 1 2
# e 1 5
# ...
#
# Saida: SAT em formato DIMACS CNF
# p cnf 18 54
# 1 2 3 0
# -1 -2 0
# -2 -3 0
# ...
#

# Script based on https://github.com/ibipul/coloring_SAT/blob/master/graph2cnf.py

import sys

for line in open(sys.argv[1]):

    if line[0] == 'p':
        # Step1:
        # gera header
        # p cnf <num_variables> <num_clauses>
        data = line.split()
        colors = int(data[1])
        vertices = int(data[2])
        edges = int(data[3])
        print("p cnf " + str(colors*vertices) + " " + str(int(vertices + vertices* colors*(colors -1)/2 + colors*edges)))

        # Step2a:
        # gera matrix de variaveis sendo que
        # para cada vertice há X cores possíveis, logo
        # num_variables = cores * vertices
        # A_red=1 OU A_green=2 OU A_blue=3
        # B_red=4 OU B_green=5 OU B_blue=6
        # ...
        vars = [[0]*(colors+1) for _ in range(vertices+1)]
        counter = 1
        v = 1
        while v <= vertices:
            c = 1
            while c <= colors:
                vars[v][c] = counter
                counter += 1
                c += 1
            v += 1

        # Step2b -> para cada vértice: gera OU de uma das 3 (ou X) cores
        # 1 OU 2 OU 3
        # 4 OU 5 OU 6
        # ...
        v = 1;
        while v <= vertices:
            c = 1;
            while c <= colors:
                print(str(vars[v][c])+" ", end='')
                if c == colors:
                    print('0')
                c += 1
            v += 1

        # Step3:
        # para cada vértice: apenas 1 cor pode ser selecionada
        # not A_red=1 OU not A_green=2 ---> not(A_red=1 and A_green=2)
        # uma das 2 cores deve ser falsa para a cláusula ser verdadeira ou as duas falsas!
        v = 1
        while v <= vertices:
            c = 1
            while c <= colors-1:
                d = c + 1
                while d <= colors:
                    print("-"+str(vars[v][c])+" -"+str(vars[v][d])+" 0")
                    d += 1
                c += 1
            v += 1

    # Step4:
    # Cada par de vértices adjacentes não podem ter o mesma cor.
    # quantidade de clausulas = (arestas*cores)
    # not A_red=1 OU B_red=4
    # not A_green=2 OU B_green=5
    # not A_blue=3 OU B_blue=6
    # not A_red=1 OU C_red=7
    # ...
    if line[0]=='e':
        data = line.split()
        u = data[1]
        v = data[2]

        c = 1
        while c <= colors:
            print("-"+str(vars[int(u)][c])+ " -" +str(vars[int(v)][c])+" 0")
            c += 1
