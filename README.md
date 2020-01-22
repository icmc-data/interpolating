# Projeto Interpolating

Projeto desenvolvido para o evento [DATA Day](https://www.icmc.usp.br/noticias/4730-data-day-evento-na-usp-discute-presente-e-futuro-da-area-de-ciencia-de-dados) ocorrido no dia 30/11/2019 e promovido pelo grupo DATA. 
O principal objetivo do projeto era o de trazer à tona a existência das GAN's (Generative Adversarial Networks) e discutir seu funcionamento e possíveis aplicações.
Com essa finalidade, foi desenvolvido um website que permitiu aos participantes interagirem pessoalmente com a StyleGAN, uma arquitetura de última geração desenvolvida pela NVIDIA em 2019.

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

 
