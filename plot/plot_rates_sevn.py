import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd

plt.rcParams.update({'font.size':25})
sing=pd.read_excel("/home/scala/tesi/analisi_dati_sevn/tabelle_output/tabelle_sevn_10^6/single_rates_10^6.xlsx",dtype=float) #choose the correct path where the data are stored
bin=pd.read_excel("/home/scala/tesi/analisi_dati_sevn/tabelle_output/tabelle_sevn_10^6/binary_rates_10^6.xlsx",dtype=float)


fig = plt.figure()
ax2 = fig.add_axes([0.1, 0.15, 0.8, 0.4])
ax1 = fig.add_axes([0.1, 0.55, 0.8, 0.4])
a,=ax1.plot(sing['Z'],sing['rate_PISN_%'],'-o',color='red',markersize=3,linewidth=1)
b,=ax1.plot(bin['Z'],bin['rate_PISN_%'],'-o',color='blue',markersize=3,linewidth=1)
ax1.set_ylabel('PISN rate (%)')
#ax1.set_xlim(0.5*10**(-12),0.1)
ax1.set_xscale('log')
ax1.legend([a,b],['Single stars','Binary systems'],loc='upper left')

c,=ax2.plot(sing['Z'],sing['rate_PPISN_%'],'-o',color='red',markersize=3,linewidth=1)
d,=ax2.plot(bin['Z'],bin['rate_PPISN_%'],'-o',color='blue',markersize=3,linewidth=1)
ax2.set_xlabel('Metallicity (Z)')
ax2.set_ylabel('PPISN rate (%)')

ax2.set_ylim(-0.3,7)
ax2.set_xscale('log')


plt.setp(ax1.get_xticklabels(), visible=False)

plt.show()
