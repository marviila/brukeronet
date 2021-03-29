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
result_df['timestamp'] = pd.to_datetime(result_df['timestamp'])
result_df['timestamp'] = result_df['timestamp'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
#result_df = result_df.drop(result_df[result_df.pi_value1 == "Pt Created"].index)
result_df = result_df[result_df.pi_value1 != "Pt Created"]
result_df['plant_name'] = plant_name
#result_df = result_df.drop_duplicates(subset=['timestamp', 'measurement_desc', 'pi_value1', 'plant_name'])


result_df.loc[result_df["measurement_desc"] == 'fibra_farelo', 'measurement_desc' ] = 'Fiber_FinishedMeal'
result_df.loc[result_df["measurement_desc"] == 'granulometria_farelo', 'measurement_desc' ] = 'Granulometry_FinishedMeal'
result_df.loc[result_df["measurement_desc"] == 'oleo_farelo', 'measurement_desc' ] = 'Oil_FinishedMeal'
result_df.loc[result_df["measurement_desc"] == 'oleo_soja', 'measurement_desc' ] = 'Oil_Bean'
result_df.loc[result_df["measurement_desc"] == 'proteina_farelo', 'measurement_desc' ] = 'Protein_FinishedMeal'
result_df.loc[result_df["measurement_desc"] == 'proteina_soja', 'measurement_desc' ] = 'Protein_Beans'
result_df.loc[result_df["measurement_desc"] == 'solubilidade_farelo', 'measurement_desc' ] = 'Solubility_Beans'
result_df.loc[result_df["measurement_desc"] == 'umidade_farelo', 'measurement_desc' ] = 'Moisture_FinishedMeal'
result_df.loc[result_df["measurement_desc"] == 'umidade_quebrados', 'measurement_desc' ] = 'Moisture_CrackedBeans'
result_df.loc[result_df["measurement_desc"] == 'umidade_saida_VSC', 'measurement_desc' ] = 'Moisture_BeansOut_VSC'
result_df.loc[result_df["measurement_desc"] == 'umidade_soja', 'measurement_desc' ] = 'Moisture_Beans'
result_df.loc[result_df["measurement_desc"] == 'farelo_branco', 'measurement_desc' ] = 'Fat_WhiteMeal'
result_df.loc[result_df["measurement_desc"] == 'umidade_farelo_dt', 'measurement_desc' ] = 'Moisture_Meal_DT'
result_df.loc[result_df["measurement_desc"] == 'umidade_farelo_secador', 'measurement_desc' ] = 'Moisture_Meal_Dryer'
result_df.loc[result_df["measurement_desc"] == 'casca_embarque', 'measurement_desc' ] = 'Fiber_Hulls'
result_df.loc[result_df["measurement_desc"] == 'oleo_casca_dehulling', 'measurement_desc' ] = 'Oil_Hulls'
result_df.loc[result_df["measurement_desc"] == 'oleo_casca_pellet', 'measurement_desc' ] = 'Oil_PelletizedHulls'

result_df.to_csv("brukerout.csv", sep='\t', index=False)