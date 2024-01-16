import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import re

#-----FUNCTIONS------#


def lookfor_SN(logtext,Z): #function to look for a SN event in the logfile

  matchnum="[+|-]?[0-9]+\.?[0-9]*(?i:e)?[+|-]?[0-9]*|(?i:nan)"
  matchname="(?:[0-9|A-Za-z]*\_)?[0-9]*"
  matchid="[0-9]+"
  matchtype="[+|-]?\d+"
  regex_str = f"S;({matchname});({matchid});(SN);({matchnum});({matchnum}):({matchnum}):({matchnum}):({matchnum}):({matchnum}):({matchtype})" #string to find in the log file

  name_mask = re.findall(regex_str,logtext) #find all the entries corresponding to event_name in logfile_0
  
  cols = ['S_name', 'ID', 'event', 's_time', 'M_preSN', 'M_Hecore', 'M_COcore', 'M_remn', 'Remn_type', 'SN_type'] # single or binary, seed, ID, event type and time of the even
  df = pd.DataFrame(np.asarray(name_mask), columns=cols)
  df = df.drop_duplicates(subset=("S_name","ID"), keep="last")
  
  return df
  
  
  
def lookfor_merger(logtext,Z): #function to look for a merger event in the logfile

  matchnum="[+|-]?[0-9]+\.?[0-9]*(?i:e)?[+|-]?[0-9]*|(?i:nan)"
  matchname="(?:[0-9|A-Za-z]*\_)?[0-9]*"
  matchid="[0-9]+"
  matchtype="[+|-]?\d+"
  regex_str = f"B;({matchname});({matchid});(MERGER);({matchnum});" #string we cant to find in the log file
  name_mask = re.findall(regex_str,logtext) #find all the entries corresponding to event_name in logfile_0
  cols = ["B_name", "ID", "event", "b_time"] # single or binary, seed, ID, event type and time of the event

  df = pd.DataFrame(np.asarray(name_mask), columns=cols)
  
  return df
  
  
  
def analysis_pisn(dfSN,dfmerger):
  
  dfPISN=dfSN.loc[dfSN["SN_type"]=='4']
  
  dfpisn_after=dfPISN[dfPISN['S_name'].isin(dfmerger['B_name'])] #select in PISN df the systems that previously experienced merger(CAN'T EXPERIENCE AFTER BECAUSE PISNe LEAVE NO REMNANT)
  dfpisn_before=dfPISN.drop(index=dfpisn_after.index)  #pisn occurring in systems not undergoing merger (consider also systems with double pisn)
  
  df_doublepisn=dfPISN[dfPISN['S_name'].duplicated(keep=False)]  #select the systems of binaries in which both stars undergo PISN
  
  return [dfPISN, dfpisn_after,dfpisn_before, df_doublepisn]
 
 
def analysis_ppisn(dfSN,dfmerger): 

  dfPPISN=dfSN.loc[dfSN["SN_type"]=='3']
  
  dfppisn_merger=dfPPISN[dfPPISN['S_name'].isin(dfmerger['B_name'])]  #select PPISN in systems that also merged 
  dfmerger_ppisn=dfmerger[dfmerger['B_name'].isin(dfPPISN['S_name'])]
  
  dfppisn_nomerger=dfPPISN.drop(index=dfppisn_merger.index)  #ppisn in systems not undergoing merger 
  
  dfppisn_merger=dfppisn_merger.set_index('S_name') #reindexing
  dfmerger_ppisn=dfmerger_ppisn.set_index('B_name')  #reindexing
  
  dfmerged=pd.concat([dfppisn_merger,dfmerger_ppisn],axis=1,join='outer',ignore_index=False)
  dfmerged=dfmerged.reset_index(drop=False)
  dfmerged.rename(columns = {'index':'S_name'}, inplace = True)

  
  
  dfmerger_before_ppisn=dfmerged.loc[dfmerged['s_time']>=dfmerged['b_time']]  #numb of systems undergoing ppisn after merging
  dfmerger_after_ppisn=dfmerged.loc[dfmerged['b_time']>=dfmerged['s_time']]  #numb of systems undergoing ppisn before merging
  
  df_doubleppisn=dfPPISN[dfPPISN['S_name'].duplicated(keep=False)]  #select the systems of binaries in which we have two PPISNe 
  
  dfdouble_e_merging=df_doubleppisn[df_doubleppisn['S_name'].isin(dfmerger['B_name'])] 
  print(len(dfdouble_e_merging))
 
  
  
  return [dfPPISN, dfppisn_merger, dfmerger_ppisn,dfmerged, dfmerger_before_ppisn, dfmerger_after_ppisn, df_doubleppisn,dfdouble_e_merging,dfppisn_nomerger]
  

###-----MAIN-----###


