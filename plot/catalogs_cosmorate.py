import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

z=['0.1','1.0','2.0','4.0','6.0','10.0']
plt.rcParams.update({'font.size':17})
fig=[]
ax1=[]
ax2=[]
for i in range(len(z)):
  
  cat=pd.read_csv(f"/home/scala/tesi/cosmo_rate_public-v2/astromodel/popI_II/A3/10^6/input_sing_pisn/output_cosmo_Rate/sing_PISN/sing_PISN_sing_pisn_MandF2017_z{z[i]}_50_SFR_pw.dat", sep=" ")  #CHANGE OFR THE CORRECT CATALOG FILE

  fig.append(plt.figure(i))
  
  ax1.append(fig[i].add_axes([0.1, 0.5, 0.8, 0.4],xticklabels=[]))
  ax2.append(fig[i].add_axes([0.1, 0.1, 0.8, 0.4]))

  ax1[i].plot(cat['Mzams[Msun]'],cat['time_delay[yr]']/10**6,'o',color='red',markersize=1)
  fig[i].text(0.8,0.8,f'z={z[i]}')
  ax2[i].hist(cat['Mzams[Msun]'],bins=100, density=True)
  ax2[i].set_xlabel('$M_{ZAMS}$ $(M_{\odot})$')

  ax1[i].set_ylabel('Delay time (Myr)')
  ax2[i].set_ylabel('PDF')

plt.show()
