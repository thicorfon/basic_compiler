from base import MotorDeEventos
from eventos import Arquivo
from eventos import ProximaLinha
from eventos import FecharArquivo
from eventos import Linha
from AnalisadorLexico import AnalisadorLexico


def abrirArquivo(sistemaDeArquivos, arquivo, tempo):
	sistemaDeArquivos.arquivoAtual = open(arquivo.path)
	log = "Arquivo {0} aberto".format(arquivo.path)
	print("Tempo: {0}\nMaquina: {1}\nLog: {2}\n\n".format(str(tempo),str(type(sistemaDeArquivos)),log))
	sistemaDeArquivos.lista.insert(0,ProximaLinha(tempo=tempo +1))

def lerProximaLinha(sistemaDeArquivos, proximaLinha, tempo):
	linhaAtual = sistemaDeArquivos.arquivoAtual.readline()
	log = "Linha Lida: {0}".format(linhaAtual)
	print("Tempo: {0}\nMaquina: {1}\nLog: {2}\n\n".format(str(tempo),str(type(sistemaDeArquivos)),log))
	if linhaAtual != '':
		sistemaDeArquivos.analisadorLexico.lista.append(Linha(tempo=tempo+1,conteudo=linhaAtual))
		sistemaDeArquivos.lista.insert(0,ProximaLinha(tempo=tempo+1))
	else:
		sistemaDeArquivos.lista.insert(0,FecharArquivo(tempo=tempo+1))

def fecharArquivo(sistemaDeArquivos, fecharArquivoE, tempo):
	sistemaDeArquivos.arquivoAtual.close()
	log = "Arquivo fechado"
	print("Tempo: {0}\nMaquina: {1}\nLog: {2}\n\n".format(str(tempo),str(type(sistemaDeArquivos)),log))


class SistemaDeArquivos(MotorDeEventos):
	def __init__(self,
				 listaInicial=[],
				 rotinasDeTratamento={type(Arquivo()):abrirArquivo,
				 					  type(ProximaLinha()):lerProximaLinha,
				 					  type(FecharArquivo()):fecharArquivo},
				 analisadorLexico = AnalisadorLexico()):
		super().__init__(listaInicial,rotinasDeTratamento)
		self.analisadorLexico = analisadorLexico

		