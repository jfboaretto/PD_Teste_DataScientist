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
    print("::::::::: Questão 1 ::::::::: \n")
    print(":::  Dentre os usuários cadastrados em Nov/2017 que assinaram o Plano Premium, qual a probabilidade do usuário virar Premium após o cadastro em ranges de dias? A escolha dos ranges deve ser feita por você, tendo em vista os insights que podemos tirar para o negócio. :::\n")

    #Load BASE
    #Load Premium students
    dtStdPr = pd.read_json('premium_students.json', orient='columns', encoding='UTF8')

    #Calculate diference between SubscriptionDate and RegistredDate, Counts and Percentage
    def ConvertStrToDateTime(row):
        date = datetime.datetime.strptime(row["RegisteredDate"], "%Y-%m-%d %H:%M:%S.%f")
        return date.date()
    dtStdPr["RegisteredDate"] = dtStdPr.apply(ConvertStrToDateTime, axis=1)
    def ConvertStrToDateTime2(row):
        date = datetime.datetime.strptime(row["SubscriptionDate"], "%Y-%m-%d %H:%M:%S.%f")
        return date.date()
    dtStdPr["SubscriptionDate"] = dtStdPr.apply(ConvertStrToDateTime2, axis=1)
    dtStdPr["DataDiff"] = pd.Series(delta.days for delta in (dtStdPr['SubscriptionDate'] - dtStdPr['RegisteredDate']))
    dtresult = dtStdPr.groupby('DataDiff', as_index=False).agg({"StudentId":"count"})    
    dtresult["DataDiff"]= dtresult["DataDiff"].astype(int) 
    dtresult['StudentId'] = dtresult['StudentId'].astype(int) 
    dtresult['Percentage'] = round((dtresult["StudentId"] / dtresult["StudentId"].sum())*100, 2)
    
    #Calculate the ranges
    dtfinalresult = pd.DataFrame({"Range":["0-1", 
                                           "2-15", 
                                           "16-30",
                                           "31-120",
                                           "121-200",
                                           ">200",], 
                                   "Percentage":[round(dtresult[dtresult['DataDiff'] < 2]['Percentage'].sum(), 2), 
                                                 round(dtresult[dtresult['DataDiff'].between(2, 15, inclusive = True)]['Percentage'].sum(), 2), 
                                                 round(dtresult[dtresult['DataDiff'].between(16, 30, inclusive = True)]['Percentage'].sum(), 2),
                                                 round(dtresult[dtresult['DataDiff'].between(31, 120, inclusive = True)]['Percentage'].sum(), 2),
                                                 round(dtresult[dtresult['DataDiff'].between(121, 200, inclusive = True)]['Percentage'].sum(), 2),
                                                 round(dtresult[dtresult['DataDiff'] > 200]['Percentage'].sum(), 2),]}) 
    print(dtfinalresult)
    
    #PLOT GRAPHICS

    #1 - Plot graphic of Range vs Percentage    
    plt.figure(figsize=(8,5))
    plt.bar(dtfinalresult["Range"], dtfinalresult['Percentage'])
    plt.bar(dtfinalresult["Range"], dtfinalresult['Percentage'])    
    plt.annotate("Maior valor em menor RANGE!", 
                xy=("0-1", 48),
                xycoords='data',
                xytext=("0-1", 43),
                textcoords='data',
                arrowprops=dict(arrowstyle="->",connectionstyle="arc3"))   
    plt.title('% Subscription x Days')    
    plt.xlabel('Days')
    plt.ylabel('Percentage')   
    plt.yscale('linear')    
    plt.grid(True)
    plt.show()

    print(":::::::::            SUCESS             ::::::::: \n")    
    
except:
    
    
    print(":::::::::            ERROR             ::::::::: \n")   
    
    print("  -> Error:", sys.exc_info()[0], sys.exc_info()[1])
    
    
finally:
    
    print("\n") 




