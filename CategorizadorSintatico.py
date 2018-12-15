from base import MotorDeEventos
from eventos import TokenId
from eventos import TokenNumero
from eventos import TokenEspecial
from eventos import TokenReservado
from eventos import TokenLinha
import machines
import sys

def print_categorizador(categorizador):
	print("maquina: {0}\nestado: {1}\npilha:{2}\nhistorico: {3}\ncode: {4}\ndata: {5}".format(categorizador['maquina'],categorizador['estado'],categorizador['pilha'],categorizador['historico'],categorizador['code'],categorizador['data']))

def build_code(code,data):
	file_object  = open("output.txt", "w")
	file_object.write(' NAME MAIN')
	file_object.write('\n ORG /100 \n')
	for line in code:
		file_object.write(line+'\n')
	for line in data:
		file_object.write(line+'\n')
	#file_object.write('SUBADR DS /2')
	#file_object.write(' ORG /600 \n')
	#file_object.write('SUB DS \n')
	file_object.write(' END 00')

def proximos(listaDeCategorizadores,evento,tempo):
	proximaLista = []
	for tupla in listaDeCategorizadores:
		if tupla[1] == True:
			categorizador = tupla[0]
			maquina = machines.machines[categorizador['maquina']]
			estado = categorizador['estado']
			pilha = categorizador['pilha'].copy()
			historico = categorizador['historico'].copy()
			code = categorizador['code'].copy()
			data = categorizador['data'].copy()
			tempCount = categorizador['tempCount']
			chainCode = categorizador['chainCode'].copy()
			forStack = categorizador['forStack'].copy()
			forFlag =  categorizador['forFlag']
			gosubFlag = categorizador['gosubFlag']
			declared = categorizador['variaveisDeclaradas'].copy()
			gosubAddress = categorizador['gosubAddress']
			transicoes = maquina[estado]
			for transicao in transicoes:
				aux = {}
				if transicao[0] == 'final':
					if len(pilha) != 0:
						aux['pilha'] = pilha.copy()
						volta = aux['pilha'].pop()
						aux['maquina'] = volta[0]
						aux['estado'] = volta[1]
						aux['historico'] = historico.copy()
						aux['historico'].append((volta[0],volta[1]))
						aux['code'] = code.copy()
						aux['data'] = data.copy()
						aux['tempCount'] = tempCount
						aux['chainCode'] = chainCode.copy()
						aux['forStack'] = forStack.copy()
						aux['forFlag'] = forFlag
						aux['variaveisDeclaradas'] = declared.copy()
						aux['gosubFlag'] = gosubFlag
						aux['gosubAddress'] = gosubAddress
						if transicao[2] == None:
							proximaLista.append((aux,True))
						else:
							proximaLista.append((transicao[2](aux.copy()),True))
							#print(transicao[2](aux))
					else:
						print("Fim da Compilação!")
						build_code(code,data)
						sys.exit()
				elif type(transicao[0]) == type(''):
					aux['maquina'] = transicao[0]
					aux['estado'] = 1
					aux['pilha'] = pilha.copy()
					aux['pilha'].append((categorizador['maquina'],transicao[1]))
					aux['historico'] = historico.copy()
					aux['historico'].append((transicao[0],1))
					aux['code'] = code.copy()
					aux['data'] = data.copy()
					aux['tempCount'] = tempCount
					aux['chainCode'] = chainCode.copy()
					aux['forStack'] = forStack.copy()
					aux['forFlag'] = forFlag
					aux['variaveisDeclaradas'] = declared.copy()
					aux['gosubFlag'] = gosubFlag
					aux['gosubAddress'] = gosubAddress
					if transicao[2] == None:
						proximaLista.append((aux,True))
					else:
						proximaLista.append((transicao[2](aux.copy()),True))
						
				else:
					if type(evento) == type(transicao[0]):
						if (evento.conteudo == transicao[0].conteudo) or transicao[0].conteudo == '':
							aux['pilha'] = pilha.copy()
							aux['maquina'] = categorizador['maquina']
							aux['estado'] = transicao[1]
							aux['historico'] = historico.copy()
							aux['historico'].append((categorizador['maquina'],transicao[1]))
							aux['code'] = code.copy()
							aux['data'] = data.copy()
							aux['tempCount'] = tempCount
							aux['chainCode'] = chainCode.copy()
							aux['forStack'] = forStack.copy()
							aux['forFlag'] = forFlag
							aux['variaveisDeclaradas'] = declared.copy()
							aux['gosubFlag'] = gosubFlag
							aux['gosubAddress'] = gosubAddress
							if transicao[2] == None:
								proximaLista.append((aux,False))
							else:
								proximaLista.append((transicao[2](aux.copy(),evento),False))
								#print(transicao[2](aux,evento))
		else:
			proximaLista.append(tupla)

	flag = True
	for tupla in proximaLista:
		if tupla[1]:
			flag = False

	if flag:
		return [x[0] for x in proximaLista]
	else:
		return proximos(proximaLista,evento,tempo)





def analisar(categorizadorSintatico,evento,tempo):
	aux = []
	log='O token recebido eh do tipo {0} e seu conteudo eh {1}'.format(type(evento),evento.conteudo)
	categorizadorSintatico.logar(tempo,log)
	for categorizador in categorizadorSintatico.categorizadores:
		aux.append((categorizador,True))
	categorizadorSintatico.categorizadores = proximos(aux,evento,tempo)
	if len(categorizadorSintatico.categorizadores) == 0:
		print('ERRO NA ANALISE SINTÁTICA')
		sys.exit()
	for categorizador in categorizadorSintatico.categorizadores:
		print_categorizador(categorizador)

	
	

class CategorizadorSintatico(MotorDeEventos):
	def __init__(self,
				 listaInicial=[],
				 rotinasDeTratamento={type(TokenId()):analisar,
				 					  type(TokenNumero()):analisar,
				 					  type(TokenEspecial()):analisar,
				 					  type(TokenReservado()):analisar,
				 					  type(TokenLinha()):analisar},
				 categorizadores  = [{'maquina': 'Program',
				 					  'estado':1,
				 					  'pilha':[],
				 					  'historico':[('Program',1)],
				 					  'code':[],
				 					  'data':[],
				 					  'tempCount' : 0,
				 					  'chainCode' : [],
				 					  'forStack': [],
				 					  'forFlag' : False,
				 					  'variaveisDeclaradas': [],
				 					  'gosubFlag': False,
				 					  'gosubAddress': ''
				 					  }
				 					 ]
				 ):
		super().__init__(listaInicial,rotinasDeTratamento)
		self.categorizadores = categorizadores