from base import MotorDeEventos
from eventos import Linha
from eventos import FimDeArquivo

def lerLinha(filtroAscii,Linha,tempo):
	log = "A linha recebida eh: {0}".format(Linha.conteudo)
	analisadorLexico.logar(tempo,log)

def finalizarArquivo(filtroAscii,fimDeArquivo,tempo):
	


class FiltroAscii(MotorDeEventos):
	def __init__(self,
				 listaInicial=[],
				 rotinasDeTratamento={type(Linha()):lerLinha,
				 					  type(FimDeArquivo()):finalizarArquivo}):
		super().__init__(listaInicial,rotinasDeTratamento)
		