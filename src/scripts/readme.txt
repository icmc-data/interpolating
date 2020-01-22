1- O arquivo de processar a pasta vai consumir todas as imagens da pasta da fila que já estiverem lá quando ele for invocado (se ele não travar). As que forem colocadas depois acho que ele não consome, mesmo se ele ainda estiver rodando quando elas forem colocadas. Ele já tá com a trava embutida, e se ele crashar a trava libera sozinha.

invoca com python3 pq a vm é ubuntu. (no colab "python" invoca o Python 3 mas no shell "python" invoca o Python 2. Pra invocar o Python 3 tem que ser "python3")

python3 process.py ....... >> out.log.txt 2>> err.log.txt

usage: process.py [-h] [--batch_fila BATCH_FILA] [--batch_net BATCH_NET]
                  fila interpolacoes bkp_fila

positional arguments:
  fila                  path para a fila (pasta) de imagens. Ou uma imagem
  interpolacoes         path para o diretorio do site com as interpolacoes a
                        serem exibidas
  bkp_fila              path para a pasta contendo a imagens da fila que jah
                        foram processadas

optional arguments:
  -h, --help            show this help message and exit
  --batch_fila BATCH_FILA
                        tamanho do batch da fila(qtd de imagens da fila a
                        serem processadas por vez
  --batch_net BATCH_NET
                        tamanho do batch da rede (qtd de imagens da fila a
                        serem processadas por vez
                       


                       
2 - Pra checar se está rodando (checa se a trava tá ativada) é só dar:

python3 check.py

ele retorna "processando" se estiver rodando, e "finalizado" caso contrário

ambos os scripts estão em My Drive/morph
q vai ser montado em /content/gdrive/My Drive/morph

3 - à medida que o script roda ele cria imagens numa pasta temporária na VM em /content/temp
a cada batch_fila as imagens de lá são movidas para a pasta destino (interpolacoes) e ele apaga a /content/temp




4 - O notebook de preparar a VM é aquele que vc compartilhou comigo "new_instance.ipynb"
A primeira vez que ele rodar ele vai só instalar o tf e o cuda e se reiniciar. Na segunda ele prepara o ngrock, ssh; muda pra pasta "...My Drive/morph" e prepara os arquivos do encoder e do interpolador


*** importante ****

assim que terminar de rodar o notebook da vm, rode o processo com uma única imagem de teste (pode ser feito pelo site msm deixando uma imagem só na fila). Por causa das coisas que ele faz na primeira vez que roda, o processo vai ser demorado na primeira vez e pode ser que dê pau ou que termine mas que deixe de interpolar algum atributo. Por isso, rode com uma única imagem de teste. Depois disso, as coisas que ele carregou vão ficar persistidas no google drive mesmo que a VM seja resetada.