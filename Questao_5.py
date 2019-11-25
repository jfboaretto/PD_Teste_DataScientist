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
    print("::::::::: Questão 5 ::::::::: \n")
    print("::: Entre os usuários que Churnaram solicitando ativamente o cancelamento do Plano Premium, o que está fortemente correlacionado com o cancelamento? (Ex: uso das features, tempo de inatividade, etc) :::\n")
    
    #Load BASES
    #Load students
    dtStd = pd.read_json('students.json', orient='columns', encoding='UTF8')
    dtStd.set_index("Id", inplace = True) 
    def ConvertStrToDateTime(row):
        date = datetime.datetime.strptime(row["RegisteredDate"], "%Y-%m-%d %H:%M:%S.%f")
        return date.date()
    dtStd["RegisteredDate"] = dtStd.apply(ConvertStrToDateTime, axis=1)
    dtStd.info()
    
    #Load Cancelation studentes
    dtCancel = pd.read_json('premium_cancellations.json', orient='columns', encoding='UTF8')
    dtCancel.set_index("StudentId", inplace = True) 
    
    #Calculate Recurrence of Cancelations 
    dtNumCancel = dtCancel.groupby('StudentId', as_index=False).agg({"CancellationDate":"count"})
    
    dtresult = pd.DataFrame({"Type":["Não Recorrentes", 
                                     "Recorrentes",], 
                              "Count":[dtNumCancel[dtNumCancel['CancellationDate'] <= 1]['CancellationDate'].sum(), 
                                       dtNumCancel[dtNumCancel['CancellationDate'] > 1]['CancellationDate'].sum(),]})     
    
    #Calculate Cancelations per month
    dtCancelMonth = pd.read_json('premium_cancellations.json', orient='columns', encoding='UTF8')
    def ConvertStrToDateTime(row):
        date = datetime.datetime.strptime(row["CancellationDate"], "%Y-%m-%d %H:%M:%S.%f")
        return date.strftime('%m-%Y')
    dtCancelMonth ["CancellationDate"] = dtCancelMonth.apply(ConvertStrToDateTime, axis=1)
    dtCancelMonth ["CancellationDate"] = pd.to_datetime(dtCancelMonth["CancellationDate"],format='%m-%Y')
    dtresultcancelmonth = dtCancelMonth.groupby('CancellationDate', as_index=False).agg({"StudentId":"count"}).sort_values('CancellationDate', ascending=True)

    #Calculate Active Time and percentage that active time per month
    #Clean duplicate Cancel data
    dtCancel = dtCancel.reset_index().drop_duplicates(subset='StudentId', keep='first').set_index('StudentId')
    dtCancel.info()
    #Merge Students and Cancelations
    dtStdCancel = pd.merge(dtStd, dtCancel, left_index=True, right_index=True, how='inner');
    dtStdCancel["CancellationDate"] = pd.to_datetime(dtStdCancel["CancellationDate"],format='%Y-%m-%d')
    dtStdCancel["RegisteredDate"] = pd.to_datetime(dtStdCancel["RegisteredDate"],format='%Y-%m-%d')
    # Calculate active time, count of active time and percentage
    dtStdCancel["Actv_Time"] = round(((dtStdCancel['CancellationDate'] - dtStdCancel['RegisteredDate']).dt.days)/30,0)
    dtStdCancel.info()
    dtresultstdcancel = dtStdCancel.groupby('Actv_Time', as_index=False).agg({"CancellationDate":"count"})
    dtresultstdcancel['Percentage'] = round((dtresultstdcancel["CancellationDate"] / dtresultstdcancel["CancellationDate"].sum())*100, 0)
    
    #PLOT GRAPHICS
    
    #1 - Plot graphic of Recurrence of cancelations
    fig1, ax1 = plt.subplots()
    ax1.pie(dtresult['Count'], labels=dtresult['Type'], autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')
    plt.title('Numero de Assinantes Premium que Cancelaram mais de 1X')
    plt.show()

    #2 - Plot Graphic of Cancelations per month
    plt.figure(figsize=(10,5))
    plt.title('Numero de Cancelamentos x Mês')
    plt.yscale('linear')
    plt.xlabel('Meses')
    plt.ylabel('Numero Cancelamentos')
    plt.xticks(rotation=90)
    plt.plot(dtresultcancelmonth['CancellationDate'], dtresultcancelmonth['StudentId'])
    plt.grid(True)
    plt.show()
    
    #3 - Plot Graphic Percentage of Cancelations vs Active Time
    plt.figure(figsize=(10,5))
    plt.title('Cancelamentos x Tempo Ativo do Assinantes Premium')
    plt.yscale('linear')
    plt.xlabel('Meses')
    plt.ylabel('% Cancelamentos')
    plt.bar(dtresultstdcancel['Actv_Time'], dtresultstdcancel['Percentage'], color='orange', align='center')
    plt.grid(True)
    plt.show()
    
    #4 - Plot Graphic Number of Cancelations vs Active Time
    plt.figure(figsize=(10,5))
    plt.title('Cancelamentos x Tempo Ativo do Assinantes Premium')
    plt.yscale('linear')
    plt.xlabel('Meses')
    plt.ylabel('Numero de Cancelamentos')
    plt.bar(dtresultstdcancel['Actv_Time'], dtresultstdcancel['CancellationDate'], color='orange', align='center')
    plt.grid(True)
    plt.show()

    print(":::::::::            SUCESS             ::::::::: \n")    
    
except:
    
    
    print(":::::::::            ERROR             ::::::::: \n")   
    
    print("  -> Error:", sys.exc_info()[0], sys.exc_info()[1])
    
    
finally:
    
    print("\n") 





