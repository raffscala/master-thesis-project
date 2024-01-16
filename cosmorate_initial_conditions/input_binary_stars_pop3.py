import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import re

pd.options.mode.chained_assignment = None

##-----FUNCTIONS--------#


def lookfor_SN(logtext,kind): #function to look for a SN event in the logfile

  matchnum="[+|-]?[0-9]+\.?[0-9]*(?i:e)?[+|-]?[0-9]*|(?i:nan)"
  matchname="(?:[0-9|A-Za-z]*\_)?[0-9]*"
  matchid="[0-9]+"
  matchtype="[+|-]?\d+"
  
  regex_str = f"S;({matchname});({matchid});(SN);({matchnum});({matchnum}):({matchnum}):({matchnum}):({matchnum}):({matchnum}):({matchtype})" #string to find in the log file
  name_mask = re.findall(regex_str,logtext) #find all the entries corresponding to event_name in logfile_0
  #print(name_mask[0])  
  cols = ['S_name', 'IDs', 'event_s', 's_time', 'M_preSN', 'M_Hecore', 'M_COcore', 'M_remn', 'Remn_type', 'SN_type'] # single or binary, seed, ID, event type and time of the even
  df = pd.DataFrame(np.asarray(name_mask), columns=cols)
  df['S_name']=df['S_name'].astype(int)
  df = df.drop_duplicates(subset=("S_name","IDs"), keep="last")
  
  return df
  
  
  
def lookfor_merger(logtext,kind): #function to look for a merger event in the logfile

  matchnum="[+|-]?[0-9]+\.?[0-9]*(?i:e)?[+|-]?[0-9]*|(?i:nan)"
  matchname="(?:[0-9|A-Za-z]*\_)?[0-9]*"
  matchid="[0-9]+"
  matchtype="[+|-]?\d+"
  
  regex_str = f"B;({matchname});({matchid});(MERGER);({matchnum});({matchid}):({matchnum}):({matchnum}):({matchnum}):({matchtype}):({matchtype}):({matchnum}):({matchid}):({matchnum}):({matchnum}):({matchnum}):({matchtype}):({matchtype}):({matchnum}):({matchnum}):" #string we cant to find in the log file
  name_mask = re.findall(regex_str,logtext) #find all the entries corresponding to event_name in logfile_0
  cols = ["B_name", "IDb", "event_b", "b_time",'1','2','3','4','5','6','7','8','9','10','11','12','13','14','M_fin'] # single or binary, seed, ID, event type and time of the event
  #print(name_mask[0])
  df = pd.DataFrame(np.asarray(name_mask), columns=cols)
  df=df.drop(columns=['1','2','3','4','5','6','7','8','9','10','11','12','13','14'])
  #print(df)
  df['B_name']=df['B_name'].astype(int)
  
  return df
  
  
  
def analysis_pisn(dfSN,dfmerger):
  
  dfPISN=dfSN.loc[dfSN["SN_type"]=='4']
  dfpisn_after=dfPISN[dfPISN['S_name'].isin(dfmerger['B_name'])] #select in PISN df the systems that previously experienced merger
  dfpisn_before=dfPISN.drop(index=dfpisn_after.index)  #pisn occurring in systems not undergoing merger (consider also systems with double pisn)
  df_doublepisn=dfPISN[dfPISN['S_name'].duplicated(keep=False)]  #select the systems of binaries in which both stars undergo PISN
  
  return [dfPISN, dfpisn_after,dfpisn_before, df_doublepisn]
 
 
 
