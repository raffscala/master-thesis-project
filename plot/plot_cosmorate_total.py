import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter


def merge_rate_unc(merger_rate, quant_low, quant_up):
    #------------------------------------
    # This function evaluates the median and N% credible interval of the merger rate density
    # if the option on the uncertainty is activated.
    # the first quantity is a matrix len(P)xlen(R) where len(P) are the number of redshift bins
    # and len(R) = N_iter
    # quant_low is the lowst quantile and quant_up is highest quantile, that is 
    # to evaluate the 50% credible interval, quant_low = 25 and quant_up = 75
    #------------------------------------
    
  MR_50 = np.zeros(len(merger_rate[:,0]))
  MR_low = np.zeros(len(merger_rate[:,0]))
  MR_up = np.zeros(len(merger_rate[:,0]))
    
  for i in range(len(MR_50)):
    MR_50[i] = np.percentile(merger_rate[i,:], 50)
    MR_low[i] = np.percentile(merger_rate[i,:], quant_low)
    MR_up[i] = np.percentile(merger_rate[i,:], quant_up)
    
  return MR_50, MR_low, MR_up

plt.rcParams.update({'font.size':20})

cb_class=['sing_pisn','bin_pisn','sing_ppisn','bin_ppisn']
sim=['sing_PISN','bin_PISN','sing_PPISN','bin_PPISN']
sing='MRD_spread_9Z_50_No_linear_0.2_Yes_Yes_False_MandF2017_1.dat'
bin='MRD_spread_16Z_50_No_linear_0.2_Yes_Yes_False_MandF2017_1.dat'
singpp='MRD_spread_16Z_50_No_linear_0.2_Yes_Yes_False_MandF2017_1.dat'
binpp='MRD_spread_16Z_50_No_linear_0.2_Yes_Yes_False_MandF2017_1.dat'
syst=[sing,bin,singpp,binpp]

#cb_class=['bin_pisn_after','bin_pisn_before','bin_ppisn_after','bin_ppisn_before']
#sim=['bin_PISNafter','bin_PISNbefore','bin_PPISNafter','bin_PPISNbefore']
#pisn_after='MRD_spread_16Z_50_No_linear_0.2_Yes_Yes_False_MandF2017_1.dat'
#pisn_before='MRD_spread_13Z_50_No_linear_0.2_Yes_Yes_False_MandF2017_1.dat'
#ppisn_after='MRD_spread_16Z_50_No_linear_0.2_Yes_Yes_False_MandF2017_1.dat'
#ppisn_before='MRD_spread_16Z_50_No_linear_0.2_Yes_Yes_False_MandF2017_1.dat'
#syst=[pisn_after,pisn_before,ppisn_after,ppisn_before]


CI = '95'
if CI == '95':
  min_ci = 2.5
  max_ci  = 97.5
elif CI == '50':
  min_ci = 25
  max_ci  = 75


N_iter=1000

path0=f"/home/scala/tesi/cosmo_rate_public-v2/astromodel/popI_II/A3/10^6/input_{cb_class[0]}/output_cosmo_Rate/{sim[0]}/"
path1=f"/home/scala/tesi/cosmo_rate_public-v2/astromodel/popI_II/A3/10^6/input_{cb_class[1]}/output_cosmo_Rate/{sim[1]}/"
path2=f"/home/scala/tesi/cosmo_rate_public-v2/astromodel/popI_II/A3/10^6/input_{cb_class[2]}/output_cosmo_Rate/{sim[2]}/"
path3=f"/home/scala/tesi/cosmo_rate_public-v2/astromodel/popI_II/A3/10^6/input_{cb_class[3]}/output_cosmo_Rate/{sim[3]}/"

z_binz0= np.loadtxt(path0+syst[0], usecols = 0)           
MRD_binz0= np.loadtxt(path0+syst[0], usecols = np.arange(1,N_iter))
MR_50_0,MR_low_0,MR_up_0=merge_rate_unc(MRD_binz0, min_ci, max_ci)
#z_true_0,MRD_true_0=np.loadtxt(path0+syst[0], unpack=True,usecols=(0,1))

z_binz1= np.loadtxt(path1+syst[1], usecols = 0) 
MRD_binz1= np.loadtxt(path1+syst[1], usecols = np.arange(1,N_iter))
MR_50_1,MR_low_1,MR_up_1=merge_rate_unc(MRD_binz1, min_ci, max_ci)
#z_true_1,MRD_true_1=np.loadtxt(path1+syst[1], unpack=True,usecols=(0,1)) 

