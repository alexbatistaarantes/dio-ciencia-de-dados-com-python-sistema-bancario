########################################################################
# UTILITÁRIOS

def filtrar_lista_de_dicionarios(lista, filtros):
    """ Retorna a lista de dicionários filtrada

    Args:
        lista (list of dict): lista de dicionários
        filtros (dict): dicionário de filtros (chave é o atributo a ser filtrado, valor é a condição)

    Returns:
        list of dict: lista filtrada
    """    

    lista_filtrada = []

    # percorre lista
    for item in lista:
        # percorre filtros
        for chave, valor in enumerate(filtros):
            if chave not in item.keys():
                break
            if item[chave] != valor:
                break
            lista_filtrada.append(item)

    return lista_filtrada

def get_cliente(cpf):
    """ Obtém cliente a partir do CPF

    Args:
        cpf (str): CPF

    Returns: Retorna o dicionário do cliente, e None se cliente não existir
    """

    clientes_filtrados = filtrar_lista_de_dicionarios(clientes, {"cpf": cpf})
    return None if len(clientes_filtrados) == 0 else clientes_filtrados[0]

def get_conta(agencia, numero):
    """ Obtém a conta a partir da agência e número da conta

    Args:
        agencia (str): Agência
        numero (int): Número da conta

    Returns: Retorna o dicionário da conta, e None se conta não existir
    """

    contas_filtradas = filtrar_lista_de_dicionarios(contas, {"agência": agencia, "número": numero})
    return None if len(contas_filtradas) == 0 else contas_filtradas[0]

########################################################################
# VARIAVEIS E CONSTANTES DE CONTROLE

NUMERO_INICIAL_CONTA = 1
TIPOS_DE_CONTA = {
    'normal': {'limite_saques_diário': 3, 'limite_valor_saque': 500}
}

clientes = [
    # {nome, data de nascimento, cpf, endereço}
]    

agencias = {
    "0001": {"número_conta_nova": NUMERO_INICIAL_CONTA}
}

contas = [
    # {agencia="0001", nº, tipo='normal', cpf, saldo}
]
    
operacoes = [
    # {agencia, nº conta, operação, valor}
]

########################################################################
# OPERAÇÕES

def sacar(*, conta, valor):
    pass

def depositar(conta, valor, /):
    pass

def visualizar_extrato(conta):
    pass

def cadastrar_cliente(cpf, nome, data_de_nascimento, endereco):
    """ Cadastra novo usuário no sistema bancário

    Args:
        cpf (str): CPF, somente números
        nome (str): Nome
        data_de_nascimento (str): data de nascimento
        endereco (str): endereço

    Returns:
        bool, str: True se operação realizada com sucesso, False se não, e uma mensagem informativa
    """

    #################
    # Validações

    # CPF já existe
    if len(filtrar_lista_de_dicionarios(clientes, {'cpf': cpf})) > 0:
        return False, "Já existe cliente cadastrado com o CPF."
    
    #################

    # Adiciona usuário na lista
    clientes.append({
        'cpf': cpf,
        'nome': nome,
        'data_de_nascimento': data_de_nascimento,
        'endereço': endereco
    })

    return True, "Cliente cadastrado com sucesso."

def cadastrar_conta(cpf, agencia, tipo):
    """ Cria nova conta no sistema bancário

    Args:
        cpf (str): CPF
        agencia (str): Agência
        tipo (str): Tipo de conta

    Returns:
        bool, str: True se operação realizada com sucesso, False se não, e uma mensagem informativa
    """    

    #################
    # Validações
    
    # Não existe cliente com CPF
    if len(filtrar_lista_de_dicionarios(clientes, {'cpf': cpf})) == 0:
        return False, "O CPF informado não pertence à nenhum cliente."
    # Agência não existe
    if agencia not in agencias.keys():
        return False, "A agência informada não existe."
    # Tipo de conta não existe
    if tipo not in TIPOS_DE_CONTA.keys():
        return False, "Tipo de conta informada não existe."
    
    #################

    # Cria conta
    contas.append({
        'agência': agencia,
        'número': agencias[agencia]['número_conta_nova'],
        'tipo': tipo,
        'cpf': cpf,
        'saldo': 0
    })

    # Incrementa número de conta na agência
    agencias[agencia]['número_conta_nova'] += 1

    return True, "Cliente cadastrado com sucesso."

########################################################################
# EXECUÇÃO

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
