import qrcode
import argparse
import mariadb
import os
from urllib.parse import quote

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'certificados',
    'port': 3306
}

def criar_tabela():
    conn = None
    try:
        conn = mariadb.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS participantes (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        nome VARCHAR(255) NOT NULL,
                        evento VARCHAR(255) NOT NULL,
                        data_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
                        valido BOOLEAN DEFAULT TRUE)''')
        conn.commit()
        
    except mariadb.Error as e:
        print(f"Erro ao conectar ao MariaDB: {e}")
    finally:
        if conn: conn.close()

def gerar_qrcode(id_participante, nome):
    os.makedirs('qrcode', exist_ok=True)
    
    # Codifica o nome para URL
    nome_codificado = quote(nome)
    url = f"https://oneway.tec.br/monkey/certificados/{nome_codificado}.jpeg"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12,
        border=6
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    nome_arquivo = f"{id_participante}_{nome.replace(' ', '_')}"
    caminho_imagem = f'qrcode/{nome_arquivo}.png'
    img.save(caminho_imagem)
    return caminho_imagem

def inserir_participante(nome, evento):
    conn = None
    try:
        conn = mariadb.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute('''INSERT INTO participantes (nome, evento)
                        VALUES (?, ?)''', (nome, evento))
        id_participante = cursor.lastrowid
        
        conn.commit()
        return id_participante
        
    except mariadb.Error as e:
        print(f"Erro no MariaDB: {e}")
        return None
    finally:
        if conn: conn.close()

if __name__ == "__main__":
    criar_tabela()

    parser = argparse.ArgumentParser(description='Gerador de QR Code para certificados')
    parser.add_argument('--nome', required=True, help='Nome do participante')
    parser.add_argument('--evento', required=True, help='Nome do evento')
    
    args = parser.parse_args()
    
    id_participante = inserir_participante(args.nome, args.evento)
    
    if id_participante:
        caminho_qrcode = gerar_qrcode(id_participante, args.nome)
        print("\n" + "="*50)
        print(f" QR Code gerado com sucesso para {args.nome}!")
        print("="*50)
        print(f" ID do participante: {id_participante}")
        print(f" Local do arquivo: {os.path.abspath(caminho_qrcode)}")
        print(f" URL do certificado: https://oneway.tec.br/monkey/certificados/{id_participante}_{quote(args.nome)}.jpeg")
        print("="*50 + "\n")
    else:
        print("Erro ao gerar o QR Code. Verifique os logs.")