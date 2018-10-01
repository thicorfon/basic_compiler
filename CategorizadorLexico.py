from base import MotorDeEventos
from eventos import Linha
from eventos import FimDeArquivo

def lerLinha(categorizadorLexico,Linha,tempo):
	log = "A linha recebida eh: {0}".format(Linha.conteudo)
	categorizadorLexico.logar(tempo,log)


class CategorizadorLexico(MotorDeEventos):
	def __init__(self,
				 listaInicial=[],
				 rotinasDeTratamento={}):
		super().__init__(listaInicial,rotinasDeTratamento)
		