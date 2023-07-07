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
        # percorre filtros, se chave não existe, ou valor diferente, sai deste loop
        for chave, valor in filtros.items():
            if chave not in item.keys():
                break
            if item[chave] != valor:
                break
        # se loop não breakou, todos os filtros bateram, então adiciona item
        else:
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

def get_operacoes_conta(conta):
    """ Retorna lista de operações da conta

    Args:
        conta (dict): Dicionário da conta

    Returns:
        list: Lista de operações da conta
    """

    return filtrar_lista_de_dicionarios(operacoes, {'agência': conta['agência'], 'número': conta['número']})

def get_tipo_conta(conta):
    """ Retorna tipo de conta

    Args:
        conta (dict): Conta

    Returns:
        dict: Tipo de conta
    """

    return TIPOS_DE_CONTA[conta['tipo']]

def add_operacao(conta, operacao, valor):
    """ Adiciona operação

    Args:
        conta (dict): Conta que realizou a operação
        operacao (str): Identificador da operação ('depósito', 'saque')
        valor (float): Valor
    """

    operacoes.append({
        'agência': conta['agência'],
        'número': conta['número'],
        'operação': operacao,
        'valor': valor
    })

########################################################################
# VARIAVEIS E CONSTANTES DE CONTROLE

NUMERO_INICIAL_CONTA = 1
TIPOS_DE_CONTA = {
    'normal': {'limite_saques_diário': 3, 'limite_valor_saque': 500}
}
agencias = {
    "0001": {"número_conta_nova": NUMERO_INICIAL_CONTA}
}

clientes = [
    # {'cpf', 'nome', 'data_de_nascimento', 'endereço'}
]    

contas = [
    # {'agência': '0001', 'número', 'tipo': 'normal', 'cpf', 'saldo'}
]

operacoes = [
    # {'agência': '0001', 'número', 'tipo': 'operação': ('depósito', 'saque'), 'saldo'}
]

########################################################################
# OPERAÇÕES

def sacar(*, conta, valor):
    """ Realiza saque na conta

    Args:
        conta (dict): Conta da operação
        valor (float): Valor de saque

    Returns:
        bool: Resultado (True se sucedido, False se falhou)
        str: Mensagem da operação
    """

    #################
    # Validações

    # Não possui saldo para saque informado
    if conta['saldo'] < valor:
        return False, "Saldo insuficiente para saque."
    
    # Não possui mais saques disponíveis no dia
    operacoes_da_conta = get_operacoes_conta(conta)
    quantidade_de_saques = len(filtrar_lista_de_dicionarios(operacoes_da_conta, {'operação': 'saque'}))
    tipo_conta = get_tipo_conta(conta)
    if quantidade_de_saques > tipo_conta['limite_saques_diário']:
        return False, f"O limite de saque diário de {tipo_conta['limite_saques_diário']} já foi atingido. Volte amanhã."
    
    # Valor de saque maior que limite do tipo de conta
    if tipo_conta['limite_valor_saque'] < valor:
        return False, f"O seu limite de saque é de R$ {tipo_conta['limite_valor_saque']:.2f}."

    # Valor menor ou igual a zero
    if valor <= 0:
        return False, f"O valor de saque deve ser maior do que {0:.2f}."

    #################

    conta['saldo'] -= valor
    
    add_operacao(conta, 'saque', valor)
    
    return True, f"Saque realizado com sucesso."

def depositar(conta, valor, /):
    """ Realiza depósito na conta

    Args:
        conta (dict): Conta da operação
        valor (float): Valor de depósito

    Returns:
        bool: Resultado (True se sucedido, False se falhou)
        str: Mensagem da operação
    """

    #################
    # Validações

    # Valor menor ou igual a zero
    if valor <= 0:
        return False, f"O valor de depósito deve ser maior do que {0:.2f}."

    #################

    conta['saldo'] += valor
    
    add_operacao(conta, 'depósito', valor)
    
    return True, f"Depósito realizado com sucesso."

def visualizar_extrato(conta):
    """ Obtém texto do extrato

    Args:
        conta (dict): Conta

    Returns:
        str: Texto do extrato
    """

    texto_extrato = """
#####################\n
####   EXTRATO   ####
#####################\n
{registros}

Saldo: R$ {saldo:.2f}
#####################\n
    """

    operacoes_conta = get_operacoes_conta(conta)

    # Se não possui operações na conta
    if len(operacoes_conta) == 0:
        registros = "Não foram realizadas movimentações\n"
    # Se possui operações na conta
    else:
        registros = ""
        # Para cada operação, adiciona registro no texto de extrato
        for operacao in operacoes_conta:
            registros += f"{operacao['operação'].title()}: R$ {operacao['valor']:.2f}\n"

    return texto_extrato.format(registros=registros, saldo=conta['saldo'])

