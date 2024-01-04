import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd

plt.rcParams.update({'font.size':17})
pisn=pd.read_excel("/home/scala/tesi/analisi_dati_sevn/tabelle_output/tabelle_sevn_10^6/PISN_binary_10^6.xlsx",dtype=float)    #choose the correct path where the data are stored
ppisn=pd.read_excel("/home/scala/tesi/analisi_dati_sevn/tabelle_output/tabelle_sevn_10^6/PPISN_binary_10^6.xlsx",dtype=float)

a,=plt.plot(pisn['Z'],pisn['PISN_before_merger_rate'],'-o',color='blue',markersize=3,linewidth=1)
b,=plt.plot(ppisn['Z'],ppisn['PPISN _before_merger_total_rate'],'-o',color='red',markersize=3,linewidth=1)

plt.xlabel('Metallicity (Z)')
plt.ylabel('rate (%)')
plt.xscale('log')
plt.legend([a,b],['Rate PISN with no previous merger','Rate PPISN  with no previous merger'])
plt.tight_layout()
plt.show()
