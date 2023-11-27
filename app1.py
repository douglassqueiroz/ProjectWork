import base64
import cv2
import os
import time
import threading
import logging
from threading import Thread, Lock 
from flask import Flask, render_template, Response, request, jsonify, redirect, url_for
from queue import Queue
from crud_users import adicionar_usuario, remover_usuario, atualizar_usuario, caminho_banco_usuarios, listar_usuarios, matricula_existe
app = Flask(__name__)

app.logger.setLevel(logging.ERROR)

# Define o caminho onde a foto será salva (altere conforme necessário)
caminho = r'C:\Users\Administrador\Desktop\projeto_Adar\ambiente_virtual_python\images'

from permissao import verificar_permissao_pasta

@app.route('/')
def index():
    #return render_template('index.html')
    return "hello, world"
# Rota para salvar a foto
@app.route('/save_photo', methods=['POST'])
def save_photo():
    try:
        # Obtém os dados da foto da solicitação JSON
        data = request.get_json()
        photo_data = data['photoData']

        # Converte os dados base64 para bytes
        photo_bytes = photo_data.split(',')[1].encode('utf-8')

        # Salva a foto no caminho especificado
        if verificar_permissao_pasta(caminho):
            save_path = os.path.join(caminho, 'photo.png')
            with open(save_path, 'wb') as f:
                f.write(base64.b64decode(photo_bytes))
            return jsonify(success=True)
        else:
            error_message = "sem premissão para acessar a pasta."
            print(f"Erro ao salvar a foto: {error_message}")
            return jsonify(success=False, error=error_message)
    except Exception as e:
        error_message = str(e)
        print(f"Erro ao salvar a foto: {error_message}")
        return jsonify(success=False, error=error_message)
    

    
@app.route('/create_user', methods = ['POST'])
def create_user():  
    try:
        # Obter dados do formulário da solicitação 
        data = request.json
        matricula = data.get('matricula')
        nome = data.get('nome')
        print(f"Matrícula recebida: {matricula}")
        print(f"Nome recebido: {nome}")

        # Verificar se a matrícula e o nome são fornecidos e válidos
        if not matricula or not nome:
            print("Matrícula e nome devem ser fornecidos.")
            return jsonify(success=False, error="Matrícula e nome são obrigatórios.")
        print("Continuando com a adição do usuário ao banco.")
        if matricula_existe(matricula):
            print(f'a matricula {matricula} ja existe no banco')
            return jsonify(success=False, error="Matrícula já existe no banco.")
        # Adicionar o usuário ao banco de dados
        adicionar_usuario(matricula, nome)        
        return redirect(url_for('create_user'))
        
    except Exception as e:
        error_message = str(e)
        print(f"Erro ao criar o usuário: {error_message}")
        return jsonify(success=False, error=error_message)
    
@app.route('/listar_usuarios', methods=['GET'])
def get_usuarios():
    usuarios = listar_usuarios()
    if usuarios is not None:
        return jsonify(success=True, usuarios=usuarios)
    else:
        return jsonify(success=False, error="Erro ao obter usuários do banco de dados.")

##############VERIFICANDO SE MATRICULA EXISTE PARA MOSTRAR AO USUARIO##############
@app.route('/verificar_matricula/<matricula>', methods=['GET'])
def verificar_matricula(matricula):
    try:
        # Chame a função matricula_existe e retorne se a matrícula existe
        matricula_existe_resultado = matricula_existe(matricula)
        print(f"Matrícula recebida: {matricula}")
        
        return jsonify(matriculaExistente=matricula_existe_resultado)
    except Exception as e:
        error_message = str(e)
        print(f"Erro ao verificar a matrícula: {error_message}")
        return jsonify(matriculaExistente=False)
##############VERIFICANDO SE MATRICULA EXISTE PARA MOSTRAR AO USUARIO##############



@app.route('/delete_user/<matricula>', methods=['DELETE'])
def delete_user(matricula):
    try:
        # Obter os dados JSON do corpo da solicitação
        dados_json = request.json
        nome = dados_json.get('nome')  # Se você precisar do nome, caso contrário, pode remover essa linha

        # Remover o usuário do banco de dados
        sucesso = remover_usuario(matricula)

        if sucesso:
            print(f"Usuário com a matrícula {matricula} removido com sucesso.")
            return jsonify(success=True)
        else:
            return jsonify(success=False, error="Erro ao remover usuário.")

    except Exception as e:
        error_message = str(e)
        print(f"Erro ao excluir o usuário: {error_message}")
        return jsonify(success=False, error=error_message)
    
@app.route('/update_user/<matricula_antiga>', methods=['PUT'])
def update_user(matricula_antiga):
    try:
        # Obter dados JSON do corpo da solicitação
        dados_json = request.json
        nova_matricula = dados_json.get('nova_matricula')
        novo_nome = dados_json.get('novo_nome')
        print(f"Matrícula antiga: {matricula_antiga}")
        print(f"Matrícula nova: {nova_matricula}")

        # Atualizar o usuário no banco de dados
        sucesso = atualizar_usuario(matricula_antiga, nova_matricula, novo_nome)

        if sucesso:
            print(f"Usuário com a matrícula {matricula_antiga} atualizado com sucesso.")
            return jsonify(success=True)
        else:
            return jsonify(success=False, error="Erro ao atualizar usuário.")

    except Exception as e:
        error_message = str(e)
        print(f"Erro ao atualizar o usuário: {error_message}")
        return jsonify(success=False, error=error_message)


if __name__ == '__main__':
    cert_path = r'C:\Users\Administrador\Desktop\projeto_Adar\ambiente_virtual_python\backend\certificado.pem'
    key_path = r'C:\Users\Administrador\Desktop\projeto_Adar\ambiente_virtual_python\backend\chave-privada.pem'
    app.run(host="0.0.0.0", port=5000, debug=True, ssl_context=(cert_path, key_path))