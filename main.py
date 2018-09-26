from base import MotorDeEventos
from eventos import Arquivo
from SistemaDeArquivos import SistemaDeArquivos
from AnalisadorLexico import AnalisadorLexico

def loopDeSimulação(t = 0, *args):
	tudoVazio = False
	while not(tudoVazio):
		tudoVazio = True
		for arg in args:
			arg.iterar(t)
			if len(arg.lista) != 0:
				tudoVazio = False
		t+=1
	return

listaDeArquivos1=[Arquivo(tempo=0,path='./arquivo1.txt'),Arquivo(tempo=100,path='./arquivo2.txt')]
analisadorLexico = AnalisadorLexico()
sistemaDeArquivos = SistemaDeArquivos(listaInicial=listaDeArquivos1,analisadorLexico=analisadorLexico)
t = 0
loopDeSimulação(t, sistemaDeArquivos, analisadorLexico)
