"""
Created on Wed Nov 20 11:50:54 2019

@author: jfboaretto
"""
# coding: utf-8 -*-
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import sys

try:
    print("\n")
    print("::::::::: Questão 4 ::::::::: \n")
    print("::: Em Novembro de 2017 fizemos uma grande mudança no PD: o Content Restriction. Os usuários não Premium passaram a poder consumir no máximo 3 arquivos diferentes por mês. Diante dessa mudança, qual passou a ser o Lifetime Value (LTV) dos usuários Premium a partir de Novembro de 2017? :::\n")

    #Load BASE
    #Load Payment studentes
    dtStdPay = pd.read_json('premium_payments.json', orient='columns', encoding='UTF8')
    
    #Calculate of payments
    def ConvertStrToDateTime(row):
        date = datetime.datetime.strptime(row["PaymentDate"], "%Y-%m-%d %H:%M:%S.%f")
        return date.strftime('%m-%Y')
    dtStdPay["PaymentDate"] = dtStdPay.apply(ConvertStrToDateTime, axis=1)
    dtStdPay["PaymentDate"] = pd.to_datetime(dtStdPay["PaymentDate"],format='%m-%Y')
    dtresult = dtStdPay.groupby('PaymentDate', as_index=False).agg({"StudentId":"count"}).sort_values('PaymentDate', ascending=True)
 
    #PLOT GRAPHICS

    #1 - Plot graphic of Premium vs No Premium
    plt.figure(figsize=(10,5))
    plt.title('Numero de Pagamentos dos Assinantes Premium x Tempo')
    plt.yscale('linear')
    plt.xlabel('Meses/Ano')
    plt.ylabel('Numero de Pagamentos')
    plt.xticks(rotation=30)
    plt.plot(dtresult['PaymentDate'], dtresult['StudentId'])
    plt.grid(True)
    plt.show()


    print(":::::::::            SUCESS             ::::::::: \n")    
    
except:
    
    
    print(":::::::::            ERROR             ::::::::: \n")   
    
    print("  -> Error:", sys.exc_info()[0], sys.exc_info()[1])
    
    
finally:
    
    print("\n") 



