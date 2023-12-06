import os
caminho_pasta_usuarios = r'C:\Users\Administrador\Desktop\projeto_Adar\ambiente_virtual_python\backend\pasta_usuarios'
caminho_banco_usuarios = r'C:\Users\Administrador\Desktop\projeto_Adar\ambiente_virtual_python\backend\banco_usuarios_teste'
caminho = r'C:\Users\Administrador\Desktop\projeto_Adar\ambiente_virtual_python\backend\pasta_usuarios'
def verificar_permissao_pasta(caminho):
    try:
        #Criar o diretório se não existir
        os.makedirs(caminho, exist_ok=True)
        
        #Verificar se é possível escrever no diretório
        with open(os.path.join(caminho, 'test_write_permission.txt'), 'w') as f:
            f.write('Teste de permissão de escrita.')

        # Remove o arquivo de teste
        os.remove(os.path.join(caminho, 'test_write_permission.txt'))

        return True
    except PermissionError:
        return False

def criar_arquivo_banco_usuarios():
    try:
        # Cria o diretório se não existir
        
        os.makedirs(caminho_banco_usuarios, exist_ok=True)

        # Verifica se o arquivo users.txt já existe
        path_arquivo = os.path.join(caminho_banco_usuarios, 'users.txt')
        if os.path.exists(path_arquivo):
            print("O arquivo de banco de usuarios já existe.")
        else:
            # Cria o arquivo users.txt se não existir
            with open(path_arquivo, 'w') as arquivo:
                arquivo.write("# Arquivo de banco de usuários\n")
            print("Arquivo de banco de usuários criado com sucesso.")

        return True
    except Exception as e:
        print(f"Erro ao criar o arquivo de banco de usuários: {str(e)}")
        return False

#VERIFICANDO SE PODEMOS CRIAR A PASTA DO ARQUIVO
if verificar_permissao_pasta(caminho_banco_usuarios):
    print("Permissões e arquivo de banco de usuários verificados com sucesso.")
else:
    print("Erro ao verificar permissões ou arquivo de banco de usuários.")
#VERIFICANDO SE PODEMOS CRIAR O ARQUIVO DO BANCO
if criar_arquivo_banco_usuarios():
    print("Criação do arquivo de banco de usuários verificada com sucesso.")
else:
    print("Erro ao criar o arquivo de banco de usuários.")
