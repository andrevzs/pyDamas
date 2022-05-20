from math import inf
from time import time
from copy import deepcopy

from input import *
from output import *
from posicao import *


def min_max(posicao, profundidade, max_jogador):
    if profundidade == 0 or posicao.get_fim_de_jogo():
        return posicao.avaliar_estado()
    if max_jogador:
        max_avaliacao = -inf
        for filho in posicao.get_proximas_jogadas():
            avaliacao = min_max(filho, profundidade - 1, False)
            max_avaliacao = max(max_avaliacao, avaliacao)
        posicao.set_avaliacao(max_avaliacao)
        return max_avaliacao
    else:
        min_avaliacao = inf
        for filho in posicao.get_proximas_jogadas():
            avaliacao = min_max(filho, profundidade - 1, True)
            min_avaliacao = min(min_avaliacao, avaliacao)
        posicao.set_avaliacao(min_avaliacao)
        return min_avaliacao


def alpha_beta(posicao, profundidade, alpha, beta, max_jogador, captura_forcada):
    if profundidade == 0 or posicao.get_fim_de_jogo():
        return posicao.avaliar_estado()
    if max_jogador:
        max_avaliacao = -inf
        for filho in posicao.get_proximas_jogadas(captura_forcada):
            avaliacao = alpha_beta(filho, profundidade - 1, alpha, beta, False, captura_forcada)
            max_avaliacao = max(max_avaliacao, avaliacao)
            alpha = max(alpha, avaliacao)
            if beta <= alpha:
                break
        posicao.set_avaliacao(max_avaliacao)
        return max_avaliacao
    else:
        min_avaliacao = inf
        for filho in posicao.get_proximas_jogadas(captura_forcada):
            avaliacao = alpha_beta(filho, profundidade - 1, alpha, beta, True, captura_forcada)
            min_avaliacao = min(min_avaliacao, avaliacao)
            beta = min(beta, avaliacao)
            if beta <= alpha:
                break
        posicao.set_avaliacao(min_avaliacao)
        return min_avaliacao


def alpha_beta_final(posicao, profundidade, alpha, beta, max_jogador, captura_forcada):
    if profundidade == 0 or posicao.get_fim_de_jogo():
        return posicao.avaliar_final_de_estado()
    if max_jogador:
        max_avaliacao = -inf
        for filho in posicao.get_proximas_jogadas(captura_forcada):
            avaliacao = alpha_beta_final(filho, profundidade - 1, alpha, beta, False, captura_forcada)
            max_avaliacao = min(max_avaliacao, avaliacao)
            alpha = max(alpha, avaliacao)
            if beta <= alpha:
                break
        posicao.set_avaliacao(max_avaliacao)
        return max_avaliacao
    else:
        min_avaliacao = inf
        for filho in posicao.get_proximas_jogadas(captura_forcada):
            avaliacao = alpha_beta_final(filho, profundidade - 1, alpha, beta, True, captura_forcada)
            min_avaliacao = min(min_avaliacao, avaliacao)
            beta = min(beta, avaliacao)
            if beta <= alpha:
                break
        posicao.set_avaliacao(min_avaliacao)
        return min_avaliacao


def determinar_profundidade_dinamica(tempo_jogada_anterior, profundidade, captura_forcada, num_jogadas):
    if captura_forcada:
        if tempo_jogada_anterior < 0.5 and num_jogadas <= 6:
            return profundidade + 1
        if profundidade > 6 and (tempo_jogada_anterior > 4 or num_jogadas > 6):
            return profundidade - 1
        return profundidade
    else:
        if tempo_jogada_anterior < 0.5:
            return profundidade + 1
        if tempo_jogada_anterior > 4.5:
            return profundidade - 1
        return profundidade


