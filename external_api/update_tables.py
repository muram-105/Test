# -*- coding: utf-8 -*-
import pymssql
import requests
server = 'localhost'
database = ''
username = ''
password = ''
url = ''
conn = pymssql.connect(server,user=username, password=password, database=database,port=1433)
cursor = conn.cursor()
headers = {'Content-type': 'application/json'}

lines = requests.post(url+'/get_sales_data',headers=headers,json={})
lines = lines.json()
lines = lines['result']
sale_col = ('transfer_date','sale_date','sale_hour','production_place','article_number',
            'quantity','unit','cost_of_sale','sale_price','currency')
sql = """insert into view_sales 
    (TransferDate,SalesDate,SalesHour,ProductionPlace,ArticleNumber,Quantity,Unit,SalesPrice,CostOfSales,Currency) 
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

for line in lines:
    cursor.execute(sql,tuple([line[i] for i in sale_col]))


lines = requests.post(url+'/get_stock_data',headers=headers,json={})
lines = lines.json()
lines = lines['result']
stock_col = ('transfer_date','production_place','article_number',
            'unit','quantity','cost','currency')
sql = """insert into View_Stock 
    (TransferDate,ProductionPlace,ArticleNumber,Unit,Quantity,Cost,Currency) 
    VALUES (%s,%s,%s,%s,%s,%s,%s)"""
for line in lines:
    cursor.execute(sql,tuple([line[i] for i in stock_col]))
conn.commit()
cursor.close()
conn.close()

