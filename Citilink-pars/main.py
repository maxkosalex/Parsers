import json
import random
import sqlite3
import datetime
import requests
import time

from config import headers, json_data


def record_products():
    with open('page.html', 'r', encoding='utf-8') as file:
        data = file.read()
        js = json.loads(data)
        i = 1
        db = sqlite3.connect('data.db')
        cursor = db.cursor()
        for i in range(len(js['data']['productsFilter']['record']['products'])):
            ID = js['data']['productsFilter']['record']['products'][i]["id"]
            name = js['data']['productsFilter']['record']['products'][i]["shortName"]
            cost = js['data']['productsFilter']['record']['products'][i]['price']["current"]
            data = datetime.datetime.now()
            cursor.execute("INSERT INTO Products (id, name, cost, data) VALUES (?, ?, ?, ?)",(ID, name, cost, data))
        db.commit()
        db.close()


def scrap():
    db = sqlite3.connect('data.db')

    try:
        i = 1

        while True:
            time.sleep(random.randint(3, 10))
            response = requests.post('https://www.citilink.ru/graphql/', headers=headers(i), json=json_data(i))
            js = json.loads(response.text)

            for j in range(len(js['data']['productsFilter']['record']['products'])):
                ID = js['data']['productsFilter']['record']['products'][j]["id"]
                name = js['data']['productsFilter']['record']['products'][j]["shortName"]
                cost = js['data']['productsFilter']['record']['products'][j]['price']["current"]
                date = datetime.datetime.now()

                cursor = db.cursor()

                if int(ID) in all_products():

                    cursor.execute("UPDATE Products SET cost = ?, date = ? WHERE id = ?",
                                   (cost, date, ID))
                    db.commit()
                    print("Такой продукт есть: ", ID, "\n", name, "\n", cost, "\n", date)

                else:
                    cursor.execute("INSERT INTO Products (id, name, cost, date) VALUES (?, ?, ?, ?)",
                                   (ID, name, cost, date))
                    db.commit()
                    print("Такого продукта нет: ", ID, "\n", name, "\n", cost, "\n", date)

            i += 1

    except Exception as ex:
        db.close()
        print(ex)


def all_products():
    db = sqlite3.connect('data.db')
    cursor = db.cursor()

    products = list(map(lambda x: x[0], cursor.execute("SELECT ID FROM Products").fetchall()))

    db.close()
    return products


if __name__ == "__main__":
    scrap()