def analysis_ppisn(dfSN,dfmerger): 

  dfPPISN=dfSN.loc[dfSN["SN_type"]=='3']
  #print('dfppisn',dfPPISN)
  
  dfppisn_merger=dfPPISN[dfPPISN['S_name'].isin(dfmerger['B_name'])]  #select PPISN in systems that also merged 
  dfmerger_ppisn=dfmerger[dfmerger['B_name'].isin(dfPPISN['S_name'])]
  dfppisn_nomerger=dfPPISN.drop(index=dfppisn_merger.index)  #ppisn in systems not undergoing merger
  
  
  dfppisn_merger=dfppisn_merger.set_index('S_name') #reindexing
  dfmerger_ppisn=dfmerger_ppisn.set_index('B_name')  #reindexing
  
  dfmerged=pd.concat([dfppisn_merger,dfmerger_ppisn],axis=1,join='outer',ignore_index=False)
  dfmerged=dfmerged.reset_index(drop=False)
  dfmerged.rename(columns = {'index':'S_name'}, inplace = True)
  #dfdouble_e_merger=dfmerged[dfmerged['S_name'].duplicated(keep=False)]  #here we have both merger and more than one pisn

  dfmerger_before_ppisn=dfmerged.loc[dfmerged['s_time']>=dfmerged['b_time']]  #number of systems undergoing ppisn after merging
  
  dfmerger_after_ppisn=dfmerged.loc[dfmerged['b_time']>=dfmerged['s_time']]  #number of systems undergoing ppisn before merging
  
  df_doubleppisn=dfPPISN[dfPPISN['S_name'].duplicated(keep=False)]  #select the systems of binaries in which we have two PPISNe 
  
  dfdouble_e_merging=df_doubleppisn[df_doubleppisn['S_name'].isin(dfmerger['B_name'])]
  
  
  return [dfPPISN,dfppisn_nomerger, dfppisn_merger, dfmerger_ppisn,dfmerged, dfmerger_before_ppisn, dfmerger_after_ppisn, df_doubleppisn,dfdouble_e_merging]
  
  
  
def lookforMzams(evolved,kind,df): #look for M at ZAMS for  systems with no merger events
  
  #--DOUBLE EVENTS
  df_double=df[df.duplicated(subset='S_name',keep=False)]  #df where we only have double events
  evolved_double=evolved[evolved['name'].isin(df_double['S_name'])]  #input parameters of stars undergoing double events
  
    
  M0d=evolved_double[['Mass_0']]
  M1d=evolved_double[['Mass_1']]
  df_double['Mzams']=np.arange(len(df_double))
  df_double0=df_double.loc[df_double['IDs']==0]
  df_double1=df_double.loc[df_double['IDs']==1]
  df_double0['Mzams']=np.asarray(M0d)
  df_double1['Mzams']=np.asarray(M1d)
  df_double=pd.concat([df_double0,df_double1],axis=0)
  df_double=df_double.sort_index(ascending=True) #reorder the rows after the concat
  #print(df_double)
  
  
  #-SINGLE EVENTS
  df_nodouble=df.drop_duplicates(subset='S_name',keep=False) #df where we eliminated all double events
  #print(df_nodouble)
  evolved=evolved[evolved['name'].isin(df_nodouble['S_name'])]# #input parameters of stars without double events
  
    
  m=evolved[['Mass_0','Mass_1']]
  m['IDs']=np.asarray(df_nodouble['IDs'])  #the order of stars correspond since in both evolved and logfile the systems are disposed in the same order during the run
  M0=m[['Mass_0','IDs']].loc[m['IDs']==0]
  M0=M0.rename(columns={'Mass_0':'Mass'})
  M1=m[['Mass_1','IDs']].loc[m['IDs']==1]
  M1=M1.rename(columns={'Mass_1':'Mass'})
  Mzams=pd.concat([M0,M1],axis=0)
  Mzams=Mzams.sort_index(ascending=True)  #reorder the rows after the concat
  
  df_nodouble['Mzams']=np.asarray(Mzams['Mass'])
  
  
  

  df_nome=pd.concat([df_nodouble,df_double],axis=0)# consider all the cases with no merger
  df_nome=df_nome.sort_index(ascending=True)
  #print(df_nome)
  
  return [df_nome,df_double] # the second outcome gives the M_ZAMS for systems undergoing double PISN/PPISN 
  
  
  
  
