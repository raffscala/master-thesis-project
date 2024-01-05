import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

z=['0.1','1.0','2.0','4.0','6.0','10.0']

fig = plt.figure()
ax=[]
ax.append(fig.add_axes([0.09, 0.15, 0.3, 0.4]))
ax.append(fig.add_axes([0.39, 0.15, 0.3, 0.4]))
ax.append(fig.add_axes([0.69, 0.15, 0.3, 0.4]))
ax.insert(0,fig.add_axes([0.09, 0.55, 0.3, 0.4]))
ax.insert(1,fig.add_axes([0.39, 0.55, 0.3, 0.4]))
ax.insert(2,fig.add_axes([0.69, 0.55, 0.3, 0.4]))
plt.rcParams['font.size']='25'

for i in range(len(z)):

  #CHANGE FOR THE CORRECT FILES
  pisn=pd.read_csv(f"/home/scala/tesi/cosmo_rate_public-v2/astromodel/popI_II/A3/10^6/input_bin_pisn_after/output_cosmo_Rate/bin_PISNafter/bin_PISNafter_bin_pisn_after_MandF2017_z{z[i]}_50_SFR_pw.dat", sep=" ")

  ppisn=pd.read_csv(f"/home/scala/tesi/cosmo_rate_public-v2/astromodel/popI_II/A3/10^6/input_bin_ppisn_after/output_cosmo_Rate/bin_PPISNafter/bin_PPISNafter_bin_ppisn_after_MandF2017_z{z[i]}_50_SFR_pw.dat", sep=" ")
  
  #Construction of the subplots
  ax[i].hist(pisn['M1[Msun]'],bins=50,log=True,density=True,histtype='step',color='red',label='PISN after merger')
  ax[i].hist(ppisn['M1[Msun]'],bins=75,log=True,density=True,histtype='step',color='blue',label='PPISN after merger')
  ax[i].text(0.15,0.9,f'z={z[i]}',va='center',ha='center',transform=ax[i].transAxes)
  ax[i].set_ylim(10**(-5),9.99*10**(-1))
  ax[i].set_xlim(16,155)
  ax[i].tick_params(axis='both', labelsize=25)
  if i<3:
    plt.setp(ax[i].get_xticklabels(), visible=False) 
    
  if i!=0 and i!=3:
    plt.setp(ax[i].get_yticklabels(), visible=False) 
    
  if i>=3 and i<=5:
    ax[i].set_xlabel('$M_{1,ZAMS}$ $(M_{\odot})$',fontsize='25')

  if i==0 or i==3:
    ax[i].set_ylabel('PDF',fontsize='25')
    
plt.legend(loc='upper center',frameon=False,ncol=2, bbox_to_anchor=(-0.5, 1.23))

plt.show()
