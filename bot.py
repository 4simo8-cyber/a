from telebot import TeleBot ,types
from dotenv import load_dotenv
import os
import query
import io
import flask
from flask import request
from db import create_table

create_table()

load_dotenv()
bot_token=os.getenv('BOT_TOKEN')

bot=TeleBot(bot_token,threaded=False)

app = flask.Flask(__name__)


admin=['979910153']

@bot.message_handler(commands=['start'])
def hello(message):
    user_id= message.from_user.id
    

    botton=types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=3)
    botton.row('محصولات')
    #if str(user_id) in admin:
    botton.row('افزودن')
    
    bot.send_message(message.chat.id,'hello',reply_markup=botton)


@bot.message_handler(func= lambda message : message.text == 'محصولات'  ) 
def choose(message):
    datas=query.select()
    botns=types.InlineKeyboardMarkup(row_width=1)
    bake_botn=types.InlineKeyboardButton(text='back',callback_data='back')

    for name , price , stock ,photo  in datas:
        botn=types.InlineKeyboardButton(text=f'{name}' , callback_data= f'P_{name}_{price}_{stock}' )
        botns.add(botn)
    botns.add(bake_botn)    
    bot.send_message(message.chat.id,'یک محصول را انتخاب کنید',reply_markup=botns)
@bot.message_handler(func= lambda message : message.text== 'افزودن'  ) 
def send(message):

    bot.reply_to(message,'''ارسال لیست محصولات را به صورت  :
عکس 
کپشن عکس:                                        
نام
قیمت(به تومان)
تعداد موجودی                                  
                             ''')




@bot.message_handler(content_types=['photo'])
def add(message):
    user_id= message.from_user.id
    if str(user_id) in admin:    
        photo_file=bot.get_file(message.photo[-1].file_id)
        photo_download=bot.download_file(photo_file.file_path) 
        caption=message.caption

        name=str(caption.split('\n')[0])
        price=str(caption.split('\n')[1])
        stock=int(caption.split('\n')[2])
        photo=photo_download
        query.insert(name,price,stock,photo)
        bot.reply_to(message,f'{name} افزوده شد')
            
        


@bot.callback_query_handler(func=lambda call: call.data.startswith('P_'))
def buying(call):

    name, price= call.data.split('_')[1],call.data.split('_')[2]
    datas=query.photos(name)
    for data in datas:
        photo=data

    botns=types.InlineKeyboardMarkup(row_width=2)
    botn2=types.InlineKeyboardButton(text='back',callback_data='back to list')
    botns.add(botn2)
    caption=f'''
{name}
{price} تومان 
             '''
    bot.send_photo(call.message.chat.id,photo,caption=caption,reply_markup=botns) 

@bot.callback_query_handler(func= lambda call : call.data =='back to list')
def choose(call):
        datas=query.select()
        botns=types.InlineKeyboardMarkup(row_width=1)
        bake_botn=types.InlineKeyboardButton(text='back',callback_data='back')

        for name , price , stock, photo in datas:
            botn=types.InlineKeyboardButton(text=f'{name}' , callback_data= f'P_{name}_{price}_{stock}' )
            botns.add(botn)
        botns.add(bake_botn)    
        bot.send_message(call.message.chat.id,'یک محصول را انتخاب کنید',reply_markup=botns)


@bot.callback_query_handler(func=lambda call: call.data=='back')
def hello(call):
    user_id= call.from_user.id
    

    botton=types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=3)
    botton.row('محصولات')
    if str(user_id) in admin:
        botton.row('افزودن')
    
    bot.send_message(call.message.chat.id,'hello',reply_markup=botton)


@app.route(f"/{bot_token}", methods=["POST"])
def webhook():
    raw = request.get_data().decode("utf-8")
    update = types.Update.de_json(raw)
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/")
def index():
    return "Bot is running!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)