from flask import Flask, render_template
# import mysql.connector
import mariadb

app = Flask(__name__)


DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'certificados',
    'port':3306
}

@app.route('/validar/<int:id_participante>')
def validar_certificado(id_participante):

    try:
        conn = mariadb.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        # cursor.execute('''SELECT * FROM participantes WHERE id = ?''', (id_participante,))
        cursor.execute('SELECT * FROM participantes WHERE id = ?', (id_participante,))

        participante = cursor.fetchone()

        # conn.close()

        if participante:
            return render_template('index.html', nome=participante['nome'], evento=participante['evento'], data=participante['data_registro'].strftime('%d/%m/%Y %H:%M'), valido=participante['valido'])
        
        return "Certificado não encontrado!", 404
    
    except mariadb.Error as e:
        return f"Erro de banco de dados: {e}", 500
    finally:
        if 'conn' in locals(): conn.close()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5500, debug=True)
                                