# bitso-py #


A Python 2 and Python 3 wrapper for the [Bitso API](https://bitso.com/api_info/) 

[![Build Status](https://travis-ci.org/mariorz/python-bitso.svg?branch=master)](https://travis-ci.org/mariorz/python-bitso) [![Requirements Status](https://requires.io/github/mariorz/python-bitso/requirements.svg?branch=master)](https://requires.io/github/mariorz/python-bitso/requirements/?branch=master) 

# Public API Usage #

```python
 >>> import bitso
 >>> api = bitso.Api()
```


# Private API Usage #

```python
 >>> import bitso
 
## Production account
 >>> api = bitso.Api(API_KEY, API_SECRET)

## Developer account
 >>> api = bitso.Api(API_KEY, API_SECRET,"dev")
  
```


# Public calls #

### Available Books ###

```python
## Order books available on Bitso
 >>> books = api.available_books()
 >>> books
AvilableBooks(books=btc_mxn,eth_mxn)
 >>> books.btc_mxn
Book(symbol=btc_mxn)
 >>> books.btc_mxn.minimum_amount
Decimal('0.00500000')
 ```


### Ticker ###

```python
## Ticker information
## Parameters
## [book] - Specifies which book to use
##                  - string
 >>> tick = api.ticker('btc_mxn')
 >>> tick
 Ticker(ask=7866.27, bid=7795.00, high=7866.27, last=7866.27, low=7707.43, datetime=2016-04-22 16:46:25, vwaplow=7795.00)
 >>> tick.last
 Decimal('7866.27')
 >>> tick.created_at
 datetime.datetime(2016, 4, 22, 16, 46, 53)
 ```


### Order Book ###

```python
## Public order book
## Parameters
## [book] - Specifies which book to use
##                  - string
## [aggregate = True] - Group orders with the same price
##                - boolean
>>> ob = api.order_book('btc_mxn')
>>> ob.updated_at
atetime.datetime(2016, 12, 13, 22, 54, 2, tzinfo=tzutc()) 
>>> ob.bids
[PublicOrder(book=btc_mxn,price=3160.00, amount=0.63966069),
 PublicOrder(book=btc_mxn,price=2959.00, amount=0.72143122),
 PublicOrder(book=btc_mxn,price=2850.00, amount=3.00000000),
 PublicOrder(book=btc_mxn,price=2750.00, amount=1.00000000),
 PublicOrder(book=btc_mxn,price=2500.12, amount=45.00000000),
 ...
]
>>> ob.asks

[PublicOrder(book=btc_mxn,price=8000.00, amount=48.37402966),
 PublicOrder(book=btc_mxn,price=8160.00, amount=0.12340000),
 PublicOrder(book=btc_mxn,price=9000.00, amount=40.00000000),
 PublicOrder(book=btc_mxn,price=9160.00, amount=0.76500000)
 ...
 ]

```

### Trades ###

```python
## Public trades
## Parameters
## [book = 'btc_mxn'] - Specifies which book to use
##                    - str
## [marker = None] - Returns objects that are older or newer (depending on 'sort’) than the object with this ID
##                    - str
## [sort = 'desc'] - Specifies ordering direction of returned objects (asc, desc)
##                    - str
## [limit = '25'] - Specifies number of objects to return. (Max is 100)
##                    - str

>>> trades = api.trades('btc_mxn')
>>> trades
[Trade(tid=1602, price=3160.00, amount=0.00797922, maker_side=buy, created_at=2016-12-13 21:32:05+00:00),
 Trade(tid=1601, price=3160.00, amount=0.01000000, maker_side=buy, created_at=2016-12-13 21:32:05+00:00),
 Trade(tid=1600, price=8000.00, amount=0.00312500, maker_side=sell, created_at=2016-12-13 21:32:04+00:00),
 Trade(tid=1599, price=8000.00, amount=0.01008572, maker_side=sell, created_at=2016-12-13 21:32:04+00:00),
 ...
 ]

>>> trades[0].price
Decimal('3160.00')
>>> trades[0].amount
Decimal('0.00797922')
>>> trades[0].created_at
datetime.datetime(2016, 12, 13, 21, 32, 5, tzinfo=tzutc())

```


# Private calls #

Private endpoints are used to manage your account and your orders. These requests must be signed
with your [Bitso credentials](https://bitso.com/api_info#generating-api-keys) 

```python
 >>> import bitso
 >>> api = bitso.Api(API_KEY, API_SECRET)
```

### Account Status ###

```python
## Your account status
>>> status = api.account_status()
>>> status.daily_limit
Decimal('5300')
>>> status.daily_remaining
Decimal('5300.00')

```



### Account Balances ###

```python
## Your account balances
>>> balances = api.balances()
>>> balances
Balances(currencies=btc,etc,eth,mxn)
>>> balances.currencies
[u'btc', u'etc', u'eth', u'mxn']
>>> balances.btc.name
u'btc'
>>> balances.btc.available
Decimal('3.46888741')

```

### Fees ###

```python
## Your trade fees
>>> fees = api.fees()
>>> fees
Fees(books=btc_mxn,eth_mxn)
>>> fees.books
[u'btc_mxn', u'eth_mxn']
>>> fees.btc_mxn
Fee(book=btc_mxn, fee_percent=0.0000)
>>> fees.btc_mxn.fee_percent
Decimal('0.8500')
>>> fees.withdrawal_fees
WithdawalFees(curencies=eth,btc)
>>> fees.withdrawal_fees.btc
Decimal('0.001')

```

### Ledger ###
```python
## A ledger of your historic operations.
## Parameters
## [marker]    - Returns objects that are older or newer (depending on 'sort’) than the object with this ID
##                 - string
## [limit = 25]   - Limit result to that many transactions
##                 - int
## [sort = 'desc'] - Sorting by datetime
##                 - string - 'asc' or
##                 - 'desc'

>>> ledger = api.ledger()
>>> ledger
[<bitso.models.LedgerEntry at 0x10d4fdc50>,
 <bitso.models.LedgerEntry at 0x10d4fd550>,
 <bitso.models.LedgerEntry at 0x10d5c4d90>,
 <bitso.models.LedgerEntry at 0x10d5c4bd0>,
 <bitso.models.LedgerEntry at 0x10d5c4550>,
 ...
 ]
>>> ledger[0].operation
u'fee'
>>> ledger[1].operation
u'trade'
>>> ledger[1].balance_updates
[BalanceUpdate(currency=mxn, amount=25.21433520,
BalanceUpdate(currency=btc, amount=-0.00797922]
>>> ledger[1].balance_updates[0].amount
Decimal('25.21433520')
```

### Withdrawals ###

```python
## Detailed info on your fund withdrawals.
## Parameters
## [wids]    - Specifies which withdrawal objects to return by IDs
##                 - list
## [marker]    - Returns objects that are older or newer (depending on 'sort’) than the object with this ID
##                 - string
## [limit = 25]   - Limit result to that many transactions
##                 - int
## [sort = 'desc'] - Sorting by datetime
##                 - string - 'asc' or
##                 - 'desc'

>>> withdrawals = api.withdrawals()
>>> withdrawals
[Withdrawal(wid=019e8f42da7eb0e44bf5ce0013475058, amount=0.001, currency=btc),
 Withdrawal(wid=efa28b88e326619d91ba809a82e1282b, amount=0.001, currency=btc),
 Withdrawal(wid=9bbde562c7de3e0c5315993a944d3873, amount=0.001, currency=btc),
 Withdrawal(wid=e19b33a5ec2606e8a25963ceea9d2254, amount=0.001, currency=btc),
 Withdrawal(wid=b76af418eb94c61b72c6bb20d316e115, amount=0.001, currency=btc),
 ...
 ]
>>> withdrawals[0].status
u'pending'
>>> withdrawals[0].method
u'Bitcoin'
>>> withdrawals[0].amount
Decimal('0.001')
```

### Fundings ###

```python
## Detailed info on your fundings.
## Parameters
## [fids]    - Specifies which funding objects to return by IDs
##                 - list
## [marker]    - Returns objects that are older or newer (depending on 'sort’) than the object with this ID
##                 - string
## [limit = 25]   - Limit result to that many transactions
##                 - int
## [sort = 'desc'] - Sorting by datetime
##                 - string - 'asc' or
##                 - 'desc'

>>> fundings = api.fundings()
>>> fundings
[Funding(fid=4e28aa988a74d8b9868f400a18d00910, amount=49596.65217865, currency=mxn),
 Funding(fid=3799c39ea8f1ccf6e6bbcaea1a0cbed1, amount=8.12500000, currency=btc)]
>>> fundings[0].status
u'complete'
>>> fundings[0].amount
Decimal('49596.65217865')
```




### User Trades ###

```python
## Your trades
## Parameters
## [book = all]- Specifies which book to use
##                 - string
## [marker]    - Returns objects that are older or newer (depending on 'sort’) than the object with this ID
##                 - string
## [limit = 25]   - Limit result to that many transactions
##                 - int
## [sort = 'desc'] - Sorting by datetime
##                 - string - 'asc' or
##                 - 'desc'
>>> utx = api.user_trades()
>>> utx
[UserTrade(tid=1610, book=btc_mxn, price=3160.00, major=-0.00797922, minor=25.21433520),
 UserTrade(tid=1609, book=btc_mxn, price=3160.00, major=-0.01000000, minor=31.60000000),
 UserTrade(tid=1608, book=btc_mxn, price=8000.00, major=0.00312500, minor=-25.00000000),
 UserTrade(tid=1607, book=btc_mxn, price=8000.00, major=0.01008572, minor=-80.68576000),
 ...,
 ]

>>> utx[0].type
'trade'
>>> utx[0].btc
Decimal('0.00981097')
>>> txs[0].btc_mxn
Decimal('7780.00')
>>> txs[0].rate
Decimal('7780.00')


```

### Open Orders ###

```python
## Returns a list of the user’s open orders
## Parameters
## [book] - Specifies which book to use
##                    - str
## [marker]    - Returns objects that are older or newer (depending on 'sort’) than the object with this ID
##                 - string
## [limit = 25]   - Limit result to that many transactions
##                 - int
## [sort = 'desc'] - Sorting by datetime
##                 - string - 'asc' or
##                 - 'desc'

>>> oo = api.open_orders('btc_mxn')
>>> oo
[Order(oid=s5ntlud6oupippk8iigw5dazjdxwq5vibjcwdp32ksk9i4h0nyxsc8svlpscuov5, side=buy, price=7000.00, original_amount=0.01000000, created_datetime=2016-04-22 14:31:10)]
>>> oo[0].price
Decimal('7000.00')
>>> oo[0].oid
s5ntlud6oupippk8iigw5dazjdxwq5vibjcwdp32ksl9i4h0nyxsc8svlpscuov5

```

### Lookup Order ###

```python
## Returns a list of details for 1 or more orders
## Parameters
## order_ids -  A list of Bitso Order IDs.
##          - string
>>> orders = api.lookup_order([ORDER_ID1, ORDER_ID2])
>>> orders
[Order(oid=s0ntlud6oupippk8iigw5dazjdxwq5vibjcwdp12ksk9i4h0nyxsc8svlpscuov5, side=buy, price=7000.00, original_amount=0.01000000, created_datetime=2016-04-22 14:31:10),
 Order(oid=whtyptv0f348fajdydoswcf6cj20d0kahd77657l7ctnnd1lrpdn2suebwfpxz0f, side=buy, price=7200.00, original_amount=0.01200000, created_datetime=2016-04-22 14:32:10)]
```

### Cancel Order ###

```python
## Cancels an open order
## Parameters
## order_id -  A Bitso Order ID.
##          - string
>>> api.cancel_order(ORDER_ID)
u'true' #on success
```

### Place Order ###

```python
## Places a buy limit order.
## [book] - Specifies which book to use (btc_mxn, eth_mxn)
##                    - str
## [side] - the order side (buy, sell) 
##                    - str
## [order_type] - the order type (limit, market) 
##                    - str
## amount - Amount of major currency to buy.
##        - string
## major  - The amount of major currency for this order. An order must be specified in terms of major or minor, never both.
##        - string. Major denotes the cryptocurrency, in our case Bitcoin (BTC) or Ether (ETH).
## minor  - The amount of minor currency for this order. Minor denotes fiat currencies, in our case Mexican Peso (MXN)
##        - string
## price  - Price per unit of major. For use only with limit orders
##        - string

>>> order = api.place_order(book='btc_mxn', side='buy', order_type='limit', major='.01', price='7000.00')
>>> order
{"oid":"jli47Q3gQqXflk1n"}
```


### Funding Destination Address ###

```python
## Gets a Funding destination address to fund your account
## fund_currency  - Specifies the currency you want to fund your account with (btc, eth, mxn)
##                            - str
>>> fd = api.funding_destination('btc')
>>> fd
FundingDestination(account_identifier_name=Bitcoin address)
## Returns a FundingDestination object
>>> fd.account_identifier
u'3CEWgs1goBbafUoThjWff4oX4wQKfxqpeV'
## account_identifier attribute is the address you can use to fund your account
```


### Bitcoin Withdrawal ###

```python
## Triggers a bitcoin withdrawal from your account
## amount  - The amount of BTC to withdraw from your account
##         - string
## address - The Bitcoin address to send the amount to
##         - string
>>> api.btc_withdrawal('0.000000001', '1TVXn5ajmMQEbkiYNobgHVutVtMWcNZGV')
ok   # Returns 'ok' on success
```

### Ether Withdrawal ###

```python
## Triggers an ether withdrawal from your account
## amount  - The amount of ETH to withdraw from your account
##         - string
## address - The Ethereum address to send the amount to
##         - string
>>> api.eth_withdrawal('0.000000001', '0x55f03a62acc946dedcf8a0c47f16ec3892b29e6d')
ok   # Returns 'ok' on success
```



### Ripple Withdrawal ###

```python
## Triggers a ripple withdrawal from your account
## currency  - The currency to withdraw
##         - string
## amount  - The amount of currency to withdraw from your account
##         - string
## address - The ripple address to send the amount to
##         - string
>>> api.ripple_withdrawal('xrp', '1.10', 'rG1QQv2nh2gr7RCZ1P8YYcBUKCCN633jCn')
ok   # Returns 'ok' on success
```



### Bank Withdrawal (SPEI) ###

```python
## Triggers a SPEI withdrawal from your account. These withdrawals are
##   immediate during banking hours (M-F 9:00AM - 5:00PM Mexico City Time).
##
## amount  - The amount of MXN to withdraw from your account
##         - string
## recipient_given_names - The recipient’s first and middle name(s)
##         - string
## recipient_family_names - The recipient’s last name)
##         - string
## clabe - The CLABE number where the funds will be sent to
##         - string
## notes_ref - The alpha-numeric reference number for this SPEI
##         - string
## numeric_ref - The numeric reference for this SPEI
##         - string


>>> api.spei_withdrawal(amount='3500.0', first_names='Satoshi', last_names='Nakamoto', clabe=CLABE, notes_ref=NOTES_REF, numeric_ref=NUMERIC_REF)
ok   # Returns 'ok' on success
```



# Transfer API #

**Access to this API is available on request, and not enabled by default. Users won’t be able to use this API unless Bitso has enabled it on their account. [API Docs](https://bitso.com/api_info/?shell#transfer-api5)**

Bitso’s powerful Transfer API allows for simple integration for routing Bitcoin payments directly through to a choice of Mexican Peso end-points.

The workflow is as follows:

```python
## Request quote
>>> quote = api.transfer_quote(amount='25.0', currency='MXN')
## Create transfer using quote
>>> transfer = api.transfer_create(amount='25.0', currency='MXN', rate=quote.rate, payment_outlet='vo', email_address='mario@ret.io', recipient_given_name='mario romero')
## Send bitcoins to address given
>>> print(transfer.wallet_address)
## Check Transfer status, after 1 confirmation, pesos are delivered
>>> print(api.transfer_status(transfer.id).status)
u'confirming'
```

### Get Transfer Quote ###

```python
## Get a quote for a transfer for various Bitso Outlets.
##
## btc_amount  - Mutually exclusive with amount. Either this, or amount should
##               be present in the request. The total amount in Bitcoins, as
##               provided by the user. NOTE: The amount is in BTC format
##               (900mbtc = .9 BTC).
##         - string
## amount  - Mutually exclusive with btc_amount. Either this, or btc_amount
##           should be present in the request. The total amount in Fiat currency.
##           Use this if you prefer specifying amounts in fiat instead of BTC.
##         - string
## currency - An ISO 4217 fiat currency symbol (ie, "MXN"). If btc_amount is
##            provided instead of amount, this is the currency to which the BTC
##            price will be converted into. Otherwise, if amount is specified
##            instead of btc_amount, this is the currency of the specified amount.
##         - string

>>> quote = api.transfer_quote(amount='25.0', currency='MXN')
>>> print(quote)
TransactionQuote(btc_amount=0.00328834, currency=MXN, rate=7602.60, created_at=2016-05-03 00:33:06, expires_at=2016-05-03 00:34:06, gross=25.00)
>>> quote.btc_amount
Decimal('0.00328834')
>>> quote.outlets.keys()
[u'sp', u'rp', u'vo', u'bw', u'pm']
>>> quote.outlets['vo']
{u'available': True,
 u'daily_limit': Decimal('0.00'),
 u'fee': Decimal('0.00'),
 u'id': u'vo',
 u'maximum_transaction': Decimal('9999.00'),
 u'minimum_transaction': Decimal('25.00'),
 u'name': u'Voucher',
 u'net': Decimal('25.00'),
 u'optional_fields': [],
 u'required_fields': {u'email_address': {u'id': u'email_address',
   u'name': u'Email Address'},
  u'recipient_given_name': {u'id': u'recipient_given_name', u'name': u''}},
 u'verification_level_requirement': u'0'}

```

### Create Transfer ###

```python
## Get a quote for a transfer for various Bitso Outlets.
##
## btc_amount  - Mutually exclusive with amount. Either this, or amount should
##               be present in the request. The total amount in Bitcoins, as
##               provided by the user. NOTE: The amount is in BTC format
##               (900mbtc = .9 BTC).
##         - string
## amount  - Mutually exclusive with btc_amount. Either this, or btc_amount
##           should be present in the request. The total amount in Fiat currency.
##           Use this if you prefer specifying amounts in fiat instead of BTC.
##         - string
## currency - An ISO 4217 fiat currency symbol (ie, "MXN"). If btc_amount is
##            provided instead of amount, this is the currency to which the BTC
##            price will be converted into. Otherwise, if amount is specified
##            instead of btc_amount, this is the currency of the specified amount.
##         - string
## rate - This is the rate (e.g. BTC/MXN), as acquired from the
##        transfer_quote method. You must request a quote in this way before
##        creating a transfer.
##      - string
## payment_outlet - The outlet_id as provided by quote method.
##      - string
## required fields parameters - Each of the other 'required_fields', 
##                              as stipulated in the TransferQuote for the chosen payment_outlet.
##      - string

>>> transfer = api.transfer_create(amount='25.0', currency='MXN', rate=quote.rate, payment_outlet='vo', email_address='satoshin@gmx.com', recipient_given_name='satoshi nakamoto')
>>> print(transfer)
TransactionQuote(btc_amount=0.00328834, currency=MXN, rate=7602.60, created_at=2016-05-03 00:33:06, expires_at=2016-05-03 00:34:06, gross=25.00)
>>> transfer.btc_amount
Decimal('0.00328834')
>>> quote.wallet_address
u'3LiLpKyfXJmeDcD5ABGtmHGjkxnZTHnBxv'}

```


### Get Transfer Status ###

```python
## Request status for a transfer order 
##
## transfer_id  - Bitso Transfer Order ID (As returned by transfer_create
##                method.
##         - string

>>> print(api.transfer_status(transfer.id).status)
u'confirming'

```
# Websocket API #

WebSocket is a protocol providing full-duplex communication channels over a single TCP connection. [Bitso's Websocket API](https://bitso.com/api_info/?shell#websocket-api) allows a continuous connection that will receive updates according to the client's subscribed channels.

#### Available Channels: ####
+ **'trades':** will send updates on each new registered trade.
+ **'diff-orders':** will send across any modifications to the order book. Specifically, any state changes in existing orders (including orders not in the top 20), and any new orders.
+ **'orders':** maintains an up-to-date list of the top 20 asks and the top 20 bids, new updates are sent across the channel whenever there is a change in either top 20.

#### Basic Example ####
Prints every trade.
```python
from bitso import websocket


class BasicBitsoListener(websocket.Listener):
    def on_connect(self):
        print("Connected")
        
    def on_update(self, data):
        for obj in data.updates:
            print(obj)
        
if __name__ == '__main__':
    listener = BasicBitsoListener()
    client = websocket.Client(listener)
    channels = ['trades']
    book = 'btc_mxn'
    client.connect(channels, book)

```

```shell
> python examples/ws_trades.py
Connected
TradeUpdate(tid=96093, amount=0.00296048, rate=8444.56,value=25)
TradeUpdate(tid=96094, amount=0.0568058, rate=8444.56,value=479.7)
TradeUpdate(tid=96095, amount=0.45721742, rate=8444.56,value=3861)
TradeUpdate(tid=96096, amount=1.25176796, rate=8335.88,value=10434.58)
TradeUpdate(tid=96097, amount=0.75948406, rate=8335.83,value=6330.93)
TradeUpdate(tid=96098, amount=0.38027314, rate=8334.31,value=3169.31)
TradeUpdate(tid=96099, amount=0.54340182, rate=8329.95,value=4526.5)
TradeUpdate(tid=96100, amount=0.44632784, rate=8323.59,value=3715.04)
TradeUpdate(tid=96101, amount=0.03216174, rate=8322.31,value=267.65)
TradeUpdate(tid=96102, amount=2.92387591, rate=8318.13,value=24321.17)
TradeUpdate(tid=96103, amount=0.27482146, rate=8313.96,value=2284.85)
TradeUpdate(tid=96104, amount=1.33065393, rate=8312,value=11060.39)
TradeUpdate(tid=96105, amount=0.70166614, rate=8310.66,value=5831.3)
TradeUpdate(tid=96106, amount=0.11416146, rate=8434.37,value=962.88)
```

#### Advanced Example ####
Gets a copy of the order book via the rest API once, and keeps it up to date using the **'diff-orders'** channel. Logs every order, spread update, or trade.

See [examples/livebookexample.py](https://github.com/bitsoex/bitso-py/blob/master/examples/livebookexample.py)

```shell
> python examples/livebookexample.py
2016-05-09 20:17:32,232 - INFO - Starting new HTTPS connection (1): bitso.com
2016-05-09 20:17:33,118 - INFO - Order Book Fetched. Best ask: 8434.3700, Best bid: 8351.3000, Spread: 83.0700
2016-05-09 20:17:33,589 - INFO - Websocket Connection Established
2016-05-09 20:17:33,711 - INFO - Best ask: 8434.3700, Best bid: 8351.3000, Spread: 83.0700
2016-05-09 20:22:30,301 - INFO - New Order. ask: 0.0000 @ 8434.3700 = 0.0000
2016-05-09 20:22:30,306 - INFO - Removed price level at: 8434.3700
2016-05-09 20:22:30,306 - INFO - Best ask: 8440.0000, Best bid: 8351.3000, Spread: 88.7000
2016-05-09 20:22:31,021 - INFO - New Order. ask: 0.1000 @ 8492.9700 = 849.2900
2016-05-09 20:22:31,022 - INFO - Best ask: 8440.0000, Best bid: 8351.3000, Spread: 88.7000
```


# Models #

The wrapper uses models to represent data structures returned by the Bitso API. 

### bitso.Book
Atribute | Type | Description | Units
------------ | ------------- | ------------- | -------------
symbol | String | Order book symbol | Major_Minor
minimum_amount | Decimal | Minimum amount of major when placing orders | Major
maximum_amount | Decimal | Maximum amount of major when placing orders | Major
minimum_price | Decimal | Minimum price when placing orders	 | Minor
maximum_price | Decimal | Maximum price when placing orders	 | Minor
minimum_value | Decimal | Minimum value amount (amount*price) when placing orders		 | Minor
maximum_value | Decimal | Maximum value amount (amount*price) when placing orders	 | Minor


### bitso.AvailableBooks
Atribute | Type | Description | Units
------------ | ------------- | ------------- | -------------
books | list | symbols for each book available | -
btc_mxn | bitso.Book | btc_mxn bitso.Book Object| -
eth_mxn | bitso.Book | eth_mxn bitso.Book Object| -


### bitso.AccountRequiredField
Atribute | Type | Description | Units
------------ | ------------- | ------------- | -------------
name | String | Field name that will be user for “account_creation” endpoint | 
description | String | Describes each field | 


### bitso.Ticker
Atribute | Type | Description | Units
------------ | ------------- | ------------- | -------------
book | String | Order book symbol | Major_Minor
ask | Decimal | Lowest sell order | Minor/Major
bid | Decimal | Highest buy order | Minor/Major
last | Decimal | Last traded price | Minor/Major
high | Decimal | Last 24 hours price high | Minor/Major
low | Decimal | Last 24 hours price low | Minor/Major
vwap | Decimal | Last 24 hours price high | Minor/Major
volume | Decimal | Last 24 hours volume | Major
created_at | Datetime | Ticker current datetime | 

### bitso.PublicOrder

Atribute | Type | Description | Units
------------ | ------------- | ------------- | -------------
book | String | Order book symbol | Major_Minor
price | Decimal | Price per unit of major | Minor
amount | Decimal | Major amount in order | Major
created_at | Datetime | The datetime at which the order was created |
updated_at | Datetime | The datetime at which the order was updated (Can be None) |


### bitso.OrderBook
Atribute | Type | Description | Units
------------ | ------------- | ------------- | -------------
asks | List | List of open asks | Minor/Major
bids | List | List of open bids | Minor/Major
created_at | Datetime | OrderBook current datetime | 


### bitso.Balance
Atribute | Type | Description | Units
------------ | ------------- | ------------- | -------------
name | String | 	Currency name | 
total | Decimal | Total balance for currency | Currency
locked | Decimal | Currency balance locked in open orders | Currency
available | Decimal | Currency balance available for use | Currency

### bitso.Balances
Atribute | Type | Description | Units
------------ | ------------- | ------------- | -------------
currencies | list | name for each currency | -
mxn | bitso.Balance | mxn bitso.Balance Object | -
btc | bitso.Balance | btc bitso.Balance Object | -
eth | bitso.Balance | eth bitso.Balance Object | -


### bitso.Fee
Atribute | Type | Description | Units
------------ | ------------- | ------------- | -------------
book | String | Order book symbol | Major_Minor
fee_decimal | Decimal | Customer trading fee as a decimal |
fee_percent | Decimal | Customer trading fee as a percentage |

### bitso.Fees
Atribute | Type | Description | Units
------------ | ------------- | ------------- | -------------
books | list | name for each book | -
btc_mxn | bitso.Fee | btc_mxn bitso.Fee Object | -
eth_mxn | bitso.Fee | eth_mxn bitso.Fee Object | -



### bitso.Trade
Atribute | Type | Description | Units
------------ | ------------- | ------------- | -------------
tid | Long | Trade ID | 
book | String | Order book symbol | Major_Minor
amount | Decimal | Major amount transacted | Major
price | Decimal | Price per unit of major | Minor
side | String | Indicates the maker order side (maker order is the order that was open on the order book) | 
created_at | Datetime | Datetime at which the trade was executed |


### bitso.Withdrawal
Atribute | Type | Description | Units
------------ | ------------- | ------------- | -------------
wid | String | Withdrawal ID | 
currency | String | Currency withdrawn symbol | 
method | String | Method for this withdrawal (MXN, BTC, ETH) | 
amount | Decimal | The withdrawn amount | currency
status | String | 	The status for this withdrawal (pending, complete, cancelled) | 
created_at | Datetime | Datetime at which the withdrawal as created |
details | Dict | 	Specific withdrawal details) | 



### bitso.Funding
Atribute | Type | Description | Units
------------ | ------------- | ------------- | -------------
fid | String | Funding ID | 
currency | String | Currency funding symbol | 
method | String | Method for this funding (MXN, BTC, ETH) | 
amount | Decimal | The funding amount | currency
status | String | 	The status for this funding (pending, complete, cancelled) | 
created_at | Datetime | Datetime at which the funding as recieved |
details | Dict | 	Specific funding details | 


### bitso.UserTrade
Atribute | Type | Description | Units
------------ | ------------- | ------------- | -------------
tid | Long | Trade ID | 
oid | String | Users’ Order ID | 
book | String | Order book symbol | Major_Minor
side | String | Indicates the user’s side for this trade (buy, sell) | 
created_at | Datetime | Datetime at which the trade was executed | 
major | Decimal | Major amount traded | Major
minor | Decimal | Minor amount traded | Minor
price | Decimal | Price per unit of major | Minor
fees_currency | String | 	Indicates the currency in which the trade fee was charged | 
fees_amount | Decimal | Indicates the amount charged as trade fee | Major

### bitso.LedgerEntry
Atribute | Type | Description | Units
------------ | ------------- | ------------- | -------------
eid | String | Entry ID	| 
operation | String | Indicates type of operation (funding, withdrawal, trade, fee) | 
created_at | Datetime | Timestamp at which the operation was recorded | 
balance_updates | List | Updates to user balances for this operation | 
details | Dict | Specific operation details | 

### bitso.BalanceUpdate
Atribute | Type | Description | Units
------------ | ------------- | ------------- | -------------
currency | String | Currency for this balance update | 
balance | Decimal | Amount added or subtracted to user balance | Currency

### bitso.Order

Atribute | Type | Description | Units
------------ | ------------- | ------------- | -------------
oid | String | The Order ID | 
book | String | Order book symbol | Major_Minor
type | String | The order type (market, limit) | 
side | String | The order side (buy, sell) | 
status | String | The order’s status (open, partial-fill, closed)) | 
created_at | Datetime | The date the order was created | 
updated_at | Datetime | Timestamp at which the order was updated (can be None) | 
price | Decimal | The order’s price | Minor
amount | Decimal | The order’s major currency amount | Major

### bitso.FundingDestination
Atribute | Type | Description | Units
------------ | ------------- | ------------- | -------------
account_identifier_name | String | Account identifier name to fund with the specified currency. | 
account_identifier | String | Identifier to where the funds can be sent to | 

### bitso.TransactionQuote

Atribute | Type | Description | Units
------------ | ------------- | ------------- | -------------
btc_amount | Decimal | The total amount in Bitcoins | Major
currency | String | An ISO 4217 fiat currency symbol (ie, “MXN”). | 
gross | Decimal |  | 
rate | Decimal | This major/manor rate (e.g. BTC/MXN) | 
outlets | Dictionary | Dictionary of Bitso Outlet options | 
created_at | Datetime | The date the quote was created | 
expires_at | Datetime | The date the quote will expire | 



### bitso.TransactionOrder

Atribute | Type | Description | Units
------------ | ------------- | ------------- | -------------
btc_amount | Decimal | The total amount in BTC | BTC
btc_pending | Decimal | Unconfirmed BTC, seen by Bitso servers  | BTC
btc_received | Decimal | Confirmed BTC seen by Bitso servers | BTC
confirmation_code | String | | 
currency | String | An ISO 4217 fiat currency symbol (ie, “MXN”). | 
currency_amount | Decimal | | 
currency_settled | Decimal | | 
currency_fees | Decimal | | 
fields | Dictionary | Required fields for Pyament Outlet | 
created_at | Datetime | The date the transfer was created | 
expires_at | Datetime | The date the transfer order will expire | 
id | String | Transfer Order ID | 
payment_outlet_id | String | Payment Outlet ID | 
qr_img_uri | String | Bitcoin payment QR Code URI | 
user_uri | String | Transfer Order URI | 
wallet_address | String | Bitcoin address you will send BTC to



### bitso.models.OrderUpdate

Atribute | Type | Description | Units
------------ | ------------- | ------------- | -------------
datetime | Datetime | Order Date/Time | 
side | String | 'bid','ask' | Market side 
rate | Decimal | Order price | Minor
amount | Decimal | Major currency amount | Major
value | Decimal | Total Order Value (amount*rate) | Minor 

### bitso.models.TradeUpdate

Atribute | Type | Description | Units
------------ | ------------- | ------------- | -------------
tid | Int | Trade ID | 
rate | Decimal | Order price | Minor
amount | Decimal | Major currency amount | Major
value | Decimal | Total Order Value (amount*rate) | Minor 

### bitso.models.StreamUpdate

Atribute | Type | Description | Units
------------ | ------------- | ------------- | -------------
channel | String | ('diff-orders', 'trades', 'orders') | 
updates | List | List of (TradeUpdate or OrderUpdate) objects | 


# Notations #

**Major** denotes the cryptocurrency, in our case Bitcoin (BTC).

**Minor** denotes fiat currencies such as Mexican Peso (MXN), etc

An order book is always referred to in the API as "Major_Minor". For example: "**btc_mxn**"


# Licence #

The MIT License (MIT)

