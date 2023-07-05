TEMPLATE_DA_MENSAGEM_DO_MENU = """

###############
## OPERAÇÕES ##
[D] Depósito
[S] Saque
[E] Extrato
[Q] Sair

Saldo: R$ {saldo:.2f}
Saques realizados hoje: {saques_realizados_hoje}

Digite o código da operação que deseja realizar: """

# Constantes operacionais
LIMITE_SAQUE_DIARIO = 3
LIMITE_VALOR_SAQUE = 500

# Variáveis da conta
saldo = 0.0
saques_realizados_hoje = 0
extrato = ""

# Loop de operação do sistema bancário
while True:

    # Mostrando o Menu
    mensagem_do_menu = TEMPLATE_DA_MENSAGEM_DO_MENU.format(saldo=saldo, saques_realizados_hoje=saques_realizados_hoje)
    operacao = input(mensagem_do_menu).strip().upper()

    print()

    # Operação de depósito
    if(operacao == 'D'):
        print("## DEPÓSITO ##")
        
        # Loop de tentativas de inserção de valor de depósito
        while True:
            valor = float(input("Valor: R$ "))

            # Se valor for menor ou igual a 0.0
            if(valor <= 0):
                print(f"O valor de depósito deve ser maior do que R$ {0:.2f}")
                continue
            break
        
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"

    # Operação de saque
    elif(operacao == 'S'):
        print("## SAQUE ##")

        # Se não possúi saques disponíveis, volta para o menu
        if(saques_realizados_hoje >= LIMITE_SAQUE_DIARIO):
            print(f"O limite de saque diário de {LIMITE_SAQUE_DIARIO} já foi atingido. Volte amanhã.")
            continue
        
        # Se não possui saldo para saque, volta para o menu
        if(not saldo > 0):
            print("Você não possui saldo para saque.")
            continue
        
        # Loop de tentativas de inserção de valor de saque
        while True:
            valor = float(input("Valor: R$ "))

            # Se valor for menor ou igual a 0.0
            if(valor <= 0):
                print(f"O valor de saque deve ser maior do que R$ {0:.2f}")
                continue
            
            # Se valor de saque for maior que o limite
            elif(valor > LIMITE_VALOR_SAQUE):
                print(f"O seu limite de saque é de R$ {LIMITE_VALOR_SAQUE:.2f}")
                continue
            
            # Se valor de saque for maior que o saldo
            elif(valor > saldo):
                print(f"Você não possui saldo o suficiente para sacar o valor (saldo: R$ {saldo:.2f})")
                continue
            
            break

        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        saques_realizados_hoje += 1

    # Operação de extrato
    elif(operacao == 'E'):
        print("## EXTRATO ##")

        print("#################")
        if(not extrato):
            print("Não foram realizadas movimentações.", end="\n\n")
        else:
            print(extrato, end="\n\n")
        print(f"Saldo: R$ {saldo:.2f}")
        print("#################")
    
    # Sair do sistema bancário
    elif(operacao == 'Q'):
        print("Saindo do sistema bancário")
        break

    # Operação inválida
    else:
        print("Operação inválida, tente novamente.")

    print()
