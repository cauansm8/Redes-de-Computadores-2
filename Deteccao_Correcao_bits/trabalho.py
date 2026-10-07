import numpy as np # para trabalhar com matrizes

coluna_fixa = 4

# MENU
def menu():
    print("1- Paridade simples")
    print("2 - Paridade bidimensional")
    print("3 - CRC")
    print("4 - Sair")

# verificando se todos os caracteres são 0s ou 1s
def verificando_entrada(texto):
    return bool(texto) and all(caractere in '01' for caractere in texto)

# verificando se a paridade é 0 ou 1
def verificando_entrada_de_paridade(paridade):
    if paridade == '1' or paridade == '0':
        return True
    return False

# verificando se a posição é válida
def verificar_posicao(posicao, tamanho):
    if int(posicao) < 0 or int(posicao) > tamanho:
        return False
    return True

# paridade simples
def paridade_simples():
    entrada = input("Digite uma string binária (exemplo 1011001): ")

    if verificando_entrada(entrada):
        paridade = input("Paridade par (0) ou impar (1): ")

        if verificando_entrada_de_paridade(paridade):
            quadro_transmitido = entrada
            bit_de_paridade = '0'
            contagem = entrada.count("1")
            
            # PAR
            if paridade == '0':
                
                # tem número par de 1s
                if contagem % 2 == 0:
                    quadro_transmitido += '0'
                    bit_de_paridade = '0'
                # número ímpar de 1s
                else:
                    quadro_transmitido += '1'
                    bit_de_paridade = '1'

            # IMPAR
            else:

                # tem número par de 1s
                if contagem % 2 == 0:
                    quadro_transmitido += '1'
                    bit_de_paridade = '1'
                # número ímpar de 1s
                else:
                    quadro_transmitido += '0'
                    bit_de_paridade = '0'

            print("------------------------------------")
            print(f"Dados originais: {entrada}")
            print(f"Quantidade de bits '1': {contagem}")
            print(f"Bit de paridade: {bit_de_paridade}")
            print(f"Quadro transmitido: {quadro_transmitido}")
            print("------------------------------------")

            simular_ruido_paridade_simples(quadro_transmitido, paridade)
            
        else:
            print("\nEntrada inválida, retornando para o menu\n")
            return

    else:
        print("\nEntrada inválida, retornando para o menu\n")
        return


# simular ruído ao trocar um bit
def simular_ruido_paridade_simples(quadro_transmitido, paridade):
    tamanho = len(quadro_transmitido)
    
    print(f"Considerando o quadro transmitido {quadro_transmitido}")
    print(f"escolha uma posição entre 1-{tamanho} para inverter o bit OU escolha 0 para não adicionar ruído")
    posicao = input("")

    if verificar_posicao(posicao, tamanho):
        if posicao != '0':
            p = int(posicao) - 1

            # transforma para lista para conseguir acessar diretamente a posição
            q = list(quadro_transmitido)


            # invertendo -> simulando ruído
            if q[p] == '0':
                q[p] = '1'
            else:
                q[p] = '0'
        
            quadro_transmitido = "".join(q)

        receptor_detectando_falha_paridade_simples(quadro_transmitido, paridade)
    else:
        print("\nEntrada inválida, retornando para o menu\n")
        return

# receptor detectando falha da paridade simples
def receptor_detectando_falha_paridade_simples(quadro_recebido, paridade):
    contagem = quadro_recebido.count('1')
    temRuido = False

    # PAR
    if paridade == '0':
        if contagem % 2 != 0:
            temRuido = True
    
    # IMPAR
    else:
        if contagem % 2 == 0:
            temRuido = True

    print("------------------------------------")
    print(f"Quadro recebido: {quadro_recebido}")
    print(f"Tipo de paridade: {paridade} - {'Par' if paridade == '0' else 'Ímpar'}")
    print(f"Encontrou ruido: {temRuido}")
    print("------------------------------------")


