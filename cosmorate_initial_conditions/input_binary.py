import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import re

pd.options.mode.chained_assignment = None

##-----FUNCTIONS--------#


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
  
  
  
def lookfor_merger(logtext,Z): #function to look for a merger event in the logfile

  matchnum="[+|-]?[0-9]+\.?[0-9]*(?i:e)?[+|-]?[0-9]*|(?i:nan)"
  matchname="(?:[0-9|A-Za-z]*\_)?[0-9]*"
  matchid="[0-9]+"
  matchtype="[+|-]?\d+"
  
  regex_str = f"B;({matchname});({matchid});(MERGER);({matchnum});({matchid}):({matchnum}):({matchnum}):({matchnum}):({matchtype}):({matchtype}):({matchnum}):({matchid}):({matchnum}):({matchnum}):({matchnum}):({matchtype}):({matchtype}):({matchnum}):({matchnum}):" #string we cant to find in the log file
  name_mask = re.findall(regex_str,logtext) #find all the entries corresponding to event_name in logfile_0
  cols = ["B_name", "IDb", "event_b", "b_time",'1','2','3','4','5','6','7','8','9','10','11','12','13','14','M_fin'] # single or binary, seed, ID, event type and time of the event
  df = pd.DataFrame(np.asarray(name_mask), columns=cols)
  df=df.drop(columns=['1','2','3','4','5','6','7','8','9','10','11','12','13','14'])
 
  
  return df
  
  
  
def analysis_pisn(dfSN,dfmerger):
  
  dfPISN=dfSN.loc[dfSN["SN_type"]=='4']
  dfpisn_after=dfPISN[dfPISN['S_name'].isin(dfmerger['B_name'])] #select in PISN df the systems that previously experienced merger
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
  
  
  return [dfPPISN,dfppisn_nomerger, dfppisn_merger, dfmerger_ppisn,dfmerged, dfmerger_before_ppisn, dfmerger_after_ppisn, df_doubleppisn,dfdouble_e_merging]
  
  
  
def lookforMzams(evolved,Z,df): #look for M at ZAMS for  systems with no merger events
  
  #--DOUBLE EVENTS
  df_double=df[df.duplicated(subset='S_name',keep=False)]  #df where we only have double events
  evolved_double=evolved[evolved['name'].isin(df_double['S_name'])]  #input parameters of stars undergoing double events
  
  dupli_double=evolved_double[evolved_double.duplicated(subset='name',keep=False)]
  evolved_double=evolved_double.drop_duplicates(subset='name',keep=False)
  if len(dupli_double)>0:
    df_double=df_double[~df_double['S_name'].isin(dupli_double['name'])]
  
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
  
  dupli=evolved[evolved.duplicated(subset='name',keep=False)]
  print(dupli)
  print(df_nodouble)
  evolved=evolved.drop_duplicates(subset='name',keep=False)
  if len(dupli)>0:
    df_nodouble=df_double[~df_nodouble['S_name'].isin(dupli['name'])]
  print(df_nodouble)
  
  m=evolved[['Mass_0','Mass_1']]
  m['IDs']=np.asarray(df_nodouble['IDs'])  #the order of stars correspond since in both evolved and logfile the systems are disposed in the same order during the run
  M0=m[['Mass_0','IDs']].loc[m['IDs']==0]
  M0=M0.rename(columns={'Mass_0':'Mass'})
  M1=m[['Mass_1','IDs']].loc[m['IDs']==1]
  M1=M1.rename(columns={'Mass_1':'Mass'})
  Mzams=pd.concat([M0,M1],axis=0)
  Mzams=Mzams.sort_index(ascending=True)  #reorder the rows after the concat
  #print(Mzams)
  df_nodouble['Mzams']=np.asarray(Mzams['Mass'])
  #print(df_nodouble)
  
  

  df_nome=pd.concat([df_nodouble,df_double],axis=0)# consider all the cases with no merger
  df_nome=df_nome.sort_index(ascending=True)
  #print(df_nome)
  
  return [df_nome,df_double] # the second outcome gives the M_ZAMS for systems undergoing double PISN/PPISN 
  
  
  
  
