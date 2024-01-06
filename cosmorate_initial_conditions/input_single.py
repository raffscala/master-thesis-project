import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import re

#pd.options.mode.chained_assignment = None

def lookfor_SN(logtext,Z): #function to look for a SN event in the logfile

  matchnum="[+|-]?[0-9]+\.?[0-9]*(?i:e)?[+|-]?[0-9]*|(?i:nan)"
  matchname="(?:[0-9|A-Za-z]*\_)?[0-9]*"
  matchid="[0-9]+"
  matchtype="[+|-]?\d+"
  regex_str = f"S;({matchname});({matchid});(SN);({matchnum});({matchnum}):({matchnum}):({matchnum}):({matchnum}):({matchnum}):({matchtype})" #string to find in the log file
  
  name_mask = re.findall(regex_str,logtext) #find all the entries corresponding to event_name in logfile_0
  #print(name_mask[0])  
  cols = ['S_name', 'IDs', 'event_s', 's_time', 'M_preSN', 'M_Hecore', 'M_COcore', 'M_remn', 'Remn_type', 'SN_type'] # single or binary, seed, ID, event type and time of the even
  df = pd.DataFrame(np.asarray(name_mask), columns=cols)
  df = df.drop_duplicates(subset=("S_name","IDs"), keep="last")
  
  return df
  


def gen_input(evolved,df,path_old,path,Z,mtot):

  
  df=df[['s_time','M_preSN','S_name','IDs']]
  df=df.astype(float)
  df['IDs']=df['IDs'].astype(int)
  df['S_name']=df['S_name'].astype(int)
  df['s_time']=df['s_time']*int(1e6)
  
  evolved=evolved[(evolved['#ID'].isin(df['IDs'])) & (evolved['name'].isin(df['S_name']))]
  
  M=np.array(evolved['Mass'])
  df['Mzams']=M
  
  df.to_csv(path_old,sep=' ',index=False,header=False) #store the colums in file
  open(path, "w").write(f"{mtot}\n" + open(path_old).read()) #write the column on a new file with also the total mass
  os.remove(path_old) #remove the old file
  
  
  return df
  

##-----------MAIN-----------##


Z = [1E-11, 1E-6 , 0.0001, 0.0002, 0.0004, 0.0005, 0.0006, 0.0008, 0.001, 0.002, 0.004,0.005, 0.008, 0.01, 0.014, 0.017]



for i in range(len(Z)):

  Zs=str(Z[i])

  
  path_output = f"/home/scala/tesi/sevn-SEVN/output_sing_KRO1_pureHE/Z{Zs}" ## MODIFY PATH
  logtext = open(f"{path_output}/logfile.dat", "r").read()  ## MODIFY LOGFILE PATH
  evolved = pd.read_csv(f"{path_output}/evolved.dat",sep='\s+')   ## MODIFY EVOLVED FILE PATH
    
  
  mtot=evolved['Mass'].astype(float).sum()
  
  dfSN = lookfor_SN(logtext,Zs) #look for SN  events
 
  dfPISN=dfSN.loc[dfSN["SN_type"]=='4']
  
  dfPPISN=dfSN.loc[dfSN["SN_type"]=='3']
  
  ## MODIFY PATHS WHERE TO STORE INITIAL CONDITIONS
  
  path_pisn_old=f'/home/scala/tesi/cosmo_rate_public-v2/astromodel/popI_II/A3/pure_he/input_sing_pisn/data_sing_PISN_{Zs}_old.txt'  
  path_pisn=f'/home/scala/tesi/cosmo_rate_public-v2/astromodel/popI_II/A3/pure_he/input_sing_pisn/data_sing_PISN_{Zs}.txt'

  path_ppisn_old=f'/home/scala/tesi/cosmo_rate_public-v2/astromodel/popI_II/A3/pure_he/input_sing_ppisn/data_sing_PPISN_{Zs}_old.txt'
  path_ppisn=f'/home/scala/tesi/cosmo_rate_public-v2/astromodel/popI_II/A3/pure_he/input_sing_ppisn/data_sing_PPISN_{Zs}.txt'
  
  
  input_pisn= gen_input(evolved,dfPISN,path_pisn_old,path_pisn,Zs,mtot)
  input_ppisn= gen_input(evolved,dfPPISN,path_ppisn_old,path_ppisn,Zs,mtot)
