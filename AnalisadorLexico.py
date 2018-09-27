from base import MotorDeEventos
from eventos import Linha
from eventos import FimDeArquivo

def lerLinha(analisadorLexico,Linha,tempo):
	log = "A linha recebida eh: {0}".format(Linha.conteudo)
	analisadorLexico.logar(tempo,log)


class AnalisadorLexico(MotorDeEventos):
	def __init__(self,
				 listaInicial=[],
				 rotinasDeTratamento={type(Linha()):lerLinha}):
		super().__init__(listaInicial,rotinasDeTratamento)
		