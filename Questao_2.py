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
    print("::::::::: Questão 2 ::::::::: \n")
    print("::: Faça uma análise geral dos dados e apresente as informações que julgar mais relevantes dessa base. :::\n")
    
    #Load BASES
    #Load Payments
    dtPay = pd.read_json('premium_payments.json', orient='columns', encoding='utf-8')    
    #Load Cancellations
    dtCan = pd.read_json('premium_cancellations.json', orient='columns', encoding='utf-8')
    #Load FileViews
    dtFlVws = pd.read_json('fileViews.json', orient='columns', encoding='UTF8')
    #Load TextBookViews
    dttxtBkSlVws = pd.read_json('textBookSolutionViews.json', orient='columns', encoding='UTF8')
    #Load StudyPlanViews
    dtstdPlVws = pd.read_json('studyPlanViews.json', orient='columns', encoding='UTF8')
    #Load Subjects
    dtsbjcts = pd.read_json('subjects.json', orient='columns', encoding='UTF8')
    #Load Questions
    dtqst = pd.read_json('questions.json', orient='columns', encoding='UTF8')
    #Load Answers
    dtaswrs = pd.read_json('answers.json', orient='columns', encoding='UTF8')
    #Load Evaluations
    dtevls = pd.read_json('evaluations.json', orient='columns', encoding='UTF8')
    #Load Evaluations
    dtses = pd.read_json('sessions.json', orient='columns', encoding='UTF8')
    
    #Load views Payments - Calcule the Gross -> First payment of the month is a gross
    dtPay = dtPay.groupby('StudentId', as_index=False).agg({"PaymentDate": "min"})
    dtPay["PaymentMonth"] = dtPay["PaymentDate"]    
    def ConvertStrToDateTime(row):
        date = datetime.datetime.strptime(row["PaymentMonth"], "%Y-%m-%d %H:%M:%S.%f")
        return date.strftime('%m-%Y')
    dtPay["PaymentMonth"] = dtPay.apply(ConvertStrToDateTime, axis=1)
    #GROOSSSS       
    dtPay = pd.DataFrame({'monthGross': dtPay.groupby('PaymentMonth', as_index=False).agg({"PaymentDate": "first"})["PaymentMonth"].values.tolist(),
                          'countGross': dtPay.groupby('PaymentMonth')['PaymentMonth'].count().values.tolist()})    
    dtPay["ordergross"] =  pd.to_datetime(dtPay["monthGross"],format='%m-%Y')    
    dtPay = dtPay.sort_values('ordergross', ascending=True)         
    
    #Load views Churn - Calcule the Churn -> First cancellation request of the month is a churn
    dtCan = dtCan.groupby('StudentId', as_index=False).agg({"CancellationDate": "min"})
    dtCan["CancellatioMonth"] = dtCan["CancellationDate"]    
    def ConvertStrToDateTime(row):
        date = datetime.datetime.strptime(row["CancellatioMonth"], "%Y-%m-%d %H:%M:%S.%f")
        return date.strftime('%m-%Y')
    dtCan["CancellatioMonth"] = dtCan.apply(ConvertStrToDateTime, axis=1)
    #Churn
    dtCan = pd.DataFrame({'monthChurn': dtCan.groupby('CancellatioMonth', as_index=False).agg({"CancellationDate": "first"})["CancellatioMonth"].values.tolist(),
                          'countChurn': dtCan.groupby('CancellatioMonth')['CancellatioMonth'].count().values.tolist()})
    dtCan["orderchurn"] =  pd.to_datetime(dtCan["monthChurn"],format='%m-%Y')    
    dtCan = dtCan.sort_values('orderchurn', ascending=True)             

    #Join of NO Premium with Premium
    dtresult = pd.merge(dtPay,                       
                        dtCan,
                        left_on='ordergross',
                        right_on='orderchurn',
                        how='outer')
    
    #Users Activity
    
    #Calculate of contents
    #Count do Numero de File Views
    dtFlVwsNum = dtFlVws.groupby('ViewDate', as_index=False).agg({"StudentId":"count"})
    #Count do Numero de TextBook Views
    dttxtBkSlVwsNum = dttxtBkSlVws.groupby('ViewDate', as_index=False).agg({"StudentId":"count"})
    #Count do Numero de Student Plan
    dtstdPlVwsNum = dtstdPlVws.groupby('ViewDate', as_index=False).agg({"StudentId":"count"})
    dtresultContent = pd.DataFrame({"Content":["TextBooks", 
                                               "FileViews", 
                                               "StudentPlans",], 
                                     "Views":[(dttxtBkSlVwsNum['StudentId'].sum()),
                                              (dtFlVwsNum['StudentId'].sum()),
                                              (dtstdPlVwsNum['StudentId'].sum()),]}) 

    #Actions
    #Count of Subjects
    dtsbjctsNum = dtsbjcts.groupby('FollowDate', as_index=False).agg({"StudentId":"count"})
    #Count of Questions
    dtqstNum = dtqst.groupby('QuestionDate', as_index=False).agg({"StudentId":"count"})
    #Count of Answers
    dtaswrsNum = dtaswrs.groupby('AnswerDate', as_index=False).agg({"StudentId":"count"})
    dtresultActions = pd.DataFrame({"Actions":[ "Questions", 
                                          "Subjects",
                                          "Answers",], 
                               "Views":[(dtqstNum['StudentId'].sum()), 
                                        (dtsbjctsNum['StudentId'].sum()), 
                                        (dtaswrsNum['StudentId'].sum()),]}) 
    
    #Evaluations
    #Count of evaluations
    dtevlsNum = dtevls.groupby('EvaluationType', as_index=False).agg({"StudentId":"count"})
    
    #Student Client
    #Count of Student Client
    dtsesNum = dtses.groupby('StudentClient', as_index=False).agg({"StudentId":"count"})

    #PLOT GRAPHICS
    
    #1 - Plot graphic of Gross vs Churn
    plt.figure(figsize=(15  ,8))
    plt.title('Gross x Churn (Mês)')
    plt.yscale('linear')
    plt.xlabel('Meses/Ano')
    plt.ylabel('Quantidade de Gross / Churn')
    plt.xticks(rotation=50)
    plt.plot(dtresult["monthGross"], dtresult["countChurn"], color='red', label='Churn')
    plt.plot(dtresult["monthGross"], dtresult["countGross"], color='green', label='Gross')
    plt.grid(True)
    plt.legend()
    plt.show()    
    
    #2 - Plot graphic of contents
    fig1, ax1 = plt.subplots()
    ax1.pie(dtresultContent['Views'], labels=dtresultContent['Content'], autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')
    plt.show()
    
    #3- Plot graphic of actions
    fig1, ax1 = plt.subplots()
    ax1.pie(dtresultActions['Views'], labels=dtresultActions['Actions'], autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')
    plt.show()
    
    #4 - Plot graphic of evaluations
    fig1, ax1 = plt.subplots()
    ax1.pie(dtevlsNum['StudentId'], labels=dtevlsNum['EvaluationType'], autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')
    plt.show()
    
    #5 - Plot graphic of student client
    fig1, ax1 = plt.subplots()
    ax1.pie(dtsesNum['StudentId'], labels=dtsesNum['StudentClient'], autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')
    plt.show()

    print(":::::::::            SUCESS             ::::::::: \n")    
    
except:
    
    
    print(":::::::::            ERROR             ::::::::: \n")   
    
    print("  -> Error:", sys.exc_info()[0], sys.exc_info()[1])
    
    
finally:
    
    print("\n") 