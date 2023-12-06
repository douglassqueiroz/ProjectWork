import os
from permissao import caminho_banco_usuarios
from permissao import criar_arquivo_banco_usuarios, caminho_pasta_usuarios
from create_path import criar_pasta_usuario, caminho_pasta_usuarios
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
        pasta_usuario = criar_pasta_usuario(matricula)
        # Se a pasta do usuário foi criada com sucesso, adicione o usuário ao arquivo de texto
        if pasta_usuario:
            with open(path_arquivo, 'a') as arquivo:
                arquivo.write(f"{matricula},{nome}\n")

            print("Usuário adicionado com sucesso.")
            return True
        else:
            print("Erro ao criar pasta do usuário. Não foi possível adicionar o usuário.")
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
        matricula_encontrada = False  # Flag para indicar se a matrícula foi encontrada
        
        with open(path_arquivo, 'w') as arquivo:
            arquivo.write(linhas[0])  # Escreve o cabeçalho

            for linha in linhas[1:]:
                if matricula not in linha:
                    arquivo.write(linha)
                else:
                    matricula, nome_remover = linha.strip().split(',')
                    # Exclui a pasta do usuário correspondente
                    pasta_usuario = os.path.join(caminho_pasta_usuarios, f'{matricula}')
                    print(f"DEBUG: {pasta_usuario}")
                    if os.path.exists(pasta_usuario):
                        os.rmdir(pasta_usuario)
                        print(f"Pasta do usuário removida: {pasta_usuario}")
  
        if matricula_encontrada:
            print(f"DEBUG: Usuário com a matrícula {matricula} removido com sucesso.")
            return True
        else:
            print(f"DEBUG: Matrícula {matricula} não encontrada. Nenhum usuário removido.")
            return False

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
        #ADICIONANDO A VERIFICAÇÃO DE MATRICULA
            matricula_encontrada = False  # Flag para indicar se a matrícula foi encontrada
        
            for linha in linhas[1:]:
                matricula, nome_antigo= linha.strip().split(',')
                print(f"DEBUG: Matricula antiga: {matricula_antiga}")
                print(f"DEBUG: Nome antigo: {nome_antigo}")   
                if int(matricula) == int(matricula_antiga):
                    matricula_encontrada = True             
                if int(matricula) == int(matricula_antiga):
                    # Atualiza a linha com os novos dados
                    print(f"DEBUG: Nova Matricula: {nova_matricula}")
                    print(f"DEBUG: Novo Nome antes da atualização: {novo_nome}")

                    linha = f"{nova_matricula},{str(novo_nome)}\n"
                    print(f"DEBUG: Linha atualizada: {linha}")
        
                    matricula = nova_matricula  # Atualiza matricula
                    # #ATUALIZANDO O NOME DA PASTA
                    pasta_antiga = os.path.join(caminho_pasta_usuarios, f"{matricula_antiga}")
                    pasta_nova = os.path.join(caminho_pasta_usuarios, f"{nova_matricula}")
                    try:
                        os.rename(pasta_antiga, pasta_nova)
                        print(f"Pasta do usuário renomeada de {pasta_antiga} para {pasta_nova}")
                    except FileNotFoundError:
                        print(f"DEBUG: Pasta do usuário não encontrada: {pasta_antiga}")

                      
                arquivo.write(linha)
            if matricula_encontrada:
                print(f"DEBUG: O tipo de matricula recebida é {type(matricula)}")
                print(f"DEBUG: Usuário com a matrícula {matricula_antiga} atualizado com sucesso.")
                return True
            else:
                print(f"DEBUG: Matrícula {matricula_antiga} não encontrada. Nenhum usuário atualizado.")
                return {"error": "Matrícula não encontrada.", "success": False}

    except Exception as e:
        print(f"Erro ao atualizar usuário: {str(e)}")
        return False


        
