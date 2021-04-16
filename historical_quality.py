import pandas as pd
import datetime as dt
import re
df = pd.read_csv(r"Novos_dados_qualidade.csv", delimiter=";", low_memory=False)

df = pd.DataFrame(df)

colunas = {'degomagem_enzimatica_acidez_secador', 'degomagem_enzimatica_sabao_ika',
                'degomagem_enzimatica_spin_test', 'degomagem_enzimatica_umidade_goma',
                'clarificacao_cor_vermelha', 'clarificacao_clorofila',
                'desodorizacao_acidez', 'desodorizacao_sabao',
                'desodorizacao_clorofila', 'desodorizacao_cor_amarela',
                'desodorizacao_cor_vermelha'}


plant_name = "Primavera do Leste"

result_df = df.melt(id_vars="data hora", value_vars=colunas, var_name="measurement_desc", value_name="pi_value1")


result_df["plant_name"] = plant_name
result_df = result_df[result_df["pi_value1"] != "No events found."]
result_df = result_df[result_df["pi_value1"] != "Arc Off-line"]


result_df['data hora'] = pd.to_datetime(result_df['data hora'])
result_df['data hora'] = result_df['data hora'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
result_df['pi_value1'] = result_df['pi_value1'].str.replace(',','.')

result_df.loc[result_df["measurement_desc"] == 'degomagem_enzimatica_acidez_secador', 'measurement_desc' ] = 'Acid_Oil_Degumming'
result_df.loc[result_df["measurement_desc"] == 'degomagem_enzimatica_sabao_ika', 'measurement_desc' ] = 'Soap_Oil_Degumming'
result_df.loc[result_df["measurement_desc"] == 'degomagem_enzimatica_spin_test', 'measurement_desc' ] = 'Spin_Oil_Degumming'
result_df.loc[result_df["measurement_desc"] == 'degomagem_enzimatica_umidade_goma', 'measurement_desc' ] = 'Moisture_Gums_Degumming'
result_df.loc[result_df["measurement_desc"] == 'clarificacao_cor_vermelha', 'measurement_desc' ] = 'RedColor_Oil_Bleaching'
result_df.loc[result_df["measurement_desc"] == 'clarificacao_clorofila', 'measurement_desc' ] = 'Chlorophyl_Oil_Bleaching'
result_df.loc[result_df["measurement_desc"] == 'desodorizacao_acidez', 'measurement_desc' ] = 'Acid_Oil_Deodorizing'
result_df.loc[result_df["measurement_desc"] == 'desodorizacao_sabao', 'measurement_desc' ] = 'Soap_Oil_Deodorizing'
result_df.loc[result_df["measurement_desc"] == 'desodorizacao_clorofila', 'measurement_desc' ] = 'Chlorophyl_Oil_Deodorizing'
result_df.loc[result_df["measurement_desc"] == 'desodorizacao_cor_amarela', 'measurement_desc' ] = 'YellowColor_Oil_Deodorizing'
result_df.loc[result_df["measurement_desc"] == 'desodorizacao_cor_vermelha', 'measurement_desc' ] = 'RedColor_Oil_Deodorizing'



result_df = result_df.dropna()

result_df.to_csv("historical_quality.csv", sep=';', index=0)