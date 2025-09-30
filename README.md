# Projeto MyRoute: Pipeline de Análise Preditiva de Clientes


Challenge do 1º ano de Data Science da FIAP (2025).

**Pitch: https://youtu.be/TdB3HnSVtTo?si=lMwTma2FNwLRVLWz**


## Sobre o Projeto

Este projeto implementa um pipeline de dados ponta-a-ponta que coleta, processa e analisa o histórico de viagens de clientes do projeto "MyRoute". O objetivo é segmentar os clientes, criar um score de fidelidade e prever suas próximas compras, gerando insights valiosos para a tomada de decisão.

A solução é totalmente automatizada utilizando Apache Airflow e containerizada com Docker, garantindo reprodutibilidade e escalabilidade.

---

## Arquitetura da Solução

O pipeline foi construído com as seguintes tecnologias:

* **Orquestração:** Apache Airflow para agendamento e execução das tarefas.
* **Banco de Dados:** Oracle Cloud como Data Warehouse para armazenar os dados processados e os scores dos clientes.
* **Containerização:** Docker e Docker Compose para criar um ambiente de desenvolvimento e produção isolado e consistente.
* **Data Viz:** Microsoft Power BI para criação de dashboards interativos e visualização dos resultados.
* **Linguagem:** Python para os scripts de extração, transformação e carga (ETL).

---

## Como Executar o Pipeline

### Pré-requisitos
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado e em execução na sua máquina.

### Passos para Execução

1.  **Clonar o Repositório**
    ```bash
    git clone https://github.com/Karen-Akemi/Challenge2025.git
    cd Challenge2025
    ```

2.  **Construir e Iniciar os Containers**
    Abra um terminal na pasta raiz do projeto e execute o comando abaixo. Ele irá construir a imagem Docker e iniciar todos os serviços necessários (Airflow, Postgres, etc.).
    ```bash
    docker-compose up -d --build
    ```

3.  **Acessar a Interface do Airflow**
    Aguarde cerca de 2-3 minutos para que os serviços sejam inicializados.
    * Acesse a interface web em: **http://localhost:8080**
    * **Login:** `airflow`
    * **Senha:** `airflow`

4.  **Executar a DAG**
    Na lista de DAGs, encontre a DAG `pipeline_myroute_analysis`, ative-a no botão de toggle e dispare uma execução manual clicando no ícone "Play" (▶️). Acompanhe a execução até que todas as tarefas fiquem verdes.

---

## Resultados

Os resultados da análise, a segmentação de clientes e os scores de fidelidade podem ser visualizados no Power BI.

**[Acesse os resultados aqui](https://app.powerbi.com/links/wkuYCZ7CaW?ctid=11dbbfe2-89b8-4549-be10-cec364e59551&pbi_source=linkShare)**

---

## Apresentação do Projeto

A apresentação completa do projeto, incluindo a metodologia, desafios e resultados, está disponível abaixo:

**[Clique para ver a apresentação da banca](https://www.canva.com/design/DAGzPJVlOF4/mmSzNGPDoxVU9IOI4e_8Jg/edit?utm_content=DAGzPJVlOF4&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)**

---

## Fontes e Dados

* **Fonte de Dados:** O dataset `dataset_traduzido.csv` contém um histórico fictício de viagens e foi fornecido como parte do desafio da FIAP.

---

## Como Parar o Ambiente

Para interromper todos os containers em execução, utilize o seguinte comando no terminal, na pasta raiz do projeto:

```bash
docker-compose down
