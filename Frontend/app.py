from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
import os

app = Flask(__name__)

# Definindo as variáveis de ambiente
API_BASE_URL = "http://backend:8000"

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para exibir o formulário de cadastro
@app.route('/cadastro', methods=['GET'])
def inserir_placa_form():
    return render_template('cadastro.html')

# Rota para enviar os dados do formulário de cadastro para a API
@app.route('/inserir', methods=['POST'])
def inserir_placa():
    modelo = request.form['modelo']
    marca = request.form['marca']
    quantidade = request.form['quantidade']
    preco = request.form['preco']

    payload = {
        'modelo': modelo,
        'marca': marca,
        'quantidade' : quantidade,
        'preco' : preco
    }

    response = requests.post(f'{API_BASE_URL}/api/v1/placas_de_video/', json=payload)
    
    if response.status_code == 201:
        return redirect(url_for('listar_placas_de_video'))
    else:
        return "Erro ao inserir placa", 500

# Rota para listar todos os placas_de_video
@app.route('/estoque', methods=['GET'])
def listar_placas_de_video():
    response = requests.get(f'{API_BASE_URL}/api/v1/placas_de_video/')
    try:
        placas_de_video = response.json()
    except:
        placas_de_video = []
    return render_template('estoque.html', placas_de_video=placas_de_video)

# Rota para exibir o formulário de edição de placa
@app.route('/atualizar/<int:placa_id>', methods=['GET'])
def atualizar_placa_form(placa_id):
    response = requests.get(f"{API_BASE_URL}/api/v1/placas_de_video/")
    #filtrando apenas o placa correspondente ao ID
    placas_de_video = [placa for placa in response.json() if placa['id'] == placa_id]
    if len(placas_de_video) == 0:
        return "placa não encontrado", 404
    placa = placas_de_video[0]
    return render_template('atualizar.html', placa=placa)

# Rota para enviar os dados do formulário de edição de placa para a API
@app.route('/atualizar/<int:placa_id>', methods=['POST'])
def atualizar_placa(placa_id):
    modelo = request.form['modelo']
    marca = request.form['marca']
    quantidade = request.form['quantidade']
    preco = request.form['preco']

    payload = {
        'id': placa_id,
        'modelo': modelo,
        'marca': marca,
        'quantidade' : quantidade,
        'preco' : preco
    }

    response = requests.patch(f"{API_BASE_URL}/api/v1/placas_de_video/{placa_id}", json=payload)
    
    if response.status_code == 200:
        return redirect(url_for('listar_placas_de_video'))
    else:
        return "Erro ao atualizar placa", 500

# Rota para exibir o formulário de edição de placa
@app.route('/vender/<int:placa_id>', methods=['GET'])
def vender_placa_form(placa_id):
    response = requests.get(f"{API_BASE_URL}/api/v1/placas_de_video/")
    #filtrando apenas o placa correspondente ao ID
    placas_de_video = [placa for placa in response.json() if placa['id'] == placa_id]
    if len(placas_de_video) == 0:
        return "placa não encontrado", 404
    placa = placas_de_video[0]
    return render_template('vender.html', placa=placa)

# Rota para vender um placa
@app.route('/vender/<int:placa_id>', methods=['POST'])
def vender_placa(placa_id):
    quantidade = request.form['quantidade']

    payload = {
        'quantidade': quantidade
    }

    response = requests.put(f"{API_BASE_URL}/api/v1/placas_de_video/{placa_id}/vender/", json=payload)
    
    if response.status_code == 200:
        return redirect(url_for('listar_placas_de_video'))
    else:
        return "Erro ao vender placa", 500

# Rota para listar todas as vendas
@app.route('/vendas', methods=['GET'])
def listar_vendas():
    response = requests.get(f"{API_BASE_URL}/api/v1/vendas/")
    try:
        vendas = response.json()
    except:
        vendas = []
    #salvando nomes dos placas_de_video vendidos
    total_vendas = 0
    for venda in vendas:
        total_vendas += float(venda['valor_venda'])
    return render_template('vendas.html', vendas=vendas, total_vendas=total_vendas)

# Rota para excluir um placa
@app.route('/excluir/<int:placa_id>', methods=['POST'])
def excluir_placa(placa_id):
    response = requests.delete(f"{API_BASE_URL}/api/v1/placas_de_video/{placa_id}")
    
    if response.status_code == 200  :
        return redirect(url_for('listar_placas_de_video'))
    else:
        return "Erro ao excluir placa", 500

#Rota para resetar o database
@app.route('/reset-database', methods=['GET'])
def resetar_database():
    response = requests.delete(f"{API_BASE_URL}/api/v1/placas_de_video/")
    
    if response.status_code == 200  :
        return render_template('confirmacao.html')
    else:
        return "Erro ao resetar o database", 500


if __name__ == '__main__':
    app.run(debug=True, port=3000, host='0.0.0.0')