import json
import pandas as pd
import datetime
import requests
from twilio.rest import Client

def EnviarResumen(df, cod):
    TWILIO_ACCOUNT_SID = "AC5033ad66512b5efa8be02142ea70175b"
    AUTH_TOKEN = "2440ef4649839a37fc949a12e8145dc4"

    client = Client(TWILIO_ACCOUNT_SID,AUTH_TOKEN)
    to_whatsapp_number='whatsapp:+56967500475'
    from_whatsapp_number='whatsapp:+14155238886'
    #from_whatsapp_number='whatsapp:+56967500475'
    
    client.messages.create(body=cod + " : " + str(df),
                        from_=from_whatsapp_number,
                        to=to_whatsapp_number)

def Codigos():
    return ["eth-clp","btc-clp","bch-clp","ltc-clp"]

def CodigosP():
    return ["bitcoin-cash","ethereum","bitcoin","litecoin"]

def GuardarPrecio(cod):
    url = 'https://www.buda.com/api/v2/markets/' + cod + '/ticker'
    response = requests.get(url).json()
    response = response['ticker']
    df = pd.DataFrame([{"Ultimo precio": response["last_price"][0],
                        "Minimo": response["min_ask"][0],
                       "Maximo": response["max_bid"][0],
                       "Volumen": response["volume"][0],
                       "Variacion 24 horas": response["price_variation_24h"],
                       "Variacion 7 dias": response["price_variation_7d"],
                       "Fecha":datetime.datetime.now()}])
    EnviarResumen(df, cod)
    return df

def GuardarExcel(df,cod):
    excel = pd.read_excel("Data/" + cod + ".xlsx")
    df = pd.concat([excel, df])
    df.to_excel("Data/" +cod + ".xlsx", index = False)
    return df

def GuardarProyeccion():
    now = datetime.datetime.now()
    for i in CodigosP():
        url = "https://dolarpeso.mx/" + i
        df = pd.read_html(url)
        #df[1].to_csv("Data/Proyeccion/" + i + "/" + now.strftime("%Y%m%d%H%M%S") + i + ".csv", index=False)
        print(i)
        df[1].to_csv("Data/Proyeccion/" + i + now.strftime("/%Y%m%d%H%M%S.csv"), index=False)
    return df[1]



if __name__ == '__main__':
    for i in Codigos():
        df = GuardarPrecio(i)
        GuardarExcel(df,i)
    GuardarProyeccion()
