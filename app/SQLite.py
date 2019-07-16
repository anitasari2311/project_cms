import sqlite3

class DB:
    def CreateDB(self):
        connected = sqlite3.connect('StoreData/DB_Crawling')
        cursors = connected.cursor()
        cursors.execute('''CREATE TABLE IF NOT EXISTS tableMerchantTokopedia(
                                Date_Crawling DATE NOT NULL,
                                Merchant_name TEXT NOT NULL,
                                Merchant_rate_point TEXT NOT NULL,
                                Merchant_location TEXT NOT NULL,
                                Merchant_established DATE NOT NULL,
                                Merchant_sold_product INT NOT NULL,
                                Merchant_succesful_transaction INT NOT NULL,
                                Merchant_showcase INT NOT NULL,
                                Merchant_active_product INT NOT NULL,
                                Merchant_followers INT NOT NULL,
                                Merchant_html_path TEXT NOT NULL,
                                Merchant_stat_1_month INT NOT NULL,
                                Merchant_stat_3_month INT NOT NULL,
                                Merchant_stat_12_month INT NOT NULL)''')
        cursors.execute('''CREATE TABLE IF NOT EXISTS tableProductTokopedia(
                                Product_name TEXT NOT NULL,
                                Product_price INT NOT NULL,
                                Product_sold  INT NOT NULL,
                                Product_rate TEXT NOT NULL,
                                Product_image TEXT,
                                Product_merchant TEXT,
                                FOREIGN KEY (Product_merchant) REFERENCES tableMerchant (Merchant_html_path))''')
        cursors.execute('''CREATE TABLE IF NOT EXISTS tableMerchantShopee(
                                Merchant_name TEXT NOT NULL,
                                Merchant_location INT NOT NULL,
                                Merchant_active_product  INT NOT NULL,
                                Merchant_followers INT NOT NULL,
                                Merchant_rate_point FLOAT NOT NULL,
                                Merchant_established TEXT NOT NULL,
                                Merchant_html_path TEXT NOT NULL)''')
        connected.commit()
        cursors.close()
        connected.close()
    def InsertDB_Merchant(self,Date_Crawling, Merchant_name, Merchant_rate_point, Merchant_location, Merchant_established, Merchant_sold_product, Merchant_succesful_transaction, Merchant_showcase, Merchant_active_product, Merchant_followers, Merchant_html_path, Merchant_stat_1_month, Merchant_stat_3_month, Merchant_stat_12_month):
        connected = sqlite3.connect('StoreData/DB_Crawling')
        cursors = connected.cursor()
        cursors.execute("INSERT INTO tableMerchantTokopedia VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(Date_Crawling, Merchant_name, Merchant_rate_point, Merchant_location, Merchant_established, Merchant_sold_product, Merchant_succesful_transaction, Merchant_showcase, Merchant_active_product, Merchant_followers, Merchant_html_path, Merchant_stat_1_month, Merchant_stat_3_month, Merchant_stat_12_month))
        connected.commit()
        cursors.close()
        connected.close()
    def InsertDB_Product(self,Product_name, Product_price, Product_sold, Product_rate, Product_image, Product_merchant):
        connected = sqlite3.connect('StoreData/DB_Crawling')
        cursors = connected.cursor()
        cursors.execute("INSERT INTO tableProductTokopedia VALUES (?,?,?,?,?,?)",(Product_name, Product_price, Product_sold, Product_rate, Product_image, Product_merchant))
        connected.commit()
        cursors.close()
        connected.close()
    def InsertDB_Product2(self,Product_name, Product_price, Product_sold, Product_rate, Product_image, Product_merchant):
        connected = sqlite3.connect('StoreData/DB_Crawling')
        cursors = connected.cursor()
        cursors.execute("INSERT INTO tableProductTokopedia2 VALUES (?,?,?,?,?,?)",(Product_name, Product_price, Product_sold, Product_rate, Product_image, Product_merchant))
        connected.commit()
        cursors.close()
        connected.close()
    def Delete_Product(self):
        connected = sqlite3.connect('StoreData/DB_Crawling')
        cursors = connected.cursor()
        cursors.execute("DELETE FROM tableProductTokopedia2")
        connected.commit()
        cursors.close()
        connected.close()
    def Create_table(self):
        connected = sqlite3.connect('StoreData/DB_Crawling')
        cursors = connected.cursor()
        cursors.execute('''CREATE TABLE IF NOT EXISTS tableProductTokopedia2(
                                Product_name TEXT NOT NULL,
                                Product_price INT NOT NULL,
                                Product_sold  INT NOT NULL,
                                Product_rate TEXT NOT NULL,
                                Product_image TEXT,
                                Product_merchant TEXT,
                                FOREIGN KEY (Product_merchant) REFERENCES tableMerchant (Merchant_html_path))''')
        connected.commit()
        cursors.close()
        connected.close()
    def Create_table_temp(self):
        connected = sqlite3.connect('StoreData/DB_Crawling')
        cursors = connected.cursor()
        cursors.execute('''CREATE TABLE IF NOT EXISTS tableTemp(
                                Merchant_html_path TEXT NOT NULL,
                                Merchant_active_product INT NOT NULL,
                                Merchant_followers INT NOT NULL)''')
        connected.commit()
        cursors.close()
        connected.close()
    def Insert_table(self):
        connected = sqlite3.connect('StoreData/DB_Crawling')
        cursors = connected.cursor()
        cursors.execute('INSERT INTO tableTemp SELECT Merchant_html_path, Merchant_active_product, Merchant_followers FROM tableMerchantTokopedia ORDER BY Merchant_followers DESC')
        connected.commit()
        cursors.close()
        connected.close()
