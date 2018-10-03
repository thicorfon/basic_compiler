from base import MotorDeEventos
from eventos import Arquivo
from SistemaDeArquivos import SistemaDeArquivos
from FiltroAscii import FiltroAscii
from CategorizadorAscii import CategorizadorAscii
from CategorizadorLexico import CategorizadorLexico
from RecategorizadorLexico import RecategorizadorLexico
from CategorizadorSintatico import CategorizadorSintatico

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

listaDeArquivos1=[Arquivo(tempo=0,path='./arquivo1.txt')]#,Arquivo(tempo=100,path='./arquivo2.txt')]
categorizadorSintatico = CategorizadorSintatico()
recategorizadorLexico = RecategorizadorLexico(categorizadorSintatico=categorizadorSintatico)
categorizadorLexico = CategorizadorLexico(recategorizadorLexico = recategorizadorLexico)
categorizadorAscii = CategorizadorAscii(categorizadorLexico=categorizadorLexico)
filtroAscii = FiltroAscii(categorizadorAscii=categorizadorAscii)
sistemaDeArquivos = SistemaDeArquivos(listaInicial=listaDeArquivos1,filtroAscii=filtroAscii)
t = 0
loopDeSimulação(t, 
				sistemaDeArquivos, 
				filtroAscii, 
				categorizadorAscii, 
				categorizadorLexico, 
				recategorizadorLexico, 
				categorizadorSintatico)
