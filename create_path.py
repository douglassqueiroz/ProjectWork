from crud_users import caminho_pasta_usuarios
import os
def criar_pasta_usuario(matricula):
    try:
        pasta_usuario = os.path.join(caminho_pasta_usuarios, f'usuario_{matricula}')
        os.makedirs(pasta_usuario, exist_ok=True)
        print(f"Pasta do usuário criada: {pasta_usuario}")
        return pasta_usuario
    except Exception as e:
        print(f"Erro ao criar pasta do usuário: {str(e)}")
        return None