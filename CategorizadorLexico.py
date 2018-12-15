from base import MotorDeEventos
from eventos import Delimitador
from eventos import Digito
from eventos import Letra
from eventos import Especial
from eventos import Controle
from eventos import TokenId
from eventos import TokenNumero
from eventos import TokenEspecial
from eventos import TokenLinha
from RecategorizadorLexico import RecategorizadorLexico
import sys



def rodarAutomato2(categorizadorLexico,evento,tempo):
	proximoEstado = categorizadorLexico.automato[categorizadorLexico.estadoAtual][type(evento)]
	if proximoEstado == 'final':
		token_content = categorizadorLexico.acumulador
		
		if categorizadorLexico.estadoAtual == 'E0':
			categorizadorLexico.acumulador = ''
		
		else:
			if categorizadorLexico.estadoAtual == 'E1' or categorizadorLexico.estadoAtual == 'E2':
				categorizadorLexico.recategorizadorLexico.lista.append(TokenId(tempo=tempo+1,conteudo=categorizadorLexico.acumulador))
				if evento.conteudo == '\n':
					categorizadorLexico.recategorizadorLexico.lista.append(TokenLinha(tempo=tempo+1))

			elif categorizadorLexico.estadoAtual == 'E3':
				categorizadorLexico.recategorizadorLexico.lista.append(TokenNumero(tempo=tempo+1,conteudo=categorizadorLexico.acumulador))
				if evento.conteudo == '\n':
					categorizadorLexico.recategorizadorLexico.lista.append(TokenLinha(tempo=tempo+1))

			elif categorizadorLexico.estadoAtual == 'E4':
				categorizadorLexico.recategorizadorLexico.lista.append(TokenEspecial(tempo=tempo+1,conteudo=categorizadorLexico.acumulador))
				if evento.conteudo == '\n':
					categorizadorLexico.recategorizadorLexico.lista.append(TokenLinha(tempo=tempo+1))

			categorizadorLexico.estadoAtual = 'E0'
			categorizadorLexico.acumulador = ''
			rodarAutomato2(categorizadorLexico,evento,tempo)


	
	elif proximoEstado == 'erro':
		categorizadorLexico.logar(tempo,'Token "{0}" invalido'.format(categorizadorLexico.acumulador+evento.conteudo))
		sys.exit()
	
	else:
		categorizadorLexico.acumulador += evento.conteudo
		categorizadorLexico.estadoAtual = proximoEstado

def rodarAutomato(categorizadorLexico,evento,tempo):
	log = 'O caracter recebido foi:{0} do tipo {1}'.format(evento.conteudo,str(type(evento)))
	#categorizadorLexico.logar(tempo,log)
	rodarAutomato2(categorizadorLexico,evento,tempo)

class CategorizadorLexico(MotorDeEventos):
	def __init__(self,
				 listaInicial=[],
				 rotinasDeTratamento={type(Delimitador()):rodarAutomato,
				 					  type(Digito()):rodarAutomato,
				 					  type(Letra()):rodarAutomato,
				 					  type(Especial()):rodarAutomato,
				 					  type(Controle()):rodarAutomato},
				 
				 automato={'E0':{type(Delimitador()):'final',
				 				 type(Letra()):'E1',
				 				 type(Digito()):'E3',
				 				 type(Especial()):'E4',
				 				 type(Controle()):'final'},
				 		   
				 		   'E1':{type(Delimitador()):'final',
				 		   		 type(Letra()):'E1',
				 		   		 type(Digito()):'E2',
				 		   		 type(Especial()):'final',
				 		   		 type(Controle()):'final'},
				 		   
				 		   'E2':{type(Delimitador()):'final',
				 		   		 type(Letra()):'erro',
				 		   		 type(Digito()):'E2',
				 		   		 type(Especial()):'final',
				 		   		 type(Controle()):'final'},

				 		   'E3':{type(Delimitador()):'final',
				 		   		 type(Letra()):'erro',
				 		   		 type(Digito()):'E3',
				 		   		 type(Especial()):'final',
				 		   		 type(Controle()):'final'},

				 		   'E4':{type(Delimitador()):'final',
				 		   		 type(Letra()):'final',
				 		   		 type(Digito()):'final',
				 		   		 type(Especial()):'E4',
				 		   		 type(Controle()):'final'}
				 		  },
				 estadoInicial = 'E0',
				 acumulador = '',
				 recategorizadorLexico=RecategorizadorLexico()):
		super().__init__(listaInicial,rotinasDeTratamento)
		self.automato = automato
		self.estadoAtual = estadoInicial
		self.acumulador = acumulador
		self.recategorizadorLexico = recategorizadorLexico
		