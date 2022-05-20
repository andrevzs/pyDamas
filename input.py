def input_escolher_peca(posicao, pecas_disponiveis=None):
    while True:
        if pecas_disponiveis:
            print("Capturas forcadas estao habilitadas! Voce so pode escolher as pecas marcadas.")
        coord = input("Insira as coordenadas da peca (linha+coluna sem espaco - Ex.: 70) <x para sair>: ")
        try:
            if coord.lower() == "x":
                return None

            coordenada = (int(coord) // 10), (int(coord) % 10)
            campo = posicao.get_tabuleiro()[coordenada[0]][coordenada[1]]

            if pecas_disponiveis:
                if coordenada in pecas_disponiveis:
                    if posicao.get_vez_da_branca() and campo.lower() == 'b':
                        proximas_jogadas = posicao.encontrar_jogadas_validas_por_peca(coordenada)
                        if len(proximas_jogadas) != 0:
                            return coordenada
                        else:
                            print("Peca escolhida nao tem jogadas disponiveis!")
                            continue
                    elif not posicao.get_vez_da_branca() and campo.lower() == 'p':
                        return coordenada
                    else:
                        print("Selecao invalida! Tente novamente.")
            else:
                if posicao.get_vez_da_branca() and campo.lower() == 'b':
                    proximas_jogadas = posicao.encontrar_jogadas_validas_por_peca(coordenada)
                    if len(proximas_jogadas) != 0:
                        return coordenada
                    else:
                        print("Peca escolhida nao tem jogadas disponiveis!")
                        continue
                elif not posicao.get_vez_da_branca() and campo.lower() == 'p':
                    return coordenada
                else:
                    print("Selecao invalida! Tente novamente.")
        except:
            print("Coordenada invalida! Tente novamente.")


def input_escolher_casa(jogadas_validas):
    while True:
        coord = input("Insira as coordenadas da casa (linha+coluna sem espaco - Ex.: 70) <x para sair>: ")
        try:
            if coord.lower() == 'x':
                return None
            coordenada = (int(coord) // 10), (int(coord) % 10)
            if coordenada not in jogadas_validas:
                print("Selecao invalida! Tente novamente.")
            else:
                return coordenada
        except:
            print("Coordenada invalida! Tente novamente")


def input_jogadas_forcadas():
    while True:
        forcadas = input("Voce que habilitar capturas forcadas? <sim|nao>: ")
        try:
            if forcadas.lower() == 'sim':
                return True
            if forcadas.lower() == 'nao':
                return False
            print("Escolha invalida! Tente novamente.")
        except:
            print("Entrada invalida! Tente novamente.")
