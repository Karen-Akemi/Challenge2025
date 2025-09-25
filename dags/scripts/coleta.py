# script coleta.py

import random
from datetime import datetime, timedelta
import pandas as pd
import oracledb

def gerar_data_aleatoria(start_date, end_date):
    time_between_dates = end_date - start_date
    seconds_between_dates = time_between_dates.total_seconds()
    random_number_of_seconds = random.randrange(int(seconds_between_dates))
    random_date = start_date + timedelta(seconds=random_number_of_seconds)
    return random_date.strftime('%Y-%m-%d')

def rodar_coleta():
    print("Iniciando simulação de coleta com análise de padrão...")

    db_user = "rm562733"
    db_password = "240505"
    db_dsn = "oracle.fiap.com.br:1521/ORCL"

    try:
        with oracledb.connect(user=db_user, password=db_password, dsn=db_dsn) as connection:
            print("Conexão para coleta bem-sucedida!")

            sql_query = 'SELECT ID_CLIENTE, ORIGEM, DESTINO, EMPRESA_ONIBUS, DATA_COMPRA FROM "VIAGENS"'
            df_base = pd.read_sql(sql_query, connection, parse_dates=['DATA_COMPRA'])

            if df_base.empty:
                print("Tabela VIAGENS está vazia. Não é possível simular uma nova compra.")
                return

            cliente_id = random.choice(df_base['ID_CLIENTE'].unique())
            
            df_cliente = df_base[df_base['ID_CLIENTE'] == cliente_id]
            
            if len(df_cliente) > 2:
                print(f"Cliente {cliente_id} tem histórico ({len(df_cliente)} viagens). Analisando padrão...")
                destino = df_cliente['DESTINO'].mode()[0]
                origem = random.choice(df_cliente['ORIGEM'].unique())
                print(f"Padrão identificado: Destino mais provável é '{destino}'.")
            else:
                print(f"Cliente {cliente_id} não tem histórico suficiente ({len(df_cliente)} viagens). Gerando destino aleatório.")
                origem, destino = random.choice(list(zip(df_base['ORIGEM'], df_base['DESTINO'])))
            
            empresa = random.choice(df_base['EMPRESA_ONIBUS'].unique())
            valor = round(random.uniform(90.0, 350.0), 2)
            
            end_date = datetime.now()
            start_date = end_date - timedelta(days=730)
            data_compra = gerar_data_aleatoria(start_date, end_date)
            
            print(f"Dados da nova compra: Data: {data_compra}, Valor: {valor}, Origem: {origem}, Destino: {destino}")

            sql_insert = f"""
            INSERT INTO "VIAGENS" (ID_CLIENTE, DATA_COMPRA, VALOR_COMPRA, ORIGEM, DESTINO, EMPRESA_ONIBUS)
            VALUES (
                {cliente_id},
                TO_DATE('{data_compra}', 'YYYY-MM-DD'),
                {valor},
                '{origem.replace("'", "''")}',
                '{destino.replace("'", "''")}',
                '{empresa.replace("'", "''")}'
            )
            """

            with connection.cursor() as cursor:
                cursor.execute(sql_insert)
                connection.commit()

            print(f"Nova compra inserida para o cliente {cliente_id}: {origem} -> {destino}")

    except Exception as e:
        print(f"Erro durante a coleta: {e}")
        return

if __name__ == "__main__":
    rodar_coleta()