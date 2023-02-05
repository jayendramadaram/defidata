import csv
import json
import requests
import os
from dotenv import load_dotenv
from time import sleep
import bisect
from collections import defaultdict


load_dotenv()

tokens = [
    "0x514910771af9ca656af840dff83e8264ecf986ca",
    "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
    "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
    "0xdAC17F958D2ee523a2206206994597C13D831ec7",
    "0x95aD61b0a150d79219dCF64E1E6Cc01f0B64C4cE",
    "0x6b175474e89094c44da98b954eedeac495271d0f",
    "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599",
    "0xae7ab96520de3a18e5e111b5eaab095312d7fe84",
    "0x6368e1e18c4c419ddfc608a0bed1ccb87b9250fc",
    "0x7f39c581f595b53c5cb19bd0b3f8da6c935e2ca0",
    "0x3432b6a60d23ca0dfca7761b7ab56459d9c964d0",
    "0xb62132e35a6c13ee1ee0f84dc5d40bad8d815206",
    "0x2b591e99afe9f32eaa6214f7b7629768c40eeb39",
    "0xd533a949740bb3306d119cc777fa900ba034cd52",
]


class ARBITRAGE:
    def __init__(self) -> None:
        self.url = os.getenv('API_CALL_URL')
        self.tokens_url = self.url + ",".join(tokens)

    def WriteToJSON(self):
        resp = requests.get(self.tokens_url)
        json_object = json.dumps(json.loads(resp.text), indent=4)
        with open('data.json', 'w') as file:
            file.write(json_object)

    def ReadJSON(self):
        with open('data.json', 'r') as file:
            resp = file.read()
        dic = json.loads(resp)

    def WriteToCsv(self):
        with open("data.csv", 'w', newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([
                "chainId", "dexId", "baseToken-symbol", "quoteToken-symbol", 'priceUsd', "priceNative", "liquidity-usd", "liquidity-base", "liquidity-quote", "fdv"
            ])
            for tok_addr in tokens:
                resp = requests.get(self.url + tok_addr)
                dic = json.loads(resp.text)
                pairs = dic["pairs"]
                print(len(pairs), self.url + tok_addr)
                if (pairs):
                    for i in pairs:
                        try:
                            csvwriter.writerow([i["chainId"], i["dexId"], i["baseToken"]
                                                ["symbol"], i["quoteToken"]["symbol"], i['priceUsd'], i["priceNative"], i["liquidity"]["usd"], i["liquidity"]["base"], i["liquidity"]["quote"], i["fdv"]])
                        except Exception as e:
                            print(i)
                            print()
                            print(e)
                            input()
                else:
                    print(pairs, tok_addr)

                sleep(3)

    def insert_in_order(self, lst, elem):
        index = bisect.bisect_left(
            [x[1] for x in lst], elem[1])
        lst.insert(index, elem)

    def cluster(self):
        clusterring = defaultdict(list)

        for tok_addr in tokens:
            resp = requests.get(self.url + tok_addr)
            dic = json.loads(resp.text)
            pairs = dic["pairs"]
            print(len(pairs), self.url + tok_addr)
            if (pairs):
                for i in pairs:
                    try:
                        key = i["baseToken"]["symbol"] + "/" + \
                            i["quoteToken"]["symbol"]
                        self.insert_in_order(
                            clusterring[key], (i["dexId"],  i['priceUsd']))
                    except Exception as e:
                        print(e)
                        print(e.__traceback__.tb_lineno)
                        input("check")
        print(clusterring)
        json_object = json.dumps(clusterring, indent=4)
        with open('cluster.json', 'w') as file:
            file.write(json_object)


obj = ARBITRAGE()
obj.cluster()
