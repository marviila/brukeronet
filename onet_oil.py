import pandas as pd
import datetime as dt
import re

df = pd.read_csv(r"Dados_ICP_Bruker_Refinaria_PRLE_Limpa_Preparada.csv", delimiter=";", low_memory=False)
df = pd.DataFrame(df)


plant_name = "Primavera do Leste"

colunas = {'acido_fosforico_ppm',
'soda_ppm',
'excesso_acido_percentil',
'excesso_acido_massico_ppm',
'equivalente_molar',
'nhp_bruto_extracao_fosforo_ppm',
'bruto_refinaria_fosforo_ppm',
'nhp_bruto_refinaria_fosforo_ppm',
'nhp_bruto_extracao_icp',
'nhp_bruto_refinaria_icp',
'nhp_day_tank_fosforo_ppm',
'nhp_day_tank_magnesio_ppm',
'nhp_day_tank_calcio_ppm',
'entrada_separadora_fosforo_ppm',
'entrada_separadora_magnesio_ppm',
'entrada_separadora_calcio_ppm',
'saida_separadora_fosforo_ppm',
'saida_separadora_magnesio_ppm',
'saida_separadora_calcio_ppm',
'saida_lavadora_fosforo_ppm',
'saida_lavadora_magnesio_ppm',
'saida_lavadora_calcio_ppm',
'saida_secador_fosforo_ppm',
'saida_secador_magnesio_ppm',
'saida_secador_calcio_ppm',
'clarificado_fosforo_ppm',
'clarificado_magnesio_ppm',
'clarificado_calcio_ppm',
'desodorizado_fosforo_ppm',
'desodorizado_magnesio_ppm',
'desodorizado_calcio_ppm'}

df2 = df.melt(id_vars="timestamp", value_vars=colunas, var_name="measurement_dsc", value_name="pi_value1")
df2["timestamp"] = df2["timestamp"].replace(['09/07/0219'], "09/07/2019")
df2["timestamp"] = df2["timestamp"].replace(['16/12/20193'], "16/12/2019")
df2["timestamp"] = df2["timestamp"].replace(['280/3/2019'], "28/03/2019")

df2["pi_value1"] = df2['pi_value1'].str.replace(r"\(.*\)","")

#df2["pi_value1"] = df2["pi_value1"].replace(to_replace=[" (ICP)$"], value="")

df2["plant_name"] = plant_name
df2 = df2[df2.timestamp != "10/13/2021"]
df2 = df2[df2.timestamp != "13/13/2019"]
df2 = df2[df2.timestamp != "21/1182019"]
df2 = df2[df2["pi_value1"] != "c"]
df2 = df2[df2["pi_value1"] != "#VALOR!"]
df2 = df2[df2["pi_value1"] != "-"]

df2['timestamp'] = pd.to_datetime(df2['timestamp'])
df2['timestamp'] = df2['timestamp'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
df2['pi_value1'] = df2['pi_value1'].str.replace(',','.')

df2 = df2.dropna()
#df2 = df2.drop_duplicates()

df2.to_csv("bruker_refinaria.csv", sep='\t', index=0)