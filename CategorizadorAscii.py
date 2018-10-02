from base import MotorDeEventos
from eventos import AsciiUtil
from eventos import AsciiControle
from eventos import AsciiDescartavel
from CategorizadorLexico import CategorizadorLexico
from constants import uppercase
from constants import lowercase
from constants import digits
from constants import special
from eventos import Delimitador
from eventos import Digito
from eventos import Letra
from eventos import Especial
from eventos import Controle

def categorizarAsciiUtil(categorizadorAscii,asciiUtil,tempo):
	log = 'O caracter recebido foi:{0} do tipo {1}'.format(asciiUtil.conteudo,str(type(asciiUtil)))
	categorizadorAscii.logar(tempo,log)
	if asciiUtil.conteudo in digits:
		categorizadorAscii.categorizadorLexico.lista.append(Digito(tempo=tempo+1,conteudo=asciiUtil.conteudo))
	elif asciiUtil.conteudo in special:
		categorizadorAscii.categorizadorLexico.lista.append(Especial(tempo=tempo+1,conteudo=asciiUtil.conteudo))
	else:
		categorizadorAscii.categorizadorLexico.lista.append(Letra(tempo=tempo+1,conteudo=asciiUtil.conteudo))

def categorizarAsciiControle(categorizadorAscii,asciiControle,tempo):
	log = 'O caracter recebido foi:{0} do tipo {1}'.format(asciiControle.conteudo,str(type(asciiControle)))
	categorizadorAscii.logar(tempo,log)
	categorizadorAscii.categorizadorLexico.lista.append(Controle(tempo=tempo+1,conteudo=asciiControle.conteudo))

def categorizarAsciiDescartavel(categorizadorAscii,asciiDescartavel,tempo):
	log = 'O caracter recebido foi:{0} do tipo {1}'.format(asciiDescartavel.conteudo,str(type(asciiDescartavel)))
	categorizadorAscii.logar(tempo,log)
	categorizadorAscii.categorizadorLexico.lista.append(Delimitador(tempo=tempo+1,conteudo=asciiDescartavel.conteudo))	


class CategorizadorAscii(MotorDeEventos):
	def __init__(self,
				 listaInicial=[],
				 rotinasDeTratamento={type(AsciiUtil()):categorizarAsciiUtil,
				 					  type(AsciiControle()):categorizarAsciiControle,
				 					  type(AsciiDescartavel()):categorizarAsciiDescartavel},
				 categorizadorLexico=CategorizadorLexico()):
		super().__init__(listaInicial,rotinasDeTratamento)
		self.categorizadorLexico = categorizadorLexico