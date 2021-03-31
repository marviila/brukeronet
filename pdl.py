import pandas as pd
import csv
import datetime as dt

df = pd.read_csv(r"bruker_crush_historical_data_pdl_test.csv", delimiter='|', low_memory=False)
df = pd.DataFrame(df)
plant_name = "Primavera do Leste"

dict_columns = {
 'timestamp_fibra_farelo': 'fibra_farelo',
 'timestamp_granulometria_farelo': 'granulometria_farelo',
 'timestamp_oleo_farelo' : 'oleo_farelo',
 'timestamp_oleo_soja' : 'oleo_soja',
 'timestamp_proteina_farelo' : 'proteina_farelo',
 'timestamp_proteina_soja' : 'proteina_soja',
 'timestamp_solubilidade_farelo' : 'solubilidade_farelo',
 'timestamp_umidade_farelo': 'umidade_farelo',
 'timestamp_umidade_quebrados': 'umidade_quebrados',
 'timestamp_umidade_saida_VSC' : 'umidade_saida_VSC',
 'timestamp_umidade_soja' : 'umidade_soja',
 'timestamp_farelo_branco' : 'farelo_branco',
 'timestamp_umidade_farelo_dt' : 'umidade_farelo_dt',
 'timestamp_umidade_farelo_secador' : 'umidade_farelo_secador',
 'timestamp_casca_embarque' : 'casca_embarque',
 'timestamp_oleo_casca_dehulling' : 'oleo_casca_dehulling',
 'timestamp_oleo_casca_pellet' :  'oleo_casca_pellet'
}

result_df = pd.DataFrame()

for dfs in dict_columns:
    timestamp_column = dfs
    measurement_column = dict_columns[dfs]
    df2 = df[[timestamp_column, measurement_column]]
    df2 = df2.rename(columns={timestamp_column: "timestamp"})
    df3 = df2.melt(id_vars="timestamp", var_name="measurement_desc", value_name="pi_value1")
    result_df = pd.concat([result_df, df3], axis=0)

result_df = result_df.dropna()
result_df = result_df.drop_duplicates()
result_df['pi_value1'] = result_df['pi_value1'].astype(str).str.replace(',','.')
result_df['timestamp'] = pd.to_datetime(result_df['timestamp'], format='%d/%m/%Y %H:%M')
result_df['timestamp'] = result_df['timestamp'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
result_df = result_df.drop(result_df[result_df.pi_value1 == "Pt Created"].index)
result_df['plant_name'] = plant_name


result_df.to_csv("", sep='\t', index=False)

#print(result_df.timestamp.head(20))