# paridade bidimensional
def paridade_bidimensional():
    entrada = input("Digite uma string binária (exemplo 10101010): ")

    if verificando_entrada(entrada):
        
        matriz = calcular_tamanho_matriz(entrada)
        
        paridade = input("Paridade par (0) ou impar (1): ")

        if verificando_entrada_de_paridade(paridade):
            mostrar_paridades(matriz, paridade)
            r = inserir_erro_paridade_bidimensional(matriz)

            # se teve entrada inválida, finaliza o programa
            if r == False:
                return

            receptor_detectando_falha_paridade_bidimensional(matriz, paridade)
            mostrar_paridades(matriz, paridade)
            
        else:
            print("\nEntrada inválida, retornando para o menu\n")
            return

    else:
        print("\nEntrada inválida, retornando para o menu\n")
        return


# serve para calcular a quantidade de linhas
def calcular_tamanho_matriz(entrada):
    N = len(entrada)

    linhas = N / coluna_fixa

    # arredondando para cima sem biblioteca
    inteiro = int(linhas)
    if linhas == inteiro:
        linhas = inteiro
    else:
        if linhas > 0:
            linhas = inteiro + 1
        else:
            linhas = inteiro

    matriz = np.zeros((linhas, coluna_fixa), dtype=int)

    entrada_lista = list(entrada)
    
    # passando os valores para a matriz
    k = 0
    for i in range (matriz.shape[0]):
        for j in range (matriz.shape[1]):
            
            if k < len(entrada):
                matriz[i,j] = int(entrada_lista[k])
                k += 1
            else:
                matriz[i, j] = 0

            

    return matriz

# mostra as paridades das linhas e colunas
def mostrar_paridades(matriz, paridade):
    linhas, colunas = matriz.shape
    matriz = matriz.astype(int)
    
    cabecalho = " ".join([f"C{j+1}" for j in range(colunas)])
    print(f"\n{cabecalho} | Paridade das Linhas")
    print("-" * (len(cabecalho) + 22))
    
    paridade_linhas = np.zeros(linhas, dtype=int)

    # verificando a paridade das linhas
    for i in range(linhas):
        linha = matriz[i, :]
        soma_linha = np.sum(linha)

        # par
        if paridade == '0':
            if soma_linha % 2 == 0:
                p = 0
            else:
                p = 1

        # impar
        else:
            if soma_linha % 2 == 0:
                p = 1
            else:
                p = 0
            
        paridade_linhas[i] = p
        
        linha_str = "  ".join(str(bit) for bit in linha)
        print(f"{linha_str}  |    {p}")
    
    paridade_colunas = []

    # verificando a paridade das colunas
    for j in range(colunas):
        soma_coluna = np.sum(matriz[:, j])

        # par
        if paridade == '0':
            if soma_coluna % 2 == 0:
                p = 0
            else:
                p = 1
        
        # impar
        else:
            if soma_coluna % 2 == 0:
                p = 1
            else:
                p = 0
        
        paridade_colunas.append(p)

    print("-" * (len(cabecalho) + 22))
    
    str_p_cols = "  ".join(str(p) for p in paridade_colunas)
    print(f"{str_p_cols}  |    <-- Paridade das colunas\n")

    return paridade_linhas, paridade_colunas

# inserir erro na paridade bidimensional
def inserir_erro_paridade_bidimensional(matriz):
    l = int(input(f"Qual linha deseja inserir o erro (1-{matriz.shape[0]}): "))
    c = int(input(f"Qual coluna deseja inserir o erro (1-{matriz.shape[1]}): "))

    if (c > 0 and c <= matriz.shape[1]) and (l > 0 and l <= matriz.shape[0]):
        c -= 1
        l -= 1

        if matriz[l, c] == 0:
            matriz[l, c] = 1
        else:
            matriz[l, c] = 0

        print("(Erro inserido)")

        return True
    else:
        print("\nEntrada inválida, retornando para o menu\n")
        return False

