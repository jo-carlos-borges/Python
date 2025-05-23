import qrcode
import argparse
import mariadb
import os
import csv
from urllib.parse import quote
from tqdm import tqdm

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
                        nome VARCHAR(255) NOT NULL UNIQUE,
                        evento VARCHAR(255) NOT NULL,
                        data_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
                        valido BOOLEAN DEFAULT TRUE)''')
        conn.commit()
        
    except mariadb.Error as e:
        print(f"Erro ao conectar ao MariaDB: {e}")
    finally:
        if conn: conn.close()

def processar_lote(arquivo_csv):
    try:
        with open(arquivo_csv, newline='', encoding='utf-8') as csvfile:
            leitor = csv.DictReader(csvfile)
            linhas = list(leitor)
            
            with mariadb.connect(**DB_CONFIG) as conn, tqdm(total=len(linhas), desc="Processando") as pbar:
                cursor = conn.cursor()
                
                for linha in linhas:
                    try:
                        nome = linha['nome']
                        # Formatar nome para arquivo
                        nome_arquivo = nome.replace(' ', '_').lower()
                        
                        # Inserir no banco
                        cursor.execute('''INSERT INTO participantes (nome, evento)
                                       VALUES (?, ?)''', 
                                       (nome, linha['evento']))
                        
                        # Gerar QR Code
                        url = f"https://oneway.tec.br/monkey/certificados/{quote(nome_arquivo)}.jpeg"
                        
                        qr = qrcode.QRCode(
                            version=1,
                            error_correction=qrcode.constants.ERROR_CORRECT_H,
                            box_size=12,
                            border=6
                        )
                        qr.add_data(url)
                        qr.make(fit=True)
                        
                        img = qr.make_image(fill_color="black", back_color="white")
                        caminho_imagem = f'qrcode/{nome_arquivo}.png'  # Nome do arquivo igual ao certificado
                        img.save(caminho_imagem)
                        
                        pbar.update(1)
                        
                    except mariadb.IntegrityError:
                        print(f"\nNome duplicado: {nome}")
                    except Exception as e:
                        print(f"\nErro no registro {nome}: {str(e)}")
                
                conn.commit()
                
    except Exception as e:
        print(f"Erro geral: {str(e)}")

if __name__ == "__main__":
    criar_tabela()

    parser = argparse.ArgumentParser(description='Gerar QR Codes em lote')
    parser.add_argument('--arquivo', required=True, help='Caminho do arquivo CSV com os participantes')
    
    args = parser.parse_args()
    
    processar_lote(args.arquivo)
    print("\nProcessamento concluído! Verifique a pasta qrcode/")