import os
from permissao import caminho_banco_usuarios
from permissao import criar_arquivo_banco_usuarios
#ADICIONANDO USUARIO
def adicionar_usuario(matricula, nome):
    try:
        print(f"Adicionando usuário ao banco: Matrícula: {matricula}, Nome: {nome}")

        if not matricula or not nome:
            print("Matrícula e nome devem ser fornecidos.")
            return False
        
        path_arquivo = os.path.join(caminho_banco_usuarios, 'users.txt')
##################VERIFICANDO SE EXISTE USUARIO NO BANCO##################
        if matricula_existe(matricula):
            print("Matrícula já existe. Não foi possível adicionar o usuário.")
            return False
        # Teste direto da função adicionar_usuario com uma matrícula que você tem certeza que não está no arquivo
        with open(path_arquivo, 'a') as arquivo:
            arquivo.write(f"{matricula},{nome}\n")
        print("Usuário adicionado com sucesso.")
        return True
    except Exception as e:
        print(f"Erro ao adicionar usuário: {str(e)}")
        return False
##################VERIFICANDO SE EXISTE USUARIO NO BANCO##################
def matricula_existe(matricula):
    try:
        path_arquivo = os.path.join(caminho_banco_usuarios, 'users.txt')
        with open(path_arquivo, 'r') as arquivo:
            for linha in arquivo:
                if ',' not in linha:
                    continue
            
            
                matricula_existente = linha.split(',')[0].strip()
                print(f"Matrícula existente: {matricula_existente}, Matrícula procurada: {matricula}")
                print(f"matricula_existe = {type(matricula_existente)} e matricula {type(matricula)} ")
                if int(matricula_existente) == matricula:
                    return True


            # Se a matrícula não foi encontrada, imprime a mensagem e retorna False
            print("Matricula nao encontrada")
            return False

 
    except Exception as e:
        print(f"Erro ao verificar se a matrícula existe: {str(e)}")
        return False
def listar_usuarios():
    try:
        path_arquivo = os.path.join(caminho_banco_usuarios, 'users.txt')
        with open(path_arquivo, 'r') as arquivo:
            linhas = arquivo.readlines()

        # Converte as linhas do arquivo em uma lista de dicionários
        usuarios = []
        for linha in linhas[1:]:  # Ignora o cabeçalho
            matricula, nome = linha.split(',')
            usuarios.append({'matricula': matricula.strip(), 'nome': nome.strip()})

        return usuarios

    except Exception as e:
        print(f"Erro ao listar usuários: {str(e)}")
        return None    

def remover_usuario(matricula):
    try:
        matricula = str(matricula)
        path_arquivo = os.path.join(caminho_banco_usuarios, 'users.txt')
        with open(path_arquivo, 'r') as arquivo:
            linhas = arquivo.readlines()

        with open(path_arquivo, 'w') as arquivo:
            arquivo.write(linhas[0])  # Escreve o cabeçalho

            for linha in linhas[1:]:
                if matricula not in linha:
                    arquivo.write(linha)

        print(f"Usuário com a matrícula {matricula} removido com sucesso.")
        return True
    except Exception as e:
        print(f"Erro ao remover usuário: {str(e)}")
        return False

# crud_users.py

def atualizar_usuario(matricula_antiga, nova_matricula, novo_nome):
    try:
        path_arquivo = os.path.join(caminho_banco_usuarios, 'users.txt')
        with open(path_arquivo, 'r') as arquivo:
            linhas = arquivo.readlines()

        with open(path_arquivo, 'w') as arquivo:
            arquivo.write(linhas[0])  # Escreve o cabeçalho

            for linha in linhas[1:]:
                matricula, nome = linha.strip().split(',')
                if matricula == matricula_antiga:
                    # Atualiza a linha com os novos dados
                    linha = f"{nova_matricula},{novo_nome}\n"
                arquivo.write(linha)
        print(f"Usuário com a matrícula {matricula_antiga} atualizado com sucesso.")
        return True
    except Exception as e:
        print(f"Erro ao atualizar usuário: {str(e)}")
        return False


        
