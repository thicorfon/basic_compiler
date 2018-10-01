from base import MotorDeEventos
from eventos import AsciiUtil
from eventos import AsciiControle

def categorizarAsciiUtil(categorizadorAscii,asciiUtil,tempo):
	log = 'O caracter recebido foi:{0}'.format(asciiUtil.conteudo)
	categorizadorAscii.logar(tempo,log)

def categorizarAsciiControle(categorizadorAscii,asciiControle,tempo):
	log = 'O caracter recebido foi:{0}'.format(asciiControle.conteudo)
	categorizadorAscii.logar(tempo,log)

class CategorizadorAscii(MotorDeEventos):
	def __init__(self,
				 listaInicial=[],
				 rotinasDeTratamento={type(AsciiUtil()):categorizarAsciiUtil,
				 					  type(AsciiControle()):categorizarAsciiControle}):
		super().__init__(listaInicial,rotinasDeTratamento)