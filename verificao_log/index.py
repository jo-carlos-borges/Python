import re
from collections import defaultdict

def extrair_ip(linha):
    """
    Extrai o primeiro endereço IP encontrado na linha.
    Assume um formato IPv4 padrão.
    """
    padrao_ip = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    match = re.search(padrao_ip, linha)
    if match:
        return match.group(0)
    return None

def analisar_logs(caminhos_arquivos_log, login_alvo, senha_alvo):
    """
    Analisa os arquivos de log para encontrar acessos de um usuário específico
    de diferentes IPs.

    Args:
        caminhos_arquivos_log (list): Uma lista de strings com os caminhos para os arquivos de log.
        login_alvo (str): O nome de usuário a ser procurado.
        senha_alvo (str): A senha a ser procurada.

    Returns:
        tuple: (dados_por_ip, total_acessos_usuario)
               dados_por_ip (defaultdict): Um dicionário onde as chaves são IPs e
                                           os valores são listas das linhas de log correspondentes.
               total_acessos_usuario (int): O número total de acessos pelo usuário alvo.
    """
    dados_por_ip = defaultdict(list)
    total_acessos_usuario = 0
    texto_login = f"login: {login_alvo}"
    texto_senha = f"password: {senha_alvo}"

    for caminho_arquivo in caminhos_arquivos_log:
        try:
            with open(caminho_arquivo, 'r', encoding='latin-1') as f:
                print(f"\nAnalisando arquivo: {caminho_arquivo}...")
                for num_linha, linha in enumerate(f, 1):
                    linha_strip = linha.strip()
                    if texto_login in linha_strip and texto_senha in linha_strip:
                        ip_encontrado = extrair_ip(linha_strip)
                        if ip_encontrado:
                            dados_por_ip[ip_encontrado].append(f"(Arquivo: {caminho_arquivo}, Linha: {num_linha}): {linha_strip}")
                            total_acessos_usuario += 1
                        else:
                            dados_por_ip["IP_NAO_ENCONTRADO"].append(f"(Arquivo: {caminho_arquivo}, Linha: {num_linha}): {linha_strip}")
                            total_acessos_usuario += 1
                            print(f"  Aviso: Login encontrado na linha {num_linha} do arquivo {caminho_arquivo}, mas nenhum IP pôde ser extraído.")
                            print(f"  Conteúdo da linha: {linha_strip}")

        except FileNotFoundError:
            print(f"Erro: Arquivo '{caminho_arquivo}' não encontrado.")
        except Exception as e:
            print(f"Erro ao processar o arquivo '{caminho_arquivo}': {e}")

    return dados_por_ip, total_acessos_usuario

def main():
    caminhos_logs = [
        "D:/PRojetos/Python/verificao_log/logs/server.log.2025-05-26",
        "D:/PRojetos/Python/verificao_log/logs/server.log.2025-05-27",
        "D:/PRojetos/Python/verificao_log/logs/server.log.2025-05-25",
        "D:/PRojetos/Python/verificao_log/logs/server.log.2025-05-24",
        "D:/PRojetos/Python/verificao_log/logs/server.log.2025-05-23",
        "D:/PRojetos/Python/verificao_log/logs/server.log.2025-05-22",
        "D:/PRojetos/Python/verificao_log/logs/server.log.2025-05-21",
        "D:/PRojetos/Python/verificao_log/logs/server.log.2025-05-20",
        "D:/PRojetos/Python/verificao_log/logs/server.log.2025-05-19",
        "D:/PRojetos/Python/verificao_log/logs/server.log",
    ]

    login_alvo = "ismaelzazzeron"
    senha_alvo = "ismaelzazzeron123"

    if not caminhos_logs or caminhos_logs == ["seu_arquivo_de_log.log"]:
        print("Por favor, edite o script e defina a variável 'caminhos_logs' com os caminhos dos seus arquivos de log.")
        return

    dados_por_ip, total_acessos_usuario = analisar_logs(caminhos_logs, login_alvo, senha_alvo)

    print("\n--- Resultados da Análise ---")
    print(f"Login alvo: {login_alvo}")

    if not dados_por_ip:
        print("Nenhum acesso encontrado para o usuário especificado.")
        return

    ips_unicos_reais = [ip for ip in dados_por_ip if ip != "IP_NAO_ENCONTRADO"]
    num_ips_diferentes = len(ips_unicos_reais)

    print(f"\nNúmero de IPs diferentes que acessaram com este login: {num_ips_diferentes}")

    if num_ips_diferentes > 0:
        if num_ips_diferentes > 1:
            print(f"\nForam encontrados {num_ips_diferentes} IPs diferentes. Detalhes de acesso para cada IP:")
        elif num_ips_diferentes == 1:
            print(f"\nFoi encontrado 1 IP diferente. Detalhes do acesso:")
    
    for ip_detalhe in sorted(dados_por_ip.keys()):
        if ip_detalhe == "IP_NAO_ENCONTRADO":
            continue 
        
        print(f"\n  IP: {ip_detalhe} (Total de acessos: {len(dados_por_ip[ip_detalhe])})")
        for linha in dados_por_ip[ip_detalhe]:
            print(f"    {linha}")

    if "IP_NAO_ENCONTRADO" in dados_por_ip:
        print(f"\n  Acessos onde o IP não pôde ser extraído (Total: {len(dados_por_ip['IP_NAO_ENCONTRADO'])}):")
        for linha in dados_por_ip["IP_NAO_ENCONTRADO"]:
            print(f"    {linha}")

    print(f"\n--- Resumo da Contagem de Acessos para '{login_alvo}' ---")
    if not ips_unicos_reais and "IP_NAO_ENCONTRADO" not in dados_por_ip :
        print("Nenhum acesso registrado.")
    else:
        if ips_unicos_reais:
            print("\nContagem por IP encontrado:")
            for ip_resumo in sorted(ips_unicos_reais):
                print(f"  - IP: {ip_resumo}, Acessos: {len(dados_por_ip[ip_resumo])}")
        
        if "IP_NAO_ENCONTRADO" in dados_por_ip:
            print(f"\n  - Acessos com IP não extraído: {len(dados_por_ip['IP_NAO_ENCONTRADO'])}")

    print(f"\nContagem total geral de acessos: {total_acessos_usuario}")
    print("--- Fim da Análise ---")

if __name__ == "__main__":
    main()
