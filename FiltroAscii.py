from base import MotorDeEventos
from CategorizadorAscii import CategorizadorAscii
from eventos import Linha
from eventos import FimDeArquivo
from eventos import AsciiUtil
from eventos import AsciiControle

uppercase = [chr(x) for x in range(65,91)]
lowercase = [chr(x) for x in range(97,123)]
digits = [chr(x) for x in range(48,58)]
special = ['!','@','#','%','&','*','(',')','_','+','+','-','=','{','[','}',']','?','/','`',"'","^",'~','<',',','>','.',':',';','|','\\','"']


def lerLinha(filtroAscii,Linha,tempo):
	for i in Linha.conteudo:
		if (i in uppercase) or (i in lowercase) or (i in digits):
			filtroAscii.categorizadorAscii.lista.append(AsciiUtil(tempo=tempo+1,conteudo=i))
		elif (i in special):
			filtroAscii.categorizadorAscii.lista.append(AsciiUtil(tempo=tempo+1,conteudo=i)) 
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
		