Z =  [1E-11, 1E-6, 0.0001, 0.0002, 0.0004, 0.0005, 0.0006, 0.0008, 0.001, 0.002, 0.004, 0.005, 0.008, 0.01, 0.014, 0.017]



dfrate = pd.DataFrame(columns=["Z", "N_SN", 'N_CCSN', 'N_PISN',"rate_PISN_%", "rate_PISN_to_CCSN_%",'N_PPISN', "rate_PPISN_%",'rate_PPISN_to_CCSN_%'])
df_PISN=pd.DataFrame(columns=['Z','SN','PISN','Merger','PISN_after_merger', 'Double_PISN'])
df_PPISN=pd.DataFrame(columns=['Z','SN','PPISN','Merger','PPISN_and_merger','PPISN_after_merger','PPISN_before_merger','PPISN_no_merger', 'Double_PPISN'])


for i in range(len(Z)):
  print(Z[i])
  Zs=str(Z[i])
  path_output = f"//home/scala/tesi/sevn-SEVN/output_bin_KRO1/Z{Zs}"  ## MODIFY SEVN OUTPATH
  logtext = open(f"{path_output}/logfile.dat", "r").read()  ## MODIFY LOGFILE PATH
  
  dfSN = lookfor_SN(logtext,Zs) #look for SN  events
  dfmerger=lookfor_merger(logtext,Zs)  #look for  binary merger
 
 
  ##---PISN---##
  [dfPISN, dfpisn_after,dfpisn_before, df_doublepisn]=analysis_pisn(dfSN,dfmerger)
  
  ##----PPISN-----##
  [dfPPISN, dfppisn_merger, dfmerger_ppisn,dfmerged, dfmerger_before_ppisn, dfmerger_after_ppisn, df_doubleppisn,dfdouble_e_merging,dfppisn_nomerger]=analysis_ppisn(dfSN,dfmerger)
 
  N_SN = len(dfSN)
  N_merger=len(dfmerger)
  
  N_PISN = len(dfSN.loc[dfSN["SN_type"]=='4'])
  N_PISN_after_merge=len(dfpisn_after)
  N_doublepisn=len(df_doublepisn)/int(2) #number of systems in which we have double PISNe 
  
  N_PPISN = len(dfPPISN)
  N_ppisn_merger=len(dfppisn_merger) #number of ppisn occurred in systems that also merged
  N_ppisn_nomerger=len(dfppisn_nomerger)
  N_merger_aft_ppisn=len(dfmerger_after_ppisn)  #number of ppisn occurred before merger
  N_merger_bef_ppisn=len(dfmerger_before_ppisn)  #number of ppisn occurred after merger
  N_doubleppisn=len(df_doubleppisn)/int(2)  #number of systems in which we have double ppisn
  N_doubleppisn_e_merger=len(dfdouble_e_merging)/int(2)  #number of systems in which we have double ppisn and also merger ì
  
  N_CCSN = len(dfSN.loc[dfSN["SN_type"]=='2'])
 
  rate_PISN = N_PISN/N_SN
  rate_PPISN = N_PPISN/N_SN
  rate_PISN_to_CCSN = N_PISN/N_CCSN
  rate_PPISN_to_CCSN = N_PPISN/N_CCSN
  
  temp = [f'{Z[i]}', N_SN,N_CCSN,N_PISN, f"{rate_PISN*100:.2f}",f"{rate_PISN_to_CCSN*100:.2f}",N_PPISN, f"{rate_PPISN*100:.2f}",f"{rate_PPISN_to_CCSN*100:.2f}"]
  temp1=[Z[i],int(N_SN), int(N_PISN),int(N_merger), int(N_PISN_after_merge), int(N_doublepisn)]
  temp2=[Z[i],int(N_SN), int(N_PPISN),int(N_merger), int(N_ppisn_merger),int(N_merger_bef_ppisn),int(N_merger_aft_ppisn), int(N_ppisn_nomerger),int(N_doubleppisn)]
  
  
  dfrate.loc[len(dfrate)] = temp
  df_PISN.loc[len(df_PISN)]=temp1
  df_PPISN.loc[len(df_PPISN)]=temp2

  
   ## MODIFY TABLES PATH
dfrate.to_excel("/home/scala/tesi/analisi_dati_sevn/tabelle_output/tabelle_sevn_kro1/binary_rates_kro1.xlsx",float_format='%.f',index=False)  
df_PISN.to_excel("/home/scala/tesi/analisi_dati_sevn/tabelle_output/tabelle_sevn_kro1/PISN_binary_kro1.xlsx",index=False)
df_PPISN.to_excel("/home/scala/tesi/analisi_dati_sevn/tabelle_output/tabelle_sevn_kro1/PPISN_binary_kro1.xlsx",index=False)









