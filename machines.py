from eventos import TokenId
from eventos import TokenNumero
from eventos import TokenEspecial
from eventos import TokenReservado
from eventos import TokenLinha
import copy
import sys

Remark = {1: [(TokenReservado(conteudo="REM"),2,None)],
		  2: [('final',None,None),
		  	  (TokenNumero(),2,None),
		  	  (TokenId(),2,None),
		  	  (TokenEspecial(),2,None),
		  	  (TokenReservado(),2,None)]}

def enterBs(categorizador):
	retorno = copy.deepcopy(categorizador)
	retorno['chainCode'].append({'lineNumber':'',
								 'valueCode':[],
								 'sub': False})
	return retorno

def lineNumber(categorizador,evento):
	retorno = copy.deepcopy(categorizador)
	retorno['chainCode'][-1]['lineNumber'] = evento.conteudo
	if retorno['forFlag'] == True:
		retorno['forStack'][-1]['destination'] = evento.conteudo
		retorno['forFlag'] = False
	if evento.conteudo == retorno['gosubAddress']:
		retorno['chainCode'][-1]['sub'] =  True
	return retorno

def exitBs(categorizador):
	retorno = copy.deepcopy(categorizador)
	chainCode = retorno['chainCode'].pop()
	flag = True
	for line in chainCode['valueCode']:
		if flag:
			if chainCode['sub']:
				retorno['code'].append(chainCode['lineNumber'] + ' DW /2')
				retorno['code'].append(line)
			else:
				retorno['code'].append(chainCode['lineNumber'] + line)
			flag = False
		else:	
			retorno['code'].append(line)
	return retorno


def enterPrint(categorizador):
	retorno = copy.deepcopy(categorizador)
	retorno['chainCode'].append({'variable':'',
								 'valueCode':[]})
	return retorno

def getVariablePrint(categorizador,evento):
	retorno = copy.deepcopy(categorizador)
	retorno['chainCode'][-1]['variable'] = evento.conteudo
	return retorno

def exitPrint(categorizador):
	retorno = copy.deepcopy(categorizador)
	chainCode = retorno['chainCode'].pop()
	variable = chainCode['variable']
	chainCode['valueCode'].append(' LD '+variable)
	for line in chainCode['valueCode']:
		retorno['chainCode'][-1]['valueCode'].append(line)
	return retorno


def enterAssign(categorizador):
	retorno = copy.deepcopy(categorizador)
	retorno['chainCode'].append({'variable':'',
								 'valueCode':[]})
	return retorno

def getVariable(categorizador,evento):
	retorno =copy.deepcopy(categorizador)
	retorno['chainCode'][-1]['variable'] = evento.conteudo
	if evento.conteudo not in retorno['variaveisDeclaradas']:
		retorno['data'].append(evento.conteudo+' DS /1')
		retorno['variaveisDeclaradas'].append(evento.conteudo)
	return retorno

def exitAssign(categorizador):
	retorno = copy.deepcopy(categorizador)
	chainCode = retorno['chainCode'].pop()
	for line in chainCode['valueCode']:
		retorno['chainCode'][-1]['valueCode'].append(line)
	return retorno

def enterExpFromAssign(categorizador):
	retorno = copy.deepcopy(categorizador)
	retorno['chainCode'].append({'variableList': [],
								 'operationList':['+'],
								 'valueCode':[],
								 'returnVariable':retorno['chainCode'][-1]['variable']})
	return retorno

def enterExpFromIf1(categorizador):
	retorno = copy.deepcopy(categorizador)
	retorno['chainCode'].append({'variableList': [],
								 'operationList':['+'],
								 'valueCode':[],
								 'returnVariable':retorno['chainCode'][-1]['variable1']})
	return retorno

def enterExpFromIf2(categorizador):
	retorno = copy.deepcopy(categorizador)
	retorno['chainCode'].append({'variableList': [],
								 'operationList':['+'],
								 'valueCode':[],
								 'returnVariable':retorno['chainCode'][-1]['variable2']})
	return retorno

