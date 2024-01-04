import numpy as np
from matplotlib.pyplot import cm
import matplotlib.pyplot as plt

#All the models adopted for pop3 stars
kind1=['LAR1','LAR5']
kind2=['KRO1','KRO5']
kind3=['TOP1','TOP5']
kind4=['LOG1','LOG2','LOG3','LOG4','LOG5']
kind5=['PAR1','PAR5']
kind=[kind1,kind2,kind3,kind4,kind5]


plt.rcParams.update({'font.size':20})

#Create two subplots
fig = plt.figure()
ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.4])
ax2 = fig.add_axes([0.1, 0.5, 0.8, 0.4])

marker= iter([':', '--', '-.', '-',(0, (3, 5, 1, 5, 1, 5))])

for i in range(len(kind)):
  color = iter(cm.plasma(np.linspace(0, 0.9, len(kind[i]))))
  mark=next(marker)
  for j in range(len(kind[i])):
  
    c = next(color)
   
    path_pisn=f"/home/scala/tesi/cosmo_rate_public-v2/astromodel/popIII/{kind[i][j]}/input_bin_pisn/output_cosmo_Rate/bin_PISN/MRD_spread_1Z_100_No_linear_0.2_No_No_False_asloth_smooth_off_1.dat"    #CHANGE FOR THE CORRECT PATHS
    path_ppisn=f"/home/scala/tesi/cosmo_rate_public-v2/astromodel/popIII/{kind[i][j]}/input_bin_ppisn/output_cosmo_Rate/bin_PPISN/MRD_spread_1Z_100_No_linear_0.2_No_No_False_asloth_smooth_off_1.dat"
  
    pisn=pd.read_csv(path_pisn,skiprows=1,header=None,sep=' ')
    ppisn=pd.read_csv(path_ppisn,skiprows=1,header=None,sep=' ')
    
    ax1.plot(ppisn[0],ppisn[1],c=c,label=f'{kind[i][j]}',linestyle=mark)
    ax2.plot(pisn[0],pisn[1],c=c,label=f'{kind[i][j]}',linestyle=mark)

ax1.set_ylabel('$\mathcal{R}$ PPISN $(Gpc^{-3}yr^{-1})$')
ax2.set_ylabel('$\mathcal{R}$ PISN $(Gpc^{-3}yr^{-1})$')
ax1.set_xlabel('Redshift ($z$)')
ax1.set_yscale('log')
ax2.set_yscale('log')
ax1.set_ylim(2*10**-1,6*10**2)
ax2.set_ylim(2*10**-1,6*10**2)

plt.legend(loc='upper center',frameon=False, bbox_to_anchor=(0.5, 1.32),ncol=7)
plt.setp(ax2.get_xticklabels(), visible=False)
plt.show()
  
