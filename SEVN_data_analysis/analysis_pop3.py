import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import re

#-----FUNCTIONS------#



def lookfor_SN(logtext,kind): #function to look for a SN event in the logfile

  matchnum="[+|-]?[0-9]+\.?[0-9]*(?i:e)?[+|-]?[0-9]*|(?i:nan)"
  matchname="(?:[0-9|A-Za-z]*\_)?[0-9]*"
  matchid="[0-9]+"
  matchtype="[+|-]?\d+"
  regex_str = f"S;({matchname});({matchid});(SN);({matchnum});({matchnum}):({matchnum}):({matchnum}):({matchnum}):({matchnum}):({matchtype})" #string to find in the log file
  
  name_mask = re.findall(regex_str,logtext) #find all the entries corresponding to event_name in logfile_0
  #print(name_mask[0])  
  cols = ['S_name', 'ID', 'event', 's_time', 'M_preSN', 'M_Hecore', 'M_COcore', 'M_remn', 'Remn_type', 'SN_type'] # single or binary, seed, ID, event type and time of the even
  df = pd.DataFrame(np.asarray(name_mask), columns=cols)
  df['S_name']=df['S_name'].astype(int)
  df = df.drop_duplicates(subset=("S_name","ID"), keep="last")
  
  return df
  
  
  
def lookfor_merger(logtext,kind): #function to look for a merger event in the logfile

  
  matchnum="[+|-]?[0-9]+\.?[0-9]*(?i:e)?[+|-]?[0-9]*|(?i:nan)"
  matchname="(?:[0-9|A-Za-z]*\_)?[0-9]*"
  matchid="[0-9]+"
  matchtype="[+|-]?\d+"
  regex_str = f"B;({matchname});({matchid});(MERGER);({matchnum});" #string we cant to find in the log file
  
  name_mask = re.findall(regex_str,logtext) #find all the entries corresponding to event_name in logfile_0
  cols = ["B_name", "ID", "event", "b_time"] # single or binary, seed, ID, event type and time of the event
  #print(name_mask[0])
  df = pd.DataFrame(np.asarray(name_mask), columns=cols)
  df['B_name']=df['B_name'].astype(int)
  return df
  
  
  
def analyses_pisn(dfSN,dfmerger):
  
  dfPISN=dfSN.loc[dfSN["SN_type"]=='4']
  dfpisn_after=dfPISN[dfPISN['S_name'].isin(dfmerger['B_name'])] #select in PISN df the systems that previously experienced merger(CAN'T EXPERIENCE AFTER BECAUSE PISNe LEAVE NO REMNANT)
  dfpisn_before=dfPISN.drop(index=dfpisn_after.index)  #pisn occurring in systems not undergoing merger (consider also systems with double pisn)
  df_doublepisn=dfPISN[dfPISN['S_name'].duplicated(keep=False)]  #select the systems of binaries in which both stars undergo PISN
  
  return [dfPISN, dfpisn_after,dfpisn_before, df_doublepisn]
 
 
def analyses_ppisn(dfSN,dfmerger): 

  dfPPISN=dfSN.loc[dfSN["SN_type"]=='3']
  
  dfppisn_merger=dfPPISN[dfPPISN['S_name'].isin(dfmerger['B_name'])]  #select PPISN in systems that also merged (the number of ppisne can be also more than one, so this df can be larger than the following)
  dfmerger_ppisn=dfmerger[dfmerger['B_name'].isin(dfPPISN['S_name'])]
  
  dfppisn_nomerger=dfPPISN.drop(index=dfppisn_merger.index)  #ppisn in systems not undergoing merger (a subgroup of this is the doubleppisn)
  
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
  
  
def resample(df,name,imf,model):  #This function resample the dataset if it is needed
  
  print(df)
  dfname=pd.read_csv(f"/data1/iorio/popIII/resampled_run/WOOSLEY/{imf}/SEVNSTABLE_WOOSLEY17_5_550_{model}/sevn_output_Z0.00000000001A1/resampled_named.dat",names=[name])
  print(dfname)
  
  dff=df.merge(right=dfname,how='left',on=name)
  print(dff)
  
  return dff
  

###-----MAIN-----###


Z = [1E-11]
kind=['KRO1','KRO5','LAR1','LAR5','PAR1','PAR5','TOP1','TOP5','LOG1','LOG2','LOG3','LOG4','LOG5','LOG6',]


Za=np.array(Z)
Zs=Za.astype(str)

