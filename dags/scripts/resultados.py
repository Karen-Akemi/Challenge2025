import pandas as pd
import oracledb
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

# --- Configure suas credenciais do Oracle Cloud aqui ---
db_user = "rm562733"
db_password = "240505"
db_dsn = "oracle.fiap.com.br:1521/ORCL"
# ----------------------------------------------------

# --- Defina os clientes que você quer analisar ---
clientes_alvo = [126, 353]
# ----------------------------------------------------

print(f"Iniciando análise de perfil para os clientes: {clientes_alvo}...")

try:
    with oracledb.connect(user=db_user, password=db_password, dsn=db_dsn) as connection:
        print("Conexão com Oracle bem-sucedida!")
        
        df_perfis_total = pd.read_sql('SELECT * FROM "PERFIS_CLIENTES"', connection)
        df_viagens_total = pd.read_sql('SELECT ID_CLIENTE, DATA_COMPRA, VALOR_COMPRA FROM "VIAGENS"', connection)

        df_perfis = df_perfis_total[df_perfis_total['ID_CLIENTE'].isin(clientes_alvo)].set_index('ID_CLIENTE')
        df_viagens = df_viagens_total[df_viagens_total['ID_CLIENTE'].isin(clientes_alvo)]
        df_viagens['DATA_COMPRA'] = pd.to_datetime(df_viagens['DATA_COMPRA'])

        if df_perfis.empty:
            print("AVISO: Nenhum dos clientes alvo foi encontrado na tabela 'PERFIS_CLIENTES'.")
        else:
            # --- ANÁLISE E VISUALIZAÇÃO ---

            # Tabela de Resumo (sem alterações)
            print("\n" + "="*60)
            print("         FICHA DE PERFIL COMPARATIVA")
            print("="*60)
            colunas_resumo = ['CLASSIFICACAO', 'SCORE', 'NIVEL_SCORE', 'TOTAL_VIAGENS', 'GASTO_TOTAL']
            print(df_perfis[colunas_resumo])
            print("="*60 + "\n")

            # --- CORREÇÃO FINAL DAS CORES APLICADA AQUI ---
            
            # Criamos um mapa de cores para garantir que cada cliente tenha a cor certa em TODOS os gráficos
            cores_mapa = {126: 'blue', 353: 'red'}
            
            # 4. Gráfico de Barras Comparativo com cores por cliente
            fig, axes = plt.subplots(1, 3, figsize=(18, 6))
            fig.suptitle('Análise Comparativa de Clientes', fontsize=20)

            # Usamos a paleta do mapa de cores e o 'hue' para colorir por cliente
            sns.barplot(x=df_perfis.index, y=df_perfis['GASTO_TOTAL'], ax=axes[0], palette=cores_mapa, hue=df_perfis.index, legend=False)
            axes[0].set_title('Gasto Total (R$)')
            axes[0].set_xlabel('ID do Cliente')
            axes[0].set_ylabel('Valor (R$)')

            sns.barplot(x=df_perfis.index, y=df_perfis['TOTAL_VIAGENS'], ax=axes[1], palette=cores_mapa, hue=df_perfis.index, legend=False)
            axes[1].set_title('Total de Viagens')
            axes[1].set_xlabel('ID do Cliente')
            axes[1].set_ylabel('Quantidade')

            sns.barplot(x=df_perfis.index, y=df_perfis['SCORE'], ax=axes[2], palette=cores_mapa, hue=df_perfis.index, legend=False)
            axes[2].set_title('Score de Fidelidade')
            axes[2].set_xlabel('ID do Cliente')
            axes[2].set_ylabel('Pontos')

            plt.tight_layout(rect=[0, 0, 1, 0.96])
            plt.savefig('grafico_comparativo_clientes.png')
            print("Gráfico 'grafico_comparativo_clientes.png' gerado com sucesso!")

            # 5. Gerar Linha do Tempo de Compras (código já estava correto)
            plt.figure(figsize=(12, 6))
            sns.scatterplot(data=df_viagens, x='DATA_COMPRA', y='ID_CLIENTE', hue='ID_CLIENTE', s=150, palette=cores_mapa)
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=6))
            plt.title('Linha do Tempo de Compras', fontsize=16)
            plt.xlabel('Data da Compra', fontsize=12)
            plt.ylabel('ID do Cliente', fontsize=12)
            plt.yticks(clientes_alvo)
            plt.grid(axis='x', linestyle='--')
            plt.legend(title='Cliente')
            plt.savefig('grafico_timeline_clientes.png')
            print("Gráfico 'grafico_timeline_clientes.png' gerado com sucesso!")

except KeyError as e:
    print(f"\nOcorreu um erro de chave: a coluna {e} não foi encontrada.")
except Exception as e:
    print(f"\nOcorreu um erro: {e}")