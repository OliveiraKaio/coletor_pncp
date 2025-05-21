import random
import time

def simular_comportamento_humano():
    espera = random.uniform(5, 15)
    print(f"[delay] Aguardando {espera:.2f}s para simular humano...")
    time.sleep(espera)
