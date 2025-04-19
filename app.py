from flask import Flask, render_template
import requests

app = Flask(__name__)

PLANILHA_ID = '1NLAAj-1Lh1X9PGkNM5K7S7z5cuMAn-9bYMc__HUzzYo'
SHEET_NAME = 'Sheet1'  # Substitua pelo nome da sua aba se for diferente

def obter_dados_planilha():
    url = f'https://docs.google.com/spreadsheets/d/{PLANILHA_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lança uma exceção para códigos de status ruins
        csv_data = response.text.strip().split('\n')
        if not csv_data:
            return []
        headers = [header.strip().strip('"') for header in csv_data[0].split(',')]
        dados = []
        for row in csv_data[1:]:
            values = [value.strip().strip('"') for value in row.split(',')]
            if len(headers) == len(values):
                dados.append(dict(zip(headers, values)))
        return dados
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a planilha: {e}")
        return []

@app.route('/')
def lista_empreendimentos():
    empreendimentos = obter_dados_planilha()
    return render_template('lista_empreendimentos.html', empreendimentos=empreendimentos)

@app.route('/detalhes/<nome>')
def detalhes_empreendimento(nome):
    empreendimentos = obter_dados_planilha()
    for empreendimento in empreendimentos:
        if empreendimento['Nome do Empreendimento'] == nome:
            return render_template('detalhes_empreendimento.html', empreendimento=empreendimento)
    return "Empreendimento não encontrado"

@app.route('/sair')
def sair():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)