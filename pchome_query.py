# 利用 Python 對資料庫查詢
cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='pchome')
cursor = cnx.cursor(dictionary=True)  # 每一筆資料以字典的形式表示

query = ("SELECT * FROM products "
         "WHERE product_name LIKE '%ASUS%'")  # '%ASUS%'：表示 ASUS 前後可以有任何東西

cursor.execute(query)

for row in cursor:
    print(row)

cursor.close()
cnx.close()