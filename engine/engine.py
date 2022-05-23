import os
import json
import redis
import psycopg2
from bottle import Bottle, request


class Sender(Bottle):
    def __init__(self):
        super().__init__()
        self.route('/', method='POST', callback=self.enviar)

        redis_host = os.getenv('REDIS_HOST', 'queue')
        self.fila = redis.StrictRedis(host=redis_host, port=6379, db=0)

        host = os.getenv('DB_HOST', 'database')
        database = os.getenv('DB_NAME', 'email_sender')
        user = os.getenv('DB_USER', 'postgres')
        password = os.getenv('DB_PASSWORD', 'postgres')
        self.conn = psycopg2.connect(host=host, database=database, user=user, password=password)

    def gravarMensagem(self, assunto, mensagem):
        query = 'INSERT INTO emails (assunto, mensagem) VALUES (%s, %s);'
        cur = self.conn.cursor()
        cur.execute(query, (assunto, mensagem))
        self.conn.commit()
        cur.close()

        msg = {'assunto': assunto, 'mensagem': mensagem}
        self.fila.rpush('sender', json.dumps(msg))
        print(f"Mensagem gravada! Assunto: {assunto} - Mensagem: {mensagem}")

    def enviar(self):
        assunto = request.forms.get('assunto')
        mensagem = request.forms.get('mensagem')
        self.gravarMensagem(assunto, mensagem)
        return f'Mensagem enfileirada! Assunto: {assunto} - Mensagem: {mensagem}'


if __name__ == "__main__":
    sender = Sender()
    sender.run(host='0.0.0.0', port=8080, debug=True)
    sender.conn.close()