def cadastrar_cliente(cpf, nome="", data_de_nascimento="", endereco=""):
    """ Cadastra novo usuário no sistema bancário

    Args:
        cpf (str): CPF, somente números
        nome (str): Nome
        data_de_nascimento (str): data de nascimento
        endereco (str): endereço

    Returns:
        bool: Resultado (True se sucedido, False se falhou)
        str: Mensagem da operação
    """

    #################
    # Validações

    # CPF já existe
    if get_cliente(cpf) != None:
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
        bool: Resultado (True se sucedido, False se falhou)
        str: Mensagem da operação
    """    

    #################
    # Validações
    
    # Não existe cliente com CPF
    if get_cliente(cpf) == None:
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
# MENU

def menu_selecionar_conta():
    """ Menu de seleção de uma conta
    """

    for index, conta in enumerate(contas):
        print(f"[{index+1}]: {conta['número']}")

    while True:
        index = int(input("Selecionar conta: "))
        if index <= 0 or index > len(contas):
            print("Inválido.")
            continue
        return contas[index-1]

def menu_selecionar_cliente():
    """ Menu de seleção de um cliente
    """

    for index, cliente in enumerate(clientes):
        print(f"[{index+1}]: {cliente['nome']}")

    while True:
        index = int(input("Selecionar cliente: "))
        if index <= 0 or index > len(clientes):
            print("Inválido.")
            continue
        return clientes[index-1]

def menu_cadastrar_cliente():
    """ Menu de cadastrar cliente
    """

    print("## CADASTRAR CLIENTE ##")

    cpf = input("CPF: ")
    nome = input("Nome: ")
    data_de_nascimento = input("Data de nascimento: ")
    endereco = input("Endereço: ")

    sucesso, mensagem = cadastrar_cliente(cpf, nome, data_de_nascimento, endereco)
    return sucesso, mensagem

def menu_criar_conta():
    """ Menu de criar conta
    """

    print("## CRIAR CONTA ##")

    if len(clientes) <= 0:
        return False, "Nenhum cliente cadastrado no sistema."

    print("Você precisa vincular a nova conta com um cliente, escolha o cliente da lista")
    cliente = menu_selecionar_cliente()

    return cadastrar_conta(cliente['cpf'], "0001", 'normal')

def menu_deposito():
    """ Menu de depósito
    """

    print("## DEPÓSITO ##")

    if len(clientes) <= 0:
        return False, "Nenhum cliente cadastrado no sistema."
    if len(contas) <= 0:
        return False, "Nenhum cliente cadastrado no sistema."

    print("Selecione a conta")
    conta = menu_selecionar_conta()

    # Loop de tentativas de inserção de valor de depósito
    while True:
        valor = float(input("Valor: R$ "))

        # Se valor for menor ou igual a 0.0
        if(valor <= 0):
            print(f"O valor de depósito deve ser maior do que R$ {0:.2f}")
            continue
        break
    return depositar(conta, valor)

def menu_saque():
    """ Menu de saque
    """

    print("## SAQUE ##")

    if len(clientes) <= 0:
        return False, "Nenhum cliente cadastrado no sistema."
    if len(contas) <= 0:
        return False, "Nenhum cliente cadastrado no sistema."
    
    print("Selecione a conta")
    conta = menu_selecionar_conta()

    # Loop de tentativas de inserção de valor de saque
    while True:
        valor = float(input("Valor: R$ "))

        # Se valor for menor ou igual a 0.0
        if(valor <= 0):
            print(f"O valor de saque deve ser maior do que R$ {0:.2f}")
            continue
        break
    return sacar(conta=conta, valor=valor)

def menu_extrato():
    """ Menu de Extrato
    """

    if len(clientes) <= 0:
        return False, "Nenhum cliente cadastrado no sistema."
    if len(contas) <= 0:
        return False, "Nenhum cliente cadastrado no sistema."

    print("## EXTRATO ##")

    print("Selecione a conta")
    conta = menu_selecionar_conta()

    print(visualizar_extrato(conta))

    return True, ""

def menu_principal():
    """ Menu do sistema bancário
    """

    operacoes_menu = {
        'U': {'descrição': 'Cadastrar cliente', 'função': menu_cadastrar_cliente},
        'C': {'descrição': 'Criar conta', 'função': menu_criar_conta},
        'D': {'descrição': 'Depósito', 'função': menu_deposito},
        'S': {'descrição': 'Saque', 'função': menu_saque},
        'E': {'descrição': 'Extrato', 'função': menu_extrato},
        'Q': {'descrição': 'Sair', 'função': (lambda: False, "Saindo do sistema.")}
    }

    while True:
        print()
        print("###############")
        print("## OPERAÇÕES ##")
        
        for cod, operacao in operacoes_menu.items():
            print(f"[{cod}] {operacao['descrição']}")

        # Mostrando o Menu
        cod = input("Digite o código da operação que deseja realizar: ").strip().upper()

        if(cod not in operacoes_menu.keys()):
            print("Operação inválida, tente novamente.")
        else:
            if(cod == 'Q'):
                break
            sucesso, mensagem = operacoes_menu[cod]['função']()
            print(mensagem) 

########################################################################
# EXECUÇÃO

menu_principal()
