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

#%%
# mdat.describe().T
# histogramas
a=5700 # após cdf
i = (mdat['Distance from site (m)'] <= a) #(mdat['Distance from site (m)'] >= 35) & 
print(f'considerando até {a}km : {100*(d[0] - mdat[i].shape[0])/d[0]:.3}% ({d[0] - mdat[i].shape[0]}|{d[0]})')
mdat[i].iloc[:,3].plot.hist(bins=60)

#%%CDF
# m = (mdat['Distance from site (m)'] < 7000) #& (mdat['Call Test Technology'] == 'UMTS')
x = mdat['Distance from site (m)'].values
x = np.sort(x)
y = np.arange(1, x.size+1)/x.size
#%%
plt.plot(x,y)
plt.axis([0,30000,0,1])
j = np.where(y>=.95)
plt.plot(x[j[0][0]], y[j[0][0]],'ro')
plt.yticks(np.arange(11)/10)
#%%
x[j[0][0]]
#%%
data_d57  = mdat[i]
# justificar distancia minima pela inconsistencia fisica dos dados
# z=(data_d57.iloc[:,3] >= 35 ) & (data_d57.iloc[:, 3] <= 200  )
# data_d57[z].plot.scatter('Distance from site (m)','Signal (dBm)')
#%% Velocidades
data_d57.iloc[:,2].describe() # viu o absurdo

data_d57.iloc[:,2].plot.hist()
#%%
# (data_d57.iloc[:,2] <0).shape

#%%
x = data_d57.iloc[:,2].values
x = np.sort(x)
y = np.arange(1, x.size+1)/x.size
plt.plot(x,y)
j = np.where(y>=.95)
plt.plot(x[j[0][0]], y[j[0][0]],'ro')
plt.yticks(np.arange(11)/10)