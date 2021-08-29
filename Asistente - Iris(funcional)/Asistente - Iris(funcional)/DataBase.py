import pymysql
from difflib import SequenceMatcher as SM 


##HABLAR
import speech_recognition as sr
import pyttsx3 as voz
## Objetos
listener = sr.Recognizer()
asistente=voz.init()
velocidad = asistente.getProperty('rate')
asistente.setProperty('rate', velocidad-20)
asistente.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0')

def hablar(texto):
	asistente.say(texto)
	asistente.runAndWait()

##TERMINA HABLAR

class Database():
	"""docstring for Database"""

	def __init__(self, host,user,password,nameDatabase):
		super(Database,self).__init__()
		self.host=host
		self.user=user
		self.password=password
		self.nameDatabase = nameDatabase
		self.cursor=self.conexion()
		
	def conexion(self):
		conexion = pymysql.connect(host="localhost", user="root", password="root", database="diccionario")
		cursor = conexion.cursor()
		return cursor

	def consulta(self,consulta,tabla):
		consulta=f"SELECT dato FROM {tabla} WHERE clave='{consulta}'"
		self.cursor.execute(consulta)
		nDatos=self.cursor.rowcount
		print("se han encontrado", nDatos)
		for i in self.cursor:
			dato=i[0]
		return dato

	def busqueda(self,frase):
		consulta="SELECT * FROM frases"
		self.cursor.execute(consulta)
		nDatos=self.cursor.rowcount
		print("se han encontrado", nDatos)	
		return self.analisis(self.cursor,frase)

	def analisis(self,datos,frase):
		for fila in datos:
			ide=fila[0]
			entrada=fila[1]
			salida=fila[2]
			similitud=SM(None, entrada,frase).ratio()
			print(similitud)
			if(similitud>=0.7):
				hablar(salida)
				return True
		return False
