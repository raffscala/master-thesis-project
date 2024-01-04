import numpy as np
import pandas as pd
from matplotlib.pyplot import cm
import matplotlib.pyplot as plt


kind1=['LAR1','LAR5']
kind2=['KRO1','KRO5']
kind3=['TOP1','TOP5']
kind4=['LOG1','LOG2','LOG3','LOG4','LOG5']
kind5=['PAR1','PAR5']
kind=[kind1,kind2,kind3,kind4,kind5]

z=['6.0','10.0','16.0','22.0','28.0']

fig = plt.figure()
ax=[]
#ax.append(fig.add_axes([0.05, 0.5, 0.3, 0.4]))
#ax.append(fig.add_axes([0.35, 0.5, 0.3, 0.4]))
#ax.append(fig.add_axes([0.65, 0.5, 0.3, 0.4]))
ax.append(fig.add_axes([0.05, 0.1, 0.3, 0.4]))
ax.append(fig.add_axes([0.35, 0.1, 0.3, 0.4]))
#ax.append(fig.add_axes([0.65, 0.1, 0.3, 0.4]))
ax.insert(0,fig.add_axes([0.05, 0.5, 0.3, 0.4]))
ax.insert(1,fig.add_axes([0.35, 0.5, 0.3, 0.4]))
ax.insert(2,fig.add_axes([0.65, 0.5, 0.3, 0.4]))

plt.rcParams['font.size']='13'

marker= iter([':', '--', '-.', '-',(0, (3, 5, 1, 5, 1, 5))])

for i in range(len(kind)):
  color = iter(cm.plasma(np.linspace(0, 0.9, len(kind[i]))))
  mark=next(marker)
  for j in range(len(kind[i])):
  
    c = next(color)

    for k in range(len(z)):
  
      pisn=pd.read_csv(f"/home/scala/tesi/cosmo_rate_public-v2/astromodel/popIII/{kind[i][j]}/input_bin_pisn_after/output_cosmo_Rate/bin_PISNafter/bin_PISNafter_bin_pisn_after_asloth_smooth_off_z{z[i]}_50_SFR_pw.dat", sep=" ")

      #ppisn=pd.read_csv(f"/home/scala/tesi/cosmo_rate_public-v2/astromodel/popIII/{kind[i][j]}/input_bin_pisn_after/output_cosmo_Rate/bin_PPISNafter/bin_PPISNafter_bin_ppisn_after_asloth_smooth_off_z{z[i]}_50_SFR_pw.dat", sep=" ")
      
      ax[k].hist(pisn['M1[Msun]'],bins=50,log=True,density=True,histtype='step',color=c,linestyle=mark,label='PISN after merger')
      #ax[i].hist(ppisn['M1[Msun]'],bins=75,log=True,density=True,histtype='step',color='blue',label='PPISN after merger')
      ax[k].text(0.1,0.9,f'z={z[i]}',va='center',ha='center',transform=ax[i].transAxes)
      

plt.show()
  