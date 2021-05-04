import pandas as pd
import datetime as dt
import re


# Please, use the file data availabe by PDL team.

df = pd.read_csv(r"Novos_dados_qualidade.csv", delimiter=";", low_memory=False)

df = pd.DataFrame(df)

colunas = {'acidez_day_tank', 'clorofila',
           'degomagem_enzimatica_sabao_ika','degomagem_enzimatica_spin_test',
           'clarificacao_cor_vermelha','clarificacao_clorofila',
           'desodorizacao_acidez','desodorizacao_sabao',
           'desodorizacao_clorofila','desodorizacao_cor_amarela',
           'desodorizacao_cor_vermelha'}


plant_name = "Primavera do Leste"

result_df = df.melt(id_vars="timestamp", value_vars=colunas, var_name="measurement_desc", value_name="pi_value1")

result_df["plant_name"] = plant_name

result_df['pi_value1'] = result_df['pi_value1'].str.replace(',','.')
result_df = result_df[result_df["pi_value1"] != "No events found."]
result_df = result_df[result_df["pi_value1"] != "Arc Off-line"]
result_df['timestamp'] = pd.to_datetime(result_df['timestamp'])
result_df['timestamp'] = result_df['timestamp'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))

result_df.loc[result_df["measurement_desc"] == 'acidez_day_tank', 'measurement_desc' ] = 'Acid_Oil_Reacting'
result_df.loc[result_df["measurement_desc"] == 'clorofila', 'measurement_desc' ] = 'Oil_Crude_Chloropyl'
result_df.loc[result_df["measurement_desc"] == 'degomagem_enzimatica_sabao_ika', 'measurement_desc' ] = 'Soap_Oil_Degumming'
result_df.loc[result_df["measurement_desc"] == 'degomagem_enzimatica_spin_test', 'measurement_desc' ] = 'Spin_Oil_Degumming'
result_df.loc[result_df["measurement_desc"] == 'clarificacao_cor_vermelha', 'measurement_desc' ] = 'RedColor_Oil_Bleaching'
result_df.loc[result_df["measurement_desc"] == 'clarificacao_clorofila', 'measurement_desc' ] = 'Chlorophyl_Oil_Bleaching'
result_df.loc[result_df["measurement_desc"] == 'desodorizacao_acidez', 'measurement_desc' ] = 'Acid_Oil_Deodorizing'
result_df.loc[result_df["measurement_desc"] == 'desodorizacao_sabao', 'measurement_desc' ] = 'Soap_Oil_Deodorizing'
result_df.loc[result_df["measurement_desc"] == 'desodorizacao_clorofila', 'measurement_desc' ] = 'Chlorophyl_Oil_Deodorizing'
result_df.loc[result_df["measurement_desc"] == 'desodorizacao_cor_amarela', 'measurement_desc' ] = 'YellowColor_Oil_Deodorizing'
result_df.loc[result_df["measurement_desc"] == 'desodorizacao_cor_vermelha', 'measurement_desc' ] = 'RedColor_Oil_Deodorizing'

result_df = result_df.dropna()

# Please, the file out needs to be uploaded in onet_tag_values_historical_tmp/Primavera_do_Leste hdfs path

result_df.to_csv("data_quality_bug_fix.csv", sep='\t', index=0)