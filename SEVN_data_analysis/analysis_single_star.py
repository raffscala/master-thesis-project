import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import re

#----------------------------------------------------------------------------------------------------

def lookfor_SN(Z): #function to look for a given event in the logfile
  path = f"/home/scala/tesi/sevn-SEVN/output_sing_KRO1/Z{Z}" ## MODIFICARE PATH DEGLI OUTPUT DI SEVN 
  matchnum="[+|-]?[0-9]+\.?[0-9]*(?i:e)?[+|-]?[0-9]*|(?i:nan)"
  matchname="(?:[0-9|A-Za-z]*\_)?[0-9]*"
  matchid="[0-9]+"
  matchtype="[+|-]?\d+"

  regex_str = f"S;({matchname});({matchid});(SN);({matchnum});({matchnum}):({matchnum}):({matchnum}):({matchnum}):({matchnum}):({matchtype})" #string to find in the log file
    
  logtext = open(f"{path}/logfile.dat", "r").read() ## MODIFY  PATH
  name_mask = re.findall(regex_str,logtext) #find all the entries corresponding to event_name in logfile_0
  #print(name_mask[0])  
  cols = ['N_name', 'ID', 'event', 'time', 'M_preSN', 'M_Hecore', 'M_COcore', 'M_remn', 'Remn_type', 'SN_type'] # single or binary, seed, ID, event type and time of the event
  df = pd.DataFrame(np.asarray(name_mask), columns=cols)
  df = df.drop_duplicates(subset=("N_name","ID"), keep="last")
  return df
 
#---------------------------------------------------------------------------------------------------------


Z = [1E-11, 1E-06, 0.0001, 0.0002, 0.0004, 0.0005, 0.0006, 0.0008, 0.001, 0.002, 0.004, 0.005, 0.008, 0.01, 0.014, 0.017]


cols = ["Z", "N_SN", 'N_CCSN', 'N_PISN',"rate_PISN_%", "rate_PISN_to_CCSN_%",'N_PPISN', "rate_PPISN_%",'rate_PPISN_to_CCSN_%']
dfout = pd.DataFrame(columns=cols)

for i in range(len(Z)):
  
  Zs=str(Z[i])
  df = lookfor_SN(Zs) #look for SN  events
  print(len(df))
  
  N_SN = len(df['N_name'])
  N_PPISN = len(df.loc[df["SN_type"]=='3'])
  N_PISN = len(df.loc[df["SN_type"]=='4'])
  N_CCSN = len(df.loc[df["SN_type"]=='2'])
  
  rate_PISN = N_PISN/N_SN
  rate_PPISN = N_PPISN/N_SN
  rate_PISN_to_CCSN = N_PISN/N_CCSN
  rate_PPISN_to_CCSN = N_PPISN/N_CCSN
  temp = [f'{Z[i]}', N_SN,N_CCSN,N_PISN, f"{rate_PISN*100:.2f}",f"{rate_PISN_to_CCSN*100:.2f}",N_PPISN, f"{rate_PPISN*100:.2f}",f"{rate_PPISN_to_CCSN*100:.2f}"]
  dfout.loc[len(dfout)] = temp
  
  
     
##MODIFY PATH

dfout.to_excel("/home/scala/tesi/analisi_dati_sevn/tabelle_output/tabelle_sevn_kro1/single_rates_kro1.xlsx",float_format='%.f',index=False) 


