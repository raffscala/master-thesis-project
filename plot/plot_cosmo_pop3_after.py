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


plt.rcParams.update({'font.size':15})

fig = plt.figure()
ax1 = fig.add_axes([0.1, 0.1, 0.4, 0.4])
ax2 = fig.add_axes([0.1, 0.5, 0.4, 0.4])
ax3 = fig.add_axes([0.5, 0.1, 0.4, 0.4])
ax4 = fig.add_axes([0.5, 0.5, 0.4, 0.4])

marker= iter([':', '--', '-.', '-',(0, (3, 5, 1, 5, 1, 5))])

for i in range(len(kind)):
  color = iter(cm.plasma(np.linspace(0, 0.9, len(kind[i]))))
  mark=next(marker)
  for j in range(len(kind[i])):
  
    c = next(color)
   
    path_pisn_aft=f"/home/scala/tesi/cosmo_rate_public-v2/astromodel/popIII/{kind[i][j]}/input_bin_pisn_after/output_cosmo_Rate/bin_PISNafter/MRD_spread_1Z_100_No_linear_0.2_No_No_False_asloth_smooth_off_1.dat"
    path_pisn_bef=f"/home/scala/tesi/cosmo_rate_public-v2/astromodel/popIII/{kind[i][j]}/input_bin_pisn_before/output_cosmo_Rate/bin_PISNbefore/MRD_spread_1Z_100_No_linear_0.2_No_No_False_asloth_smooth_off_1.dat"
    path_ppisn_aft=f"/home/scala/tesi/cosmo_rate_public-v2/astromodel/popIII/{kind[i][j]}/input_bin_ppisn_after/output_cosmo_Rate/bin_PPISNafter/MRD_spread_1Z_100_No_linear_0.2_No_No_False_asloth_smooth_off_1.dat"
    path_ppisn_bef=f"/home/scala/tesi/cosmo_rate_public-v2/astromodel/popIII/{kind[i][j]}/input_bin_ppisn_before/output_cosmo_Rate/bin_PPISNbefore/MRD_spread_1Z_100_No_linear_0.2_No_No_False_asloth_smooth_off_1.dat"
  
    pisnaft=pd.read_csv(path_pisn_aft,skiprows=1,header=None,sep=' ')
    pisnbef=pd.read_csv(path_pisn_bef,skiprows=1,header=None,sep=' ')
    ppisnaft=pd.read_csv(path_ppisn_aft,skiprows=1,header=None,sep=' ')
    ppisnbef=pd.read_csv(path_ppisn_bef,skiprows=1,header=None,sep=' ')
    
    ax1.plot(ppisnaft[0],ppisnaft[1],c=c,label=f'{kind[i][j]}',linestyle=mark)
    ax2.plot(pisnaft[0],pisnaft[1],c=c,label=f'{kind[i][j]}',linestyle=mark)
    ax3.plot(ppisnbef[0],ppisnbef[1],c=c,label=f'{kind[i][j]}',linestyle=mark)
    ax4.plot(pisnbef[0],pisnbef[1],c=c,label=f'{kind[i][j]}',linestyle=mark)

ax1.set_ylabel('$\mathcal{R}$ PPISN after merger $(Gpc^{-3}yr^{-1})$',fontsize=12 )
ax2.set_ylabel('$\mathcal{R}$ PISN after merger $(Gpc^{-3}yr^{-1})$',fontsize=12)
ax3.set_ylabel('$\mathcal{R}$ PPISN before merger $(Gpc^{-3}yr^{-1})$',fontsize=12)
ax4.set_ylabel('$\mathcal{R}$ PISN no merger $(Gpc^{-3}yr^{-1})$',fontsize=12)

ax1.set_xlabel('Redshift ($z$)')
ax3.set_xlabel('Redshift ($z$)')
ax1.set_yscale('log')
ax2.set_yscale('log')
ax3.set_yscale('log')
ax4.set_yscale('log')

ax1.set_ylim(2*10**-4,5*10**2)
ax2.set_ylim(2*10**-4,5*10**2)
ax3.set_ylim(2*10**-4,5*10**2)
ax4.set_ylim(2*10**-4,5*10**2)

ax3.yaxis.set_label_position("right")
ax4.yaxis.set_label_position("right")

ax3.yaxis.tick_right()
ax4.yaxis.tick_right()

plt.legend(loc='upper center',frameon=False, bbox_to_anchor=(0.0, 1.25),ncol=7,fontsize=13)
plt.setp(ax2.get_xticklabels(), visible=False)
plt.setp(ax4.get_xticklabels(), visible=False)
plt.show()
  