def enterExpFromFor1(categorizador):
	retorno = copy.deepcopy(categorizador)
	retorno['chainCode'].append({'variableList': [],
								 'operationList':['+'],
								 'valueCode':[],
								 'returnVariable':retorno['chainCode'][-1]['initialValue']})
	return retorno

def enterExpFromFor2(categorizador):
	retorno = copy.deepcopy(categorizador)
	retorno['chainCode'].append({'variableList': [],
								 'operationList':['+'],
								 'valueCode':[],
								 'returnVariable':retorno['chainCode'][-1]['guarda']})
	return retorno

def enterExpFromForStep(categorizador):
	retorno = copy.deepcopy(categorizador)
	retorno['chainCode'].append({'variableList': [],
								 'operationList':['+'],
								 'valueCode':[],
								 'returnVariable':retorno['chainCode'][-1]['step']})
	return retorno

def enterExpFromEb(categorizador):
	retorno = copy.deepcopy(categorizador)
	retorno['chainCode'].append({'variableList': [],
								 'operationList':['+'],
								 'valueCode':[],
								 'returnVariable':retorno['chainCode'][-1]['returnVariable']})
	return retorno


def addOp(categorizador,evento):
	retorno = copy.deepcopy(categorizador)
	retorno['chainCode'][-1]['operationList'].append(evento.conteudo)
	return retorno

def exitExp(categorizador):
	retorno = copy.deepcopy(categorizador)
	chainCode = retorno['chainCode'].pop()
	previousValueCode = retorno['chainCode'][-1]['valueCode']
	chainCode['valueCode'].append(' LV /0')
	while len(chainCode['variableList']) != 0:
		variable = chainCode['variableList'].pop(0)
		op = chainCode['operationList'].pop(0)
		if op == '+':
			chainCode['valueCode'].append(' + '+variable)
		elif op == '-':
			chainCode['valueCode'].append(' - '+variable)
		elif op == '*':
			chainCode['valueCode'].append(' * '+variable)
		elif op == '/':
			chainCode['valueCode'].append(' / '+variable)
	chainCode['valueCode'].append(' MM '+chainCode['returnVariable'])
	for line in chainCode['valueCode']:
		previousValueCode.append(line)
	return retorno

def enterEb(categorizador):
	retorno = copy.deepcopy(categorizador)
	returnVariable = 'T'+str(retorno['tempCount'])
	retorno['tempCount'] += 1
	retorno['chainCode'][-1]['variableList'].append(returnVariable)
	if returnVariable not in retorno['variaveisDeclaradas']:
		retorno['data'].append(returnVariable+' DS /1')
		retorno['variaveisDeclaradas'].append(returnVariable)
	retorno['chainCode'].append({'valueCode':[],
								 'returnVariable':returnVariable})
	return retorno

def ebConstant(categorizador,evento):
	retorno = copy.deepcopy(categorizador)
	retorno['chainCode'][-1]['valueCode'].append(' LV /0'+evento.conteudo)
	return retorno

def ebVariable(categorizador,evento):
	retorno = copy.deepcopy(categorizador)
	retorno['chainCode'][-1]['valueCode'].append(' LD '+evento.conteudo)
	return retorno

def exitEb(categorizador):
	retorno =copy.deepcopy(categorizador)
	chainCode = retorno['chainCode'].pop()
	previousValueCode = retorno['chainCode'][-1]['valueCode']
	returnVariable = chainCode['returnVariable']
	chainCode['valueCode'].append(' MM '+ returnVariable)
	for line in chainCode['valueCode']:
		previousValueCode.append(line)
	return retorno

def enterGoto(categorizador):
	retorno = copy.deepcopy(categorizador)
	retorno['chainCode'].append({'variable':'',
								 'valueCode':[]})
	return retorno

def getJumpLocation(categorizador,evento):
	retorno =copy.deepcopy(categorizador)
	retorno['chainCode'][-1]['variable'] = evento.conteudo
	return retorno