def lookforMmerger(evolved,Z,df,df_merger): #add info about M_zams and mass after merger for systems undergoing PISN after merger

  evolved=evolved[evolved['name'].isin(df['S_name'])]
  
  dupli=evolved[evolved.duplicated(subset='name',keep=False)]
  print(dupli)
  print(df)
  evolved=evolved.drop_duplicates(subset='name',keep=False)
  if len(dupli)>0:
    df=df[~df['S_name'].isin(dupli['name'])]
   
  print(df)
  m=evolved[['Mass_0','Mass_1']]
  df[['Mass_0','Mass_1']]=np.asarray(m)  #add the initial masses to the dataframe

  
  df_merger['B_name']=df_merger['B_name'].astype(int)
  df_merger=df_merger[df_merger['B_name'].isin(df['S_name'])]  #select systems both merging and exploding
  M_merged=df_merger['M_fin']
  
  df['Mass_merger']=np.asarray(M_merged)  #add mass of merger outcome to dataframe
  
  return df
  
  
def lookforMmerger_ppisn(evolved,Z,df,df_merger): #add info about M_zams and mass after merger for systems undergoing PPISN after merger

  evolved=evolved[evolved['name'].isin(df['S_name'])]
  
  dupli=evolved[evolved.duplicated(subset='name',keep=False)]
  print(dupli)
  print(df)
  evolved=evolved.drop_duplicates(subset='name',keep=False)
  if len(dupli)>0:
    df=df[~df['S_name'].isin(dupli['name'])]
   
  print(df)
  
  m=evolved[['Mass_0','Mass_1']]
  
  
  df[['Mass_0','Mass_1']]=np.asarray(m)
  
  df_merger['B_name']=df_merger['B_name'].astype(int)
  df_merger=df_merger[df_merger['B_name'].isin(df['S_name'])]
  M_merged=df_merger['M_fin']
  df['Mass_merger']=np.asarray(M_merged)
  
  return df
  
  
def lookforMzams_bef(evolved,Z,df): #look for M at ZAMS for systems exploding before merger 
  
  evolved=evolved[evolved['name'].isin(df['S_name'])]
  
  dupli=evolved[evolved.duplicated(subset='name',keep=False)]
  print(dupli)
  print(df)
  evolved=evolved.drop_duplicates(subset='name',keep=False)
  if len(dupli)>0:
    df=df[~df['S_name'].isin(dupli['name'])]
     
  print(df)
  
  m=evolved[['Mass_0','Mass_1']]
  m['IDs']=np.asarray(df['IDs'])

  M0=m[['Mass_0','IDs']].loc[m['IDs']==0]
  M0=M0.rename(columns={'Mass_0':'Mass'})
  M1=m[['Mass_1','IDs']].loc[m['IDs']==1]
  M1=M1.rename(columns={'Mass_1':'Mass'})
  
  Mzams=pd.concat([M0,M1],axis=0)
  Mzams=Mzams.sort_index(ascending=True)
  
  df['Mzams']=np.asarray(Mzams['Mass'])
  
  
  return df
  
 
def gen_input_nome(df,path_old,path,Z,mtot): #generate input for systems not undergoing merger

  
  df=df[['s_time','M_preSN','S_name','IDs']]
  df=df.astype(float)
  df['IDs']=df['IDs'].astype(int)
  df['S_name']=df['S_name'].astype(int)
  df['s_time']=df['s_time']*int(1e6)
  df=lookforMzams(evolved,Z,df)[0]  #add a column with initial mass
  #print(df)
  
  df.to_csv(path_old,sep=' ',index=False,header=False)
  open(path, "w").write(f"{mtot}\n" + open(path_old).read())  #write the input in a file with the total mass
  os.remove(path_old)
  
  
  return df
  
  
def gen_input_doub(df,path_old,path,Z,mtot): #generate input for systems with double PISN/PPISN

  
  df=df[['s_time','M_preSN','S_name','IDs']]
  df=df.astype(float)
  df['IDs']=df['IDs'].astype(int)
  df['S_name']=df['S_name'].astype(int)
  df['s_time']=df['s_time']*int(1e6)
  df=lookforMzams(evolved,Z,df)[1]  #add a column with initial mass for the double
  #print(df)
  df.to_csv(path_old,sep=' ',index=False,header=False)
  
  open(path, "w").write(f"{mtot}\n" + open(path_old).read())
  os.remove(path_old)
  
  return df


