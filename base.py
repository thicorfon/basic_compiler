class Evento(object):
	def __init__(self, tempo=0, tarefa='T0'):
		self.tempo = tempo
		self.tarefa = tarefa
	

class MotorDeEventos(object):
	def __init__(self, listaInicial=[], rotinasDeTratamento={}):
		self.lista = listaInicial
		self.rotinasDeTratamento = rotinasDeTratamento

	def iterar(self,tempo):
		while(len(self.lista) != 0):
			topEvent = self.lista[0]
			if topEvent.tempo == tempo:
				eventoAtual = self.lista.pop(0)
				self.rotinasDeTratamento[type(eventoAtual)](self,eventoAtual,tempo)
			else:
				return
		return

	def logar(self,tempo,log):
		print("Tempo: {0}\nMaquina: {1}\nLog: {2}\n\n".format(str(tempo),str(type(self)),log))
		


		
		