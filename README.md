# Projeto Interpolating

Projeto desenvolvido para o evento [DATA Day](https://www.icmc.usp.br/noticias/4730-data-day-evento-na-usp-discute-presente-e-futuro-da-area-de-ciencia-de-dados) ocorrido no dia 30/11/2019 e promovido pelo grupo DATA. 
O principal objetivo do projeto era o de trazer à tona a existência das GAN's (Generative Adversarial Networks) e discutir seu funcionamento e possíveis aplicações.
Com essa finalidade, foi desenvolvido um website que permitiu aos participantes interagirem pessoalmente com a StyleGAN, uma arquitetura de última geração desenvolvida pela NVIDIA em 2019.

![](resources/demo_interpolation_gif.gif)

## Organização do projeto

    ├── LICENSE
    ├── README.md                   <- informações gerais acerca do projeto.
    ├── notebooks                   <- notebooks python utilizados no projeto.
    │   ├── gerar_instancia.ipynb   <- notebook utilizados para configurar a aplicação server-side.
    ├── src                         <- códigos fontes utilizados no projeto client-side.
    │   ├── manage.py               <- script python utilizado pelo django para iniciar o projeto na máquina.
    │   ├── www_interpolar          <- pasta padrão utilizada pelo django para configurar o projeto.
    │   ├── scripts                 <- scripts python que serão utilizados no server-side em conjunto com o notebook.
    │   │   ├── proccess.py         <- script responsável por realizar as interpolações nas imagens.
    │   │   ├── check.py            <- verifica se há alguma instância de proccess.py sendo executada no momento.
    │   ├── website                 <- pasta padrão utilizada pelo django para configurar o projeto. 
    │   │   ├── urls.py             <- realiza o mapeamento das rotas com suas devidas views.
    │   │   ├── views.py            <- responsável por receber e executar as requisições do website.
    │   │   ├── forms.py            <- define para o django quais são os formulários existentes no website.
    │   │   ├── models.py           <- implementa todas as rotinas e funções utilizadas pelo website.
    │   │   ├── templates           <- templates html utilizados pelo website.
    │   │   ├── nao_processadas     <- diretório utilizado para salvar as imagens na fila para serem processadas pela GAN.
    │   │   ├── processadas         <- diretório utilizado para salvar as imagens já processadas pela GAN.
    │   │   ├── static              <- recursos utilizados pelo website como CSS, Javascripts e imagens
    │   │   │   ├── interpolacoes   <- diretório utilizado para salvar os resultados das imagens processadas pela GAN.

##  Requisitos e dependências

A versão do python e também de todas as dependências utilizadas no projeto podem ser encontradas no arquivo *environment.yml*. 
Para a execução da GAN localmente é necessário a utilização do CUDA e do TensorFlow nas versões especificadas no notebook *gerar_instancia.ipynb*.

## Rodando o projeto

O projeto desenvolvido é dividido em duas frentes distintas para que possa funcionar. Sendo elas:

 - **Front-side:** Responsável pela execução do website; captação de imagens para serem processadas; funções iterativas para o usuário final.
 - **Server-side:** Responsável pela execução dos scripts de processamento. Deve possuir uma GPU que comporte a execução da StyleGAN.

 O Website foi desenvolvido em  django e basta, portanto, baixar os arquivos da pasta */src* em um diretório local e executar o seguinte comando via terminal:

    $ python manage.py runserver 0.0.0.0:8000

Já quanto ao servidor, recomendamos que se siga as instruções passo a passo do notebook em uma instância do Google Collab. Uma vez compreendido quais arquivos são utilizados no mesmo é possível reproduzir a arquitetura utilizada em qualquer serviço de nuvem (ou localmente) que possua os pré-requisitos necessários.

## Autores 

Cézanne Alves, Gabriel Van Loon, Gustavo Soares e Victor Henrique Rodrigues.
