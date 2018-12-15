from base import MotorDeEventos
from eventos import Arquivo
from eventos import ProximaLinha
from eventos import FecharArquivo
from eventos import Linha
from eventos import FimDeArquivo
from FiltroAscii import FiltroAscii


def abrirArquivo(sistemaDeArquivos, arquivo, tempo):
	sistemaDeArquivos.arquivoAtual = open(arquivo.path)
	log = "Arquivo {0} aberto".format(arquivo.path)
	#sistemaDeArquivos.logar(tempo,log)
	sistemaDeArquivos.lista.insert(0,ProximaLinha(tempo=tempo +1))

def lerProximaLinha(sistemaDeArquivos, proximaLinha, tempo):
	linhaAtual = sistemaDeArquivos.arquivoAtual.readline()
	log = "Linha Lida: {0}".format(linhaAtual)
	#sistemaDeArquivos.logar(tempo,log)
	if linhaAtual != '':
		sistemaDeArquivos.filtroAscii.lista.append(Linha(tempo=tempo+1,conteudo=linhaAtual))
		sistemaDeArquivos.lista.insert(0,ProximaLinha(tempo=tempo+1))
	else:
		sistemaDeArquivos.lista.insert(0,FecharArquivo(tempo=tempo+1))
		sistemaDeArquivos.filtroAscii.lista.append(FimDeArquivo(tempo=tempo+1))

def fecharArquivo(sistemaDeArquivos, fecharArquivoE, tempo):
	sistemaDeArquivos.arquivoAtual.close()
	log = "Arquivo fechado"
	#sistemaDeArquivos.logar(tempo,log)


class SistemaDeArquivos(MotorDeEventos):
	def __init__(self,
				 listaInicial=[],
				 rotinasDeTratamento={type(Arquivo()):abrirArquivo,
				 					  type(ProximaLinha()):lerProximaLinha,
				 					  type(FecharArquivo()):fecharArquivo},
				 filtroAscii = FiltroAscii()):
		super().__init__(listaInicial,rotinasDeTratamento)
		self.filtroAscii = filtroAscii

		