def condicoes_finalizacao(posicao, contador_pecas, captura_forcada):
    jogadas = posicao.get_proximas_jogadas(captura_forcada)
    num_pecas = posicao.contar_pecas()
    if num_pecas[0] == 0:
        print("Pretas venceram!")
        return True
    if num_pecas[1] == 0:
        print("Brancas venceram!")
        return True
    if num_pecas[0] + num_pecas[1] == contador_pecas[0]:
        contador_pecas[1] += 1
        if contador_pecas[1] == 50:
            print("Empate!")
            return True
    else:
        contador_pecas[0] = num_pecas[0] + num_pecas[1]
        contador_pecas[1] = 0
    if not jogadas:
        print("Nao ha mais jogadas possiveis! O jogo acabou.")
        return True
    return False


def main():
    tabuleiro = [['.', 'p', '.', 'p', '.', 'p', '.', 'p'],
                 ['p', '.', 'p', '.', 'p', '.', 'p', '.'],
                 ['.', 'p', '.', 'p', '.', 'p', '.', 'p'],
                 ['.', '.', '.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.', '.', '.'],
                 ['b', '.', 'b', '.', 'b', '.', 'b', '.'],
                 ['.', 'b', '.', 'b', '.', 'b', '.', 'b'],
                 ['b', '.', 'b', '.', 'b', '.', 'b', '.']]
    captura_forcada = input_jogadas_forcadas()

    posicao = Posicao(tabuleiro, True)
    tempo_jogada_anterior = 4.5
    profundidade = 6
    nenhuma_captura = [0, 0]

    while True:
        if condicoes_finalizacao(posicao, nenhuma_captura, captura_forcada):
            break

        print("Nova profundidade: {} ".format(profundidade))
        pecas_disponiveis = posicao.encontrar_capturas()
        if captura_forcada:
            exibir_tabuleiro(posicao.get_tabuleiro(), pecas_disponiveis)
            peca = input_escolher_peca(posicao, pecas_disponiveis)
        else:
            exibir_tabuleiro(posicao.get_tabuleiro())
            peca = input_escolher_peca(posicao)

        if not peca:
            break
        jogadas_validas = posicao.encontrar_jogadas_validas_por_peca(peca, captura_forcada)
        exibir_tabuleiro(posicao.get_tabuleiro(), peca, jogadas_validas)
        nova_posicao = input_escolher_casa(jogadas_validas)
        if not nova_posicao:
            break
        tabuleiro_anterior = deepcopy(posicao.get_tabuleiro())
        posicao = posicao.executar_jogada(peca, nova_posicao)
        diferencas = posicao.encontrar_jogada_feita(tabuleiro_anterior)
        exibir_tabuleiro(posicao.get_tabuleiro(), diferencas)
        print("Usuario fez a jogada mostrada acima.\n\n\n")
        if condicoes_finalizacao(posicao, nenhuma_captura, captura_forcada):
            break
        num_jogadas = len(posicao.get_proximas_jogadas())
        profundidade = determinar_profundidade_dinamica(tempo_jogada_anterior, profundidade, captura_forcada, num_jogadas)
        tabuleiro_anterior = deepcopy(posicao.get_tabuleiro())
        print("PENSANDO.....................................")
        t1 = time()
        num_pecas = posicao.contar_pecas()
        if num_pecas[0] + num_pecas[1] > 6:
            alpha_beta(posicao, profundidade, -inf, inf, True, captura_forcada)
            posicao = max(posicao.get_proximas_jogadas())
        else:
            alpha_beta_final(posicao, 20, -inf, inf, True, captura_forcada)
            posicao = max(posicao.get_proximas_jogadas())
        t2 = time()
        tempo_jogada_anterior = t2 - t1
        diferencas = posicao.encontrar_jogada_feita(tabuleiro_anterior)
        print(tempo_jogada_anterior)
        exibir_tabuleiro(posicao.get_tabuleiro(), diferencas)
        print("Computador fez a jogada mostrada acima.\n\n\n")


if __name__ == '__main__':
    main()
