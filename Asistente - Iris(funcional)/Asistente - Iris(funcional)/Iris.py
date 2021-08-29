import sys
import webbrowser
import speech_recognition as sr
#import pyttsx3 as voz
#import pyautogui as gui
#import datetime
#import subprocess as subp
#import mysql.connector

#import pywhatkit
import urllib.request
import json

from difflib import SequenceMatcher as SM 
from time import sleep
from control import *
from DataBase import *
from Asistente import *

## Objetos
listener = sr.Recognizer()
objAplicaciones=Aplicaciones()
objBusquedas=BusquedasWeb()
objRedactar=RedactarTexto()
objTareas=TareasSimples()
objDataB=Database("localhost","root","root","diccionario")
objAsis=talk()

## Variables
redactando=False
msgError="Lo siento, ha ocurrido un problema"
nameP=''
## Comandos

afirmaciones=['sí','por favor', 'sí por favor','si por favor']
lastComand=''

##  Metodos generales

def escuchar(comando):
	with sr.Microphone() as source:
		audio = listener.listen(source)
		try:
		    text = listener.recognize_google(audio, language='es-ES')
		    #if name in text:
		    text=text.lower()
		    print('Has dicho: {}'.format(text))
		    if comando==True:
			    global lastComand
			    lastComand=text
		    return text
		except sr.UnknownValueError:
			objAsis.hablar('No te he entendido')
			if comando == False:
				audio = listener.listen(source)
				try:
				    text = listener.recognize_google(audio, language='es-ES')
				    text=text.lower()
				    print('Has dicho: {}'.format(text))
				    return text
				except:
					objAsis.hablar('Lo siento, no logre entenderte')
			return ''
		except sr.RequestError as e:
			print("No es posible obtener la respuesta de Google Speech Recognition{0}".format(e))

def reconocer():
	comando=escuchar(True)
	similitud=SM(None, objAsis.salir,comando).ratio()
	#print(f"la similitud es: {similitud}")
	if objAsis.salir in comando or similitud>=0.8:
		print('Terminando.....')
		return True
	else:
		similitud=SM(None, nameP,comando).ratio()
		if nameP in comando:
			lastComand=comando
			interpretar(comando)
		return False

keyswords={'redactar':objRedactar.abrir_blocNotas,'escribe':objRedactar.abrir_blocNotas,'abre':objBusquedas.abrir_pagWeb,'ejecuta':objAplicaciones.ejecutarPrograma,
'reproduce':objBusquedas.buscarEn_youtube,'hora':objTareas.hora,"fecha":objTareas.fecha}

questions={'qué':objBusquedas.buscarSignificado,'quién':objBusquedas.buscarSignificado,'dónde':objBusquedas.buscarSignificado,'cuántos':objBusquedas.buscarSignificado,
'cuánto':objBusquedas.buscarSignificado,'cuando':objBusquedas.buscarSignificado,'quien':objBusquedas.buscarSignificado}

def error(arg):
    objAsis.hablar('Lo siento no me es posible realizar esta tarea')

def interpretar(comando):
	print('Interpretando')
	comando = comando.split(' ')
	valido=False
	action=False

	##ANEXADO
	try:
		for ite in keyswords.keys():
			similitud=SM(None, ite,lastComand).ratio()
			if ite in comando or similitud>=0.80:
				print("entró if",ite)
				keyswords.get(ite,error)(lastComand)
				action=True

		if action==False:
			if objDataB.busqueda(lastComand)==True:
			    print("respondiendo.-.")
			    action=True
			#else:
			    #print('No me es posible realizar esta acción.')
			else:
				for ite in questions.keys():
						if ite in comando:
							hablar("¿Quieres que lo busque en la web?")
							if escuchar(False) in afirmaciones:
								print("Buscando en wiki")
								objBusquedas.buscarSignificado(lastComand)
							break
				'''for ite in questions.keys():
					if ite in comando:
						print("entró if",ite)
						questions.get(ite,error)(lastComand)'''
	except Exception as e:
		print("ocurrio un problema tratando de implementar el comando ",e)
		objAsis.hablar(msgError)

def iniciar():
	try:
		terminarAsistente=False
		#objDataB.conexion();
		global nameP
		nameP=str(objAsis.nameP())
		objAsis.hablar(f'Hola soy {nameP}, tu asistente de voz. ¿Qué deseas que haga?')

		while terminarAsistente==False:
			print('A reconocer. ',terminarAsistente)
			objTareas.fecha("fecha")
			terminarAsistente=reconocer()
	except Exception as e:
		print("Ocurrio un problema - Error: ",e)

	objAsis.hablar('Fue un gusto servirte, hasta pronto')

iniciar()