def lookforMmerger(evolved,kind,df,df_merger): #add info about M_zams and mass after merger for systems undergoing PISN after merger

  evolved=evolved[evolved['name'].isin(df['S_name'])]
  
    
  m=evolved[['Mass_0','Mass_1']]
  print(len(m))
  print(len(df))
  df[['Mass_0','Mass_1']]=np.asarray(m)  #add the initial masses to the dataframe
  #print(evolved)
  #print(df)
  
  df_merger['B_name']=df_merger['B_name'].astype(int)
  df_merger=df_merger[df_merger['B_name'].isin(df['S_name'])]  #select systems both merging and exploding
  M_merged=df_merger['M_fin']
  
  #print(df_merger)
  df['Mass_merger']=np.asarray(M_merged)  #add mass of merger outcome to dataframe
  #print(df)
  
  return df
  
  
def lookforMmerger_ppisn(evolved,kind,df,df_merger): #add info about M_zams and mass after merger for systems undergoing PPISN after merger

  evolved=evolved[evolved['name'].isin(df['S_name'])]
    
  df_merger['B_name']=df_merger['B_name'].astype(int)
  df_merger=df_merger[df_merger['B_name'].isin(df['S_name'])]
  m=evolved[['Mass_0','Mass_1']]
  M_merged=df_merger['M_fin']
  df[['Mass_0','Mass_1']]=np.asarray(m)
  #print(df_merger)
  df['Mass_merger']=np.asarray(M_merged)
  #print(df)
  
  return df
  
  
def lookforMzams_bef(evolved,kind,df): #look for M at ZAMS for systems exploding before merger (is analogous to the case of no merger at all)
  
  evolved=evolved[evolved['name'].isin(df['S_name'])]
  
  m=evolved[['Mass_0','Mass_1']]
  m['IDs']=np.asarray(df['IDs'])

  M0=m[['Mass_0','IDs']].loc[m['IDs']==0]
  M0=M0.rename(columns={'Mass_0':'Mass'})
  M1=m[['Mass_1','IDs']].loc[m['IDs']==1]
  M1=M1.rename(columns={'Mass_1':'Mass'})
  
  Mzams=pd.concat([M0,M1],axis=0)
  Mzams=Mzams.sort_index(ascending=True)
  #print(Mzams)
  df['Mzams']=np.asarray(Mzams['Mass'])
  #print(df)
  
  return df
  
 
def gen_input_nome(df,path_old,path,kind,mtot): #generate input for systems not undergoing merger

  
  df=df[['s_time','M_preSN','S_name','IDs']]
  df=df.astype(float)
  df['IDs']=df['IDs'].astype(int)
  df['S_name']=df['S_name'].astype(int)
  df['s_time']=df['s_time']*int(1e6)
  df=lookforMzams(evolved,kind,df)[0]  #add a column with initial mass
  print(df)
  
  df.to_csv(path_old,sep=' ',index=False,header=False)
  open(path, "w").write(f"{mtot}\n" + open(path_old).read())  #write the input in a file with the total mass
  os.remove(path_old)
  
  
  return df
  
  
def gen_input_doub(df,path_old,path,kind,mtot): #generate input for systems with double PISN/PPISN

  
  df=df[['s_time','M_preSN','S_name','IDs']]
  df=df.astype(float)
  df['IDs']=df['IDs'].astype(int)
  df['S_name']=df['S_name'].astype(int)
  df['s_time']=df['s_time']*int(1e6)
  df=lookforMzams(evolved,kind,df)[1]  #add a column with initial mass for the double
  print(df)
  df.to_csv(path_old,sep=' ',index=False,header=False)
  
  open(path, "w").write(f"{mtot}\n" + open(path_old).read())
  os.remove(path_old)
  
  return df


