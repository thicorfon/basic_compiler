from base import MotorDeEventos
from eventos import TokenId
from eventos import TokenNumero
from eventos import TokenEspecial
from eventos import TokenReservado

def foo(categorizadorSintatico,evento,tempo):
	log='O token recebido eh do tipo {0} e seu conteudo eh {1}'.format(type(evento),evento.conteudo)
	categorizadorSintatico.logar(tempo,log)

class CategorizadorSintatico(MotorDeEventos):
	def __init__(self,
				 listaInicial=[],
				 rotinasDeTratamento={type(TokenId()):foo,
				 					  type(TokenNumero()):foo,
				 					  type(TokenEspecial()):foo,
				 					  type(TokenReservado()):foo}):
		super().__init__(listaInicial,rotinasDeTratamento)