def exitGoto(categorizador):
	retorno =copy.deepcopy(categorizador)
	chainCode = retorno['chainCode'].pop()
	previousValueCode = retorno['chainCode'][-1]['valueCode']
	chainCode['valueCode'].append(' JP '+ chainCode['variable'])
	for line in chainCode['valueCode']:
		previousValueCode.append(line)
	return retorno

def enterIf(categorizador):
	retorno =copy.deepcopy(categorizador)
	retorno['chainCode'].append({'variable1':'T'+str(retorno['tempCount']),
								 'variable2':'T'+str(retorno['tempCount']+1),
								 'valueCode':[],
								 'compare':'',
								 'destination':''})
	retorno['tempCount'] += 2
	return retorno

def getCompare(categorizador,evento):
	retorno = copy.deepcopy(categorizador)
	retorno['chainCode'][-1]['compare'] = evento.conteudo
	return retorno

def getDestination(categorizador,evento):
	retorno = copy.deepcopy(categorizador)
	retorno['chainCode'][-1]['destination'] = evento.conteudo
	return retorno

def exitIf(categorizador):
	retorno = copy.deepcopy(categorizador)
	chainCode = retorno['chainCode'].pop()
	variable1 = chainCode['variable1']
	variable2 = chainCode['variable2']
	destination = chainCode['destination']
	previousValueCode = retorno['chainCode'][-1]['valueCode']
	if chainCode['compare'] == '=':
		chainCode['valueCode'].append(' LD '+variable1)
		chainCode['valueCode'].append(' - '+variable2)
		chainCode['valueCode'].append(' JZ '+destination)
	elif chainCode['compare'] == '<':
		chainCode['valueCode'].append(' LD '+variable1)
		chainCode['valueCode'].append(' - '+variable2)
		chainCode['valueCode'].append(' JN '+destination)
	elif chainCode['compare'] == '>':
		chainCode['valueCode'].append(' LD '+variable2)
		chainCode['valueCode'].append(' - '+variable1)
		chainCode['valueCode'].append(' JN '+destination)
	for line in chainCode['valueCode']:
		previousValueCode.append(line)
	return retorno

def enterFor(categorizador):
	retorno = copy.deepcopy(categorizador)
	retorno['chainCode'].append({'iterator':'',
								 'initialValue':'T'+str(retorno['tempCount']),
								 'guarda': 'T'+str(retorno['tempCount']+1),
								 'step': 'T'+str(retorno['tempCount']+2),
								 'stepFlag': False,
								 'valueCode': []})
	retorno['data'].append('T'+str(retorno['tempCount'])+' DS /1')
	retorno['data'].append('T'+str(retorno['tempCount']+1)+' DS /1')
	retorno['data'].append('T'+str(retorno['tempCount']+2)+' DS /1')
	retorno['variaveisDeclaradas'].append('T'+str(retorno['tempCount']))
	retorno['variaveisDeclaradas'].append('T'+str(retorno['tempCount']+1))
	retorno['variaveisDeclaradas'].append('T'+str(retorno['tempCount']+2))
	retorno['tempCount'] += 3
	return retorno

def getIterator(categorizador,evento):
	retorno = copy.deepcopy(categorizador)
	retorno['chainCode'][-1]['iterator'] = evento.conteudo
	if evento.conteudo not in retorno['variaveisDeclaradas']:
		retorno['data'].append(evento.conteudo+' DS /1')
		retorno['variaveisDeclaradas'].append(evento.conteudo)
	return retorno

def receivedStep(categorizador,evento):
	retorno = copy.deepcopy(categorizador)
	retorno['chainCode'][-1]['stepFlag'] = True
	return retorno

