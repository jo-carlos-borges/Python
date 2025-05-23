from flask import Flask, render_template, request, session, redirect

import random

app = Flask(__name__)
app.template_folder = 'templates'
app.secret_key = 'teste'

jogadores = {}

def iniciar_jogo():
    lista_palavras = ["amigos", "programação", "computador", "jogos", "musicas", "guarda-chuva"]
    palavra_maquina = random.choice(lista_palavras)
    chances = 10
    palavra_secreta = "-" * len(palavra_maquina)
    return palavra_maquina, chances, palavra_secreta

def encaixar_letra(letra_esc, palavra_maquina, palavra_secreta):
    palavra_lista = list(palavra_secreta)
    for index, letra in enumerate(palavra_maquina):
        if letra == letra_esc:
            palavra_lista[index] = letra_esc
    return "".join(palavra_lista)

def processar_tentativa(letra, palavra_secreta, chances, palavra_maquina, nome_jogador):
    letra = letra.lower()
    nova_palavra_secreta = encaixar_letra(letra, palavra_maquina, palavra_secreta)
    mensagem = ""

    if chances == 0:
        if nova_palavra_secreta == palavra_maquina:
            mensagem = "Parabéns, você venceu!"
        elif chances == 1:
            mensagem = f"Última tentativa! A palavra era {palavra_maquina}"
        elif chances == 0:
            mensagem = f"Você perdeu! A palavra era {palavra_maquina}"
        else:
            mensagem = f"A letra '{letra}' não pertence à palavra secreta. Restam {chances - 1} tentativas."

        pontuacao = calcular_pontuacao(chances)
        if nome_jogador in jogadores:
            jogadores[nome_jogador]["pontuação"] += pontuacao
            jogadores[nome_jogador]["historico"].append(palavra_maquina)
        else:
            jogadores[nome_jogador] = {"pontuacao": pontuacao, "historico": [palavra_maquina]}

    return nova_palavra_secreta, chances - 1, mensagem

def calcular_pontuacao(chances):

    return 100 - chances * 10

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome_jogador = request.form['nome']
        session['nome_jogador'] = nome_jogador
        session['palavra_maquina'], session['chances'], session['palavra_secreta'] = iniciar_jogo()
        return redirect('/')
    else:
        if 'palavra_maquina' not in session:
            return render_template('index.html', novo_jogo=True)
        else:
            return render_template('index.html', nome_jogador=session['nome_jogador'], novo_jogo=False,
                                   palavra_secreta=session['palavra_secreta'], chances=session['chances'])

@app.route('/', methods=['POST'])
def iniciar_novo_jogo():
    nome_jogador = request.form['nome_jogador']
    session['nome_jogador'] = nome_jogador
    session['palavra_maquina'], session['chances'], session['palavra_secreta'] = iniciar_jogo()
    return redirect('/')

@app.route('/guess', methods=['POST'])
def guess():
    letra = request.form['letra'].lower()
    palavra_maquina = session['palavra_maquina']
    chances = session['chances']
    palavra_secreta = session['palavra_secreta']
    nome_jogador = session['nome_jogador']

    palavra_secreta, chances, mensagem = processar_tentativa(letra, palavra_secreta, chances, palavra_maquina, nome_jogador)

    session['chances'] = chances
    session['palavra_secreta'] = palavra_secreta

    return render_template('index.html', palavra_secreta=palavra_secreta, chances=chances, mensagem=mensagem)

@app.route('/reiniciar', methods=['POST'])
def reiniciar():
    session.pop('palavra_maquina', None)
    session.pop('chances', None)
    session.pop('palavra_secreta', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
