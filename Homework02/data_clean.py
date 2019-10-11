#%% imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#%% load data
mos_data_raw = pd.read_excel('dataset_raw.xlsx')

#%% spec data
print('\nData info:\n')
display(mos_data_raw.info())
display(mos_data_raw.describe().T)
total_NaN = mos_data_raw.isna().sum().sum()
total_data = mos_data_raw.dropna().shape[0]
loss_NaN = 100 - 100*(total_data - total_NaN)/total_data
print(f'\nTotal of null values: {total_NaN} ({loss_NaN:.3})%')

#%% drop NaN
mos_data = mos_data_raw.dropna()
print('\nNon-null data info:\n')
display(mos_data.info())
display(mos_data.describe().T)
display(mos_data.head())
# Removing from memory data with NaN values:
del mos_data_raw

#%% non numeric data
results = mos_data['Call Test Result'].value_counts()
tech = mos_data['Call Test Technology'].value_counts()
print(f''' Qt. of categorical data:\n\n{results}\n\n{tech}\n
Percentage of catecorical data:\n
{100 - 100 * (total_data - results)/total_data}\n
{100 - 100 * (total_data - tech)/total_data}''')

#%% select data
# Select only rows with 'SUCCESS':
mask = mos_data['Call Test Result'] == 'SUCCESS'
# Changing dataset:
target_data = mos_data[mask]
total_data = target_data.shape[0]
# data after
results = target_data['Call Test Result'].value_counts()
tech = target_data['Call Test Technology'].value_counts()
print(f''' Qt. of categorical data:\n\n{results}\n\n{tech}\n
Percentage of catecorical data:\n
{100 - 100 * (total_data - results)/total_data}\n
{100 - 100 * (total_data - tech)/total_data}\n''')

# Select only rows corresponding to UMTS technology:
mask = target_data['Call Test Technology'] == 'UMTS'
target_data = target_data[mask]

# Resume data:
display(target_data.info())
display(target_data.head())
# removing extra variables from memory
# del mask, mos_data

#%% drop columns
# Removing Call Test Result and Call Test Technology columns
target_data = target_data.drop(columns=['Call Test Result','Call Test Technology'])
display(target_data.head())
target_data.describe().T

#%% date
# Extract hour information of Date Of Test column:
date_of_test = target_data['Date Of Test']
test_hour = date_of_test.apply(lambda dt: dt.hour)

# Visualizing:
# plt.figure()
# plt.scatter(np.arange(10000), test_hour.values[:10000], 
            # c=target_data['MOS'][:10000], marker='x')
# plt.colorbar()

# Add hour column to dataframe and drop the column 'Date Of Test'
target_data = target_data.drop(columns='Date Of Test')
target_data.insert(0, 'Test Hour', test_hour)
display(target_data.head())
display(target_data.describe().T)
#%% dados invalidos
# Visualizing data distribution
fig, ax = plt.subplots(2, 4, figsize=(16, 7)) 
ax = ax.ravel()
fig.suptitle('Histogram of the Data')
for i in range(0, 7):
    ax[i].set_xlabel(target_data.columns[i])
    ax[0].set_ylabel('Frequency')
    ax[4].set_ylabel('Frequency')
    ax[i].hist(target_data.iloc[:, i], bins=16, alpha=.75)
fig.delaxes(ax[7])
# plt.savefig('hw02-figs/hist_data.pdf')

#%%
def empirical_cdf(data):
   x, y = np.unique(data, return_counts=True)
   return x, np.cumsum(y)/data.size
#%%
# os dados 3rd quartil menores que 1km
# box plot:
sns.boxplot(target_data.iloc[:,3])
plt.xlim(0, 5000)

# cdf :
x, y = empirical_cdf(target_data.iloc[:,3])
plt.figure()
plt.plot(x,y)
plt.axis([0,10000,0,1])
plt.yticks(np.arange(11)/10)

# 
print(x[np.where(y>=.95)[0][0]])

#%%
mask = (target_data.iloc[:,3] <= 35)
target_data[mask].plot.scatter('Distance from site (m)','Signal (dBm)')
# argumento macro celula modelo... distancia minima do usuário para a base
# impraticavel na realidade algo assim...

#%% discarding outliers of distance values
mask = (target_data.iloc[:,3] >= 35) & (target_data.iloc[:,3] <= 5565)
target_data = target_data[mask]
target_data.describe().T # descarte de % dos dados

#%% velocidade invalida
# 
mask = target_data.iloc[:,2] < 0
print(f'Qt. of invalid speed data: {target_data[mask].shape[0]}')

# removing columns of speed values < 0
mask = target_data.iloc[:,2] >= 0
target_data = target_data[mask]
display(target_data.describe().T)
#%% observando outliers velocidade
sns.boxplot(target_data.iloc[:,2])

x, y = empirical_cdf(target_data.iloc[:,2])
plt.figure()
plt.plot(x,y)
# plt.axis([0,10000,0,1])
plt.yticks(np.arange(11)/10)

#%% quanto de dados...
mask = (target_data.iloc[:,2] <60) #& (target_data.iloc[:,2] < 70) 
target_data[mask].shape[0],100-100*(target_data.shape[0] - target_data[mask].shape[0])/target_data.shape[0]
# lidando com 85 %
# plt.figure()
# plt.scatter(target_data.iloc[:,1], target_data.iloc[:,2], 
#             c=target_data['MOS'], marker='x')
# plt.colorbar()
#%%
# target_data.describe()
# salvando sem alteração do máximo de velocidade
target_data.to_excel('target_mos_data.xlsx', index=False)
#%% reducing data
mask = target_data.iloc[:,2] < 40
target_data = target_data[mask]
display(target_data.describe().T)
display(target_data.head())
#salvando com alteraçao
target_data.to_excel('mos_data_v0-40.xlsx', index=False)

# justificar distancia minima pela inconsistencia fisica dos dados
# z=(data_d57.iloc[:,3] >= 35 ) & (data_d57.iloc[:, 3] <= 200  )
# data_d57[z].plot.scatter('Distance from site (m)','Signal (dBm)')

#%%
def split_data(data, rate):
    n = data.shape[0]
    idx = np.random.permutation(n)
    test_set = data.iloc[idx[:int(n*rate)]] # test: n*rate frist rows
    train_set = data.iloc[idx[int(n*rate):]] # train: the rest
    return train_set, test_set

#%%
test, train = split_data(target_data, 2/3)
#%% Save train and test datasets:
test.to_excel('mos_datav0-40_test.xlsx', index=False)
train.to_excel('mos_datav0-40_train.xlsx', index=False)
#%%
# test.to_hdf('mos_datav0-40_test.hdf5', 'test', index=False)