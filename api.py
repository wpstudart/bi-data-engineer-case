from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_restful import reqparse
import mysql.connector
from mysql.connector import errorcode
import json
from collections import Counter
from datetime import datetime, time, timedelta

app=Flask(__name__)

@app.route('/')
def main():
    return "Welcome!"

@app.route('/postjson', methods=['POST'])
def postJSONHandler():
    print()
    #print (request.is_json)
    content = request.get_json() # Inserts the JSON in a Dictionary

    aggregation = content.get("aggregation")
    startTimestamp = content.get("startTimestamp")
    endTimestamp = content.get("endTimestamp")
    platform = content.get("platform")
    product = content.get("product")

    # 2016-01-03 13:55:00
    startTimestampDT = datetime.strptime(startTimestamp, '%Y-%m-%d %H:%M:%S')
    endTimestampDT = datetime.strptime(endTimestamp, '%Y-%m-%d %H:%M:%S')

    aggregationDelta = timedelta(minutes=aggregation)
    auxTimestampDT = startTimestampDT
    productBoughtCount = dict()
    productBoughtPlatform = dict()
    timestamps = []
    timestampBought = []
    timestamps.append(auxTimestampDT)

    while auxTimestampDT < endTimestampDT:
        #print(auxTimestampDT)
        
        try:
            cnx = mysql.connector.connect(user='root', password='password',
                                      host='127.0.0.1', database='bi_amaro')
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Wrong Credentials")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:

            if platform and product: # Working
                cursor = cnx.cursor()
                query = ("SELECT order_items.code_color AS code_color, COUNT(order_items.code_color) AS count, orders.device_type AS platform\
                        FROM orders LEFT JOIN order_items ON orders.id = order_items.order_id \
                        WHERE orders.order_date = '" + str(auxTimestampDT) + "' AND orders.device_type='" + platform + "' \
                        AND order_items.code_color= '" + product + "' GROUP BY order_items.code_color, orders.device_type;")
                #print(query)
                cursor.execute(query, multi=True)

                for(code_color, count, platform) in cursor:
                    print("{} {} {}".format(code_color, count, platform))
                    productBoughtCount[code_color] = count
                    productBoughtPlatform[code_color] = platform
                    timestampBought.append(auxTimestampDT)
                cursor.close()

            elif platform: # Working
                cursor = cnx.cursor()
                query = ("SELECT order_items.code_color AS code_color, COUNT(order_items.code_color) AS count, orders.device_type AS platform\
                        FROM orders LEFT JOIN order_items ON orders.id = order_items.order_id \
                        WHERE orders.order_date = '" + str(auxTimestampDT) + "' AND orders.device_type='" + platform + "' GROUP BY order_items.code_color, orders.device_type;")
                #print(query)
                cursor.execute(query, multi=True)

                for(code_color, count, platform) in cursor:
                    print("{} {} {}".format(code_color, count, platform))
                    productBoughtCount[code_color] = count
                    productBoughtPlatform[code_color] = platform
                    timestampBought.append(auxTimestampDT)
                cursor.close()

            elif product: # Working
                cursor = cnx.cursor()
                query = ("SELECT order_items.code_color AS code_color, COUNT(order_items.code_color) AS count, orders.device_type AS platform\
                        FROM orders LEFT JOIN order_items ON orders.id = order_items.order_id \
                        WHERE orders.order_date = '" + str(auxTimestampDT) + "' AND order_items.code_color= '" + product + "' GROUP BY order_items.code_color, orders.device_type;")
                #print(query)
                cursor.execute(query, multi=True)

                for(code_color, count, platform) in cursor:
                    print("{} {} {}".format(code_color, count, platform))
                    productBoughtCount[code_color] = count
                    productBoughtPlatform[code_color] = platform
                    timestampBought.append(auxTimestampDT)
                cursor.close()

            else: 
                cursor = cnx.cursor()
                query = ("SELECT order_items.code_color AS code_color, COUNT(order_items.code_color) AS count, orders.device_type AS platform\
                        FROM orders LEFT JOIN order_items ON orders.id = order_items.order_id \
                        WHERE orders.order_date = '" + str(auxTimestampDT) + "' GROUP BY order_items.code_color, orders.device_type;")
                cursor.execute(query, multi=True)

                for(code_color, count, platform) in cursor:
                    print("{} {} {}".format(code_color, count, platform))
                    productBoughtCount[code_color] = count
                    productBoughtPlatform[code_color] = platform
                    timestampBought.append(auxTimestampDT)
                cursor.close()

        auxTimestampDT = auxTimestampDT + aggregationDelta
        timestamps.append(auxTimestampDT)

    cnx.close()

    with open('productEvent_20160201.json') as json_file:
        data = json.load(json_file)
        products = []
        for i in data:
            if i['events'][0]['event_type'] == "custom_event":
                aux = i['events'][0]['data']['custom_attributes']['codeColor']
                products.append(aux)
    productEventCount = dict()
    for i in products:
        productEventCount[i] = productEventCount.get(i, 0) + 1

    CTR_Product = dict()
    for product in productEventCount:
        if product in productBoughtCount:
            CTR_Product[product] = "{0:.4f}".format(productBoughtCount[product]/productEventCount[product])
        else:
            CTR_Product[product] = "{0:.4f}".format(0)

    print(CTR_Product['20000686_002'])
    #timestampsJSON = dict()
    timestampsJSON = []
    for t in timestamps:
        #timestampsJSON['startTimestamp'] = datetime.strftime(t, '%Y-%m-%d %H:%M:%S')
        timestampsJSON.append(datetime.strftime(t, '%Y-%m-%d %H:%M:%S'))
        #print(json.dumps(response))

    response = [("startTimestamp", ts) for ts in timestampsJSON]

    '''
    response = json.dumps({"startTimestamp":ts, for ts in timestampsJSON.items()
                "platform":plat, for plat in productBougPlatform.items()ht
                "product":pro, for pro, key in productBoughtCount.items()
                "ctr":ctr, for ctr in CTR_Product.items()})
    '''
    #print(json.dumps(response))

    return 'JSON posted'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8090)