def gen_input_bef(df,path_old,path,kind,mtot): #generate input for systems undergoing PISN/PPISN before merger 

  
  df=df[['s_time','M_preSN','S_name','IDs']]
  #print(df)
  df=df.astype(float)
  df['IDs']=df['IDs'].astype(int)
  df['S_name']=df['S_name'].astype(int)
  df['s_time']=df['s_time']*int(1e6)
  df=lookforMzams_bef(evolved,kind,df)
  print(df)
  df.to_csv(path_old,sep=' ',index=False,header=False)
 
  open(path, "w").write(f"{mtot}\n" + open(path_old).read())
  os.remove(path_old)
  
  return df


def gen_input_after_merger(df,df_merger,path_old,path,kind,mtot): #generate input for systems undergoing PISN after merger

  df=df[['s_time','M_preSN','S_name','IDs']]
  #print(df)
  df=df.astype(float)
  df['IDs']=df['IDs'].astype(int)
  df['S_name']=df['S_name'].astype(int)
  df['s_time']=df['s_time']*int(1e6)
  df=lookforMmerger(evolved,kind,df,df_merger)
  print(df)
  df.to_csv(path_old,sep=' ',index=False,header=False)
  
  open(path, "w").write(f"{mtot}\n" + open(path_old).read())
  os.remove(path_old)
  
  return df
  
  
  
def gen_input_after_merger_ppisn(df,df_merger,path_old,path,kind,mtot): #generate input for systems undergoing PPISN after merger

  df=df[['s_time','M_preSN','S_name','IDs']]
  #print(df)
  df=df.astype(float)
  df['IDs']=df['IDs'].astype(int)
  df['S_name']=df['S_name'].astype(int)
  df['s_time']=df['s_time']*int(1e6)
  df=lookforMmerger_ppisn(evolved,kind,df,df_merger)
  print(df)
  df.to_csv(path_old,sep=' ',index=False,header=False)

  open(path, "w").write(f"{mtot}\n" + open(path_old).read())
  os.remove(path_old)
  
  return df
  

def gen_input(df,path_old,path,kind,mtot):

  
  df=df[['s_time','M_preSN','S_name','IDs']]
  df=df.astype(float)
  df['IDs']=df['IDs'].astype(int)
  df['S_name']=df['S_name'].astype(int)
  df['s_time']=df['s_time']*int(1e6)
  print(df)
  df.to_csv(path_old,sep=' ',index=False,header=False)
  open(path, "w").write(f"{mtot}\n" + open(path_old).read())
  os.remove(path_old)
  
  
  return df
  
def resample(df,name,imf,model): #perform a resampling for the models that need it
  
  #MODIFY THE PATH WHERE THE INDEXES FOR RESAMPLING ARE STORED
  dfname=pd.read_csv(f"/data1/iorio/popIII/resampled_run/WOOSLEY/{imf}/SEVNSTABLE_WOOSLEY17_5_550_{model}/sevn_output_Z0.00000000001A1/resampled_named.dat",names=[name])
  #print(dfname)
  
  dff=df.merge(right=dfname,how='left',on=name)

  #print(dff)
  return dff
  

##-----------MAIN-----------##


Z = 1E-11
kind=['LAR1','LAR5','KRO1','KRO5','TOP1','TOP5','LOG1','LOG2','LOG3','LOG4','LOG5','LOG6','PAR1','PAR5']  #pop3 models


