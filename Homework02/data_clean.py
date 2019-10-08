#%% imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#%%
data = pd.read_excel('data_umts_raw_dropna_success_vm0.xlsx')
#%%
data[(data['Distance from site (m)'] >= 35)].shape

#%%
data[(data['Distance from site (m)'] <= 40000)].shape

#%%
plt.figure()
data[(data['Distance from site (m)'] <= 30)].plot.scatter('Distance from site (m)','Signal (dBm)')
plt.show()

# dados de distância maior que 30!