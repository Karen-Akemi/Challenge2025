\# Projeto MyRoute: Pipeline de Análise Preditiva de Clientes



Challenge do 1º ano de Data Science da FIAP (2025).



\## Sobre o Projeto



Este projeto implementa um pipeline de dados ponta-a-ponta que coleta, processa e analisa o histórico de viagens de clientes da empresa fictícia "MyRoute". O objetivo é segmentar os clientes, criar um score de fidelidade e prever suas próximas compras, gerando insights valiosos para a tomada de decisão.



A solução é totalmente automatizada utilizando Apache Airflow e containerizada com Docker, garantindo reprodutibilidade e escalabilidade.



---



\## Arquitetura da Solução



O pipeline foi construído com as seguintes tecnologias:



\* \*\*Orquestração:\*\* Apache Airflow para agendamento e execução das tarefas.

\* \*\*Banco de Dados:\*\* Oracle Cloud como Data Warehouse para armazenar os dados processados e os scores dos clientes.

\* \*\*Containerização:\*\* Docker e Docker Compose para criar um ambiente de desenvolvimento e produção isolado e consistente.

\* \*\*Data Viz:\*\* Microsoft Power BI para visualização dos resultados.

\* \*\*Linguagem:\*\* Python para os scripts de extração, transformação e carga (ETL).



---



\## Como Executar o Pipeline



\### Pré-requisitos

\* \[Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado e em execução na sua máquina.



\### Passos para Execução



1\.  \*\*Clonar o Repositório\*\*

&nbsp;   ```bash

&nbsp;   git clone \[https://github.com/Karen-Akemi/Challenge2025.git](https://github.com/seu-usuario/seu-repositorio.git)

&nbsp;   cd seu-repositorio

&nbsp;   ```



2\.  \*\*Construir e Iniciar os Containers\*\*

&nbsp;   Abra um terminal na pasta raiz do projeto e execute o comando abaixo. Ele irá construir a imagem Docker e iniciar todos os serviços necessários (Airflow, Postgres, etc.).

&nbsp;   ```bash

&nbsp;   docker-compose up -d --build

&nbsp;   ```



3\.  \*\*Acessar a Interface do Airflow\*\*

&nbsp;   Aguarde cerca de 2-3 minutos para que os serviços sejam inicializados.

&nbsp;   \* Acesse a interface web em: \*\*http://localhost:8080\*\*

&nbsp;   \* \*\*Login:\*\* `airflow`

&nbsp;   \* \*\*Senha:\*\* `airflow`



4\.  \*\*Executar a DAG\*\*

&nbsp;   Na lista de DAGs, encontre a DAG `pipeline\_myroute\_analysis`, ative-a no botão de toggle e dispare uma execução manual clicando no ícone "Play" (▶️). Acompanhe a execução até que todas as tarefas fiquem verdes.



---



\## Resultados e Dashboard



Os resultados da análise, a segmentação de clientes e os scores de fidelidade podem ser visualizados no Power BI.



&nbsp;\*\*\[Acesse os gráficos aqui](https://app.powerbi.com/links/wkuYCZ7CaW?ctid=11dbbfe2-89b8-4549-be10-cec364e59551\&pbi\_source=linkShare)\*\*



---



\## Apresentação do Projeto



A apresentação completa do projeto está disponível abaixo:



&nbsp;\*\*\[Clique para ver a apresentação da banca (PDF)]("C:\\Users\\karen\\OneDrive\\Documentos\\Faculdade\\Challege\\sprint4\\EC\_sprint4\_1TSCPF\_solucaofinal\_MyRoute.\_TALK\\EC\_sprint4\_1TSCPF\_solucaofinal\_MyRoute.\_TALK.pdf")\*\*



---



\## Fontes e Dados



\* \*\*Fonte de Dados:\*\* O dataset `dataset\_traduzido.csv` contém um histórico fictício de viagens e foi fornecido como parte do desafio da FIAP.



---



\## Como Parar o Ambiente



Para interromper todos os containers em execução, utilize o seguinte comando no terminal, na pasta raiz do projeto:



```bash

docker-compose down

