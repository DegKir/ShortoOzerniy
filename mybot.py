import telebot
from telebot import types
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import sqrt

#test commit
def MLS_line(_X,_Y,zero=0):
    X=pd.Series(_X)
    Y=pd.Series(_Y)
    XY=X*Y
    X2=X*X
    Y2=Y*Y
    if(zero==0):
        k=np.mean(XY)/np.mean(X2)
        k_er = sqrt(1/len(X))*sqrt(np.mean(Y2)/np.mean(X2)-k*k)
        result=[k,k_er,0,0]
        return result
    else:
        k=(np.mean(XY)-np.mean(X)*np.mean(Y))/(np.mean(X2)-np.mean(X)**2)
        k_er=1/sqrt(9)*sqrt(abs((np.mean(Y2)-np.mean(Y)**2)/(np.mean(X2)-np.mean(X)**2)-k**2))
        b=np.mean(Y)-k*np.mean(X)
        b_er = k_er*sqrt(np.mean(X2)-np.mean(X)**2)
        result=[k,k_er,b,b_er]
        return result
    
def make_and_safe_image():
    global x
    global y
    x_o=x
    y_o=y
    graph_data=MLS_line(x, y,1)
    k=graph_data[0]
    b =graph_data[2]
    x_=np.linspace(x,1,100)
    y1=k*x_+b
    plt.plot(x_, y1, color = 'black')
    plt.scatter(x_o,y_o,color='green')
    # plt.errorbar(x, y, yerr=0, xerr=0, fmt='.', label='Кресты погрешностей',ecolor='g')
    plt.savefig("graph1")


x=[1,2,3,4]
y=[1,2,4,3]
a=""
bot = telebot.TeleBot("1632966567:AAHfi7Jc1TkU1rLuwvCIc-6QMMhddXpu58I", parse_mode=None)

data = open("text.txt",'w')
data.close()

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "/graph возвращает график построеный по таблице \n /add x,y - добавляет два числа в таблицу \n /see выводит строки введенных данных - первая массив иксов вторая массив игриков \n /clear убирает за тобой")

@bot.message_handler(commands=['see'])
def give_data(message):
    bot.reply_to(message,str(x)+str(y))

@bot.message_handler(commands=['add'])
def add_new_row(message):
    try:
        c,a,b = (str(x) for x in message.text.split())
        x.append(float(a)) 
        y.append(float(b))
    except ValueError:
        bot.reply_to(message,"введите два числа через пробел")

@bot.message_handler(commands=['clear'])
def clear(message):
    global x
    global y
    bot.reply_to(message,"Я убрал за тобой, сладенький")
    x=[]
    y=[]

@bot.message_handler(commands=['graph'])
def graph(message):

    make_and_safe_image()
    chat_ide=message.chat.id
    bot.send_photo(chat_id=chat_ide, photo=open('graph1.png','rb'))

@bot.message_handler(content_types=['text'])
def texte(message):
    bot.reply_to(message,"Лучше напиши \help или \start")


bot.polling(none_stop=True, interval=0)