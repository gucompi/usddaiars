import requests
import json
import schedule
import time
import smtplib


def obtenerCotizacion():
    pesos_compra = 0
    pesos_venta = 0
    dolares_compra = 0
    dolares_venta = 0

    resp = requests.get('https://be.buenbit.com/api/market/tickers/')
    if resp.status_code != 200:
        raise ApiError('GET /buenbit/ {}'.format(resp.status_code))

    respuesta = resp.json()
    if respuesta and 'object' in respuesta:
        if 'daiars' in respuesta['object']:
            pesos_compra = respuesta['object']['daiars']['purchase_price']
            pesos_venta = respuesta['object']['daiars']['selling_price']
        if 'daiusd' in respuesta['object']:
            dolares_compra = respuesta['object']['daiusd']['purchase_price']
            dolares_venta = respuesta['object']['daiusd']['selling_price']
    print('dai pesos_compra = ' + pesos_compra)
    print('dai dolares_venta = ' + dolares_venta)
    print('------------------------------')
    if (float(pesos_compra) > 110) and (float(dolares_compra) < 1.14):
      server=smtplib.SMTP('smtp.gmail.com',587)
      server.starttls()
      server.login("mail","psw")
      msg="Subject:OPORTUNIDAD EN DAI ** \n usd/dai: " + dolares_compra + "\n dai/ars: "+pesos_compra
      print("OPORTUNIDAD EN DAI: \n usd/dai: " + dolares_compra + "\n dai/ars: "+pesos_compra)
      server.sendmail("from@gmail.com","to@gmail.com , to2@gmail.com",msg)

obtenerCotizacion()
schedule.every(30).minutes.do(obtenerCotizacion)

while True:
    schedule.run_pending()
    time.sleep(1)