import pyttsx3 as voz
from DataBase import *

asistente=voz.init()
velocidad = asistente.getProperty('rate')
asistente.setProperty('rate', velocidad-20)
asistente.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0')

objDataB=Database("localhost","root","root","diccionario")

class talk():
	"""docstring for talk"""
	salir='finaliza el programa'
	
	def __init__(self):
		super(talk,self).__init__()
		objDataB.conexion();
		self.config()

	def config(self):
		self.name=objDataB.consulta("name","configuracion")

	def nameP(self):
		return self.name

	def hablar(self,texto):
		asistente.say(texto)
		asistente.runAndWait()