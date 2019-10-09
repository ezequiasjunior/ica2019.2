#%% imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#%% loads
# umts = pd.read_excel('data_umts_raw_dropna.xlsx')
mdat = pd.read_excel('dataset_raw.xlsx')
#%%
D = mdat.shape
mdat = mdat.dropna()
d = mdat.shape

#%%
tech = mdat['Call Test Technology'].value_counts()

umts = mdat.groupby('Call Test Technology').get_group('UMTS')
lte = mdat.groupby('Call Test Technology').get_group('LTE')
gsm = mdat.groupby('Call Test Technology').get_group('GSM')

#%%
result = mdat['Call Test Result'].value_counts()

#%% 
us = umts.shape
us35 = umts[(umts['Distance from site (m)'] >= 35)].shape
us3540 = umts[(umts['Distance from site (m)'] >= 35) & (umts['Distance from site (m)'] <= 40000) ].shape

mask = umts['Speed (m/s)'] < 0
uv1 = umts[mask].shape
mask = umts['Speed (m/s)'] >= 0
usv0 = umts[mask].shape

mask = umts['Call Test Result'] == 'SUCCESS'
uss = umts[mask].shape
#%%
print(f'''
dados totais = {D[0]}
dados nulos = {(D[0] - d[0])}
porcentagem dos nulos : {100*(D[0] - d[0])/D[0] :.3}%

Dados nNulos lte e gsm: 
{tech[1:]}

porcentagem dos dados lte+gsm: {100 * (d[0]-tech[0])/d[0] :.3}%

Dados Sucesso/ falha:
{result}

porcentagem dos dados por resultado: Suc Fail, fail
{100 - 100 * (d[0]-result[0])/d[0] :.3}%
{100 - 100 * (d[0]-result[1])/d[0] :.3}%
{100 - 100 * (d[0]-result[2])/d[0] :.3}%
considerando apenas sucessos, a perda nos dados é de : {100 * (d[0]-result[0])/d[0] :.3}%
''')

print(f'''
UMTS total dropna = {us[0]}
UMTS dados com distância maior que 35m: {us35[0]}
entre 35m e 40km: {us3540[0]}
perda no dados com a redução: {100 * (us[0]-us3540[0])/us[0] :.3}%
''')
print(f'''
UMTS velocidade -1 -> erro: {uv1[0]}
UMTS velocidade >= 0: {usv0[0]}
porcentagem dos dados retirados: {100 * (us[0] - usv0[0])/us[0] :.3}%
''')
print(f'''UMTS só sucesso: {uss[0]}
porcentagem dos dados falha: {100 * (us[0] - uss[0])/us[0] :.3}%
''')
#%% reduc
mask1 = (umts['Distance from site (m)'] >= 35) & (umts['Distance from site (m)'] <= 40000)
mask2 = umts['Speed (m/s)'] >= 0


#%%
# mask=
plt.figure()
d['MOS'].plot.hist()#('Distance from site (m)','Signal (dBm)')
plt.show()

# dados de distância maior que 30!