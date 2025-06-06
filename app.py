import os
from flask import Flask, request, jsonify
from psycopg2 import connect
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Healthcheck para o Render
@app.route('/')
def health():
    return 'OK'

def get_conn():
    return connect(os.environ["SUPABASE_URL"], cursor_factory=RealDictCursor)

@app.route('/salas', methods=['GET'])
def get_salas():
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM salas')
                salas = cur.fetchall()
                return jsonify(salas)
    except Exception as e:
        print("Erro ao buscar salas:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/reservas', methods=['GET'])
def get_reservas():
    dia = request.args.get('dia')
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT r.*, s.nome AS sala_nome, u.nome AS usuario_nome, u.email AS usuario_email, s.outlook_email
                    FROM reservas r
                    JOIN salas s ON r.sala_id = s.id
                    JOIN usuarios u ON r.usuario_id = u.id
                    WHERE r.inicio::date = %s
                    ORDER BY r.inicio
                """, (dia,))
                reservas = cur.fetchall()
                return jsonify(reservas)
    except Exception as e:
        print("Erro ao buscar reservas:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/reservas', methods=['POST'])
def criar_reserva():
    data = request.get_json()
    sala_id = data['sala_id']
    usuario_id = data['usuario_id']
    inicio = data['inicio']
    fim = data['fim']
    assunto = data['assunto']
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                # Verifica conflito
                cur.execute("""
                    SELECT * FROM reservas WHERE sala_id = %s AND (
                        (inicio < %s AND fim > %s)
                    )
                """, (sala_id, fim, inicio))
                if cur.fetchone():
                    return jsonify({'error': 'Horário já reservado para esta sala!'}), 400
                # Insere reserva
                cur.execute("""
                    INSERT INTO reservas (sala_id, usuario_id, inicio, fim, assunto)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING *
                """, (sala_id, usuario_id, inicio, fim, assunto))
                reserva = cur.fetchone()
                conn.commit()
                return jsonify(reserva), 201
    except Exception as e:
        print("Erro ao criar reserva:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)