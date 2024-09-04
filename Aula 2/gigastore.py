# Função para cadastrar novas peças
def cadastrar_placa(estoque):
    nome = input("Digite o nome da Placa de vídeo: ")
    geracao = input("Digite a geração da placa de vídeo: ")
    quantidade = int(input("Digite a quantidade em estoque: "))
    preco = input("Digite o preço: ")
    estoque.append({"nome": nome, "geracao": geracao, "quantidade": quantidade, "preco": preco})
    print(f"Placa '{nome}' cadastrada no estoque!")

# Função para listar as placas
def listar_placas(estoque):
    if len(estoque) == 0:
        print("Nenhuma placa cadastrada.")
    else:
        for placa in estoque:
            print(f"Nome: {placa['nome']}, Geração: {placa['geracao']}, Quantidade: {placa['quantidade']}, Preço: R${placa['preco']}")

# Função para consultar Peças
def consultar_placas(estoque):
    nome = input("Digite o nome da placa para consultar: ")
    for placa in estoque:
        if placa["nome"] == nome:
            print(f"Nome: {placa['nome']}, Geração: {placa['geracao']}, Quantidade: {placa['quantidade']}, Preço: R${placa['preco']}")
            return
    print("Placa não encontrada no estoque.")

# Função para vender a placa
def vender_placa(estoque):
    nome = input("Digite o nome da placa que será vendida: ")
    for placa in estoque:
        if placa["nome"] == nome:
            quantidade = int(input("Digite a quantidade a vender: "))
            if quantidade <= placa["quantidade"]:
                placa["quantidade"] -= quantidade
                print(f"Venda registrada! Quantidade restante de '{nome}': {placa['quantidade']}")
            else:
                print("Erro: Quantidade em estoque insuficiente.")
            return
    print("Placa não encontrada no estoque.")

# Função main
def main():
    estoque = []

    while True:
        print("\n-----Bem vindo(a) a Gigabyte - Setor de placas gráficas-----")
        print("\nMenu de opções:")
        print("1. Cadastrar placa de vídeo")
        print("2. Consultar placa de vídeo")
        print("3. Listar placas de vídeo")
        print("4. Vender Placa de vídeo")
        print("5. Sair")

        opcao = input("\nEscolha uma opção: ")

        if opcao == '1':
            cadastrar_placa(estoque)
        elif opcao == '2':
            consultar_placas(estoque)
        elif opcao == '3':
            listar_placas(estoque)
        elif opcao == '4':
            vender_placa(estoque)
        elif opcao == '5':
            print("Saindo...")
            break
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    main()
