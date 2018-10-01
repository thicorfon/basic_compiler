from base import MotorDeEventos
from CategorizadorAscii import CategorizadorAscii
from eventos import Linha
from eventos import FimDeArquivo
from eventos import AsciiUtil
from eventos import AsciiControle
from eventos import AsciiDescartavel
from constants import uppercase
from constants import lowercase
from constants import digits
from constants import special


def lerLinha(filtroAscii,Linha,tempo):
	for i in Linha.conteudo:
		if (i in uppercase) or (i in lowercase) or (i in digits):
			filtroAscii.categorizadorAscii.lista.append(AsciiUtil(tempo=tempo+1,conteudo=i))
		elif (i in special):
			filtroAscii.categorizadorAscii.lista.append(AsciiUtil(tempo=tempo+1,conteudo=i))
		elif i == ' ':
			filtroAscii.categorizadorAscii.lista.append(AsciiDescartavel(tempo=tempo+1,conteudo=i))
		else:
			filtroAscii.categorizadorAscii.lista.append(AsciiControle(tempo=tempo+1,conteudo=i))
	log = "A linha recebida eh: {0}".format(Linha.conteudo)
	filtroAscii.logar(tempo,log)


def finalizarArquivo(filtroAscii,fimDeArquivo,tempo):
	pass



class FiltroAscii(MotorDeEventos):
	def __init__(self,
				 listaInicial=[],
				 rotinasDeTratamento={type(Linha()):lerLinha,
				 					  type(FimDeArquivo()):finalizarArquivo},
				 categorizadorAscii=CategorizadorAscii()):
		super().__init__(listaInicial,rotinasDeTratamento)
		self.categorizadorAscii = categorizadorAscii
		