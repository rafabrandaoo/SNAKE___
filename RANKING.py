def arquivoExiste(nome):
    try:
        a = open(nome, 'rt')
        a.close()
    except FileNotFoundError:
        return False
    except Exception as erro:
        print(f'{erro.__class__}')
    else:
        return True

def criararquivo(nome):
    try:
        a = open(nome, 'wt+')
        a.close()
    except:
        print('Houve um erro para criar o arquivo')

def lerarquivos(nome):
    try:
        a = open(nome, 'rt')
    except:
        print('Não possivel ler o arquivo')
    else:
        for linha in a:
            dado = linha.split(';')
            dado[1] = dado[1].replace('\n', '')
            print(f'{dado[0].upper():<40}{dado[1]:>3} pontos')

    finally:
        a.close()

def cadastrar(arq, nome = 'desconhecido', pontuacao = 0):
    try:
        a = open(arq, 'at')
    except:
        print('Erro na abertura do arquivo')
    else:
        try:
            a.write(f'{nome};{pontuacao}\n')
        except:
            print('Houve um erro na hora do cadastro0')
        else:
            a.close()