def gen_input_bef(df,path_old,path,Z,mtot): #generate input for systems undergoing PISN/PPISN before merger 

  
  df=df[['s_time','M_preSN','S_name','IDs']]
  #print(df)
  df=df.astype(float)
  df['IDs']=df['IDs'].astype(int)
  df['S_name']=df['S_name'].astype(int)
  df['s_time']=df['s_time']*int(1e6)
  df=lookforMzams_bef(evolved,Z,df)
  #print(df)
  df.to_csv(path_old,sep=' ',index=False,header=False)
 
  open(path, "w").write(f"{mtot}\n" + open(path_old).read())
  os.remove(path_old)
  
  return df


def gen_input_after_merger(df,df_merger,path_old,path,Z,mtot): #generate input for systems undergoing PISN after merger

  df=df[['s_time','M_preSN','S_name','IDs']]
  #print(df)
  df=df.astype(float)
  df['IDs']=df['IDs'].astype(int)
  df['S_name']=df['S_name'].astype(int)
  df['s_time']=df['s_time']*int(1e6)
  df=lookforMmerger(evolved,Z,df,df_merger)
  #print(df)
  df.to_csv(path_old,sep=' ',index=False,header=False)
  
  open(path, "w").write(f"{mtot}\n" + open(path_old).read())
  os.remove(path_old)
  
  return df
  
  
  
def gen_input_after_merger_ppisn(df,df_merger,path_old,path,Z,mtot): #generate input for systems undergoing PPISN after merger

  df=df[['s_time','M_preSN','S_name','IDs']]
  #print(df)
  df=df.astype(float)
  df['IDs']=df['IDs'].astype(int)
  df['S_name']=df['S_name'].astype(int)
  df['s_time']=df['s_time']*int(1e6)
  #print(df.loc[df['S_name']==295655126694860])
  df=lookforMmerger_ppisn(evolved,Z,df,df_merger)
  #print(df)
  df.to_csv(path_old,sep=' ',index=False,header=False)

  open(path, "w").write(f"{mtot}\n" + open(path_old).read())
  os.remove(path_old)
  
  return df
  
  
  
  

##-----------MAIN-----------##

pure_He=True#if generating IC for pure helium stars set to True

Z = [1E-11, 1E-06, 0.0001, 0.0002, 0.0004, 0.0005, 0.0006, 0.0008, 0.001, 0.002, 0.004,0.005, 0.008, 0.01, 0.014, 0.017]



