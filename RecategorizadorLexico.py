from base import MotorDeEventos
from CategorizadorSintatico import CategorizadorSintatico
from eventos import TokenId
from eventos import TokenNumero
from eventos import TokenEspecial
from eventos import TokenReservado
from eventos import TokenLinha
from constants import palavrasReservadas


def rodarAutomato2(recategorizadorLexico,evento,tempo):
	if recategorizadorLexico.estadoAtual == 'E0':
		if type(evento) == type(TokenNumero()) or type(evento) == type(TokenEspecial()) or type(evento) == type(TokenLinha()):
			evento.tempo += 1
			recategorizadorLexico.categorizadorSintatico.lista.append(evento)
		else:
			if evento.conteudo in palavrasReservadas:
				recategorizadorLexico.categorizadorSintatico.lista.append(TokenReservado(tempo=tempo+1,conteudo=evento.conteudo))
			elif evento.conteudo == "DEF" or evento.conteudo == "GO":
				recategorizadorLexico.acumulador = evento.conteudo
				recategorizadorLexico.estadoAtual = 'E1'
			elif type(evento) == type(TokenId()):
				evento.tempo += 1
				recategorizadorLexico.categorizadorSintatico.lista.append(evento)

	elif recategorizadorLexico.estadoAtual == 'E1':
		if not((recategorizadorLexico.acumulador == "DEF" and evento.conteudo == "FN") or (recategorizadorLexico.acumulador == "GO" and evento.conteudo == "TO")):
			recategorizadorLexico.categorizadorSintatico.lista.append(TokenId(tempo=tempo+1,conteudo=recategorizadorLexico.acumulador))
			recategorizadorLexico.estadoAtual = 'E0'
			recategorizadorLexico.acumulador = ''
			rodarAutomato(recategorizadorLexico,evento,tempo)
		else:
			if recategorizadorLexico.acumulador == "DEF":
				recategorizadorLexico.categorizadorSintatico.lista.append(TokenReservado(tempo=tempo+1,conteudo="DEF FN"))
			else:
				recategorizadorLexico.categorizadorSintatico.lista.append(TokenReservado(tempo=tempo+1,conteudo="GOTO"))
		recategorizadorLexico.estadoAtual = 'E0'
		recategorizadorLexico.acumulador = ''

def rodarAutomato(recategorizadorLexico,evento,tempo):
	log='O token recebido eh do tipo {0} e seu conteudo eh {1}'.format(type(evento),evento.conteudo)
	#recategorizadorLexico.logar(tempo,log)
	rodarAutomato2(recategorizadorLexico,evento,tempo)


class RecategorizadorLexico(MotorDeEventos):
	def __init__(self,
				 listaInicial=[],
				 rotinasDeTratamento={type(TokenId()):rodarAutomato,
				 					  type(TokenNumero()):rodarAutomato,
				 					  type(TokenEspecial()):rodarAutomato,
				 					  type(TokenLinha()):rodarAutomato},
				 categorizadorSintatico=CategorizadorSintatico(),
				 acumulador = '',
				 estadoInicial = 'E0'):
		super().__init__(listaInicial,rotinasDeTratamento)
		self.categorizadorSintatico = categorizadorSintatico
		self.acumulador = acumulador
		self.estadoAtual = estadoInicial
		