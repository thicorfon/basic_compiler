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
 		


