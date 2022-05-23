import os
import json
import redis
from time import sleep
from random import randint

if __name__ == "__main__":
    print("Aguardando mensagens...")

    redis_host = os.getenv('REDIS_HOST', 'queue')
    fila = redis.Redis(host=redis_host, port=6379, db=0)

    while True:
        mensagem = json.loads(fila.blpop('sender')[1])

        # Simular envio de email
        print(f"Enviando a mensagem {mensagem['assunto']}...")
        sleep(randint(15, 45))
        print(f"Mensagem {mensagem['assunto']} enviada!")
