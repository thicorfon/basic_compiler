from base import Evento

class Arquivo(Evento):
	def __init__(self, tempo=0, tarefa='T0', path='/'):
		super().__init__(tempo,tarefa)
		self.path = path

class ProximaLinha(Evento):
	def __init__(self, tempo=0, tarefa='T0'):
 		super().__init__(tempo,tarefa)

class FecharArquivo(Evento):
	def __init__(self, tempo=0, tarefa='T0'):
 		super().__init__(tempo,tarefa)	

############################################################################# 		

class Linha(Evento):
 	def __init__(self, tempo=0, tarefa='T0', conteudo=''):
 		super().__init__(tempo,tarefa)
 		self.conteudo = conteudo

class FimDeArquivo(Evento):
	def __init__(self, tempo=0, tarefa='T0'):
 		super().__init__(tempo,tarefa)


#############################################################################

class AsciiUtil(Evento):
	def __init__(self, tempo=0, tarefa='T0', conteudo=''):
 		super().__init__(tempo,tarefa)
 		self.conteudo = conteudo

class AsciiControle(Evento):
	def __init__(self, tempo=0, tarefa='T0', conteudo=''):
 		super().__init__(tempo,tarefa)
 		self.conteudo = conteudo

class AsciiDescartavel(Evento):
	def __init__(self, tempo=0, tarefa='T0', conteudo=''):
 		super().__init__(tempo,tarefa)
 		self.conteudo = conteudo

#############################################################################


class Delimitador(Evento):
 	def __init__(self, tempo=0, tarefa='T0', conteudo=''):
 		super().__init__(tempo,tarefa)
 		self.conteudo = conteudo

class Letra(Evento):
 	def __init__(self, tempo=0, tarefa='T0', conteudo=''):
 		super().__init__(tempo,tarefa)
 		self.conteudo = conteudo

class Digito(Evento):
 	def __init__(self, tempo=0, tarefa='T0', conteudo=''):
 		super().__init__(tempo,tarefa)
 		self.conteudo = conteudo

class Especial(Evento):
 	def __init__(self, tempo=0, tarefa='T0', conteudo=''):
 		super().__init__(tempo,tarefa)
 		self.conteudo = conteudo

class Controle(Evento):
 	def __init__(self, tempo=0, tarefa='T0', conteudo=''):
 		super().__init__(tempo,tarefa)
 		self.conteudo = conteudo


#############################################################################

class TokenId(Evento):
	def __init__(self, tempo=0, tarefa='T0', conteudo=''):
 		super().__init__(tempo,tarefa)
 		self.conteudo = conteudo

class TokenNumero(Evento):
	def __init__(self, tempo=0, tarefa='T0', conteudo=''):
 		super().__init__(tempo,tarefa)
 		self.conteudo = conteudo

class TokenEspecial(Evento):
	def __init__(self, tempo=0, tarefa='T0', conteudo=''):
 		super().__init__(tempo,tarefa)
 		self.conteudo = conteudo

