import random

def gerar_resistencia() -> int:
    '''
    Está função gera os pontos de resistência dos fighters.
    Não recebe nenhum parametro e retorna um valor inteiro entre
    7 e 12, possivelmente pode mudar no futuro.
    '''
    return random.randint(7,12)