# detectando falha de paridade bidimensional e corrigindo
def receptor_detectando_falha_paridade_bidimensional(matriz, paridade):
    
    p_linhas, p_colunas = mostrar_paridades(matriz, paridade)

    input("Pressione Enter para que o receptor detecte e corrija o erro...")


    for i in range (len(p_linhas)):
        for j in range (len(p_colunas)):
            if p_linhas[i] == 1 and p_colunas[j] == 1:
                if matriz[i, j] == 0:
                    matriz[i, j] = 1
                else:
                    matriz[i, j] = 0

                print("(Erro corrigido)")

                return


# crc
def CRC():
    entrada = input("Digite a string de dados (exemplo 1011): ")
    polinomio = input("Digite o polinômio gerador (exemplo 1101): ")

    if verificando_entrada(entrada) and verificando_entrada(polinomio):

        # adicionando os zeros
        entrada_para_calculo = grau_do_polinomio_gerador(entrada, polinomio)

        polinomio = list(polinomio)

        resto = calcular_resto_CRC(entrada_para_calculo, polinomio)
        mensagem = entrada + resto

        print("------------------------------------")
        print(f"Dados originais: {entrada}")
        print(f"Polinômio: {"".join(polinomio)}")
        print(f"Resto: {resto}")
        print(f"Mensagem transmitida: {mensagem}")
        print("------------------------------------")

        receptor_CRC(mensagem, polinomio)
    
    else:
        print("\nEntrada inválida, retornando para o menu\n")
        return False

# descobre o grau do polinomio e adiciona os zeros
def grau_do_polinomio_gerador(entrada, polinomio):

    grau = len(polinomio) - 1

    entrada = entrada + '0' * grau

    return entrada

# calcula o resto do CRC
def calcular_resto_CRC(entrada, polinomio):
    # tamanho do divisor
    p = len(polinomio)
    
    # pega os primeiros bits da divisão
    tmp = list(entrada[:p])
    
    while p < len(entrada):
        
        # se o primeiro termo for zero, então faz o XOR
        if tmp[0] == '1':
            for i in range(1, len(polinomio)):
                if tmp[i] == polinomio[i]:
                    tmp[i-1] = '0'
                else:
                    tmp[i-1] = '1'
            
        # se o primeiro termo for zero, então desloca tudo para a esquerda
        else:
            for i in range (1, len(polinomio)):
                tmp[i - 1] = tmp[i]
        
        # pega o próximo bit
        tmp[len(polinomio) - 1] = entrada[p]
        
        p += 1
    
    # agr o XOR para os últimos bits
    if tmp[0] == '1':
        
        for i in range (1, len(polinomio)):
            
            if tmp[i] == polinomio[i]:
                tmp[i-1] = '0'
            
            else:
                tmp[i-1] = '1'
    
    # se não, só faz os deslocamentos
    else:
        
        for i in range (1, len(polinomio)):
            tmp[i-1] = tmp[i]
    # descarta o último elemento -> tmp fica com o tamanho do divisor, só que o resto da divisão polinomial é
    # sempre grau do polinomio - 1
    
    return "".join(tmp[:-1])

# cálculo do CRC no receptor -> resto 0
def receptor_CRC(mensagem, polinomio):
    input("Pressione Enter para que o receptor calcule o CRC e veja que o resto será zero...")
    
    resto_receptor = calcular_resto_CRC(mensagem, polinomio)

    print("------------------------------------")
    print(f"Mensagem recebida: {mensagem}")
    print(f"Polinômio: {"".join(polinomio)}")
    print(f"Resto: {resto_receptor}")
    print("------------------------------------")

def main():
    while True:
        menu()
        escolha = input("")

        if escolha == '1':
            paridade_simples()

        elif escolha == '2':
            paridade_bidimensional()

        elif escolha == '3':
            CRC()

        else:
            print("FIM DO PROGRAMA!")
            break


main()