for i in range(len(Z)):
  Zs=str(Z[i])
 
  path_output = f"/home/scala/tesi/sevn-SEVN/output_bin_KRO1_pureHE/Z{Zs}/"  ## MODIFY SEVN PATH
  logtext = open(f"{path_output}logfile.dat", "r").read()  ## MODIFY LOGFILE PATH
  evolved = pd.read_csv(f"{path_output}evolved.dat",sep='\s+')  ## MODIFY EVOLVED FILE PATH

  
  m0=evolved["Mass_0"].astype(float).sum()
  m1=evolved["Mass_1"].astype(float).sum()
  mtot=m1+m0

  #print(mtot)
  
  dfSN = lookfor_SN(logtext,Zs) #look for SN  events  
  dfmerger=lookfor_merger(logtext,Zs)  #look for  binary merger
  dfmerger_copy=dfmerger.copy()
  
  ##--INPUT-PISN--##
  
  path_pisn_before_old=f'/home/scala/tesi/cosmo_rate_public-v2/astromodel/popI_II/A3/pure_he/input_bin_pisn_before/data_bin_PISNbefore_{Z[i]}_old.txt' ## MODIFY PATHS 
  path_pisn_before=f'/home/scala/tesi/cosmo_rate_public-v2/astromodel/popI_II/A3/pure_he/input_bin_pisn_before/data_bin_PISNbefore_{Z[i]}.txt'
  
  path_pisn_after_old=f'/home/scala/tesi/cosmo_rate_public-v2/astromodel/popI_II/A3/pure_he/input_bin_pisn_after/data_bin_PISNafter_{Z[i]}_old.txt'
  path_pisn_after=f'/home/scala/tesi/cosmo_rate_public-v2/astromodel/popI_II/A3/pure_he/input_bin_pisn_after/data_bin_PISNafter_{Z[i]}.txt'
  
  path_pisn_double_old=f'/home/scala/tesi/cosmo_rate_public-v2/astromodel/popI_II/A3/pure_he/input_bin_pisn_double/data_bin_PISNdouble_{Z[i]}_old.txt'
  path_pisn_double=f'/home/scala/tesi/cosmo_rate_public-v2/astromodel/popI_II/A3/pure_he/input_bin_pisn_double/data_bin_PISNdouble_{Z[i]}.txt'
  
  

  [dfPISN, dfpisn_after,dfpisn_before, df_doublepisn]=analysis_pisn(dfSN,dfmerger) 
  
  input_pisn_before=gen_input_nome(dfpisn_before,path_pisn_before_old,path_pisn_before,Zs,mtot)  #pisn no merger
  
  input_pisn_double=gen_input_doub(df_doublepisn,path_pisn_double_old,path_pisn_double,Zs,mtot)  #double pisn 
  

  
  ##--INPUT-PPISN--##
  
  path_ppisn_nomerger_old=f'/home/scala/tesi/cosmo_rate_public-v2/astromodel/popI_II/A3/pure_he/input_bin_ppisn_nomerger/data_bin_PPISNnomerger_{Z[i]}_old.txt' ## MODIFY PATHS 
  path_ppisn_nomerger=f'/home/scala/tesi/cosmo_rate_public-v2/astromodel/popI_II/A3/pure_he/input_bin_ppisn_nomerger/data_bin_PPISNnomerger_{Z[i]}.txt'
  
  path_ppisn_double_old=f'/home/scala/tesi/cosmo_rate_public-v2/astromodel/popI_II/A3/pure_he/input_bin_ppisn_double/data_bin_PPISNdouble_{Z[i]}_old.txt'
  path_ppisn_double=f'/home/scala/tesi/cosmo_rate_public-v2/astromodel/popI_II/A3/pure_he/input_bin_ppisn_double/data_bin_PPISNdouble_{Z[i]}.txt'
  
  path_ppisn_before_old=f'/home/scala/tesi/cosmo_rate_public-v2/astromodel/popI_II/A3/pure_he/input_bin_ppisn_before/data_bin_PPISNbefore_{Z[i]}_old.txt'
  path_ppisn_before=f'/home/scala/tesi/cosmo_rate_public-v2/astromodel/popI_II/A3/pure_he/input_bin_ppisn_before/data_bin_PPISNbefore_{Z[i]}.txt'
  
  path_ppisn_after_old=f'/home/scala/tesi/cosmo_rate_public-v2/astromodel/popI_II/A3/pure_he/input_bin_ppisn_after/data_bin_PPISafter_{Z[i]}_old.txt'
  path_ppisn_after=f'/home/scala/tesi/cosmo_rate_public-v2/astromodel/popI_II/A3/pure_he/input_bin_ppisn_after/data_bin_PPISNafter_{Z[i]}.txt'
  
  
  
  [dfPPISN,dfppisn_nomerger, dfppisn_merger, dfmerger_ppisn,dfmerged, dfmerger_before_ppisn, dfmerger_after_ppisn, df_doubleppisn,dfdouble_e_merging]=analysis_ppisn(dfSN,dfmerger)
  
  input_ppisn_nomerger=gen_input_nome(dfppisn_nomerger,path_ppisn_nomerger_old,path_ppisn_nomerger,Zs,mtot)  #no merger(contains also double ppisn) 

  input_ppisn_double=gen_input_doub(df_doubleppisn,path_ppisn_double_old,path_ppisn_double,Zs,mtot)  #double pisn 
  
  input_ppisn_before=gen_input_bef(dfmerger_after_ppisn,path_ppisn_before_old,path_ppisn_before,Zs,mtot)  #we have merger and ppisn occurs before merger
 
  input_ppisn_after=gen_input_after_merger_ppisn(dfmerger_before_ppisn,dfmerger_copy,path_ppisn_after_old,path_ppisn_after,Zs,mtot)  #we have merger and ppisn occurs after merger
  
  
  input_pisn_after=gen_input_after_merger(dfpisn_after,dfmerger,path_pisn_after_old,path_pisn_after,Zs,mtot)  #pisn after merger
  
  
