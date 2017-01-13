#!/usr/bin/env python

#
#The MIT License (MIT)
#
#Copyright (c) 2016 Mario Romero 
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

import mock
import os
import unittest
import sys
import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import bitso

from decimal import Decimal
import datetime

class FakeResponse(requests.Response):
    def __init__(self, content='', status_code=200):
        super(FakeResponse, self).__init__()
        self._content = content
        self._content_consumed = True
        self.status_code = status_code

class PublicApiTest(unittest.TestCase):
    def setUp(self):
        self.api = bitso.Api()

    def test_bad_response(self):
        response = FakeResponse(b"""{"success": false, "error": "something went wrong"}""")
        with mock.patch('requests.get', return_value=response):
            self.assertRaises(
                bitso.ApiError, self.api.ticker, "btc_mxn")

    def test_ticker(self):
        response = FakeResponse(b"""
        {
        "success": true,
        "payload": {
            "book": "btc_mxn",
            "volume": "22.31349615",
            "high": "5750.00",
            "last": "5633.98",
            "low": "5450.00",
            "vwap": "5393.45",
            "ask": "5632.24",
            "bid": "5520.01",
            "created_at": "2016-04-08T17:52:31.000+00:00"
            }
        }
            """)
        with mock.patch('requests.get', return_value=response):
            ticker = self.api.ticker('btc_mxn')
        self.assertIsInstance(ticker, bitso.Ticker)



    def test_order_book(self):
        response = FakeResponse(b"""
        {
            "success": true,
            "payload": {
                "asks": [{
                    "book": "btc_mxn",
                    "price": "5632.24",
                    "amount": "1.34491802",
                    "created_at": "2016-04-08T17:52:31.000+00:00",
                    "updated_at": null
                }],
                "bids": [{
                    "book": "btc_mxn",
                    "price": "6123.55",
                    "amount": "1.12560000",
                    "created_at": "2016-04-08T17:52:31.000+00:00",
                    "updated_at": null
                },{
                    "book": "btc_mxn",
                    "price": "6122.55",
                    "amount": "1.02560000",
                    "created_at": "2016-04-08T17:52:30.000+00:00",
                    "updated_at": null
                }],
                "created_at": "2016-04-08T17:52:31.000+00:00"
            }
        }
            """)
        with mock.patch('requests.get', return_value=response):
            result = self.api.order_book('btc_mxn')
        self.assertIsInstance(result, bitso.OrderBook)
        self.assertIsInstance(result.asks, list)
        self.assertEqual(len(result.asks), 1)
        self.assertIsInstance(result.bids, list)
        self.assertEqual(len(result.bids), 2)
        self.assertEqual(result.asks[0].price, Decimal("5632.24"))
        self.assertEqual(result.asks[0].amount, Decimal("1.34491802"))
        self.assertEqual(result.bids[0].price, Decimal("6123.55"))
        self.assertEqual(result.bids[0].amount, Decimal("1.12560000"))

        
        
    def test_trades(self):
        response = FakeResponse(b"""
        {
        "success": true,
        "payload": [{
           "book": "btc_mxn",
           "created_at": "2016-04-08T17:52:31.000+00:00",
           "amount": "0.02000000",
           "side": "buy",
           "price": "5545.01",
           "tid": 55845
        }, {
           "book": "btc_mxn",
           "created_at": "2016-04-08T17:52:31.000+00:00",
           "amount": "0.33723939",
           "side": "sell",
           "price": "5633.98",
           "tid": 55844
           }]
       }
        """)
        with mock.patch('requests.get', return_value=response):
            txs = self.api.trades(book='btc_mxn', time='hour')
        self.assertIsInstance(txs, list)
        self.assertEqual(len(txs), 2)
        self.assertEqual(txs[0].price, Decimal("5545.01"))
        self.assertEqual(txs[0].created_at.year, 2016)
        self.assertEqual(txs[0].created_at.month, 4)
        self.assertEqual(txs[0].created_at.day, 8)
        self.assertEqual(txs[0].created_at.hour, 17)
        self.assertEqual(txs[0].created_at.minute, 52)


          
    def test_trades_time_fail(self):
        self.assertRaises(bitso.ApiClientError,
                          self.api.trades, 'btc_mxn', 'hours')


    

                

