from base import MotorDeEventos
from eventos import Linha
from eventos import FimDeArquivo

def lerLinha(AnalisadorLexico,Linha,tempo):
	log = "A linha recebida eh: {0}".format(Linha.conteudo)
	print("Tempo: {0}\nMaquina: {1}\nLog: {2}\n\n".format(str(tempo),str(type(AnalisadorLexico)),log))


class AnalisadorLexico(MotorDeEventos):
	def __init__(self,
				 listaInicial=[],
				 rotinasDeTratamento={type(Linha()):lerLinha}):
		super().__init__(listaInicial,rotinasDeTratamento)
		