def exitFor(categorizador):
	retorno = copy.deepcopy(categorizador)
	chainCode = retorno['chainCode'].pop()
	previousValueCode = retorno['chainCode'][-1]['valueCode']
	retorno['forStack'].append({'iterator':chainCode['iterator'],
								'guarda':chainCode['guarda'],
								'step': chainCode['step'],
								'destination':''})
	if chainCode['stepFlag'] == False:
		chainCode['valueCode'].append(' LV /1')
		chainCode['valueCode'].append(' MM '+chainCode['step'])
		retorno['data'].append(chainCode['step']+' DS /1')
	chainCode['valueCode'].append(' LD '+chainCode['initialValue'])
	chainCode['valueCode'].append(' MM '+chainCode['iterator'])
	for line in chainCode['valueCode']:
		previousValueCode.append(line)
	retorno['forFlag'] = True
	return retorno
	

def enterNext(categorizador):
	retorno = copy.deepcopy(categorizador)
	if len(retorno['forStack']) != 0:
		forStack = retorno['forStack'].pop()
		retorno['chainCode'].append({'iterator': forStack['iterator'],
									 'guarda': forStack['guarda'],
									 'step': forStack['step'],
									 'destination': forStack['destination'],
									 'valueCode': []
									})
	return retorno

def checkIterator(categorizador,evento):
	retorno = copy.deepcopy(categorizador)
	if evento.conteudo != retorno['chainCode'][-1]['iterator']:
		print("VARIAVEL ERRADA NO FOR")
		sys.exit()
	return retorno

def exitNext(categorizador):
	retorno = copy.deepcopy(categorizador)
	chainCode = retorno['chainCode'].pop()
	previousValueCode = retorno['chainCode'][-1]['valueCode']
	chainCode['valueCode'].append(' LD '+chainCode['iterator'])
	chainCode['valueCode'].append(' + '+chainCode['step'])
	chainCode['valueCode'].append(' MM '+chainCode['iterator'])
	chainCode['valueCode'].append(' - '+chainCode['guarda'])
	chainCode['valueCode'].append(' JN '+chainCode['destination'])
	for line in chainCode['valueCode']:
		previousValueCode.append(line)
	return retorno

def enterGosub(categorizador):
	retorno = copy.deepcopy(categorizador)
	retorno['chainCode'].append({'destination': '',
								 'valueCode': []})
	return retorno

def getSubRoutineDest(categorizador,evento):
	retorno = copy.deepcopy(categorizador)
	retorno['chainCode'][-1]['destination'] = evento.conteudo
	return retorno

def exitGosub(categorizador):
	retorno = copy.deepcopy(categorizador)
	chainCode = retorno['chainCode'].pop()
	previousValueCode = retorno['chainCode'][-1]['valueCode']
	chainCode['valueCode'].append(' SC '+chainCode['destination'])
	retorno['gosubFlag'] = True
	retorno['gosubAddress'] = chainCode['destination']
	for line in chainCode['valueCode']:
		previousValueCode.append(line)
	return retorno

def enterReturn(categorizador):
	retorno = copy.deepcopy(categorizador)
	retorno['chainCode'].append({'destination': retorno['chainCode'][-1]['lineNumber'],
								 'valueCode': []})
	return retorno

def exitReturn(categorizador):
	retorno = copy.deepcopy(categorizador)
	chainCode = retorno['chainCode'].pop()
	previousValueCode = retorno['chainCode'][-1]['valueCode']
	chainCode['valueCode'].append(' RS '+retorno['gosubAddress'])
	retorno['gosubAddress'] = ''
	retorno['gosubFlag'] = False
	for line in chainCode['valueCode']:
		previousValueCode.append(line)
	return retorno






Assign = {1: [(TokenReservado(conteudo="LET"),2,None)],
		  2: [(TokenId(),3,getVariable)],
		  3: [(TokenEspecial(conteudo="="),4,None)],
		  4: [('Exp',5,enterExpFromAssign)],
		  5: [('final',None,exitAssign)]}


Exp = {1: [('Eb',2,enterEb)],
	   2: [('final',None,exitExp),
	   	   (TokenEspecial(conteudo="+"),3,addOp),
		   (TokenEspecial(conteudo="-"),3,addOp),
		   (TokenEspecial(conteudo="*"),3,addOp),
		   (TokenEspecial(conteudo="/"),3,addOp)],
	   3: [('Eb',2,enterEb)]}



