# main.py
from threading import Thread
from keep_alive import run as keep_alive
from coletor.listar import executar_coleta
from dotenv import load_dotenv
import os

load_dotenv()

# Inicia servidor Flask para manter Replit acordado
Thread(target=keep_alive).start()

# Executa a coleta principal
executar_coleta()
