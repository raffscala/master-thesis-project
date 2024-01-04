import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd

plt.rcParams.update({'font.size':25})
pisn=pd.read_excel("/home/scala/tesi/analisi_dati_sevn/tabelle_output/tabelle_sevn_10^6/PISN_binary_10^6.xlsx",dtype=float)
ppisn=pd.read_excel("/home/scala/tesi/analisi_dati_sevn/tabelle_output/tabelle_sevn_10^6/PPISN_binary_10^6.xlsx",dtype=float)

a,=plt.plot(pisn['Z'],pisn['Merger']/1000000*100,'-o',color='green',markersize=3,linewidth=1)
b,=plt.plot(pisn['Z'],pisn['rate_PISN_after'],'-o',color='blue',markersize=3,linewidth=1)
c,=plt.plot(ppisn['Z'],ppisn['rate_PPISN_after'],'-o',color='red',markersize=3,linewidth=1)
plt.xlabel('Metallicity (Z)')
plt.ylabel('rate (%)')
plt.xscale('log')
plt.legend([a,b,c],['Total merger rate','Rate PISN after merger','Rate PPISN after merger'],fontsize=20)
plt.tight_layout()
plt.show()