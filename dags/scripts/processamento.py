# script processamento.py

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.dialects import oracle
from datetime import datetime, timedelta

def classificar_cliente(df_cliente):
    meses_unicos = df_cliente['data_compra'].dt.month.nunique()
    if meses_unicos > 1:
        return 'Explorador'
    return 'Conservador'

def calcular_score_e_mensagem(row):
    if row['CLASSIFICACAO'] == 'Explorador':
        score = int(row['GASTO_TOTAL'] / 20)
        mensagem = f"Viajante {row['CLASSIFICACAO']}! Compre uma passagem de até R$ 45,00 e ganhe 10 pontos."
    else:
        score = row['TOTAL_VIAGENS'] * 5
        mensagem = f"Viajante {row['CLASSIFICACAO']}! Compre uma passagem nos próximos 2 dias e ganhe 10 pontos."
    return min(score, 100), mensagem

def definir_nivel_score(score):
    """Define o nível (Bronze, Prata, Ouro) com base no score."""
    if score <= 35:
        return 'Bronze'
    elif score <= 65:
        return 'Prata'
    else:
        return 'Ouro'

def rodar_processamento():
    print("Iniciando processamento com conexão direta...")

    db_user = "rm562733"
    db_password = "240505"
    db_dsn = "oracle.fiap.com.br:1521/ORCL"

    try:
        engine = create_engine(f'oracle+oracledb://{db_user}:{db_password}@{db_dsn}')
        print("Conexão com o Oracle Cloud bem-sucedida!")
    except Exception as e:
        print(f"Erro ao conectar com o Oracle: {e}")
        return

    # 1. Leitura dos dados da tabela VIAGENS
    df = pd.read_sql("SELECT ID_CLIENTE, DATA_COMPRA, ORIGEM, DESTINO, VALOR_COMPRA FROM VIAGENS", engine)
    df['data_compra'] = pd.to_datetime(df['data_compra'])

    # 2. Classificação dos clientes
    classificacao = df.groupby('id_cliente').apply(classificar_cliente).rename('CLASSIFICACAO').reset_index()
    print("Classificação de clientes concluída.")

    # 3. Agregação para criar perfis
    perfis = df.groupby('id_cliente').agg(
        TOTAL_VIAGENS=('id_cliente', 'size'),
        GASTO_TOTAL=('valor_compra', 'sum'),
        DATA_ULTIMA_COMPRA=('data_compra', 'max')
    ).reset_index()
    perfis = pd.merge(perfis, classificacao, on='id_cliente')
    print("Criação de perfis concluída.")

    # 4. Cálculo de Score, Nível e Mensagens Personalizadas
    perfis[['SCORE', 'MENSAGEM_PERSONALIZADA']] = perfis.apply(calcular_score_e_mensagem, axis=1, result_type='expand')
    perfis['NIVEL_SCORE'] = perfis['SCORE'].apply(definir_nivel_score)
    
    # 5. Cálculo de Validade dos Pontos
    perfis['PONTOS_EXPIRAM_EM'] = perfis['DATA_ULTIMA_COMPRA'] + pd.DateOffset(months=6)
    perfis['PONTOS_EXPIRAM_BONUS_EM'] = perfis['DATA_ULTIMA_COMPRA'] + pd.DateOffset(months=3)
    print("Cálculo de score e validade dos pontos concluído.")

    # 6. Predição de Próximo Destino Provável
    prox_destino = df.groupby(['id_cliente', 'destino']).size().reset_index(name='contagem')
    prox_destino = prox_destino.loc[prox_destino.groupby('id_cliente')['contagem'].idxmax()]
    prox_destino = prox_destino[['id_cliente', 'destino']].rename(columns={'destino': 'PROXIMO_DESTINO_PROVAVEL'})
    print("Predição de próximos destinos gerada.")
    
    # 7. Geração de Predições de Compra Futura
    df = df.sort_values(by=['id_cliente', 'data_compra'])
    df['diferenca_dias'] = df.groupby('id_cliente')['data_compra'].diff().dt.days
    media_dias = df.groupby('id_cliente')['diferenca_dias'].mean().fillna(90).round(0)
    
    predicoes_df = pd.merge(perfis[['id_cliente', 'DATA_ULTIMA_COMPRA']], media_dias.reset_index(), on='id_cliente')
    predicoes_df.rename(columns={'diferenca_dias': 'DIAS_ATE_PROXIMA_VIAGEM'}, inplace=True)
    
    predicoes_df['PROXIMA_DATA_PROVAVEL_COMPRA'] = predicoes_df.apply(
        lambda row: row['DATA_ULTIMA_COMPRA'] + timedelta(days=row['DIAS_ATE_PROXIMA_VIAGEM']), axis=1
    )
    
    predicoes_df['JANELA_VIAGEM_7_A_30_DIAS'] = np.where(
        (predicoes_df['DIAS_ATE_PROXIMA_VIAGEM'] >= 7) & (predicoes_df['DIAS_ATE_PROXIMA_VIAGEM'] <= 30),
        'sim',
        'nao'
    )
    print("Geração de predições de compra futura concluída.")

    # 8. Juntar e Salvar os dados
    predicoes_para_salvar = predicoes_df[['id_cliente', 'PROXIMA_DATA_PROVAVEL_COMPRA', 'DIAS_ATE_PROXIMA_VIAGEM', 'JANELA_VIAGEM_7_A_30_DIAS']]
    predicoes_final = pd.merge(predicoes_para_salvar, prox_destino, on='id_cliente')
    
    ordem_perfis = ['CLASSIFICACAO', 'SCORE', 'NIVEL_SCORE', 'MENSAGEM_PERSONALIZADA', 'TOTAL_VIAGENS', 
                    'GASTO_TOTAL', 'DATA_ULTIMA_COMPRA', 'PONTOS_EXPIRAM_EM', 'PONTOS_EXPIRAM_BONUS_EM']
    perfis = perfis.set_index('id_cliente')[ordem_perfis]

    predicoes_final.set_index('id_cliente', inplace=True)

    dtype_perfis = {
        'GASTO_TOTAL': oracle.NUMBER(12, 2),
        'SCORE': oracle.NUMBER,
        'TOTAL_VIAGENS': oracle.NUMBER
    }
    dtype_predicoes = {
        'DIAS_ATE_PROXIMA_VIAGEM': oracle.NUMBER
    }

    perfis.to_sql('perfis_clientes', engine, if_exists='replace', index=True, index_label='ID_CLIENTE', dtype=dtype_perfis)
    predicoes_final.to_sql('predicoes_viagens', engine, if_exists='replace', index=True, index_label='ID_CLIENTE', dtype=dtype_predicoes)

    print("Processamento concluído! Tabelas 'perfis_clientes' e 'predicoes_viagens' foram salvas/atualizadas no Oracle.")

if __name__ == "__main__":
    rodar_processamento()