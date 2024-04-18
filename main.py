import textwrap


def menu():
    opcao = input("""
[d] Depositar
[s] Sacar
[e] Extrato
[u] Novo Usuário
[c] Nova Conta
[l] Listar Contas
[q] Sair
=> """)
    return opcao


def deposito(valor, saldo, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print(f'Depósito realizado com sucesso!')
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato


def saque(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print(f"Operação falhou! O valor do saque excede o limite de R$ {limite:.2f}.")
    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print('Saque realizado com sucesso!')
    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo, extrato, numero_saques


def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

    return saldo, extrato


def novo_usuario(usuarios):
    cpf = str(input('CPF: (apenas números) '))
    usuario = filtrar_usuarios(cpf, usuarios)

    if usuario:
        print('CPF já cadastrado!')
        return

    nome = str(input('Nome: '))
    dt_nasc = str(input('Data de Nascimento: dd/mm/aaaa '))
    endereco = str(input('Logradouro,nº - Bairro - Cidade/Sigla Estado: '))

    usuarios.append({'nome': nome, 'dt_nasc': dt_nasc, 'cpf': cpf, 'endereco': endereco})

    print('Cadastro realizado com sucesso!')


def filtrar_usuarios(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario['cpf'] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def nova_conta(agencia, nro_conta, usuarios):
    cpf = str(input('CPF: '))
    usuario = filtrar_usuarios(cpf, usuarios)

    if usuario:
        print('Conta criada com sucesso!')
        return {'agencia': agencia, 'nro_contas': nro_conta, 'usuario': usuario}

    print('Usuário não encontrado! Criação de conta encerrada.')


def exibir_contas(contas):
    for conta in contas:
        linha = f'''\
        Agência :\t{conta['agencia']}
        C/C:\t\t{conta['nro_contas']}
        Titular:\t{conta['usuario']['nome']}
        '''
        print('='*100)
        print(textwrap.dedent(linha))


saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3
usuarios = []
contas = []
AGENCIA = '0001'
nro_conta = 0

while True:
    opcao = menu()

    if opcao == "d":
        valor = float(input("Informe o valor do depósito: "))
        saldo, extrato = deposito(valor, saldo, extrato)

    if opcao == "s":
        valor = float(input("Informe o valor do saque: "))
        saldo, extrato, numero_saques = saque(saldo=saldo, valor=valor, extrato=extrato, limite=limite, numero_saques=numero_saques, limite_saques=LIMITE_SAQUES)

    elif opcao == "e":
        saldo, extrato = exibir_extrato(saldo, extrato=extrato)

    elif opcao == 'u':
        novo_usuario(usuarios)

    elif opcao == 'c':
        nro_conta = len(contas) + 1
        conta = nova_conta(AGENCIA, nro_conta, usuarios)

        if conta:
            contas.append(conta)

    elif opcao == 'l':
        exibir_contas(contas)

    elif opcao == "q":
        break
else:
    print("Operação inválida, por favor selecione novamente a operação desejada.")