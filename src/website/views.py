from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import PictureForm, PlayForm, MoveForm, ProccessForm, ID_ProccessForm
from .models import processar_imagem, verificar_imagem, listar_imagems, carregar_paths
from .models import buscar_dados_processamento, mover_finalizadas, ssh_processar_id, ssh_processar_imagens


'''
A fim de permitir que apenas os membros do grupo estejam habilitados a
enviar requisições para o website, um token de segurança é utilizado em
todos os formulários do website.
Portanto, é necessário definir abaixo uma string que servirá como tal token.
'''
TOKEN_ADMIN = 'INSIRA_TOKEN_SEGURANCA' 

def homepage(request):
    '''
    (Não finalizada)
    Página com descrição básica acerca do projeto, com foto dos membros e uma
    breve explicação acerca do que está sendo feito.
    '''
    return render(request, 'homepage.html', {} )


def picture(request):
    '''
    Página responsável por enviar fotos dos participantes da amostra que
    estiverem interessados em testar as modificações da StyleGAN.
    '''

    form_result = 'none'
    image_id    = '0'

    print('Requisicao: ', request)
    if request.method == 'POST':
        form = PictureForm(request.POST, request.FILES)
        if form.is_valid() and form.cleaned_data['auth_token'] == TOKEN_ADMIN:
            image_id    = processar_imagem(request.FILES['photo'])
            form_result = 'success'
        else:
            print(form.errors)
            print(form.non_field_errors)
            form_result = 'error'

    return render(request, 'picture.html', { 'form_result':form_result,  'image_id':image_id })

def list(request):
    '''
    Exibe na tela todas as imagens processadas que foram recebidas
    pela view /picture.
    '''
    paths = listar_imagems(famosos=False)
    return render(request, 'list.html', {'paths':paths} )

def examples(request):
    '''
    Possui o mesmo layout da view /list. No entanto exibe uma série
    de imagens de famosos pré-selecionados antes da amostra.
    '''
    paths = listar_imagems(famosos=True)
    return render(request, 'list.html', {'paths':paths} )

def play(request):
    '''
    Exibe as interpolações do resultado selecionado por meio de uma
    interface simples e amigável para que o usuário possa interagir
    com os resultados.
    '''
    image_id = 0
    paths    = {}

    if request.method == 'GET':
        form = PlayForm(request.GET)
        if form.is_valid() and verificar_imagem(form.cleaned_data['id']):
            image_id = form.cleaned_data['id']
            paths    = carregar_paths(image_id) 

    return render(request, 'play.html', { 'image_id':image_id, 'paths':paths } )

def settings(request):
    '''
    Exibe algumas informações acerca de quantas imagens já foram processadas e também
    permite solicitar a execução de scripts para o servidor. Uso para fins exclusivos de controle.
    '''
    if request.method == 'POST':
        form = MoveForm(request.POST)
        if form.is_valid() and form.cleaned_data['auth_token'] == TOKEN_ADMIN:
            mover_finalizadas()

        form2 = ProccessForm(request.POST)
        if form2.is_valid() and form2.cleaned_data['auth_token'] == TOKEN_ADMIN:
            ssh_processar_imagens()

        form3 = ID_ProccessForm(request.POST)
        if form3.is_valid() and form3.cleaned_data['auth_token'] == TOKEN_ADMIN:
            ssh_processar_id( form3.cleaned_data['imagem_id'] )

    # mover_finalizadas()
    dados = buscar_dados_processamento()
    return render(request, 'settings.html', {'dados':dados} )