dfrate = pd.DataFrame(columns=["Type", "N_SN", 'N_CCSN', 'N_PISN',"rate_PISN_%", "rate_PISN_to_CCSN_%",'N_PPISN', "rate_PPISN_%",'rate_PPISN_to_CCSN_%'])
df_PISN=pd.DataFrame(columns=['Type','SN','PISN','Merger','PISN_after_merger', 'Double_PISN'])
df_PPISN=pd.DataFrame(columns=['Type','SN','PPISN','Merger','PPISN_no_merger', 'Double_PPISN','PPISN_and_merger','PPISN_after_merger','PPISN_before_merger'])


for i in range(len(kind)):
  print(kind[i])
  
  path = f"/home/scala/tesi/pop3_sevn_output/{kind[i]}/Z0.00000000001A1/"
  logtext = open(f"{path}/logfile.dat", "r").read()
  dfSN = lookfor_SN(logtext,kind[i]) #look for SN  events
  dfmerger=lookfor_merger(logtext,kind[i])  #look for  binary merger
  
  #The resample is needed for this four models
  if kind[i]=='KRO1' :
    dfSN=resample(dfSN,'S_name','KROUPA','KRO_1')
    dfmerger=resample(dfmerger,'B_name','KROUPA','KRO_1')
  
  if kind[i]=='KRO5' :
    dfSN=resample(dfSN,'S_name','KROUPA','KRO_5')
    dfmerger=resample(dfmerger,'B_name','KROUPA','KRO_5')
    
  if kind[i]=='LAR1' :
    dfSN=resample(dfSN,'S_name','LARSON','LAR_1')
    dfmerger=resample(dfmerger,'B_name','LARSON','LAR_1')
    
  if kind[i]=='LAR5' :
    dfSN=resample(dfSN,'S_name','LARSON','LAR_5')
    dfmerger=resample(dfmerger,'B_name','LARSON','LAR_5')
 
  ##---PISN---##
  [dfPISN, dfpisn_after,dfpisn_before, df_doublepisn]=analyses_pisn(dfSN,dfmerger)
  
  ##----PPISN-----##
  [dfPPISN, dfppisn_merger, dfmerger_ppisn,dfmerged, dfmerger_before_ppisn, dfmerger_after_ppisn, df_doubleppisn,dfdouble_e_merging,dfppisn_nomerger]=analyses_ppisn(dfSN,dfmerger)
 
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
  N_doubleppisn_e_merger=len(dfdouble_e_merging)/int(2)  ##number of systems in which we have double ppisn and also merger (is 0 at alla Z)
  
  N_CCSN = len(dfSN.loc[dfSN["SN_type"]=='2'])
 
  rate_PISN = N_PISN/N_SN
  rate_PPISN = N_PPISN/N_SN
  rate_PISN_to_CCSN = N_PISN/N_CCSN
  rate_PPISN_to_CCSN = N_PPISN/N_CCSN
  
  temp = [f'{kind[i]}', N_SN,N_CCSN,N_PISN, f"{rate_PISN*100:.2f}",f"{rate_PISN_to_CCSN*100:.2f}",N_PPISN, f"{rate_PPISN*100:.2f}",f"{rate_PPISN_to_CCSN*100:.2f}"]
  temp1=[kind[i],int(N_SN), int(N_PISN),int(N_merger), int(N_PISN_after_merge), int(N_doublepisn)]
  temp2=[kind[i],int(N_SN), int(N_PPISN),int(N_merger), int(N_ppisn_nomerger),int(N_doubleppisn), int(N_ppisn_merger),int(N_merger_bef_ppisn),int(N_merger_aft_ppisn)]
  
  
  dfrate.loc[len(dfrate)] = temp
  df_PISN.loc[len(df_PISN)]=temp1
  df_PPISN.loc[len(df_PPISN)]=temp2
  
  
#MODIFY TABLES PATHS
dfrate.to_excel("/home/scala/tesi/analisi_dati_sevn/tabelle_output/tabelle_sevn_pop3/binary_rates_resample.xlsx",float_format='%.f',index=False)
df_PISN.to_excel("/home/scala/tesi/analisi_dati_sevn/tabelle_output/tabelle_sevn_pop3/PISN_binary_resample.xlsx",index=False)
df_PPISN.to_excel("/home/scala/tesi/analisi_dati_sevn/tabelle_output/tabelle_sevn_pop3/PPISN_binary_resample.xlsx",index=False)










