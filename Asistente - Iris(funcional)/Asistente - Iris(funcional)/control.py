import webbrowser
import pyautogui as gui
import subprocess as subp
import datetime
import wikipedia
import speech_recognition as sr
import pywhatkit

#from Iris import *
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from difflib import SequenceMatcher as SM 
#from scrapy.selector import Selector
from parsel import Selector
from time import sleep
from Asistente import *

## Objetos
listener = sr.Recognizer()
objAsis=talk()

## Variables
msgError="Ha ocurrido un error: "
msgErrorI="Lo siento, no he podido realizar lo que me pides"

#comandos
terminarEscritura="terminar escritura"
terminarEscritura1="terminar la escritura"

##config
wikipedia.set_lang("es")
		
## Control de aplicaciones del sistemas
class Aplicaciones():
	"""docstring for aplicaciones"""
	def __init__(self):
		super(Aplicaciones, self).__init__()

	programsDefect={'calculadora':'calc.exe','excel':'EXCEL.exe', 
	'word':'winword.exe','power point':'POWERPNT.exe', 'paint':'mspaint.exe',
	'dibujar':'mspaint.exe','control':'control'}

	def ejecutarPrograma(self, program):
		for i in Aplicaciones.programsDefect.keys():
			if i in program:
				programa = Aplicaciones.programsDefect.get(i)
				print('Ejecutando '+programa.replace('.exe',''))
				sleep(1)
				subp.call('start '+programa, shell=True)    


## Busquedas web
class BusquedasWeb():
	"""docstring for busquedasWeb"""
	def __init__(self):
		super(BusquedasWeb, self).__init__()
	
	diccPaginasWeb={'google':'www.google.com','youtube':'www.youtube.com','facebook':'web.facebook.com'}

	def abrir_pagWeb(self, pag):
		appSystem=False;
		try:
			for i in BusquedasWeb.diccPaginasWeb.keys():
				if i in pag:
					webbrowser.open(BusquedasWeb.diccPaginasWeb.get(i))
					appSystem=True
					break
			if not appSystem:
				page=pag.replace(" ","+")
				base_url='https://www.google.com'
				url='https://www.google.com/search?q='+page
				driver = webdriver.Edge(executable_path="D:/Cesar Bonilla/Unillanos/Electiva 1/Proyecto/Asistente - Iris/edgedriver_win64/msedgedriver.exe")
				driver.get(url)

				sel = Selector(driver.page_source)
				primer_resultado = sel.xpath('//div[@class="yuRUbf"]/a/@href').extract_first()
				print(primer_resultado)
				driver.get(primer_resultado)
				#webbrowser.open('https://www.google.com/search?q='+page)
		except Exception as e:
			print(msgError,e)

	def buscarSignificado(self, busqueda):
		try:
			objAsis.hablar(wikipedia.summary( busqueda, sentences = 1 , chars = 0 , auto_suggest = True , redirect = True )) 
		except Exception as e:
			print("No se ha encotrado la busqueda - ",e)
			#objAsis("Lo siento, no he podido encontrar lo que me pides")
		
	def buscarEn_youtube(self, titulo):
		try:
			music=titulo.replace('reproduce', '')
			print('Reproduciendo '+ music)
			pywhatkit.playonyt(music)
		except Exception as e:
			print("No se ha encotrado la busqueda - error:",e)
			#objAsis("Lo siento, no he podido encontrar lo que me pides")
		#pywhatkit.playonyt(music)

		#from selenium import webdriver
		#from bs4 import BeautifulSoup
		#driver = webdriver.Chrome("ACA PONES LA RUTA DE TU DRIVER")
		#content = driver.page_source
		#soup = BeautifulSoup(content,'html.parser')
		#driver.get('https://www.youtube.com/results?search_query=intheend')
		#Link=driver.find_element_by_id("video-title").get_attribute("href")
		#print(Link)

##Redactar texto en bloc de notas	
class RedactarTexto():
	"""docstring for RedactarTexto"""
	def __init__(self):
		super(RedactarTexto, self).__init__()

	def redactar(self):
	    try:
	        escribiendo=True
	        with sr.Microphone() as source:
	            while(escribiendo==True):
	                audio = listener.listen(source)
	                textU = listener.recognize_google(audio, language='es-ES')
	                print(textU)
	                textU = textU.lower()
	                similitud=SM(None, textU,terminarEscritura).ratio()
	                #print(f"la similitud es: {similitud}")

	                if similitud<0.75:
	                    gui.write(textU+ " ") 
	                else:
	                    escribiendo=False
	    except Exception as e:
	        print("Ha ocurrido un error:",e)
	        objAsis("No te he entendido")
	        self.redactar() 

	def abrir_blocNotas(self,arg):
		try:
		    msgInicio="ESTOY LISTA PARA REDACTAR";
		    subp.call('start notepad.exe', shell=True)
		    sleep(2.5)
		    objAsis.hablar(msgInicio)
		    self.redactar()
		    print("ESCRITURA EN BLOC DE NOTAS TERMINADA")			
		except Exception as e:
			raise

				
class TareasSimples():
	"""docstring for ClassName"""
	def __init__(self):
		super(TareasSimples, self).__init__()

	def hora(self,comand):
		if 'hora' in comand:
			hora = datetime.datetime.now().strftime('%I:%M %p')
			objAsis.hablar("Son las " + hora)

	def fecha(self,comand):
		if 'fecha' in comand:
			fecha = datetime.datetime.now().strftime('%Y/%m/%d') #'%d/%m/%Y'
			print("fecha: ",fecha)
			objAsis.hablar("Hoy es " + fecha)
		