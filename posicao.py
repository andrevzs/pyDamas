from copy import deepcopy
from math import inf


class Posicao(object):

    def __init__(self, tabuleiro, vez_da_branca=True):
        self._tabuleiro        = tabuleiro
        self._proximas_jogadas = None
        self._fim_de_jogo      = False
        self._vez_da_branca    = vez_da_branca
        self._avaliacao        = 0

    def __gt__(self, other):
        return self._avaliacao > other.get_avaliacao()

    def __ge__(self, other):
        return self._avaliacao >= other.get_avaliacao()

    def __le__(self, other):
        return self._avaliacao <= other.get_avaliacao()

    def __lt__(self, other):
        return self._avaliacao < other.get_avaliacao()

    def __eq__(self, other):
        return self._avaliacao == other.get_avaliacao()

    def get_tabuleiro(self):
        return self._tabuleiro

    def get_fim_de_jogo(self):
        return self._fim_de_jogo

    def get_vez_da_branca(self):
        return self._vez_da_branca

    def set_vez_da_branca(self, valor):
        self._vez_da_branca = valor

    def get_avaliacao(self):
        return self._avaliacao

    def set_avaliacao(self, nova_avaliacao):
        self._avaliacao = nova_avaliacao

    def get_proximas_jogadas(self, forcadas=False):
        if self._proximas_jogadas is None:
            self.gerar_proximas_jogadas(forcadas)
        return self._proximas_jogadas

    def contar_pecas(self):
        num_brancas = 0
        num_pretas  = 0

        for i in range(len(self._tabuleiro)):
            for j in range(len(self._tabuleiro[i])):
                if self._tabuleiro[i][j] == 'b':
                    num_brancas += 1
                if self._tabuleiro[i][j] == 'B':
                    num_brancas += 1
                if self._tabuleiro[i][j] == 'p':
                    num_pretas += 1
                if self._tabuleiro[i][j] == 'P':
                    num_pretas += 1

        return num_brancas, num_pretas

    def encontrar_jogada_feita(self, anterior):
        jogada = []

        for i in range(len(self._tabuleiro)):
            for j in range(len(self._tabuleiro[i])):
                if self._tabuleiro[i][j] != anterior[i][j]:
                    jogada.append((i, j))

        return jogada

    def avaliar_final_de_estado(self):
        valor_brancas = 0
        valor_pretas  = 0

        for i in range(len(self._tabuleiro)):
            for j in range(len(self._tabuleiro[i])):
                if self._tabuleiro[i][j] == 'b':
                    valor_brancas += 2
                if self._tabuleiro[i][j] == 'B':
                    valor_brancas += 3
                if self._tabuleiro[i][j] == 'p':
                    valor_pretas += 2
                if self._tabuleiro[i][j] == 'P':
                    valor_pretas += 3

        self._avaliacao = valor_pretas - valor_brancas

        return self._avaliacao

    def encontrar_capturas(self):
        pecas_capturadas = []

        for i in range(len(self._tabuleiro)):
            for j in range(len(self._tabuleiro[i])):
                if self._vez_da_branca and (self._tabuleiro[i][j] == 'b' or self._tabuleiro[i][j] == 'B'):
                    jogada = self.encontrar_jogadas_validas_por_peca((i, j))
                    for disponivel in jogada:
                        if i - disponivel[0] == 2 or i - disponivel[0] == -2:
                            pecas_capturadas.append((i, j))
                            break
                if not self._vez_da_branca and (self._tabuleiro[i][j] == 'p' or self._tabuleiro[i][j] == 'P'):
                    jogada = self.encontrar_jogadas_validas_por_peca((i, j))
                    for disponivel in jogada:
                        if i - disponivel[0] == 2 or i - disponivel[0] == -2:
                            pecas_capturadas.append((i, j))
                            break
        return pecas_capturadas

    def avaliar_estado(self):
        valor_brancas = 0
        valor_pretas  = 0
        num_brancas   = 0
        num_pretas    = 0

        for i in range(len(self._tabuleiro)):
            for j in range(len(self._tabuleiro[i])):
                if self._tabuleiro[i][j] == 'b':
                    num_brancas += 1
                    if 2 < i < 5 and 1 < j < 6:
                        valor_brancas += 50
                    elif i < 4:
                        valor_brancas += 45
                    else:
                        valor_brancas += 40

                if self._tabuleiro[i][j] == 'B':
                    num_brancas += 1
                    valor_brancas += 60

                if self._tabuleiro[i][j] == 'p':
                    num_pretas += 1
                    if 2 < i < 5 and 1 < j < 6:
                        valor_pretas += 50
                    elif i > 3:
                        valor_pretas += 45
                    else:
                        valor_pretas += 40

                if self._tabuleiro[i][j] == 'P':
                    num_pretas += 1
                    valor_pretas += 60

        self._avaliacao = valor_pretas - valor_brancas

        if num_brancas == 0:
            self._avaliacao = inf
            self._fim_de_jogo = True
        if num_pretas == 0:
            self._avaliacao = -inf
            self._fim_de_jogo = True

        return self._avaliacao

    def gerar_proximas_jogadas(self, forcadas=False):
        self._proximas_jogadas = []
        capturas               = []
        todas_jogadas          = []

        for i in range(len(self._tabuleiro)):
            for j in range(len(self._tabuleiro[i])):
                if self._vez_da_branca:
                    if self._tabuleiro[i][j] == 'b' or self._tabuleiro[i][j] == 'B':
                        jogadas_validas = self.encontrar_jogadas_validas_por_peca((i, j), forcadas)

                        for jogada in jogadas_validas:
                            if jogada[0] - i == 2 or jogada[0] - i == -2:
                                novo_tabuleiro = self.gerar_novo_estado((i, j), jogada)
                                posicao = Posicao(novo_tabuleiro, not self._vez_da_branca)
                                capturas.append(posicao)
                            else:
                                novo_tabuleiro = self.gerar_novo_estado((i, j), jogada)
                                posicao = Posicao(novo_tabuleiro, not self._vez_da_branca)
                                todas_jogadas.append(posicao)

                else:
                    if self._tabuleiro[i][j] == 'p' or self._tabuleiro == 'P':
                        jogadas_validas = self.encontrar_jogadas_validas_por_peca((i, j), forcadas)

                        for jogada in jogadas_validas:
                            if jogada[0] - i == 2 or jogada[0] - i == -2:
                                novo_tabuleiro = self.gerar_novo_estado((i, j), jogada)
                                posicao = Posicao(novo_tabuleiro, not self._vez_da_branca)
                                capturas.append(posicao)
                            else:
                                novo_tabuleiro = self.gerar_novo_estado((i, j), jogada)
                                posicao = Posicao(novo_tabuleiro, not self._vez_da_branca)
                                todas_jogadas.append(posicao)

        if forcadas and len(capturas) > 0:
            self._proximas_jogadas = capturas
        else:
            self._proximas_jogadas = capturas + todas_jogadas

    def gerar_novo_estado(self, casa, jogada):
        copia_tabuleiro = deepcopy(self._tabuleiro)
        tipo_casa = copia_tabuleiro[casa[0]][casa[1]]

        if tipo_casa == 'b' or tipo_casa == 'B':
            if jogada[0] == 0:
                copia_tabuleiro[casa[0]][casa[1]] = 'B'
            if casa[0] - jogada[0] == 2 or casa[0] - jogada[0] == -2:
                linha  = casa[0] + (jogada[0] - casa[0]) // 2
                coluna = casa[1] + (jogada[1] - casa[1]) // 2
                copia_tabuleiro[linha][coluna] = '.'

        if tipo_casa == 'p' or tipo_casa == 'P':
            if jogada[0] == 7:
                copia_tabuleiro[casa[0]][casa[1]] = 'B'
            if casa[0] - jogada[0] == 2 or casa[0] - jogada[0] == -2:
                linha  = casa[0] + (jogada[0] - casa[0]) // 2
                coluna = casa[1] + (jogada[1] - casa[1]) // 2
                copia_tabuleiro[linha][coluna] = '.'

        copia_tabuleiro[casa[0]][casa[1]], copia_tabuleiro[jogada[0]][jogada[1]] = copia_tabuleiro[jogada[0]][jogada[1]], copia_tabuleiro[casa[0]][casa[1]]

        return copia_tabuleiro

    def executar_jogada(self, casa, jogada):
        tabuleiro = self.gerar_novo_estado(casa, jogada)
        posicao = None

        for estado in self.get_proximas_jogadas():
            if tabuleiro == estado.get_tabuleiro():
                posicao = estado
                break

        return posicao

    def encontrar_jogadas_validas_por_peca(self, coord, forcadas=False):
        capturas        = []
        jogadas_validas = []
        casa            = self._tabuleiro[coord[0]][coord[1]]

        if casa != 'b':
            if 0 <= coord[0] < 7:
                if (coord[1] - 1) >= 0:
                    if self._tabuleiro[coord[0] + 1][coord[1] - 1] == '.':
                        jogadas_validas.append((coord[0] + 1, coord[1] - 1))
                    elif coord[0] + 2 < 8 and coord[1] - 2 >= 0:
                        if self._tabuleiro[coord[0] + 2][coord[1] - 2] == '.':
                            if casa.lower() != self._tabuleiro[coord[0] + 1][coord[1] - 1].lower():
                                capturas.append((coord[0] + 2, coord[1] - 2))

                if (coord[1] + 1) < 8:
                    if self._tabuleiro[coord[0] + 1][coord[1] + 1] == '.':
                        jogadas_validas.append((coord[0] + 1, coord[1] + 1))
                    elif coord[0] + 2 < 8 and coord[1] + 2 < 8:
                        if self._tabuleiro[coord[0] + 2][coord[1] + 2] == '.':
                            if casa.lower() != self._tabuleiro[coord[0] + 1][coord[1] + 1].lower():
                                capturas.append((coord[0] + 2, coord[1] + 2))

        if casa != 'p':
            if 0 < coord[0] < 8:
                if (coord[1] - 1) >= 0:
                    if self._tabuleiro[coord[0] - 1][coord[1] - 1] == '.':
                        jogadas_validas.append((coord[0] - 1, coord[1] - 1))
                    elif coord[0] - 2 >= 0 and coord[1] - 2 >= 0:
                        if self._tabuleiro[coord[0] - 2][coord[1] - 2] == '.':
                            if casa.lower() != self._tabuleiro[coord[0] - 1][coord[1] - 1].lower():
                                capturas.append((coord[0] - 2, coord[1] - 2))

                if (coord[1] + 1) < 8:
                    if self._tabuleiro[coord[0] - 1][coord[1] + 1] == '.':
                        jogadas_validas.append((coord[0] - 1, coord[1] + 1))
                    elif coord[0] - 2 >= 0 and coord[1] + 2 < 8:
                        if self._tabuleiro[coord[0] - 2][coord[1] + 2] == '.':
                            if casa.lower() != self._tabuleiro[coord[0] - 1][coord[1] + 1].lower():
                                capturas.append((coord[0] - 2, coord[1] + 2))

        if forcadas and len(capturas) != 0:
            return capturas

        return capturas + jogadas_validas
