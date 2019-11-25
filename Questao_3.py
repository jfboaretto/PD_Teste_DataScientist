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
    print("::::::::: Questão 3 ::::::::: \n")
    print("::: Faça uma análise comparativa do comportamento dos usuários não Premium e dos usuários Premium. Que tipos de ações podemos direcionar para usuários não Premium fazerem com o objetivo de termos um maior número de assinantes? :::\n")
    print("\n\n -> Favor aguardar carga de 3MM de registros.\n")

    #Load BASES
    #Load Students
    dtStd = pd.read_json('students.json', orient='columns', encoding='utf-8')    
    #Load Payment
    dtStdPay = pd.read_json('premium_payments.json', orient='columns', encoding='utf-8')
    #Load view
    dtView = pd.read_json('fileViews.json', orient='columns', encoding='utf-8')
          
    #Select the Students PREMIUM
    aggregations = {
    'PaymentDate': lambda x: max(x)
    }
    dtStdPay = dtStdPay.groupby('StudentId').agg(aggregations)    
    dtStd = pd.merge(dtStd, 
                      dtStdPay[['PaymentDate']],
                      left_on='Id',
                      right_on='StudentId',
                      how='left')          

    #Load views Students premium X Students NO premium 
    dtView["ViewMonth"] = dtView["ViewDate"]
    dtView["ViewDate"] = pd.to_datetime(dtView["ViewDate"],format='%Y-%m-%d %H:%M:%S.%f')    
    def ConvertStrToDateTime(row):
        date = datetime.datetime.strptime(row["ViewMonth"], "%Y-%m-%d %H:%M:%S.%f")
        return date.strftime('%m-%Y')
    dtView["ViewMonth"] = dtView.apply(ConvertStrToDateTime, axis=1)
        
    #Date of CONTENT RESTRICTION
    dataini = datetime.datetime(2017, 12, 1, 0, 0)
    
    #Select NOOOOO Premium with CONTENT RESTRICTION
    dtViewNoPremium = pd.merge(dtView[dtView['ViewDate'] >= dataini],                       
                                      dtStd[dtStd['PaymentDate'].isna()][['Id']],
                                      left_on='StudentId',
                                      right_on='Id',
                                      how='inner')
    
    #Select PREMIUM with CONTENT RESTRICTION
    dtViewPremium = pd.merge(dtView[dtView['ViewDate'] >= dataini],                       
                                      dtStd[dtStd['PaymentDate'].notnull()][['Id']],
                                      left_on='StudentId',
                                      right_on='Id',
                                      how='inner')    
    
    #Calcule PREMIUM  
    dtPremiumViewVsAccess = pd.DataFrame({'month': dtViewPremium.groupby('ViewMonth', as_index=False).agg({"ViewDate": "first"})["ViewMonth"].values.tolist(),
                                          'countViewsMonthPremium': dtViewPremium.groupby('ViewMonth')['ViewMonth'].count().values.tolist(), 
                                          'countStdViewsMonthPremium': dtViewPremium.groupby(['StudentId', 'ViewMonth'], as_index=False).agg({"ViewDate": "first"}).groupby('ViewMonth', as_index=False).agg({"StudentId":"count"})["StudentId"].values.tolist()})
    dtPremiumViewVsAccess["order"] =  pd.to_datetime(dtPremiumViewVsAccess["month"],format='%m-%Y')    
    dtPremiumViewVsAccess = dtPremiumViewVsAccess.sort_values('order', ascending=True)    
    dtPremiumViewVsAccess["mediaAccessPremium"] =  round(dtPremiumViewVsAccess["countViewsMonthPremium"] /  dtPremiumViewVsAccess["countStdViewsMonthPremium"], 2)
             
    #Calcule NOOOO PREMIUM        
    dtNoPremiumViewVsAccess = pd.DataFrame({'month': dtViewNoPremium.groupby('ViewMonth', as_index=False).agg({"ViewDate": "first"})["ViewMonth"].values.tolist(),
                                            'countViewsMonthNoPremium': dtViewNoPremium.groupby('ViewMonth')['ViewMonth'].count().values.tolist(), 
                                            'countStdViewsMonthNoPremium': dtViewNoPremium.groupby(['StudentId', 'ViewMonth'], as_index=False).agg({"ViewDate": "first"}).groupby('ViewMonth', as_index=False).agg({"StudentId":"count"})["StudentId"].values.tolist()})
    dtNoPremiumViewVsAccess["order"] =  pd.to_datetime(dtNoPremiumViewVsAccess["month"],format='%m-%Y')    
    dtNoPremiumViewVsAccess = dtNoPremiumViewVsAccess.sort_values('order', ascending=True)
    dtNoPremiumViewVsAccess["mediaAccessNoPremium"] =  round(dtNoPremiumViewVsAccess["countViewsMonthNoPremium"] /  dtNoPremiumViewVsAccess["countStdViewsMonthNoPremium"], 2)
    #Definition Content restriction of NO PREMIUM
    dtNoPremiumViewVsAccess["goalNoPremium"] = 3
    
    #Join of NO Premium with Premium
    dtresult = pd.merge(dtNoPremiumViewVsAccess,                       
                        dtPremiumViewVsAccess,
                        on='order',
                        how='left')  

    #PLOT GRAPHICS

    #1 - Plot graphic of Premium vs No Premium
    labels = ['Premium', 'NO Premium']
    sizes = [dtStd['PaymentDate'].count(), dtStd['PaymentDate'].isna().sum()]    
    fig1, ax1 = plt.subplots()    
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    plt.title('Usuários Premium x Usuários NO Premium')
    ax1.axis('equal')    
    plt.show()
        
    #2 - Plot graphic the View of Premium x NO Premium
    plt.figure(figsize=(10,5))
    plt.title('Usuários x Visualizações de Documentos (Mês)')
    plt.yscale('linear')
    plt.xlabel('Meses/Ano')
    plt.ylabel('Número de documentos visuzalidados')
    plt.xticks(rotation=0)
    plt.plot(dtresult["month_x"], dtresult["goalNoPremium"], color='red', label='Content Restriction')
    plt.plot(dtresult["month_x"], dtresult["mediaAccessPremium"], color='green', label='Visualizações Premium')
    plt.plot(dtresult["month_x"], dtresult["mediaAccessNoPremium"], color='blue', label='Visualizações NO Premium')
    plt.grid(True)
    plt.legend()
    plt.show()

    #3 - Plot graphic Details the Vision NOOOO Premium
    plt.figure(figsize=(10,5))
    plt.title('Usuários NO Premium x Content Restriction (Mês)')
    plt.yscale('linear')
    plt.xlabel('Meses/Ano')
    plt.ylabel('Número de documentos visuzalidados')
    plt.xticks(rotation=0)
    plt.plot(dtNoPremiumViewVsAccess["month"], dtNoPremiumViewVsAccess["goalNoPremium"], color='red', label='Content Restriction')
    plt.plot(dtNoPremiumViewVsAccess["month"], dtNoPremiumViewVsAccess["mediaAccessNoPremium"], color='blue', label='Visualizações NO Premium')  
    plt.grid(True)
    plt.show()
    

    print(":::::::::            SUCESS             ::::::::: \n")    
    
except:
    
    
    print(":::::::::            ERROR             ::::::::: \n")   
    
    print("  -> Error:", sys.exc_info()[0], sys.exc_info()[1])
    
    
finally:
    
    print("\n") 