"""
Created on Wed Nov 20 11:50:54 2019

@author: jfboaretto
"""
# coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import sys

try:
    print("\n")
    print("::::::::: Questão 6 ::::::::: \n")
    print("::: Quais são as 5 maiores universidades no Passei Direto? E quais são os principais tipos de Arquivos consumidos em cada uma delas? :::\n")

    #Load BASES
    #Load Payment studentes
    dtPay = pd.read_json('premium_payments.json', orient='columns', encoding='UTF8')
    dtPay.set_index("StudentId", inplace = True) 
    
    #Load students
    dtStd = pd.read_json('students.json', orient='columns', encoding='UTF8')
    dtStd.set_index("Id", inplace = True)     
    
    #Load fileViews
    dtFileVws = pd.read_json('fileViews.json', orient='columns', encoding='UTF8')
    dtFileVws.set_index("StudentId", inplace = True) 
    
    #Limpar duplicados
    dtPay = dtPay.reset_index().drop_duplicates(subset='StudentId', keep='first').set_index('StudentId')
        
    #Merge Students and Payments
    dtStdPay = pd.merge(dtStd, dtPay, left_index=True, right_index=True, how='inner');
    
    # Calculate 5 largest universities
    dtresult5university = dtStdPay.groupby('UniversityName', as_index=False).agg({"PaymentDate":"count"}).sort_values('PaymentDate', ascending=False).head(5)
    print(dtresult5university)
    
    #Merge Students and FileViews
    dtStdFileVws = pd.merge(dtStd, dtFileVws, left_index=True, right_index=True, how='inner');
    
    #Calculate files more visualized for each university
    #1 - Estácio
    dtresultado10filesEST = dtStdFileVws[dtStdFileVws['UniversityName'] == 'ESTÁCIO'].groupby('FileName', as_index=False).agg({"RegisteredDate":"count"}).sort_values('RegisteredDate', ascending=False).head(10)
    #2 - Estácio EAD
    dtresultado10filesESTEAD = dtStdFileVws[dtStdFileVws['UniversityName'] == 'ESTÁCIO EAD'].groupby('FileName', as_index=False).agg({"RegisteredDate":"count"}).sort_values('RegisteredDate', ascending=False).head(10)
    #3 - UNINTER
    dtresultado10filesUNIN = dtStdFileVws[dtStdFileVws['UniversityName'] == 'UNINTER'].groupby('FileName', as_index=False).agg({"RegisteredDate":"count"}).sort_values('RegisteredDate', ascending=False).head(10)
    #4 - UNIP
    dtresultado10filesUNIP = dtStdFileVws[dtStdFileVws['UniversityName'] == 'UNIP'].groupby('FileName', as_index=False).agg({"RegisteredDate":"count"}).sort_values('RegisteredDate', ascending=False).head(10)
    #5 - UNOPAR
    dtresultado10filesUNO = dtStdFileVws[dtStdFileVws['UniversityName'] == 'UNOPAR'].groupby('FileName', as_index=False).agg({"RegisteredDate":"count"}).sort_values('RegisteredDate', ascending=False).head(10)


   #PLOT GRAPHICS
   
    #1 - Plot graphic of 5 largest universities  
    fig1, ax1 = plt.subplots()
    ax1.pie(dtresult5university['PaymentDate'], labels=dtresult5university['UniversityName'], autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')
    plt.show()
    
    #2 - Plot graphic of 10 more visualized files of ESTÁCIO
    plt.barh(dtresultado10filesEST['FileName'],dtresultado10filesEST['RegisteredDate'], color='orange')
    plt.ylabel("Arquivos mais consumidos")
    plt.xlabel("Quantidade de consumo")
    plt.title("10 Arquivos mais consumidos pela Universidade ESTÁCIO")
    plt.show()
    
    #3 - Plot graphic of 10 more visualized files of ESTÁCIO EAD
    plt.barh(dtresultado10filesESTEAD['FileName'],dtresultado10filesESTEAD['RegisteredDate'], color='orange')
    plt.ylabel("Arquivos mais consumidos")
    plt.xlabel("Quantidade de consumo")
    plt.title("10 Arquivos mais consumidos pela Universidade ESTÁCIO EAD")
    plt.show()
    
    #4 - Plot graphic of 10 more visualized files of UNINTER
    plt.barh(dtresultado10filesUNIN['FileName'],dtresultado10filesUNIN['RegisteredDate'], color='orange')
    plt.ylabel("Arquivos mais consumidos")
    plt.xlabel("Quantidade de consumo")
    plt.title("10 Arquivos mais consumidos pela Universidade UNINTER")
    plt.show()
    
    #5 - Plot graphic of 10 more visualized files of UNIP
    plt.barh(dtresultado10filesUNIP['FileName'],dtresultado10filesUNIP['RegisteredDate'], color='orange')
    plt.ylabel("Arquivos mais consumidos")
    plt.xlabel("Quantidade de consumo")
    plt.title("10 Arquivos mais consumidos pela Universidade UNIP")
    plt.show()
    
    #6 - Plot graphic of 10 more visualized files of UNOPAR
    plt.barh(dtresultado10filesUNO['FileName'],dtresultado10filesUNO['RegisteredDate'], color='orange')
    plt.ylabel("Arquivos mais consumidos")
    plt.xlabel("Quantidade de consumo")
    plt.title("10 Arquivos mais consumidos pela Universidade UNOPAR")
    plt.show()

    print(":::::::::            SUCESS             ::::::::: \n")    
    
except:
    
    
    print(":::::::::            ERROR             ::::::::: \n")   
    
    print("  -> Error:", sys.exc_info()[0], sys.exc_info()[1])
    
    
finally:
    
    print("\n") 
