
class Cores:
    VERDE        = '\u001b[32m'
    VERMELHO     = '\u001b[31m'
    AZUL         = '\u001b[36m'
    PRETO        = '\u001b[30;1m'
    BRANCO       = '\u001b[37;1m'
    FUNDO_AZUL   = '\u001b[44;1m'
    FUNDO_BRANCO = '\u001b[47;1m'
    FUNDO_ROSA   = '\u001b[45m'
    FIM          = '\033[0m'


def exibir_tabuleiro(tabuleiro, selecionado=None, jogadas_validas=None):
    for i in range(len(tabuleiro)):
        if i == 0:
            print("    0    1    2    3    4    5    6    7")
            print("  __________________________________________")
        for j in range(len(tabuleiro[i])):
            if j == 0:
                print(i, end=" |")
            if tabuleiro[i][j] == 'b' or tabuleiro[i][j] == 'B':
                if selecionado and ((i, j) in selecionado or (i, j) == selecionado):
                    print(Cores.FUNDO_AZUL + Cores.PRETO + " " + str(tabuleiro[i][j]) + " " + Cores.FIM, end="  ")
                else:
                    print(Cores.VERDE + " " + str(tabuleiro[i][j]) + " " + Cores.FIM, end="  ")
            elif tabuleiro[i][j] == 'p' or tabuleiro[i][j] == 'P':
                if selecionado and ((i, j) in selecionado or (i, j) == selecionado):
                    print(Cores.FUNDO_AZUL + Cores.PRETO + " " + str(tabuleiro[i][j]) + " " + Cores.FIM, end="  ")
                else:
                    print(Cores.VERMELHO + " " + str(tabuleiro[i][j]) + " " + Cores.FIM, end="  ")
            elif jogadas_validas and (i, j) in jogadas_validas:
                print(Cores.FUNDO_BRANCO + Cores.PRETO + str(i) + " " + str(j) + Cores.FIM, end=" ")
            else:
                if selecionado and ((i, j) in selecionado or (i, j) == selecionado):
                    print(Cores.FUNDO_ROSA + Cores.PRETO + " " + str(tabuleiro[i][j]) + " " + Cores.FIM, end="  ")
                else:
                    print(" " + str(tabuleiro[i][j]) + " ", end="  ")
        print("| " + str(i))
    print("  ------------------------------------------")
    print("    0    1    2    3    4    5    6    7")