for i in range(len(kind)):
  print(kind[i])
  path_output = f"/home/scala/tesi/pop3_sevn_output/{kind[i]}/Z0.00000000001A1/"  ## MODIFY SEVN PATH
  logtext = open(f"{path_output}logfile.dat", "r").read()  ## MODIFY LOGFILE PATH
  evolved = pd.read_csv(f"{path_output}evolved.dat",sep='\s+')  ## MODIFY EVOLVED FILE PATH
  evolved['name']=evolved['name'].astype(int)
  
  dupli=evolved[evolved.duplicated(subset='name',keep=False)]
  evolved=evolved.drop_duplicates(subset='name',keep=False)
  
  dfSN = lookfor_SN(logtext,kind[i]) #look for SN  events  
  dfmerger=lookfor_merger(logtext,kind[i])  #look for  binary merger
  dfmerger_copy=dfmerger.copy()
  
  #RESAMPLING
  if len(dupli)>0:
    dfSN=dfSN[~dfSN['S_name'].isin(dupli['name'])]
    dfmerger=dfmerger[~dfmerger['B_name'].isin(dupli['name'])]
    dfmerger_copy=dfmerger_copy[~dfmerger_copy['B_name'].isin(dupli['name'])]
 
  if kind[i]=='KRO1' :
    dfSN=resample(dfSN,'S_name','KROUPA','KRO_1')
    dfmerger=resample(dfmerger,'B_name','KROUPA','KRO_1')
    dfmerger_copy=resample(dfmerger_copy,'B_name','KROUPA','KRO_1')
    evolved=resample(evolved,'name','KROUPA','KRO_1')
    mtot=1349500000.
  
  if kind[i]=='KRO5' :
    dfSN=resample(dfSN,'S_name','KROUPA','KRO_5')
    dfmerger=resample(dfmerger,'B_name','KROUPA','KRO_5')
    dfmerger_copy=resample(dfmerger_copy,'B_name','KROUPA','KRO_5')
    evolved=resample(evolved,'name','KROUPA','KRO_5')
    mtot=1522100000.
    
  if kind[i]=='LAR1' :
    dfSN=resample(dfSN,'S_name','LARSON','LAR_1')
    dfmerger=resample(dfmerger,'B_name','LARSON','LAR_1')
    dfmerger_copy=resample(dfmerger_copy,'B_name','LARSON','LAR_1')
    evolved=resample(evolved,'name','LARSON','LAR_1')
    mtot=1201400000.
    
  if kind[i]=='LAR5' :
    dfSN=resample(dfSN,'S_name','LARSON','LAR_5')
    dfmerger=resample(dfmerger,'B_name','LARSON','LAR_5')
    dfmerger_copy=resample(dfmerger_copy,'B_name','LARSON','LAR_5')
    evolved=resample(evolved,'name','LARSON','LAR_5')
    mtot=1300400000.

    
  ##--INPUT-PISN--##
  ## Modify paths
  
  path_pisn_before_old=f'/home/scala/tesi/cosmo_rate_public-v2/astromodel/popIII/{kind[i]}/input_bin_pisn_before/data_bin_PISNbefore_{Z}_old.txt' 
  path_pisn_before=f'/home/scala/tesi/cosmo_rate_public-v2/astromodel/popIII/{kind[i]}/input_bin_pisn_before/data_bin_PISNbefore_{Z}.txt'
  
  
  path_pisn_after_old=f'/home/scala/tesi/cosmo_rate_public-v2/astromodel/popIII/{kind[i]}/input_bin_pisn_after/data_bin_PISNafter_{Z}_old.txt'
  path_pisn_after=f'/home/scala/tesi/cosmo_rate_public-v2/astromodel/popIII/{kind[i]}/input_bin_pisn_after/data_bin_PISNafter_{Z}.txt'
  
  
  path_pisn_double_old=f'/home/scala/tesi/cosmo_rate_public-v2/astromodel/popIII/{kind[i]}/input_bin_pisn_double/data_bin_PISNdouble_{Z}_old.txt'
  path_pisn_double=f'/home/scala/tesi/cosmo_rate_public-v2/astromodel/popIII/{kind[i]}/input_bin_pisn_double/data_bin_PISNdouble_{Z}.txt'
  
  path_pisn_old=f'/home/scala/tesi/cosmo_rate_public-v2/astromodel/popIII/{kind[i]}/input_bin_pisn/data_bin_PISN_{Z}_old.txt'
  path_pisn=f'/home/scala/tesi/cosmo_rate_public-v2/astromodel/popIII/{kind[i]}/input_bin_pisn/data_bin_PISN_{Z}.txt'

  [dfPISN, dfpisn_after,dfpisn_before, df_doublepisn]=analysis_pisn(dfSN,dfmerger) 
  
  input_pisn_before=gen_input_nome(dfpisn_before,path_pisn_before_old,path_pisn_before,kind[i],mtot)  #pisn no merger
  
  input_pisn_double=gen_input_doub(df_doublepisn,path_pisn_double_old,path_pisn_double,kind[i],mtot)  #double pisn 
  
  input_pisn=gen_input(dfPISN,path_pisn_old,path_pisn,kind[i],mtot)
  

  
  
  ##--INPUT-PPISN--##
  
  
  path_ppisn_nomerger_old=f'/home/scala/tesi/cosmo_rate_public-v2/astromodel/popIII/{kind[i]}/input_bin_ppisn_nomerger/data_bin_PPISNnomerger_{Z}_old.txt' 
  path_ppisn_nomerger=f'/home/scala/tesi/cosmo_rate_public-v2/astromodel/popIII/{kind[i]}/input_bin_ppisn_nomerger/data_bin_PPISNnomerger_{Z}.txt'
  
  
  path_ppisn_double_old=f'/home/scala/tesi/cosmo_rate_public-v2/astromodel/popIII/{kind[i]}/input_bin_ppisn_double/data_bin_PPISNdouble_{Z}_old.txt'
  path_ppisn_double=f'/home/scala/tesi/cosmo_rate_public-v2/astromodel/popIII/{kind[i]}/input_bin_ppisn_double/data_bin_PPISNdouble_{Z}.txt'
  
  
  path_ppisn_before_old=f'/home/scala/tesi/cosmo_rate_public-v2/astromodel/popIII/{kind[i]}/input_bin_ppisn_before/data_bin_PPISNbefore_{Z}_old.txt'
  path_ppisn_before=f'/home/scala/tesi/cosmo_rate_public-v2/astromodel/popIII/{kind[i]}/input_bin_ppisn_before/data_bin_PPISNbefore_{Z}.txt'
  
  path_ppisn_after_old=f'/home/scala/tesi/cosmo_rate_public-v2/astromodel/popIII/{kind[i]}/input_bin_ppisn_after/data_bin_PPISafter_{Z}_old.txt'
  path_ppisn_after=f'/home/scala/tesi/cosmo_rate_public-v2/astromodel/popIII/{kind[i]}/input_bin_ppisn_after/data_bin_PPISNafter_{Z}.txt'
  
  path_ppisn_old=f'/home/scala/tesi/cosmo_rate_public-v2/astromodel/popIII/{kind[i]}/input_bin_ppisn/data_bin_PPISN_{Z}_old.txt'
  path_ppisn=f'/home/scala/tesi/cosmo_rate_public-v2/astromodel/popIII/{kind[i]}/input_bin_ppisn/data_bin_PPISN_{Z}.txt'
  
  [dfPPISN,dfppisn_nomerger, dfppisn_merger, dfmerger_ppisn,dfmerged, dfmerger_before_ppisn, dfmerger_after_ppisn, df_doubleppisn,dfdouble_e_merging]=analysis_ppisn(dfSN,dfmerger)
  
  input_ppisn_nomerger=gen_input_nome(dfppisn_nomerger,path_ppisn_nomerger_old,path_ppisn_nomerger,kind[i],mtot)  #no merger

  input_ppisn_double=gen_input_doub(df_doubleppisn,path_ppisn_double_old,path_ppisn_double,kind[i],mtot)  #double pisn 
  
  input_ppisn_before=gen_input_bef(dfmerger_after_ppisn,path_ppisn_before_old,path_ppisn_before,kind[i],mtot)  #we have merger and ppisn occurs before merger
 
  input_ppisn_after=gen_input_after_merger_ppisn(dfmerger_before_ppisn,dfmerger_copy,path_ppisn_after_old,path_ppisn_after,kind[i],mtot)  #we have merger and ppisn occurs after merger
  
  input_ppisn=gen_input(dfPPISN,path_ppisn_old,path_ppisn,kind[i],mtot)
  
  input_pisn_after=gen_input_after_merger(dfpisn_after,dfmerger,path_pisn_after_old,path_pisn_after,kind[i],mtot)  #pisn after merger
  
  