class PrivateApiTest(unittest.TestCase):
    def setUp(self):
        self.api = bitso.Api('id', 'key','secret')


    def test_account_balance(self):
        response = FakeResponse(b"""
        {
            "success": true,
            "payload": {
                "balances": [{
                    "currency": "mxn",
                    "total": "100.1234",
                    "locked": "25.1234",
                    "available": "75.0000"
                }, {
                    "currency": "btc",
                    "total": "4.12345678",
                    "locked": "25.00000000",
                    "available": "75.12345678"
                }, {
                    "currency": "cop",
                    "total": "500000.1234",
                    "locked": "40000.1234",
                    "available": "10000.0000"
                }]
            }
        }
        """)
        with mock.patch('requests.get', return_value=response):
            result = self.api.balance()
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], bitso.Balance)
        self.assertIsInstance(result[1], bitso.Balance)
        self.assertIsInstance(result[2], bitso.Balance)
        self.assertEqual(result[0].available, Decimal("75.0000"))
        self.assertEqual(result[1].available, Decimal("75.12345678"))
        self.assertEqual(result[0].locked, Decimal("25.1234"))
        self.assertEqual(result[0].currency, "mxn")
    

    def test_fees(self):
        response = FakeResponse(b"""
        {
            "success": true,
            "payload": {
                "fees": [{
                    "book": "mxn_btc",
                    "fee_decimal": "0.0001",
                    "fee_percent": "0.01"
                }, {
                    "book": "mxn_eth",
                    "fee_decimal": "0.001",
                    "fee_percent": "0.1"
                }, {
                    "book": "cop_btc",
                    "fee_decimal": "0.01",
                    "fee_percent": "1"
                }]
            }
        }
        """)
        with mock.patch('requests.get', return_value=response):
            result = self.api.fees()
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], bitso.Fee)
        self.assertIsInstance(result[1], bitso.Fee)
        self.assertIsInstance(result[2], bitso.Fee)
        self.assertEqual(result[0].book, "mxn_btc")
        self.assertEqual(result[0].fee_decimal, Decimal("0.0001"))
        self.assertEqual(result[0].fee_percent, Decimal("0.01"))

    
    def test_ledger(self):
        with open('tests/ledger.json') as data_file:   
            response = FakeResponse(data_file.read().replace('\n', ''))
        with mock.patch('requests.get', return_value=response):
            result = self.api.ledger()
        for item in result:
            for bu in item.balance_updates:
                self.assertIsInstance(bu, bitso.BalanceUpdate)
                self.assertIsInstance(bu.amount, Decimal)
            self.assertIsInstance(item.created_at, datetime.datetime)
        
        
    def test_user_trades(self):
        response = FakeResponse(b"""
        {
            "success": true,
            "payload": [{
                "book": "btc_mxn",
                "major": "-0.25232073",
                "created_at": "2016-04-08T17:52:31.000+00:00",
                "minor": "1013.540958479115",
                "fees_amount": "-10.237787459385",
                "fees_currency": "mxn",
                "price": "4057.45",
                "tid": 51756,
                "oid": "19vaqiv72drbphig81d3y1ywri0yg8miihs80ng217drpw7xyl0wmytdhtby2ygk",
                "side": "sell"
            }, {
                "book": "eth_mxn",
                "major": "4.86859395",
                "created_at": "2016-04-08T17:52:31.000+00:00",
                "minor": "-626.77",
                "fees_amount": "-0.04917771",
                "fees_currency": "eth",
                "price": "127.45",
                "tid": 51757,
                "oid": "19vaqiv72drbphig81d3y1ywri0yg8miihs80ng217drpw7xyl0wmytdhtby2ygk",
                "side": "buy"
            }]
        }        
            """)
        with mock.patch('requests.get', return_value=response):
            trades = self.api.user_trades('btc_mxn', sort='desc')
        self.assertIsInstance(trades, list)
        self.assertEqual(len(trades), 2)
        self.assertEqual(trades[0].major, Decimal("-0.25232073"))
        self.assertEqual(trades[0].minor, Decimal("1013.540958479115"))
        self.assertEqual(trades[0].book, "btc_mxn")
        self.assertEqual(trades[0].tid, 51756)
        self.assertEqual(trades[0].oid, "19vaqiv72drbphig81d3y1ywri0yg8miihs80ng217drpw7xyl0wmytdhtby2ygk")
        self.assertEqual(trades[0].price, Decimal("4057.45"))
        self.assertEqual(trades[0].side, "sell")
        self.assertIsInstance(trades[0].created_at,datetime.datetime)

    
    def test_user_trades_fail(self):
        self.assertRaises(bitso.ApiClientError,
                          self.api.user_trades, "btc_mxn", sort='dec')


    

        
    def test_open_orders(self):
        response = FakeResponse(b"""
            {
                "success": true,
                "payload": [{
                    "book": "btc_mxn",
                    "amount": "0.01000000",
                    "created_at": "2016-04-08T17:52:31.000+00:00",
                    "updated_at": "2016-04-08T17:52:51.000+00:00",
                    "price": "5600.00",
                    "oid": "543cr2v32a1h684430tvcqx1b0vkr93wd694957cg8umhyrlzkgbaedmf976ia3v",
                    "side": "buy",
                    "status": "partial-fill",
                    "type": "limit"
                }, {
                    "book": "btc_mxn",
                    "amount": "0.12680000",
                    "created_at": "2016-04-08T17:52:31.000+00:00",
                    "updated_at": "2016-04-08T17:52:41.000+00:00",
                    "price": "4000.00",
                    "oid": "qlbga6b600n3xta7actori10z19acfb20njbtuhtu5xry7z8jswbaycazlkc0wf1",
                    "side": "sell",
                    "status": "open",
                    "type": "limit"
                }, {
                    "book": "btc_mxn",
                    "amount": "1.12560000",
                    "created_at": "2016-04-08T17:52:31.000+00:00",
                    "updated_at": "2016-04-08T17:52:41.000+00:00",
                    "price": "6123.55",
                    "oid": "d71e3xy2lowndkfmde6bwkdsvw62my6058e95cbr08eesu0687i5swyot4rf2yf8",
                    "side": "sell",
                    "status": "open",
                    "type": "limit"
                }]
            }
         """)
        with mock.patch('requests.get', return_value=response):
            result = self.api.open_orders()
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].amount, Decimal("0.01000000"))
        self.assertEqual(result[0].price, Decimal("5600.00"))
        self.assertEqual(result[0].type, 'limit')
        self.assertEqual(result[0].side, 'buy')
        self.assertEqual(result[0].status, 'partial-fill')
        self.assertEqual(result[0].oid, '543cr2v32a1h684430tvcqx1b0vkr93wd694957cg8umhyrlzkgbaedmf976ia3v')
        self.assertIsInstance(result[0].created_at,datetime.datetime)
        self.assertIsInstance(result[0].updated_at,datetime.datetime)
        self.assertEqual(result[1].status, 'open')
        self.assertEqual(result[1].price, Decimal("4000"))


    def test_lookup_order(self):
        response = FakeResponse(b"""
        {
            "success": true,
            "payload": [{
                "book": "btc_mxn",
                "amount": "0.01000000",
                "created_at": "2016-04-08T17:52:31.000+00:00",
                "updated_at": "2016-04-08T17:52:51.000+00:00",
                "price": "5600.00",
                "oid": "543cr2v32a1h684430tvcqx1b0vkr93wd694957cg8umhyrlzkgbaedmf976ia3v",
                "side": "buy",
                "status": "partial-fill",
                "type": "limit"
            }, {
                "book": "btc_mxn",
                "amount": "0.12680000",
                "created_at": "2016-04-08T17:52:31.000+00:00",
                "updated_at": "2016-04-08T17:58:31.000+00:00",
                "price": "4000.00",
                "oid": "qlbga6b600n3xta7actori10z19acfb20njbtuhtu5xry7z8jswbaycazlkc0wf1",
                "side": "sell",
                "status": "open",
                "type": "limit"

            }, {
                "book": "btc_mxn",
                "amount": "1.12560000",
                "created_at": "2016-04-08T17:52:31.000+00:00",
                "updated_at": "2016-04-08T17:53:31.000+00:00",
                "price": "6123.55",
                "oid": "d71e3xy2lowndkfmde6bwkdsvw62my6058e95cbr08eesu0687i5swyot4rf2yf8",
                "side": "sell",
                "status": "open",
                "type": "limit"
            }]
        }
        """)
        
        with mock.patch('requests.get', return_value=response):
            result = self.api.lookup_order(['543cr2v32a1h684430tvcqx1b0vkr93wd694957cg8umhyrlzkgbaedmf976ia3v','qlbga6b600n3xta7actori10z19acfb20njbtuhtu5xry7z8jswbaycazlkc0wf1'])

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].type, 'limit')
        self.assertEqual(result[0].price, Decimal('5600.00'))
        self.assertEqual(result[0].amount, Decimal('0.01000000'))
    
    def test_cancel_order(self):
        response = FakeResponse(b"""
        {
            "success": true,
            "payload":[
                "543cr2v32a1h684430tvcqx1b0vkr93wd694957cg8umhyrlzkgbaedmf976ia3v",
                "qlbga6b600n3xta7actori10z19acfb20njbtuhtu5xry7z8jswbaycazlkc0wf1",
                "d71e3xy2lowndkfmde6bwkdsvw62my6058e95cbr08eesu0687i5swyot4rf2yf8"
                ]
        }
        """)
        with mock.patch('requests.delete', return_value=response):
            result = self.api.cancel_order(["543cr2v32a1h684430tvcqx1b0vkr93wd694957cg8umhyrlzkgbaedmf976ia3v","qlbga6b600n3xta7actori10z19acfb20njbtuhtu5xry7z8jswbaycazlkc0wf1","d71e3xy2lowndkfmde6bwkdsvw62my6058e95cbr08eesu0687i5swyot4rf2yf8"])
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)
        

    def test_funding_destination(self):
        response = FakeResponse(b"""
        {
            "success": true,
            "payload": {
                "account_identifier_name": "SPEI CLABE",
                "account_identifier": "646180115400346012"             
            }
        }   
        """)
        with mock.patch('requests.get', return_value=response):
            result = self.api.funding_destination('mxn')
        self.assertIsInstance(result, bitso.FundingDestination)
        self.assertEqual(result.account_identifier_name, "SPEI CLABE")
        self.assertEqual(result.account_identifier, "646180115400346012")
        

    def test_btc_withdrawal(self):
        response = FakeResponse(b"""
        {
            "success": true,
            "payload": {
                "wid": "c5b8d7f0768ee91d3b33bee648318688",
                "status": "pending",
                "created_at": "2016-04-08T17:52:31.000+00:00",
                "currency": "btc",
                "method": "Bitcoin",
                "amount": "0.48650929",
                "details": {
                    "withdrawal_address": "3EW92Ajg6sMT4hxK8ngEc7Ehrqkr9RoDt7",
                    "tx_hash": null
                }
            }
        }
        """)
        with mock.patch('requests.post', return_value=response):
            result = self.api.btc_withdrawal('0.48650929','3EW92Ajg6sMT4hxK8ngEc7Ehrqkr9RoDt7')
        self.assertIsInstance(result, bitso.Withdrawal)
        self.assertIsInstance(result.details, dict)
        self.assertIsInstance(result.created_at, datetime.datetime)
        self.assertEqual(result.amount, Decimal("0.48650929"))

    def test_eth_withdrawal(self):
        response = FakeResponse(b"""
        {
            "success": true,
            "payload": {
                "wid": "c5b8d7f0768ee91d3b33bee648318698",
                "status": "pending",
                "created_at": "2016-04-08T17:52:31.000+00:00",
                "currency": "btc",
                "method": "Ether",
                "amount": "10.00",
                "details": {
                    "withdrawal_address": "0x55f03a62acc946dedcf8a0c47f16ec3892b29e6d",
                    "tx_hash": null
                }
            }
        }
        """)
        with mock.patch('requests.post', return_value=response):
            result = self.api.eth_withdrawal('10.00','0x55f03a62acc946dedcf8a0c47f16ec3892b29e6d')
        self.assertIsInstance(result, bitso.Withdrawal)
        self.assertIsInstance(result.details, dict)
        self.assertIsInstance(result.created_at, datetime.datetime)
        self.assertEqual(result.amount, Decimal("10.00"))

    def test_ripple_withdrawal(self):
        response = FakeResponse(b"""
        {
            "success": true,
            "payload": {
                "wid": "c5b8d7f0768ee91d3b33bee648318688",
                "status": "pending",
                "created_at": "2016-04-08T17:52:31.000+00:00",
                "currency": "btc",
                "method": "Ripple",
                "amount": "0.48650929",
                "details": {
                    "withdrawal_address": "rG1QQv2nh2gr7RCZ1P8YYcBUKCCN633jCn",
                    "tx_id": null
                }
            }
        }
        """)
        with mock.patch('requests.post', return_value=response):
            result = self.api.ripple_withdrawal('btc', '0.48650929','rG1QQv2nh2gr7RCZ1P8YYcBUKCCN633jCn')
        self.assertIsInstance(result, bitso.Withdrawal)
        self.assertIsInstance(result.details, dict)
        self.assertIsInstance(result.created_at, datetime.datetime)
        self.assertEqual(result.amount, Decimal("0.48650929"))

    def test_spei_withdrawal(self):
        response = FakeResponse(b"""
        {
            "success": true,
            "payload": {
                "wid": "p4u8d7f0768ee91d3b33bee6483132i8",
                "status": "pending",
                "created_at": "2016-04-08T17:52:31.000+00:00",
                "currency": "mxn",
                "method": "SPEI Transfer",
                "amount": "300.15",
                "details": {
                    "sender_name": "JUAN ESCUTIA",
                    "receive_clabe": "012610001967722183",
                    "sender_clabe": "646180115400467548",
                    "numeric_reference": "80416",
                    "concepto": "Tacos del viernes",
                    "clave_rastreo": null,
                    "beneficiary_name": "FRANCISCO MARQUEZ"
                }
            }
        }
        """)
        with mock.patch('requests.post', return_value=response):
            result = self.api.spei_withdrawal(amount='0.48650929', first_names="FRANCISCO", last_names="MARQUEZ", clabe="012610001967722183")
        self.assertIsInstance(result, bitso.Withdrawal)
        self.assertIsInstance(result.details, dict)
        self.assertIsInstance(result.created_at, datetime.datetime)
        self.assertEqual(result.amount, Decimal("300.15"))
                                        
    


    def test_place_order(self):
        response = FakeResponse(b"""
        {
            "success": true,
            "payload": {
                "book": "btc_mxn",
                "amount": "0.01000000",
                "created_at": "2016-04-08T17:52:31.000+00:00",
                "updated_at": null,
                "price": "5600.00",
                "oid": "543cr2v32a1h684430tvcqx1b0vkr93wd694957cg8umhyrlzkgbaedmf976ia3v",
                "side": "buy",
                "status": "open",
                "type": "limit"
            }
        }
        """)
        with mock.patch('requests.post', return_value=response):
            result = self.api.place_order(book='btc_mxn', side='buy', order_type='limit', major='0.1', price='5600')
        self.assertIsInstance(result, bitso.Order)
        self.assertIsInstance(result.created_at,datetime.datetime)
        self.assertEqual(result.amount, Decimal('0.01000000'))

    def test_transfer_quote(self):
        response = FakeResponse(b'''
        {
           "payload":{
              "btc_amount":"0.14965623",
              "currency":"MXN",
              "rate":"3340.99",
              "gross":"500.00",
              "outlets":{
                 "sp":{
                    "id":"sp",
                    "name":"SPEI Transfer",
                    "required_fields":[
                       "recipient_given_names",
                       "recipient_family_names",
                       "clabe",
                       "bank_name"
                    ],
                    "minimum_transaction":"500.00",
                    "maximum_transaction":"2500000.00",
                    "daily_limit":"10000.00",
                    "fee":"12.00",
                    "net":"488.00",
                    "available":"1",
                    "verification_level_requirement":"0"
                 },
                 "vo":{
                    "id":"vo",
                    "name":"Voucher",
                    "required_fields":[
                       "email_address"
                    ],
                    "minimum_transaction":"25.00",
                    "maximum_transaction":"9999.00",
                    "fee":"0.00",
                    "daily_limit":"0.00",
                    "net":"500.00",
                    "available":"1",
                    "verification_level_requirement":"0"
                 },
                 "rp":{
                    "id":"rp",
                    "name":"Ripple",
                    "required_fields":[
                       "ripple_address"
                    ],
                    "minimum_transaction":"0.00",
                    "maximum_transaction":"10000000.00",
                    "fee":"5.00",
                    "daily_limit":"0.00",
                    "net":"495.00",
                    "available":"1",
                "verification_level_requirement":"0"
             },
             "pm":{
                "id":"pm",
                "name":"Pademobile",
                "required_fields":[
                   "phone_number"
                ],
                "minimum_transaction":"1.00",
                "maximum_transaction":"1000000.00",
                "fee":"0.00",
                "daily_limit":"0.00",
                "net":"500.00",
                "available":"1",
                "verification_level_requirement":"0"
             },
             "bw":{
                "id":"bw",
                "name":"Bank Wire",
                "required_fields":[
                   "recipient_full_name",
                   "account_holder_address",
                   "bank_name",
                   "bank_address",
                   "account_number",
                   "swift",
                   "other_instructions"
                ],
                "minimum_transaction":"1000.00",
                "maximum_transaction":"2500000.00",
                "daily_limit":"2500000.00",
                "fee":"500.00",
                "net":"0.00",
                "available":"1",
                "verification_level_requirement":"0"
             }
          },
          "created_at":"2016-04-08T17:52:31.000+00:00",
          "expires_at":"2016-04-08T18:02:31.000+00:00"
       },
       "success":true
        }''')
        with mock.patch('requests.post', return_value=response):
            result = self.api.transfer_quote(amount='0.14965623', currency='MXN')
        self.assertIsInstance(result, bitso.TransactionQuote)
        self.assertEqual(result.btc_amount, Decimal('0.14965623'))
        self.assertEqual(result.currency, 'MXN')
        self.assertEqual(result.rate, Decimal('3340.99'))
        self.assertEqual(result.gross, Decimal('500.00'))
        self.assertIsInstance(result.outlets, dict)
        self.assertEqual(result.outlets['sp']['minimum_transaction'], Decimal('500.00'))
        self.assertEqual(result.outlets['sp']['maximum_transaction'], Decimal('2500000.00'))
        self.assertEqual(result.outlets['bw']['daily_limit'], Decimal('2500000.00'))
        self.assertEqual(result.outlets['bw']['fee'], Decimal('500.00'))
        self.assertEqual(result.outlets['bw']['net'], Decimal('0.00'))
        self.assertEqual(result.outlets['bw']['available'], True)


    def test_create_transfer(self):
        response = FakeResponse(b'''
        {
            "payload":{
              "btc_amount":"0.14965623",
              "btc_pending":"0",
              "btc_received":"0",
              "confirmation_code":"9b2a4",
              "created_at": "2016-04-08T17:52:31.000+00:00",
              "currency":"MXN",
              "currency_amount":"0",
              "currency_fees":"0",
              "currency_settled":"0",
              "expires_at":"2016-04-08T18:02:31.000+00:00",
              "fields":{
                 "phone_number":"5554181042"
              },
              "id":"9b2a431b98597312e99cbff1ba432cbf",
              "payment_outlet_id":"pm",
              "qr_img_uri":"https:\/\/chart.googleapis.com\/chart?chl=bitcoin%3AmgKZfNdFJgztvfvhEaGgMTQRQ2iHCadHGa%3Famount%3D0.14965623&chs=400x400&cht=qr&choe=UTF-8&chld=L%7C0",
              "user_uri":"https:\/\/api.bitso.com\/v2\/transfer\/9b2a431b98597312e99cbff1ba432cbf",
              "wallet_address":"mgKZfNdFJgztvfvhEaGgMTQRQ2iHCadHGa"
           },
           "success":true
        }''')
        with mock.patch('requests.post', return_value=response):
            result = self.api.transfer_create(btc_amount='0.14965623',
                                   currency='MXN',
                                   rate='7585.20',
                                   payment_outlet='pm')
        self.assertIsInstance(result, bitso.TransactionOrder)
        self.assertEqual(result.btc_amount, Decimal('0.14965623'))

        self.assertEqual(result.btc_pending, Decimal('0'))
        self.assertEqual(result.btc_received, Decimal('0.0'))
        self.assertEqual(result.confirmation_code, '9b2a4')
        self.assertEqual(result.currency, 'MXN')
        self.assertEqual(result.fields['phone_number'], '5554181042')
        self.assertEqual(result.btc_amount, Decimal('0.14965623'))
        self.assertEqual(result.wallet_address, 'mgKZfNdFJgztvfvhEaGgMTQRQ2iHCadHGa')
        


        
if __name__ == '__main__':
    unittest.main()
