from copy import deepcopy

# posicao do elemento


def get_pos(state, elem):
    return [(i, row.index(elem))
            for i, row in enumerate(state)
            if elem in row][0]


def movePec(state, x, y, i, j):
    child = deepcopy(state)
    child[x][y] = child[i][j]
    child[i][j] = ' '
    return child


def children(state):
    pos_empty = get_pos(state, ' ')
    x, y = pos_empty[0], pos_empty[1]

    states = []

    if x - 1 >= 0:
        states.append(movePec(state, x, y, x - 1, y))
    if x + 1 < 3:
        states.append(movePec(state, x, y, x + 1, y))
    if y - 1 >= 0:
        states.append(movePec(state, x, y, x, y - 1))
    if y + 1 < 3:
        states.append(movePec(state, x, y, x, y + 1))

    return states


def nmoves(queue, state):
    n = 0

    while queue[state]['path'] != -1:
        n = n + 1
        state = queue[state]['path']
    return n

# Distancia de Manhattan para calcular a diferença entre 2 pontos


def manhattan(state, final):
    h = 0
    for i, row in enumerate(state):
        for j, elem in enumerate(row):
            x, y = get_pos(final, elem)
            h = h + (abs(x - i) + abs(y - j))
    return h
# algoritmo de busca em largura (implementação adaptada)


def bfs(inicio, final):
    queue, path, visitados = [], [], []
    state = 0

    elem = {
        'state': inicio,
        'path': -1
    }

    foundsolution = False
    queue.append(elem)
    path.append(elem)

    while queue:
        current = queue.pop(0)

        if current['state'] == final:
            foundsolution = True
            break

        if current['state'] in visitados:
            continue

        visitados.append(current['state'])
        for child in children(current['state']):
            if child not in visitados:
                elem = {
                    'state': child,
                    'path': state
                }
                queue.append(elem)
                path.append(elem)

        state = state + 1

    return nmoves(path, state) if foundsolution else -1

# guloso com 2 arrays inicial e final ate chegar no ultimo passo


def guloso(inicio, final):
    queue, path, visitados = [], [], []
    state = 0

    elem = {
        'state': inicio,
        'path': -1,
        'h': manhattan(inicio, final)
    }

    foundsolution = False
    queue.append(elem)
    path.append(elem)

# loop para enquanto tiver fila pra executar
    while queue:
        current = queue.pop(0)

        if current['state'] == final:
            foundsolution = True
            break

        if current['state'] in visitados:
            continue

        visitados.append(current['state'])
        for child in children(current['state']):
            if child not in visitados:
                elem = {
                    'state': child,
                    'path': state,
                    'h': manhattan(child, final)
                }
                queue.append(elem)
                path.append(elem)

        queue = sorted(queue, key=lambda k: k['h'])
        state = state + 1

    return nmoves(path, state) if foundsolution else -1

# aEstrela tambem tem array inicial e final e chegando ate o passo final


def aEstrela(inicio, final):
    queue, path, visitados = [], [], []
    state = 0

    elem = {
        'state': inicio,
        'path': -1,
        'g': 0,
        'h+g': manhattan(inicio, final) + 0
    }

    foundsolution = False
    queue.append(elem)
    path.append(elem)

    while queue:
        current = queue.pop(0)

        if current['state'] == final:
            foundsolution = True
            break

        if current['state'] in visitados:
            continue

        visitados.append(current['state'])
        for child in children(current['state']):
            if child not in visitados:
                elem = {
                    'state': child,
                    'path': state,
                    'g': current['g'] + 1,
                    'h+g': manhattan(child, final) + current['g'] + 1
                }
                queue.append(elem)
                path.append(elem)

        queue = sorted(queue, key=lambda k: k['h+g'])
        state = state + 1

    return nmoves(path, state) if foundsolution else -1


def printar(label, board):
    print(label)
    for row in board:
        print(row)
    print('\n')

# Solucao


def test(test, obje, label='Test'):

    print('\n' + label)
    printar('Objetivo:', obje)
    printar('Inicial:', test)
    # print custo para resolver
    print('ALGORITMO GULOSO - Quantidade de passos: ', guloso(test, obje))
    print('ALGORITMO A ESTRELA - Quantidade de passos: ', aEstrela(test, obje))
    print('ALGORITMO BFS - Quantidade de passos: ', bfs(test, obje))


# main, aqui pode ser colocado os vetores como quiser para testar
if __name__ == '__main__':
    obje = [[' ', '1', '2'], ['3', '4', '5'], ['6', '7', '8']]

    test([[' ', '1', '2'], ['3', '4', '5'], [
         '6', '7', '8']], obje, 'TESTE - Solução')
    test([['1', '3', ' '], ['2', '4', '5'], ['6', '8', '7']],
         obje, 'TESTE - 2')  # rapido
    test([['1', '3', '4'], ['2', '5', '8'], ['6', ' ', '7']], obje, 'TESTE - 3')
    test([['6', '3', '8'], ['4', '1', '7'], [' ', '2', '5']], obje, 'TESTE - 4')
    test([['2', '3', '1'], [' ', '8', '6'], ['4', '7', '5']],
         obje, 'TESTE - 5')  # mais demorado e complicado
