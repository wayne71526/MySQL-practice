import requests
import mysql.connector
from mysql.connector import errorcode
import time

# 與 mysql 連線
DB_NAME = 'pchome'
try:
    cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1')
                                
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)

cursor = cnx.cursor()


# 建立 database 
def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))

try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)

        
# 建立 table
TABLES = {}
TABLES['products'] = (
    "CREATE TABLE `products` ("
    "  `product_name` varchar(100) NOT NULL,"
    "  `price` int NOT NULL,"
    "  PRIMARY KEY (`product_name`)"
    ") ENGINE=InnoDB")

table_description = TABLES['products']
try:
    print("Creating table products: ", end='')
    cursor.execute(table_description)
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
        print("already exists.")
    else:
        print(err.msg)
else:
    print("OK")

    
# 輸入資料
add_product = ("INSERT IGNORE INTO products " # IGNORE：遇到重複的 primary key 直接跳過
               "(product_name, price) "
               "VALUES (%s, %s)")

for page in range(1, 16):
    r = requests.get('https://24h.pchome.com.tw/search/v4.3/all/results?q=%E6%9B%B2%E9%9D%A2%E8%9E%A2%E5%B9%95&page={}&sort=rnk/dc'.format(page))
    if r.status_code == 200:
        print(page)
        d = r.json()
        prods = d['Prods']    
        if prods == [ ]:
            print(page)
            break
        for prod in prods:
            product_name = prod['Name']
            price        = prod['Price']
            data_product = (product_name, price)
            cursor.execute(add_product, data_product)
    else:
        print(r.status_code)
    time.sleep(5)
cnx.commit()

print('closing')
cursor.close()
cnx.close()