Eb = {1:[(TokenEspecial(conteudo="("),2,None),
		 (TokenNumero(),4,ebConstant),
		 (TokenId(),4,ebVariable),
		 (TokenReservado(conteudo="FN"),5,None)],
	  2:[('Exp',3,enterExpFromEb)],
	  3:[(TokenEspecial(conteudo=")"),4,None)],
	  4:[('final',None,exitEb)],
	  5:[(TokenId(),6,None)],
	  6:[(TokenEspecial(conteudo="("),2,None)]}

Read = {1:[(TokenReservado(conteudo="READ"),2)],
		2:[('Var',3)],
		3:['final']}#,
		   #(TokenReservado(conteudo=","),4)],
		#4:[('Var',3)]}

Print = {1:[(TokenReservado(conteudo="PRINT"),2,None)],
		 2:[(TokenId(),3,getVariablePrint)],
		 3:[('final',None,exitPrint)]}

Goto = {1:[(TokenReservado(conteudo="GOTO"),2,None)],
		2:[(TokenNumero(),3,getJumpLocation)],
		3:[('final',None,exitGoto)]}

If = {1: [(TokenReservado(conteudo="IF"),2,None)],
	  2: [('Exp',3,enterExpFromIf1)],
	  3: [(TokenEspecial(conteudo="="),4,getCompare),
	  	  (TokenEspecial(conteudo=">"),4,getCompare),
	  	  (TokenEspecial(conteudo="<"),4,getCompare)],
	  4: [('Exp',5,enterExpFromIf2)],
	  5: [(TokenReservado(conteudo="THEN"),6,None)],
	  6: [(TokenNumero(),7,getDestination)],
	  7: [('final',None,exitIf)]}

For = {1:[(TokenReservado(conteudo="FOR"),2,None)],
	   2:[(TokenId(),3,getIterator)],
	   3:[(TokenEspecial(conteudo="="),4,None)],
	   4:[('Exp',5,enterExpFromFor1)],
	   5:[(TokenReservado(conteudo="TO"),6,None)],
	   6:[('Exp',7,enterExpFromFor2)],
	   7:[('final',None,exitFor),
	   	  (TokenReservado(conteudo="STEP"),8,receivedStep)],
	   8:[('Exp',9,enterExpFromForStep)],
	   9:[('final',None,exitFor)]}

Next = {1: [(TokenReservado(conteudo="NEXT"),2,None)],
		2: [(TokenId(),3,checkIterator)],
		3: [('final',None,exitNext)]}

Gosub = {1: [(TokenReservado(conteudo="GOSUB"),2,None)],
		 2: [(TokenNumero(),3,getSubRoutineDest)],
		 3: [('final',None,exitGosub)]}

Return = {1: [(TokenReservado(conteudo="RETURN"),2,None)],
		  2: [('final',None,exitReturn)]}

BS = {1: [(TokenNumero(),2, lineNumber)],
	  2: [('Remark',3,None),
	  	  ('Assign',3,enterAssign),
	  	  ('Print',3,enterPrint),
	  	  ('Goto',3,enterGoto),
	  	  ('If',3,enterIf),
	  	  ('For',3,enterFor),
	  	  ('Next',3,enterNext),
	  	  ('Gosub',3,enterGosub),
	  	  ('Return',3,enterReturn)],
	  3: [(TokenLinha(),4,None)],
	  4: [('final',None,exitBs)]}

Program = {1:[('BS',2,enterBs)],
		   2:[('BS',2,enterBs),
		   	  (TokenNumero(),3,None)],
		   3:[(TokenReservado(conteudo="END"),4,None)],
		   4:[('final',None,None)]}

machines = {'Remark': Remark,
			'BS':BS,
			'Program':Program,
			'Assign': Assign,
			'Exp': Exp,
			'Eb': Eb,
			'Read': Read,
			'Print': Print,
			'Goto': Goto,
			'If': If,
			'For': For,
			'Next': Next,
			'Gosub': Gosub,
			'Return': Return}