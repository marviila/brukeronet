import pandas as pd
import datetime as dt
import re

df = pd.read_csv(r"Dados_ICP_Bruker_Refinaria_PRLE_Limpa_Preparada.csv", delimiter=';', low_memory=False)
df = pd.DataFrame(df)
plant_name = "Primavera do Leste"

df["timestamp"] = df['timestamp'].str.cat(df['time'],sep=" ")
df.drop(['time'], axis='columns', inplace=True)

colunas = {'acido_fosforico_ppm',
'soda_ppm',
'excesso_acido_percentil',
'excesso_acido_massico_ppm',
'equivalente_molar',
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

result_df = df.melt(id_vars="timestamp", value_vars=colunas, var_name="measurement_desc", value_name="pi_value1")
result_df["timestamp"] = result_df["timestamp"].replace(['09/07/0219 16:00:00'], "09/07/2019 16:00:00")
result_df["timestamp"] = result_df["timestamp"].replace(['09/07/0219 00:00:00'], "09/07/2019 00:00:00")
result_df["timestamp"] = result_df["timestamp"].replace(['16/12/20193 00:00:00'], "16/12/2019 00:00:00")
result_df["timestamp"] = result_df["timestamp"].replace(['280/3/2019 23:00:00'], "28/03/2019 23:00:00")
result_df["timestamp"] = result_df["timestamp"].replace(['19/11/2018 08;00'], "19/11/2018 08:00:00")
result_df["timestamp"] = result_df["timestamp"].replace(['280/3/2019 23:20:00'], "28/03/2019 23:20:00")

result_df["pi_value1"] = result_df['pi_value1'].str.replace(r"\(.*\)","")

result_df["plant_name"] = plant_name
result_df = result_df[result_df.timestamp != "10/13/2021 16:00:00"]
result_df = result_df[result_df.timestamp != "13/13/2019 08:00:00"]
result_df = result_df[result_df.timestamp != "21/1182019 16:00:00"]
result_df = result_df[result_df["pi_value1"] != "c"]
result_df = result_df[result_df["pi_value1"] != "#VALOR!"]
result_df = result_df[result_df["pi_value1"] != "-"]

result_df['timestamp'] = pd.to_datetime(result_df['timestamp'])
result_df['timestamp'] = result_df['timestamp'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
result_df['pi_value1'] = result_df['pi_value1'].str.replace(',','.')

result_df.loc[result_df["measurement_desc"] == 'acido_fosforico_ppm', 'measurement_desc' ] = 'FosAcid_Degumming_ppm'
result_df.loc[result_df["measurement_desc"] == 'soda_ppm', 'measurement_desc' ] = 'Soda_Degumming_ppm'
result_df.loc[result_df["measurement_desc"] == 'excesso_acido_percentil', 'measurement_desc' ] = 'FosAcidExcess_Degumming_percent'
result_df.loc[result_df["measurement_desc"] == 'excesso_acido_massico_ppm', 'measurement_desc' ] = 'FosAcidExcess_Degumming_ppm'
result_df.loc[result_df["measurement_desc"] == 'equivalente_molar', 'measurement_desc' ] = 'MolarEquivalent_Degumming'
result_df.loc[result_df["measurement_desc"] == 'nhp_bruto_extracao_fosforo_ppm', 'measurement_desc' ] = 'NHP_CrudeOil_Extracting_NIR'
result_df.loc[result_df["measurement_desc"] == 'bruto_refinaria_fosforo_ppm', 'measurement_desc' ] = 'Fos_CrudeOil_Degumming'
result_df.loc[result_df["measurement_desc"] == 'nhp_bruto_refinaria_fosforo_ppm', 'measurement_desc' ] = 'NHP_CrudeOil_Degumming_NIR'
result_df.loc[result_df["measurement_desc"] == 'nhp_bruto_extracao_icp', 'measurement_desc' ] = 'NHP_CrudeOil_Extracting'
result_df.loc[result_df["measurement_desc"] == 'nhp_bruto_refinaria_icp', 'measurement_desc' ] = 'NHP_CrudeOil_Degumming'
result_df.loc[result_df["measurement_desc"] == 'nhp_day_tank_fosforo_ppm', 'measurement_desc' ] = 'NHP_Oil_DayTank'
result_df.loc[result_df["measurement_desc"] == 'nhp_day_tank_magnesio_ppm', 'measurement_desc' ] = 'Mg_Oil_DayTank'
result_df.loc[result_df["measurement_desc"] == 'nhp_day_tank_calcio_ppm', 'measurement_desc' ] = 'Ca_Oil_DayTank'
result_df.loc[result_df["measurement_desc"] == 'entrada_separadora_fosforo_ppm', 'measurement_desc' ] = 'Fos_Oil_PrimaryCentrifuge_In'
result_df.loc[result_df["measurement_desc"] == 'entrada_separadora_magnesio_ppm', 'measurement_desc' ] = 'Mg_Oil_PrimaryCentrifuge_In'
result_df.loc[result_df["measurement_desc"] == 'entrada_separadora_calcio_ppm', 'measurement_desc' ] = 'Ca_Oil_PrimaryCentrifuge_In'
result_df.loc[result_df["measurement_desc"] == 'saida_separadora_fosforo_ppm', 'measurement_desc' ] = 'Fos_Oil_PrimaryCentrifuge_Out'
result_df.loc[result_df["measurement_desc"] == 'saida_separadora_magnesio_ppm', 'measurement_desc' ] = 'Mg_Oil_PrimaryCentrifuge_Out'
result_df.loc[result_df["measurement_desc"] == 'saida_separadora_calcio_ppm', 'measurement_desc' ] = 'Ca_Oil_PrimaryCentrifuge_Out'
result_df.loc[result_df["measurement_desc"] == 'saida_lavadora_fosforo_ppm', 'measurement_desc' ] = 'Fos_Oil_SecondaryCentrifuge_Out'
result_df.loc[result_df["measurement_desc"] == 'saida_lavadora_magnesio_ppm', 'measurement_desc' ] = 'Mg_Oil_SecondaryCentrifuge_Out'
result_df.loc[result_df["measurement_desc"] == 'saida_lavadora_calcio_ppm', 'measurement_desc' ] = 'Ca_Oil_SecondaryCentrifuge_Out'
result_df.loc[result_df["measurement_desc"] == 'saida_secador_fosforo_ppm', 'measurement_desc' ] = 'Fos_Oil_OilDrier_Out'
result_df.loc[result_df["measurement_desc"] == 'saida_secador_magnesio_ppm', 'measurement_desc' ] = 'Mg_Oil_OilDrier_Out'
result_df.loc[result_df["measurement_desc"] == 'saida_secador_calcio_ppm', 'measurement_desc' ] = 'Ca_Oil_OilDrier_Out'
result_df.loc[result_df["measurement_desc"] == 'clarificado_fosforo_ppm', 'measurement_desc' ] = 'Fos_Oil_Bleaching_Out'
result_df.loc[result_df["measurement_desc"] == 'clarificado_magnesio_ppm', 'measurement_desc' ] = 'Mg_Oil_Bleaching_Out'
result_df.loc[result_df["measurement_desc"] == 'clarificado_calcio_ppm', 'measurement_desc' ] = 'Ca_Oil_Bleaching_Out'
result_df.loc[result_df["measurement_desc"] == 'desodorizado_fosforo_ppm', 'measurement_desc' ] = 'Fos_Oil_Deodorization_Out'
result_df.loc[result_df["measurement_desc"] == 'desodorizado_magnesio_ppm', 'measurement_desc' ] = 'Mg_Oil_Deodorization_Out'
result_df.loc[result_df["measurement_desc"] == 'desodorizado_calcio_ppm', 'measurement_desc' ] = 'Ca_Oil_Deodorization_Out'

result_df = result_df.dropna()

result_df.to_csv("bruker_refinaria.csv", sep='\t', index=0)