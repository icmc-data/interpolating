import os, shutil, paramiko, time
from PIL import Image
from django.db import models

'''
CONFIGURAÇÔES NGROK

A fim de utilizar o NGROK para envio de comandos via Paramiko, configure
abaixo as variáveis utilizadas para a conexão SSH.
'''
NGROK_PORT        =  111111
NGROK_PASS        = 'INSIRA_SUA_SENHA'
NGROK_TCP_ADDR    = '0.tcp.ngrok.io'


'''
PASTAS DE IMAGENS

Variáveis utilizadas para acessar as três pastas utilizadas pelo website.
'''
PROJECT_DIR           = os.path.dirname(os.path.abspath(__file__))
NAO_PROCESSADOS_DIR   = PROJECT_DIR + '\\nao_processadas'
PROCESSADOS_DIR       = PROJECT_DIR + '\\processadas'
INTERPOLACOES_DIR     = PROJECT_DIR + '\\static\\interpolacoes'


# Função responsável pelo carregamento da imagem
def processar_imagem(f):
    '''
    Recebe uma imagem enviada pelo usuário, define para ela um número de
    identificação (id) e a salva no diretório NAO_PROCESSADOS.
    Obs.: Converte a imagem para PNG caso não seja.
    '''

    print('Iniciando processamento da imagem...', f.name)
    next_id = '10000'

    # Recuperando o proximo id
    if os.path.isfile(INTERPOLACOES_DIR+'\\_next_id_.txt'):
        id_file = open(INTERPOLACOES_DIR+'\\_next_id_.txt', 'r')
        next_id = id_file.readline()
        id_file.close()

    # Verificando se o id já não está sendo utilizado
    while os.path.isdir(INTERPOLACOES_DIR + '\\' + next_id ) or os.path.isdir(NAO_PROCESSADOS_DIR + '\\' + next_id):
        next_id = str(int(next_id)+1)

    # Criando o novo diretorio de imagems
    image_dir = NAO_PROCESSADOS_DIR

    # Pegando a extensao da imagem
    image_ext = f.name.split('.')[1]

    # Salvando a imagem com o id
    destination =  open( '{}\\{}.{}'.format(image_dir, next_id, image_ext), 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

    # Caso a imagem não seja png altera ela para PNG
    if image_ext != 'png':
        im = Image.open('{}\\{}.{}'.format(image_dir, next_id, image_ext))
        im.save( '{}\\{}.png'.format(image_dir, next_id) )
        im.close()
        os.remove( '{}\\{}.{}'.format(image_dir, next_id, image_ext) )

    # Incrementando o id
    id_file = open(INTERPOLACOES_DIR + '\\_next_id_.txt', 'w')
    id_file.write('{}'.format(int(next_id)+1))
    id_file.close()

    return next_id

def verificar_imagem(image_id):
    '''
    Verifica se a imagem de id @image_id já foi processada e se encontra 
    na pasta INTERPOLACOES_DIR.
    '''

    print("Verificando imagem de id nº{}".format(image_id))
    image_id  = str(image_id)
    image_dir = INTERPOLACOES_DIR + '\\' + image_id

    # Verificando se a imagem existe
    if not os.path.isdir(image_dir):
        return False
    elif not os.path.isfile(image_dir + '\\{}_original.png'.format(image_id)):
        return False

    #Verificando quais categorias foram computadas
    #categories = ['age', 'gender', 'smile', 'glasses']
    #categories = [c for c in categories if os.path.isdir(image_dir + '\\' + c)]
    #print('Categorias existentes... {}'.format(categories))
    return True

def listar_imagems(famosos=False):
    '''
    Retorna uma lista com todas as imagens já processadas que sem encontram
    na pasta PROCESSADOS_DIR. A flag @famosos é utilizada para diferenciar os
    resultados que devem ser retornados na view /list da view /examples.
    '''

    paths = []
    dirs  = [x[1] for x in os.walk(INTERPOLACOES_DIR)][0]
    dirs.reverse()

    print(dirs)

    print('Diretórios descobertos:', dirs)
    for d in dirs:
        ehFamoso = os.path.isfile('{}\\{}\\famoso.txt'.format(INTERPOLACOES_DIR,d))
        print('Imagem nº', d, 'Famoso?', ehFamoso)
        if verificar_imagem(d) and (famosos == ehFamoso ):
            paths.append({
                'path':'/static/interpolacoes/{}/{}.png'.format(d,d), 
                'id':d
            })
        
    print('Paths descobertos:', paths)
    return paths

def carregar_paths(image_id):
    '''
    Carrega um dicionário com o path das interpolações realizadas para determinada
    imagem. Seu objetivo é servir os paths para serem utilizado pela view /play
    '''
    paths = {}
    image_id  = str(image_id)
    image_dir = INTERPOLACOES_DIR + '\\' + image_id
    
    # Carregando a imagem original e latente
    if not os.path.isfile(image_dir + '\\{}_original.png'.format(image_id)):
        return False
    elif not os.path.isfile(image_dir + '\\{}_latent.png'.format(image_id)):
        return False

    paths['original'] = '/static/interpolacoes/{}/{}_original.png'.format(image_id, image_id)
    paths['latent']   = '/static/interpolacoes/{}/{}_latent.png'.format(image_id, image_id)

    # Carregando o path dos resultados
    paths['results'] = {}

    # Verificando quais resultados foram gerados
    categories = ['age', 'gender', 'smile', 'eyeglasses', 'pose']
    categories = [c for c in categories if os.path.isdir(image_dir + '\\' + c)]

    for c in categories:
        paths['results'][c] = []

        for r, d, f in os.walk('{}/{}'.format(image_dir,c)):
            for fname in f:
                paths['results'][c].append( '/static/interpolacoes/{}/{}/{}'.format(image_id, c, fname ) )
        #for i in range(0,48):
            #paths['results'][c].append( '/static/interpolacoes/{}/{}/000_{}.jpg'.format(image_id, c, str(i).zfill(3) ) )

    return paths

def buscar_dados_processamento():
    '''
    Realiza uma contagem de quantas imagens já foram processadas e quantos ainda
    estão na fila para serem processadas. Também pode realizar chamada à check.py 
    por meio do Paramiko.
    '''

    dados = {'nao_processados': 0, 'processados': 0, 'finalizados': 0, 'status': 'error' }

    if os.path.isdir(NAO_PROCESSADOS_DIR):
        dados['nao_processados'] = len(os.listdir(NAO_PROCESSADOS_DIR))

    if os.path.isdir(PROCESSADOS_DIR):
        dados['processados'] = len(os.listdir(PROCESSADOS_DIR))

    if os.path.isdir(INTERPOLACOES_DIR):
        dados['finalizados'] = len(os.listdir(INTERPOLACOES_DIR))

    # Verificando check.py, descomente para fazer a chamada SSH.
    '''
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(NGROK_TCP_ADDR, port=NGROK_PORT, username='root', password=NGROK_PASS)
    stdin, stdout, stderr = client.exec_command('cd /content; python3 check.py')

    time.sleep(2)
    aux = stdout.readlines()
    print('PARAMIKO Verificando Processo...', aux)
    print('PARAMIKO Verificando Erros...',  stderr.readlines())
    if isinstance(aux, list) and len(aux) != 0:
        dados['status'] = aux[0]
    else:
        dados['status'] = 'error'
    print('Status do servidos: {}'.format(dados['status']))

    client.close()
    '''
    return dados

# (Não utilizada) Movendo as imagens finalizadas para a pasta de interpolações
def mover_finalizadas():
    for f in os.listdir(PROCESSADOS_DIR):
        shutil.move('{}\\{}'.format(PROCESSADOS_DIR, f), INTERPOLACOES_DIR)

def ssh_processar_imagens():
    '''
    Realiza uma chamada SSH via Paramiko a fim de invocar o script proccess.py.
    '''

    print("PARAMIKO: Chamada para  o processamento das imagens...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('0.tcp.ngrok.io', port=NGROK_PORT, username='root', password=NGROK_PASS)
    stdin, stdout, stderr = client.exec_command('cd /content; nohup python3 process.py /content/gdrive/My\ Drive/dataday/dataday_interpolar/website/nao_processadas /content/gdrive/My\ Drive/dataday/dataday_interpolar/website/static/interpolacoes /content/gdrive/My\ Drive/dataday/dataday_interpolar/website/processadas &')
    client.close()
    return True

# (Não utilizada) Manda o servidor processar uma imagem em especifico
def ssh_processar_id(image_id):
    # TODO: Chamada no Paramiko para fazer a execução de uma imagem especifica
    print("PARAMIKO: Chamada para  o processamento da imagem {}...".format(image_id))
    return True