z_binz2= np.loadtxt(path2+syst[2], usecols = 0) 
MRD_binz2= np.loadtxt(path2+syst[2], usecols = np.arange(1,N_iter))
MR_50_2,MR_low_2,MR_up_2=merge_rate_unc(MRD_binz2, min_ci, max_ci)
#z_true_2,MRD_true_2=np.loadtxt(path2+syst[2], unpack=True,usecols=(0,1)) 

z_binz3= np.loadtxt(path3+syst[3], usecols = 0) 
MRD_binz3= np.loadtxt(path3+syst[3], usecols = np.arange(1,N_iter))
MR_50_3,MR_low_3,MR_up_3=merge_rate_unc(MRD_binz3, min_ci, max_ci)
#z_true_3,MRD_true_3=np.loadtxt(path3+syst[3], unpack=True,usecols=(0,1)) 

fig = plt.figure()


ax2 = fig.add_axes([0.1, 0.1, 0.4, 0.4])
ax1=fig.add_axes([0.1, 0.5, 0.4, 0.4])
ax4 = fig.add_axes([0.5, 0.1, 0.4, 0.4])
ax3=fig.add_axes([0.5, 0.5, 0.4, 0.4])

ax1.plot(z_binz0, MR_50_0, label = 'Median rate')
ind_min = 0
ax1.fill_between(z_binz0[ind_min:], MR_low_0[ind_min:], MR_up_0[ind_min:],  label = CI+'% C.I. ', alpha = 0.5)#,color = color_p0)
#ax1.plot(z_true_0[ind_min:], MRD_true_0[ind_min:],  label = 'Expected rate ', linestyle = '--')#,color = color_p0)
ax1.set_yscale('log')
ax1.set_ylim(10**0,10**5)
ax1.set_xlim(-0.8,15.8)
ax1.set_ylabel('$\mathcal{R}$ PISN in SSP $(Gpc^{-3}yr^{-1})$', fontsize=15)


ax2.plot(z_binz1, MR_50_1,  label = 'Median rate')
#color_p1 = p1[0].get_color()
ind_min = 0
ax2.fill_between(z_binz1[ind_min:], MR_low_1[ind_min:], MR_up_1[ind_min:],  label = CI+'% C.I. ', alpha = 0.5)#,color = color_p1)
#ax2.plot(z_true_1[ind_min:], MRD_true_1[ind_min:],  label = 'Expected rate ', linestyle = '--')#color = color_p1
ax2.set_yscale('log')
ax2.set_ylim(10**0,10**5)
ax2.set_xlim(-0.8,15.8)
ax2.set_xlabel('Redshift (z)')
ax2.set_ylabel('$\mathcal{R}$ PISN in BSP $(Gpc^{-3}yr^{-1})$', fontsize=15)
ax2.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))

ax3.plot(z_binz2, MR_50_2, label = 'Median rate')
ind_min = 0
ax3.fill_between(z_binz2[ind_min:], MR_low_2[ind_min:], MR_up_2[ind_min:],  label = CI+'% C.I. ', alpha = 0.5)#,color = color_p0)
#ax3.plot(z_true_2[ind_min:], MRD_true_2[ind_min:],  label = 'Expected rate ', linestyle = '--')#,color = color_p0)
ax3.set_yscale('log')
ax3.set_ylim(10**0,10**5)
ax3.set_xlim(-0.8,15.8)
ax3.yaxis.tick_right()
ax3.yaxis.set_label_position("right")
ax3.set_ylabel('$\mathcal{R}$ PPISN in SSP $(Gpc^{-3}yr^{-1})$', fontsize=15)

ax4.plot(z_binz3, MR_50_3,  label = 'Median rate')
#color_p1 = p1[0].get_color()
ind_min = 0
ax4.fill_between(z_binz3[ind_min:], MR_low_3[ind_min:], MR_up_3[ind_min:],  label = CI+'% C.I. ', alpha = 0.5)#,color = color_p1)
#ax4.plot(z_true_3[ind_min:], MRD_true_3[ind_min:],  label = 'Expected rate ', linestyle = '--')#color = color_p1
ax4.set_yscale('log')
ax4.set_ylim(10**0,10**5)
ax4.set_xlim(-0.8,15.8)
ax4.set_xlabel('Redshift (z)')
ax4.yaxis.tick_right()
ax4.yaxis.set_label_position("right")
ax4.set_ylabel('$\mathcal{R}$ PPISN in BSP $(Gpc^{-3}yr^{-1})$', fontsize=15)
ax4.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))
plt.setp(ax2.get_yticklabels()[0], visible=False) 
plt.setp(ax4.get_yticklabels()[0], visible=False) 
plt.setp(ax1.get_xticklabels(), visible=False)
plt.setp(ax3.get_xticklabels(), visible=False)
plt.legend(loc='upper center',frameon=False, bbox_to_anchor=(0.0, 1.2),ncol=2)

plt.show()

