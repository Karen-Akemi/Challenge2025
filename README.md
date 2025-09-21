# Challenge2025
Arquivos do projeto MyRoute. para o Challenge do 1º ano de Data Science da FIAP

# Projeto MyRoute: Pipeline de Análise Preditiva de Clientes

Este projeto implementa um pipeline de dados automatizado que analisa o histórico de viagens para segmentar clientes, criar um score de fidelidade e prever as próximas compras.

**Arquitetura:** Python, Oracle Cloud, Docker e Apache Airflow.

---

### Pré-requisitos

* **Docker Desktop** instalado e em execução.

---

### Como Executar o Pipeline

**1. Baixar o Projeto**
   * Faça o download deste repositório para a sua máquina.

**2. Construir e Iniciar o Ambiente**
   * Abra um terminal na pasta raiz do projeto.
   * Execute o seguinte comando. Ele irá construir a imagem Docker e iniciar todos os serviços (Airflow, Postgres, etc.):
     ```bash
     docker-compose up -d --build
     ```

**5. Executar o Pipeline no Airflow**
   * Aguarde 2-3 minutos para que os serviços inicializem.
   * Acesse a interface do Airflow em [http://localhost:8080](http://localhost:8080).
     * **Login:** `airflow`
     * **Senha:** `airflow`
   * Na lista de DAGs, encontre `pipeline_clickbus_dataset_final`, ative-a e dispare uma execução manual clicando no botão "Play" (▶️).
   * Acompanhe a execução. Quando as tarefas ficarem verdes, o processo foi concluído com sucesso.

**6. Verificar os Resultados**
   * Usando PowerBI é possível visualizar os resultos por meio de gráficos e dashboards.

**7. Para interromper o docker-compose**
   * No terminal, onde está sendo executado o docker-compose.
   * Execute o seguinte comando:
     ```bash
     docker-compose down
     ```
