# Importação:
from geracoes_automaticas import *

class Fighter:
    '''
    Esta é a classe Fighter que irá conter todos os atributos principais dos combatentes,
    mais a frente terá uma função que recebe 2 Fighters como parametro e executa o combate.
    TODO: ESTÁ CLASSE SERÀ COMPLETAMENTE REFATORADA PARA MONTAR CLASSES MENORES E AUXILIARES DA CLASSE FIGHTER,
    ONDE ELA IRÁ MANTER APENAS O BÁSICO PARA ESTRUTURA DO FIGHTER EM QUESTÃO.
    MAS ANTES PRECISO FINALIZAR ELA PARA SABER O QUE NECESSARIAMENTE IRÁ PRECISAR DE REFATORAÇÃO.
    '''
    def __init__(self, nome: str) -> None:
        '''
        Metodo construtor que recebe como parametro apenas o nome. O resto é definido aleatoriamente
        pelo sistema de criação de ficha.
        
        Nível e Experiência:
        '''
        self.nivel = 1
        self.experiencia = 0

        '''
        Atributos e Informações Básicas:
        '''
        self.nome = nome

        # Atributos Principais Visiveis do Fighter:
        self.forca = 2
        self.agilidade = 2
        self.velocidade = 2
        # Atributo Principal não visivel:
        self.resistencia = gerar_resistencia()
        
        '''
        Atributos Secundarios Visiveis:
        '''
        self._taxa_critico = 0.05  # 5% de chance de critico
        self._multiplicador_dano_critico = 1.5  # Aumento de 50% base no dano.
        self._dano_base = 5

        '''
        Lista de Armas e Pets do Fighter:
        '''
        # Arma padrão:
        self.lista_de_armas = []  # Será uma lista de Classes (Objetos já prontos das armas).
        self.arma_equipada = None  # Será um objeto da arma equipada.

        # Lista de efeitos:
        self.vantagens = []
        self.buffs_ativos = []
        self.debuffs_ativos = []

        # Pet Padrão:
        self.pets = []  # Lista de objetos pets que o lutador poderá ter.

        '''
        Dados Ocultos:
        Todos as taxas e dados abaixo são representados por um valor em porcentagem sendo o 0.01 -> 1% e o 1 -> 100%.
        '''
        
        # Armadura Base:
        ''' Atributo armadura será um percentual que irá reduzir diretamente 
        o dano recebido, após todos os modificadores e manobras
        Ex: Dano = 15 Armadura = 0.08 (8%) -> Dano = 13.8'''
        self._armadura = 0.0  # Será calculado em porcentagem.
        
        # Precisão Base:
        ''' Precisão será o atributo base para acertar o antagonista direto da 
        evasão. '''
        self._precisao = 0.80  # Valor base se inicia em 80% e é aumentado pelo valor de agilidade.

        # Chance de bloquear o dano:
        '''A taxa de bloqueio é o atributo que determina a chance base padrão para se bloquear
        um ataque, este valor será usando no calculo da propriedade bloqueio que irá retornar
        valor real de bloqueio do Fighter.
        Ao bloquear um ataque o Fighter recebe apenas 10% do dano real do ataque que ainda será reduzido
        pela Armadura
        Ex: Dano = 100 -> Após bloqueado Dano = 10 -> Após Armadura = 0.1 (10% de redução de dano) Dano = 9.
        '''
        self._taxa_bloqueio = 0.05  # O este é o valor base para calculo, não representa a chance real de bloquear.

        # Chance de Combo:
        ''' A taxa de combo é o atributo que determina a chance base padrão para quando um personagem atacar
        ele poder executar um novo ataque em sequencia. Um ataque de combo, nunca pode gerar outro ataque de
        combo, assim evitando um  possivel loop inifinito de ataques. '''
        self._taxa_combo = 0.05 # O valor base de calculo.
        
        # Chance de Contra-Atacar Base:
        ''' O contra-ataque é o atributo que determina se o Fighter quando for receber um ataque, irá atacar antes
        de receber o golpe do oponente ou não. Junto com a Deflexão (ver abaixo) eles formam a ideia central do 
        contra-ataque. '''
        self._taxa_contra_ataque = 0.05  # Valor base para contra-atacar.

        # Chance de Defletir ataques:
        ''' Deflexão é o atributo que determina quando o Fighter executa um contra-ataque bem sucedido, a chance 
        de evitar que o usuario ataque após receber o dano do contra-ataque. '''
        self._taxa_deflexao = 0.1  # 10%

        # Chance de Desarmar ao atacar:
        '''O Desarme é o atributo que determina quando o Fighter ataca, a chance que ele tem de desarmar o alvo. '''
        self._taxa_desarme = 0.05  # Valor base de desarmar o alvo.

        # Chance de Evasão base:
        ''' A Evasão é o atributo que determina se o Fighter irá se esquivar ou não, tendo sua chance reduzida pelo
        atributo self.precisao, caso a esquiva seja ativada o Fighter ignora completamente o dano que irá receber.
        Das manobras ela é a prioridade no teste, antes de qualquer outra manobra ser testada ela é sempre a primeira a
        ser validada'''
        self._taxa_evasao = 0.05  # Valor base que é aumentado pelo valor de agilidade.

        # Chance de Reversão ao receber ataques:
        ''' A reversão é o atributo que determina a chance do Fighter de atacar, após receber um ataque, ele só funciona se
        o Fighter tiver recebido dano ou bloqueado, não sendo ativado caso o fighter tenha esquivado. '''
        self._taxa_reversao = 0.05  #

        '''
        Modificadores de Atributo Primario e Secundario: Os modificadores serão separados em dois modelos:
        FIXOS ->
        PERCENTUAIS -> 
        '''
        # Modificadores de atributo principais:
        
        # Força:
        self.modificador_percentual_forca = 1.0  # Aumento em Porcentagem % usado para calculos.
        self.modificador_fixo_forca = 0  # Aumento fixo ↑ inteiro
        # Agilidade:
        self.modificador_percentual_agilidade = 1.0  # Aumento em Porcentagem %
        self.modificador_fixo_agilidade = 0  # Aumento fixo ↑ inteiro
        # Velocidade:
        self.modificador_percentual_velocidade = 1.0  # Aumento em Porcentagem %
        self.modificador_fixo_velocidade = 0  # Aumento fixo ↑ inteiro
        # Resistência:
        self.modificador_percentual_resistencia = 1.0  # Aumento em Porcentagem %
        self.modificador_fixo_resistencia = 0  # Aumento fixo ↑ inteiro

        # Modificadores de atributos secundarios:

        # Pontos de Vida:
        self.modificador_percentual_pontos_vida = 1.0  # Será em porcentagem.
        self.modificador_fixo_pontos_vida = 0  # Será inteiro.
        # Iniciativa:
        self.modificador_percentual_iniciativa = 1.0  # Será em porcentagem.
        self.modificador_fixo_iniciativa = 0  #
        # Armadura:
        ''' Na Armadura os aumentos serão diferentes, só existem aumentos fixos que impactam
        diretamente no percentual do atriburo self._armadura'''
        self.modificador_fixo_armadura = 0.0
        # Dano:
        ''' O dano pode ser aumentado atravez de forma percentual e de forma fixa. '''
        self.modificador_percentual_dano = 1.0 # É em porcentagem.
        self.modificador_fixo_dano = 0 # É um valor fixo inteiro.
        # Critico (Chance e Multiplicador de Dano):
        ''' No critico os aumentos fixos percentuais que impactam no dano e na chance de causar um acerto critico.
        Estes valores serão em porcentagem, mas serão somados em vez de serem multiplicados Exemplo:
        -> Atual = 5% + 0.5% modificado. '''
        self.modificador_fixo_chance_critico = 0.0 
        self.modificador_fixo_dano_critico = 0.0  #
        # Precisão:
        ''' Precisão só a modificadores fixos que serão somados diretamente na base de calculo. '''
        self.modificador_fixo_precisao = 0

        # Modificadores de Manobras de Combate (Evasão, Contra-Ataque, Reversão, etc):
        ''' Esses atributos são os modificadores fixos das manobras de combate, onde eles serão alterados
        para realização de calculos no propertys respectivos, baseado em seus atributos. '''
        # Bloqueio:
        self.modificador_fixo_bloqueio = 0.0 # 95%
        # Combo:
        self.modificador_fixo_combo = 0.0
        # Contra-ataque:
        self.modificador_fixo_contra_ataque = 0.0
        # Deflexão:
        self.modificador_fixo_deflexao = 0.0
        # Desarme:
        self.modificador_fixo_desarme = 0.0
        # Evasão:
        self.modificador_fixo_evasao = 0.0
        # Reversão:
        self.modificador_fixo_reversao = 0.0
            
        # Inicializando os pontos de vida atuais:
        self._pontos_vida_atual = self.pontos_vida_maximo
        # Final do Construtor.
    
    def __repr__(self):
        return f"<Fighter: {self.nome} | PV: {self.pontos_vida_atual:.1f}/{self.pontos_vida_maximo:.1f} | Nível: {self.nivel}>"

    # Propriedades da Classe Fighter:
    '''
    Atributos Principais Finais: (Após todos modificadores)
    '''
    @property
    def forca_final (self):
        ''' Retorna a força final, a que aparecera como atributo do Fighter. '''
        return (self.forca + self.modificador_fixo_forca) * self.modificador_percentual_forca
    
    @property
    def agilidade_final (self):
        ''' Retorna a agilidade final, a que aparecera como atributo do Fighter. '''
        return (self.agilidade + self.modificador_fixo_agilidade) * self.modificador_percentual_agilidade
    
    @property
    def velocidade_final (self):
        ''' Retorna a velocidade final, a que aparecera como atributo do Fighter. '''
        return (self.velocidade + self.modificador_fixo_velocidade) * self.modificador_percentual_velocidade
    
    @property
    def resistencia_final (self):
        ''' Retorna a resistência final, a que aparecera como atributo do Fighter. '''
        return (self.resistencia + self.modificador_fixo_resistencia) * self.modificador_percentual_resistencia
    
    @property
    def pontos_vida_maximo (self):
        ''' Determina o quanto de vida o Fighter tem. '''
        base = 50 + (self.resistencia_final * 4) + ((self.nivel ** 1.2) * 1.2)
        return (base + self.modificador_fixo_pontos_vida) * self.modificador_percentual_pontos_vida
    
    @property
    def pontos_vida_atual (self):
        return self._pontos_vida_atual
    
    @pontos_vida_atual.setter
    # Garanto que o valor não seja maior que os pontos de vida máximo e nem seja menor que 0:
    def pontos_vida_atual (self, incremento_decremento):
        ''' Atributo Property que será responsavel pela auteração dos pontos de vida. '''
        self._pontos_vida_atual = max(0, min(incremento_decremento, self.pontos_vida_maximo))
    
    '''
    Atributos Secundários: 
    '''
    # Armadura Final: (Usada nos calculos para redução de dano)
    @property
    def armadura_final (self) -> float: # Porcentagem.
        '''
        Retorna o valor final de Armadura, que será aplicado nos calculos de redução de dano. 
        O valor retornado será em porcentagem de 0.0 = 0% á 1.0 = 100%, sendo que só é possivel
        reduzir o dano até no máximo 50%.
        '''
        armadura_final = self._armadura + self.modificador_fixo_armadura
        return min(armadura_final, 0.5) # Aqui uso o min e limito o valor maximo ser o 0.5 = 50%.
    
    # Iniciativa Final: (Usado para determinar a ordem na rodada) 
    @property
    def iniciativa_final (self) -> int:
        ''' Retorna o valor final da Iniciativa, que será aplicado nos calculos de ordem da rodada. '''
        iniciativa = (self.velocidade * 2) + self.agilidade + self.modificador_fixo_iniciativa
        return iniciativa * self.modificador_percentual_iniciativa
    
    # Precisão Final: (Usado para determinar se o Fighter irá acertar ou não)
    @property
    # TODO: Implementar um sistema balanceado de evasão/bloqueio e precisão.
    def precisao_final (self) -> float: # Porcentagem.
        '''
        Retorna o valor final da precisão já adicionado todos modificadores e atributos:
        Base de calculo dos atributos é:
        A cada 1 ponto de Agilidade = +1% em precisão
        A cada 2 pontos de Velocidade = +1% em precisão (1 ponto de velocidade fornece +0.5% em precisão)
        '''
        base = self._precisao + self.modificador_fixo_precisao
        modificador_atributo = (self.agilidade_final * 0.01) + ((self.velocidade_final / 2) * 0.01)
        # Caso a lista de buffs esteja vazia:
        if not self.buffs_ativos:
            # Calcula a base ao modificadores de atributos:
            precisao_total = base + modificador_atributo
            # Retorna o valor total:
            return min(precisao_total, 1.0) # Precisão não será maior que 1.0 (100%).
        # Caso a lista não esteja vazia:
        else:
            # Olha se existem buffs que envolvem precisão:
            for buff in self.buffs_ativos:
                # Testa atributo por atributo procurando o self.modificador_fixo_precisao:
                if hasattr (buff, "modificador_fixo_precisao"): # Se achar.
                    # Adiciona o valor do buff a base do calculo:
                    base += buff.modificador_fixo_precisao
            # Olha se existem debuffs que envolvem precisão:
            for debuff in self.debuffs_ativos:
                # Testa atributo por atributo procurando o self.modificador_fixo_precisao:
                if hasattr (debuff, "modificador_fixo_precisao"): # Se achar.
                    # Adiciona o valor do debuff a base do calculo:
                    base -= debuff.modificador_fixo_precisao
            # Calcula a base aumentada ou decrementada ao modificadores de atributos:
            precisao_total = base + modificador_atributo
            # Retorna o valor total:
            return max(0.10, precisao_total) # Limita para que a precisão minima não caia menor que 10%.
    
    # Velocidade de Ataque Final: (Determina quantas vezes o Fighter irá agir na rodada)                        
    @property
    # TODO: Decidir se o no combate a ação sera baseada na decrementação da hit speed ou na incrementação até
    # chegar no valor da hit speed.
    def velocidade_ataque_final(self) -> float:
        '''
        Retorna o valor da velocidade de ataque que sera decrementada ou incrementada (ainda não decide) por tick 
        até alcançar o valor da ação.
        '''
        # Definindo a base para caso
        if self.arma_equipada and hasattr(self.arma_equipada, "modificador_velocidade_ataque"):
            base = self.arma_equipada.modificador_velocidade_ataque
        else:
            base = 1.0  # base padrão desarmado.
        # Incrementos de velocidade e agilidade usando raiz quadrada, para valores muito altos não
        # acabarem sobrepujando os valores mais baixos. Exemplo:
        # Alguem com 100 de velocidade e 2 de agilidade só seria em torno de 2.5x mais rapido que alguem com
        # 10 de velocidade e 2 de agilidade, tornando a curva de subida mais suave.
        incremento_velocidade = (self.velocidade_final ** 0.5) * 0.3
        incremento_agilidade = (self.agilidade_final ** 0.5) * 0.2
        # Calculando finalmente a velocidade de ataque real:
        velocidade = base + incremento_velocidade + incremento_agilidade
        # Retornando o valor com no minimo 0.5, para que nenhum player fique travado:
        return max(0.5, velocidade)
    
    # Chance de Crítico Final: (Determina a chance do personagem causar um golpe crítico ao atacar)
    @property
    def chance_critica_final(self):
        '''
        Retorna a chance final de acerto crítico.
        A fórmula é composta por três partes:
        1. Um valor base (5%) que representa a chance mínima de crítico que todo personagem possui.
        2. Um bônus baseado na **Agilidade Final**, calculado da seguinte forma:
        - Para cada 3 pontos de Agilidade, o personagem ganha aproximadamente **1.2%** de chance de crítico.
        - Ou seja, a `chance bônus = (Agilidade Final ÷ 3) × 0.012`
        3. Caso o personagem esteja usando uma arma que forneça uma chance adicional de crítico, este valor será usado no lugar do valor base.
        A chance total é limitada a no máximo 80% (0.8), mesmo com alta agilidade ou armas muito poderosas.
        Exemplo:
        - Agilidade Final = 30 → Bônus = (30 / 3) × 0.012 = 0.12 (12%)
        - Com base de 5%, chance final = 17% (ou mais se a arma contribuir).
        
        O valor final é limitado a no máximo 80% de chance.
        '''
        # Modificador de crítico baseado na agilidade:
        modificador_agilidade = (self.agilidade_final / 3 * 0.012)
        
        # Define a base de chance de crítico:
        if self.arma_equipada and hasattr(self.arma_equipada, "taxa_critica"):
            base = self.arma_equipada.taxa_critica  # Usa a taxa crítica da arma, se existir
        else:
            base = self._taxa_critico  # Usa a taxa crítica base do personagem
        
        # Soma os modificadores e retorna o valor final limitado a 80%:
        chance_critica = base + modificador_agilidade
        return min(0.8, chance_critica)
    
    @property
    def multiplicador_dano_critico_final (self):
        dano_critico = self._multiplicador_dano_critico + self.modificador_fixo_dano_critico
        return dano_critico

    '''
    Atributos de Combate (Refatorados com modificadores_bonus):
    '''
    @property
    def chance_bloqueio(self) -> float:
        bonus_forca = self.forca_final * 0.0020
        base = self._taxa_bloqueio + self.modificador_fixo_bloqueio
        modificadores_bonus = self.calcular_modificadores(base, "taxa_bloqueio", "modificador_fixo_bloqueio")
        return bonus_forca + modificadores_bonus

    @property
    def chance_combo(self) -> float:
        base_atributos = (self.velocidade_final * 0.0020) + ((self.agilidade_final / 2) * 0.0020)
        base = self._taxa_combo + self.modificador_fixo_combo
        modificadores_bonus = self.calcular_modificadores(base, "taxa_combo", "modificador_fixo_combo")
        return base_atributos + modificadores_bonus

    @property
    def chance_contra_ataque(self) -> float:
        base_atributos = (self.agilidade_final * 0.002) + (self.velocidade_final * 0.002)
        base = self._taxa_contra_ataque + self.modificador_fixo_contra_ataque
        modificadores_bonus = self.calcular_modificadores(base, "taxa_contra_ataque", "modificador_fixo_contra_ataque")
        return base_atributos + modificadores_bonus

    @property
    def chance_deflexao(self) -> float:
        base_atributos = (self.agilidade_final * 0.0015) * (self.velocidade_final * 0.0010)
        base = self._taxa_deflexao + self.modificador_fixo_deflexao
        modificadores_bonus = self.calcular_modificadores(base, "taxa_deflexao", "modificador_fixo_deflexao")
        return base_atributos + modificadores_bonus

    @property
    def chance_desarme(self) -> float:
        bonus_forca = (self.forca_final * 0.001) + ((self.forca_final ** 0.7) * 0.002)
        bonus_agilidade = (self.agilidade_final * 0.0005) + ((self.agilidade_final ** 0.7) * 0.001)
        base = self._taxa_desarme + self.modificador_fixo_desarme
        modificadores_bonus = self.calcular_modificadores(base, "taxa_desarme", "modificador_fixo_desarme")
        return bonus_forca + bonus_agilidade + modificadores_bonus

    @property
    def chance_evasao(self) -> float:
        bonus_agilidade = ((self.agilidade_final ** 0.85) * 0.01) * 0.5
        bonus_velocidade = ((self.velocidade_final ** 0.6) * 0.02) / 2
        base = self._taxa_evasao + self.modificador_fixo_evasao
        modificadores_bonus = self.calcular_modificadores(base, "taxa_evasao", "modificador_fixo_evasao")
        return bonus_agilidade + bonus_velocidade + modificadores_bonus

    @property
    def chance_reversao(self) -> float:
        bonus_forca = (self.forca_final * 0.0035) + ((self.forca_final ** 0.025) * 0.015)
        bonus_velocidade = (self.velocidade_final * 0.0035) + ((self.velocidade_final ** 0.01) * 0.01)
        base = self._taxa_reversao + self.modificador_fixo_reversao
        modificadores_bonus = self.calcular_modificadores(base, "taxa_reversao", "modificador_fixo_reversao")
        return bonus_forca + bonus_velocidade + modificadores_bonus
    
    
    def calcular_modificadores (self, base:float, taxa_str:str, modificador_str:str) -> float:
        modificador_arma = 0
        if self.arma_equipada and hasattr(self.arma_equipada, taxa_str):
            modificador_arma = getattr(self.arma_equipada, taxa_str, 0)
        for buff in self.buffs_ativos:
            if hasattr(buff, modificador_str):
                base += getattr(buff, modificador_str, 0)
        for debuff in self.debuffs_ativos:
            if hasattr(debuff, modificador_str):
                base -= getattr(debuff, modificador_str, 0)
        return modificador_arma + base
      
    @property
    def dano(self):
        # Dano base:
        if self.arma_equipada is None:
            return (self._dano_base + self.forca_final + self.modificador_fixo_dano) * self.modificador_percentual_dano
        # Dano armado:
        else:
            return (self.arma_equipada.dano + self.forca_final + self.modificador_fixo_dano) * self.modificador_percentual_dano
    
    @property
    def esta_vivo(self) -> bool:
        '''
        Retorna `True` se o personagem ainda tiver pontos de vida acima de zero.
        Caso contrário, retorna `False`, indicando que está morto ou inconsciente.
        '''
        return self.pontos_vida_atual > 0
     
    # Métodos de uso no combate:
    

    def chance_acerto (self, alvo:'Fighter') -> float:
        return (self.precisao_final ** 1.0) * ((1 - alvo.chance_evasao) ** 0.8)

    def ataque(self, alvo:'Fighter', combo:True):
        # Checagem se acertou ou não:
        rolagem = random.random() # Gerando o sorteio.
        # Acertou:
        if rolagem <= self.chance_acerto(alvo):
            return True
        # Errou (Caso o alvo esquive do ataque):
        else:
            return False
        
    def calcular_combo (self) -> int:
        '''
        Retorna a quantidade de ataques que será o combo:
        Testa as chances de quantos ataques de combo serão executados.
        
        **Parâmetros:**
        - `Não recebe parâmetros.`
        
        **Retorno:**
        - Retorna quantos ataques de combo serão executados `(int)`.
        '''
        # Inicializa a variavel combo:
        combo = 0
        # Sorteio de combo:
        while random.random() <= self.chance_combo:
            combo+=1 # Sempre que é sorteado o combo é executado.
        # Retorno do método:
        return combo
        
    def ataque_combo (self, alvo:'Fighter', quantidade_ataques:int):
        pass
        
    def receber_ataque (self, dano:float, acertou:bool):
        pass
        
    def bloquear(self):
        pass
    
    def esquivar(self, dano):
        pass
    
    def sacar_arma(self):
        pass
    
    def trocar_arma(self):
        pass
    
    def arremessar_arma(self):
        pass
    
    def desarmar_oponente(self):
        pass
    
    def contra_atacar(self):
        pass
    
    def defletir(self):
        pass
    
    def reverter(self):
        pass
    
    def ativar_vantagens(self):
        pass
        
    def ganhar_exp(self):
        pass
    
    def subir_nivel(self):
        pass
        
    def escolher_alvo_combate(self):
        pass
    
    
    '''
    MÉTODOS PRONTOS:
    '''
    
    # Metodo de redução de dano: TODO: PRONTO!
    def calcular_reducao_dano(self, dano:float) -> float:
        '''
        Calcula a redução de dano com base na armadura final do personagem.

        Parâmetros:
        - dano (float): Valor bruto de dano que seria recebido antes da mitigação.

        Retorna:
        - float: Valor efetivo do dano após aplicação da redução pela armadura.

        A fórmula utilizada é:
        dano_reduzido = dano * (1 - armadura_final)

        Onde `armadura_final` representa a porcentagem de mitigação de dano.
        Exemplo:
        - Se armadura_final = 0.10 (10%) e o dano recebido é 100,
        então o dano efetivo será 100 * (1 - 0.10) = 90.
        '''
        # Formula para reduzir o dano:
        dano_reduzido = dano * (1 - self.armadura_final)
        # Retorno do metodo:
        return dano_reduzido

    # Método receber_dano: TODO: PRONTO!
    def receber_dano(self, dano:float) -> None:
        '''
        Este método não retorna nada, apenas altera o valor dos pontos de vida atual do Fighter
        baseado no dano recebido.
        
        Parâmetros:
        - Dano (float)
        
        Retorna:
        - None
        '''
        self.pontos_vida_atual -= dano 
    
    # Método Dano Critico: TODO: PRONTO!
    def dano_critico(self, dano: float) -> float:
        '''
        Calcula o valor final do dano crítico com base no dano original e
        no multiplicador de dano crítico do personagem.

        Parâmetros:
        - dano (float): Valor base de dano antes do crítico.

        Retorna:
        - float: Dano total após aplicação do multiplicador de crítico.

        Exemplo:
        - Dano = 50
        - Multiplicador_dano_critico_final = 2.0
        - Resultado = 100
        '''
        dano_total = dano * self.multiplicador_dano_critico_final
        return dano_total
    
    # Recuperar pontos de vida: TODO: PRONTO!
    def recuperar_pontos_vida(self, recuperacao:float) -> None:
        '''
        Altera os pontos de vida do personagem com base no valor fornecido.

        Parâmetros:
        - valor (float): Valor a ser somado aos pontos de vida.
        Pode ser positivo (cura) ou negativo (dano).

        Observações:
        - A integridade dos pontos de vida (mínimo 0, máximo permitido) é garantida pelo setter.
        - Usar valor negativo permite simular efeitos como cura revertida ou drenagem de vida.
        '''
        self.pontos_vida_atual += recuperacao
    
    # Desequipar arma equipada: TODO: PRONTO!
    def perder_arma(self) -> None:
        '''
        Este método não retorna nada, apenas altera o valor de self.arma_equipada para None assim
        "desarmando" o Fighter alvo. É acionado ao Desarme retornar True. 
        
        Parâmetros:
        - None
        
        Retorna:
        - None
        '''
        self.arma_equipada = None