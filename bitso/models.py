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

try:
  basestring
except NameError:
  basestring = str

from datetime import datetime
from decimal import Decimal

import dateutil.parser
from six import string_types


class BaseModel(object):

    """ Base class for other models. """
    
    def __init__(self, **kwargs):
        self._default_params = {}

    @classmethod
    def _NewFromJsonDict(cls, data, **kwargs):
        if kwargs:
            for key, val in kwargs.items():
                data[key] = val
        return cls(**data)


class Book(BaseModel):
    """A class that represents the Bitso orderbook and it's limits"""

    def __init__(self, **kwargs):
        self._default_params = {
            'symbol': kwargs.get('book'),
            'minimum_amount': Decimal(kwargs.get('minimum_amount')),
            'maximum_amount': Decimal(kwargs.get('maximum_amount')),
            'minimum_price': Decimal(kwargs.get('minimum_price')),
            'maximum_price': Decimal(kwargs.get('maximum_price')),
            'minimum_value': Decimal(kwargs.get('minimum_value')),
            'maximum_value': Decimal(kwargs.get('maximum_value'))
        }
        
        for (param, val) in self._default_params.items():
            setattr(self, param, val)

    def __repr__(self):
        return "Book(symbol={symbol})".format(symbol=self.symbol)
            

class AvailableBooks(BaseModel):
    """A class that represents Bitso's orderbooks"""
    def __init__(self, **kwargs):
        self.books = []
        for ob in kwargs.get('payload'):
            self.books.append(ob['book'])
            setattr(self, ob['book'], Book._NewFromJsonDict(ob))

    def __repr__(self):
        return "AvilableBooks(books={books})".format(books=','.join(self.books))


class AccountStatus(BaseModel):
    def __init__(self, **kwargs):
        self._default_params = {
            'client_id': kwargs.get('client_id'),
            'status': kwargs.get('status'),
            'cellphone_number': kwargs.get('cellphone_number'),
            'cellphone_number_stored': kwargs.get('cellphone_number_stored'),
            'email_stored': kwargs.get('email_stored'),
            'official_id': kwargs.get('official_id'),
            'proof_of_residency': kwargs.get('proof_of_residency'),
            'signed_contract': kwargs.get('signed_contract'),
            'origin_of_funds': kwargs.get('origin_of_funds'),
            'daily_limit': Decimal(kwargs.get('daily_limit')),
            'monthly_limit': Decimal(kwargs.get('monthly_limit')),
            'daily_remaining': Decimal(kwargs.get('daily_remaining')),
            'monthly_remaining': Decimal(kwargs.get('monthly_remaining'))
        }
        
        for (param, val) in self._default_params.items():
            setattr(self, param, val)

    def __repr__(self):
        return "AccountStatus(client_id={client_id})".format(client_id=self.client_id)
            
    

class AccountRequiredField(BaseModel):
    def __init__(self, **kwargs):
        self._default_params = {
            'name': kwargs.get('field_name'),
            'description': kwargs.get('field_description'),
        }
        
        for (param, val) in self._default_params.items():
            setattr(self, param, val)

    def __repr__(self):
        return "AccountRequiredField(name={name})".format(name=self.name)



class Ticker(BaseModel):

    """ A class that represents a Bitso ticker. """
    
    def __init__(self, **kwargs):
        self._default_params = {
            'book': kwargs.get('book'),
            'ask': Decimal(kwargs.get('ask')),
            'bid': Decimal(kwargs.get('bid')),
            'high': Decimal(kwargs.get('high')),
            'last': Decimal(kwargs.get('last')),
            'low': Decimal(kwargs.get('low')),
            'vwap': Decimal(kwargs.get('vwap')),
            'volume': Decimal(kwargs.get('volume')),
            'created_at': dateutil.parser.parse(kwargs.get('created_at'))
        }
        
        for (param, val) in self._default_params.items():
            setattr(self, param, val)

    def __repr__(self):
        return "Ticker(book={book},ask={ask},bid={bid}, high={high}, last={last}, low={low}, volume={volume}, created_at={created_at}, vwap={vwap})".format(
            book=self.book,
            ask=self.ask,
            bid=self.bid,
            high=self.high,
            low=self.low,
            last=self.last,
            vwap=self.vwap,
            volume=self.volume,
            created_at=self.created_at)

class PublicOrder(BaseModel):
    def __init__(self, **kwargs):
        self._default_params = {
            'book': kwargs.get('book'),
            'price': Decimal(kwargs.get('price')),
            'amount': Decimal(kwargs.get('amount'))
        }

            
        for (param, val) in self._default_params.items():
            setattr(self, param, val)

        if kwargs.get('oid'):
            setattr(self, 'oid',  kwargs.get('oid'))
        else:
            setattr(self, 'oid',  None)


    def __repr__(self):
        return "PublicOrder(book={book},price={price}, amount={amount})".format(
            book=self.book,
            price=self.price,
            amount=self.amount)


            
class OrderBook(BaseModel):

    """ A class that represents a Bitso order book. """
    
    def __init__(self, **kwargs):
        self._default_params = {
            'asks': kwargs.get('asks'),
            'bids': kwargs.get('bids'),
            'updated_at': dateutil.parser.parse(kwargs.get('updated_at')),
            'sequence': int(kwargs.get('sequence'))
        }

        for (param, val) in self._default_params.items():
            if param in ['asks', 'bids']:
                public_orders = []
                for order in val:
                    public_orders.append(PublicOrder._NewFromJsonDict(order))
                setattr(self, param, public_orders)
                continue
            setattr(self, param, val)


    def __repr__(self):
        return "OrderBook({num_asks} asks, {num_bids} bids, updated_at={updated_at})".format(
            num_asks=len(self.asks),
            num_bids=len(self.bids),
            updated_at=self.updated_at)


class Balance(BaseModel):
        
    """ A class that represents a Bitso user's balance for a specifc currency. """

    
    def __init__(self, **kwargs):
        
        self._default_params = {
            'name': kwargs.get('currency'),
            'total': Decimal(kwargs.get('total')),
            'locked': Decimal(kwargs.get('locked')),
            'available': Decimal(kwargs.get('available'))
        }

        for (param, val) in self._default_params.items():
            setattr(self, param, val)

    def __repr__(self):
        return "Balance(name={name}, total={total})".format(
            name=self.name,
            total=self.total)

class Balances(BaseModel):
    """ A class that represents a Bitso user's balances """

    def __init__(self, **kwargs):
        self.currencies = []
        for balance in kwargs.get('balances'):
            self.currencies.append(balance['currency'])
            setattr(self, balance['currency'],  Balance._NewFromJsonDict(balance))


    def __repr__(self):
        return "Balances(currencies={currencies})".format(
            currencies=','.join(self.currencies))



class Fee(BaseModel):
        
    """ A class that represents a Bitso user's fees for a specifc order book. """

    
    def __init__(self, **kwargs):
        
        self._default_params = {
            'book': kwargs.get('book'),            
            'fee_decimal': Decimal(kwargs.get('fee_decimal')),
            'fee_percent': Decimal(kwargs.get('fee_percent'))
        }

        for (param, val) in self._default_params.items():
            setattr(self, param, val)
            
    def __repr__(self):
        return "Fee(book={book}, fee_percent={fee_percent})".format(
            book=self.book,
            fee_percent=self.fee_percent)

    
class WithdrawalFees(BaseModel):
    """ A class that represents a Bitso user's withdrawal fees """

    def __init__(self, **kwargs):
        self.currencies = []
        for currency,fee in kwargs.items():
            self.currencies.append(currency)
            setattr(self, currency, Decimal(fee))

    def __repr__(self):
        return "WithdawalFees(curencies={currencies})".format(
            currencies=','.join(self.currencies))



class Fees(BaseModel):
    """ A class that represents a Bitso user's fees """

    def __init__(self, **kwargs):
        self.books = []
        for fee in kwargs.get('fees'):
            self.books.append(fee['book'])
            setattr(self, fee['book'], Fee._NewFromJsonDict(fee))
        setattr(self, 'withdrawal_fees', WithdrawalFees._NewFromJsonDict(kwargs.get('withdrawal_fees')))

    def __repr__(self):
        return "Fees(books={books},withdrawal_fees={currencies})".format(
            books=','.join(self.books),currencies=','.join(self.withdrawal_fees.currencies))




class Trade(BaseModel):

    """ A class that represents a Bitso public trade. """

    
    def __init__(self, **kwargs):
        self._default_params = {
            'book': kwargs.get('book'),
            'tid': kwargs.get('tid'),
            'amount': Decimal(kwargs.get('amount')),
            'price': Decimal(kwargs.get('price')),
            'maker_side': kwargs.get('maker_side'),
            'created_at': dateutil.parser.parse(kwargs.get('created_at'))
        }

        for (param, val) in self._default_params.items():
            setattr(self, param, val)

    def __repr__(self):
        return "Trade(tid={tid}, price={price}, amount={amount}, maker_side={maker_side}, created_at={created_at})".format(
            tid=self.tid,
            price=self.price,
            amount=self.amount,
            maker_side=self.maker_side,
            created_at=self.created_at)

class Withdrawal(BaseModel):

    """ A class that represents a User Withdrawal """
    
    def __init__(self, **kwargs):
        self._default_params = {
            'wid': kwargs.get('wid'),
            'status': kwargs.get('status'),
            'created_at': dateutil.parser.parse(kwargs.get('created_at')),
            'currency': kwargs.get('currency'),
            'method': kwargs.get('method'),
            'amount': Decimal(kwargs.get('amount')),
            'details': kwargs.get('details')
        }

        for (param, val) in self._default_params.items():
            setattr(self, param, val)

    def __repr__(self):
        return "Withdrawal(wid={wid}, amount={amount}, currency={currency})".format(
            wid=self.wid,
            amount=self.amount,
            currency=self.currency)

class Funding(BaseModel):

    """ A class that represents a User Funding """
    
    def __init__(self, **kwargs):
        self._default_params = {
            'fid': kwargs.get('fid'),
            'status': kwargs.get('status'),
            'created_at': dateutil.parser.parse(kwargs.get('created_at')),
            'currency': kwargs.get('currency'),
            'method': kwargs.get('method'),
            'amount': Decimal(kwargs.get('amount')),
            'details': kwargs.get('details')
        }

        for (param, val) in self._default_params.items():
            setattr(self, param, val)

    def __repr__(self):
        return "Funding(fid={fid}, amount={amount}, currency={currency})".format(
            fid=self.fid,
            amount=self.amount,
            currency=self.currency)
       
           
            
class UserTrade(BaseModel):

    """ A class that represents a trade for a Bitso user. """

    def __init__(self, **kwargs):
        self._default_params = {
            'book': kwargs.get('book'),
            'tid': kwargs.get('tid'),
            'oid': kwargs.get('oid'),
            'created_at': dateutil.parser.parse(kwargs.get('created_at')),
            'major': Decimal(kwargs.get('major')),
            'minor': Decimal(kwargs.get('minor')),
            'price': Decimal(kwargs.get('price')),
            'fees_amount': Decimal(kwargs.get('fees_amount')),
            'fees_currency': kwargs.get('fees_currency'),
            'side': kwargs.get('side')
        }

        for (param, val) in self._default_params.items():
            setattr(self, param, val)

    def __repr__(self):
        return "UserTrade(tid={tid}, book={book}, price={price}, major={major}, minor={minor})".format(
            tid=self.tid,
            book=self.book,
            price=self.price,
            major=self.major,
            minor=self.minor)
       



class LedgerEntry(BaseModel):
    """A class that represents a Bitso Ledger entry."""
    def __init__(self, **kwargs):
        for (param, value) in kwargs.items():
            if param == 'created_at':
                value = dateutil.parser.parse(value)
            if param == 'balance_updates':
                value = [BalanceUpdate._NewFromJsonDict(item) for item in value]
            setattr(self, param, value)
        


class BalanceUpdate(BaseModel):
    """A class that represents a Bitso Balance Update"""
    def __init__(self, **kwargs):
        for (param, value) in kwargs.items():
            if param == 'amount':
                value = Decimal(value)
            setattr(self, param, value)
    
    def __repr__(self):
        return "BalanceUpdate(currency={currency}, amount={amount}".format(
            currency=self.currency,
            amount=self.amount)

class Order(BaseModel):

    """ A class that represents a Bitso order. """
 
    def __init__(self, **kwargs):
        self._default_params = {
            'book': kwargs.get('book'),
            'oid': kwargs.get('oid'),
            'created_at': dateutil.parser.parse(kwargs.get('created_at')),
            'updated_at': kwargs.get('updated_at'),
            'original_amount': kwargs.get('original_amount'),
            'unfilled_amount': Decimal(kwargs.get('unfilled_amount')),
            'price': Decimal(kwargs.get('price')),
            'side': kwargs.get('side'),
            'status': kwargs.get('status'),
            'type': kwargs.get('type')
        }
        for (param, val) in self._default_params.items():
            setattr(self, param, val)
            setattr(self, 'updated_at',  dateutil.parser.parse(kwargs.get('updated_at')))

        if kwargs.get('original_amount') != None:
            setattr(self, 'original_amount',  Decimal(kwargs.get('original_amount')))
        if kwargs.get('original_value') != None:
            setattr(self, 'original_value',  Decimal(kwargs.get('original_value')))        
        if kwargs.get('updated_at') != None:
            setattr(self, 'updated_at',  dateutil.parser.parse(kwargs.get('updated_at')))



    def __repr__(self):
        return "Order(oid={oid}, side={side}, type={order_type}, price={price}, original_amount={original_amount})".format(
            oid=self.oid,
            side=self.side,
            order_type=self.type,
            price=self.price,
            original_amount=self.original_amount)



class FundingDestination(BaseModel):
    """A class that represents a Bitso Funding Destination"""
    def __init__(self, **kwargs):
        for (param, value) in kwargs.items():
            setattr(self, param, value)

    def __repr__(self):
        return "FundingDestination(account_identifier_name={account_identifier_name})".format(
            account_identifier_name=self.account_identifier_name)

    
class OutletDictionary(dict):
    
    """ A Dictionary subclass to represet Bitso Transfer Outlets with parsed decimals. """

    def __init__(self, data):
        _decimal_keys = ('minimum_transaction',
                          'maximum_transaction',
                          'daily_limit',
                          'fee',
                          'net')

        for k, v in data.items():
            if isinstance(v, dict):
                self[k] = OutletDictionary(v)
            else:
                if isinstance(v, string_types) and k in _decimal_keys:
                    v = Decimal(v)
                elif k == 'available':
                    if v=='1':
                        v = True
                    else:
                        v = False
                self[k] = v
                    
                
class TransactionQuote(BaseModel):

    """ A class that represents a Bitso Transaction Quote. """

        
    def __init__(self, **kwargs):

        for (param, value) in kwargs.items():
            if param=='outlets':
                setattr(self, param, OutletDictionary(value))
            else:
                setattr(self, param, value)

        setattr(self, 'created_at', dateutil.parser.parse(kwargs.get('created_at')))
        setattr(self, 'expires_at', dateutil.parser.parse(kwargs.get('expires_at')))

        
        setattr(self, 'btc_amount', Decimal(self.btc_amount))
        setattr(self, 'gross', Decimal(self.gross))
        setattr(self, 'rate', Decimal(self.rate))
        
        
    def __repr__(self):
        return "TransactionQuote(btc_amount={btc_amount}, currency={currency}, rate={rate}, created_at={created_at}, expires_at={expires_at}, gross={gross})".format(
            btc_amount=self.btc_amount,
            currency=self.currency,
            rate=self.rate,
            gross= self.gross,
            created_at=self.created_at,
            expires_at=self.expires_at)



               
class TransactionOrder(BaseModel):

    """ A class that represents a Bitso Transaction Quote. """

        
    def __init__(self, **kwargs):
        setattr(self, 'btc_amount', None)


        for (param, value) in kwargs.items():
            setattr(self, param, value)
        #setattr(self, 'created_at', dateutil.parser.parse(kwargs.get('created_at')))
        setattr(self, 'expires_at', dateutil.parser.parse(self.expires_at))
        if self.btc_amount:
            setattr(self, 'btc_amount', Decimal(self.btc_amount))
        if self.btc_pending:
            setattr(self, 'btc_pending', Decimal(self.btc_pending))
        if self.btc_received:
            setattr(self, 'btc_received', Decimal(self.btc_received))
        if self.currency_amount:
            setattr(self, 'currency_amount', Decimal(self.currency_amount))
        if self.currency_fees:
            setattr(self, 'currency_fees', Decimal(self.currency_fees))
        if self.currency_settled:
            setattr(self, 'currency_settled', Decimal(self.currency_settled))



class OrderUpdate(BaseModel):
    def __init__(self, **kwargs):
        for (param, value) in kwargs.items():
            if param == 'd':
                setattr(self, 'timestamp', value)
                setattr(self, 'datetime', datetime.fromtimestamp(int(value)/1000))
            elif param == 'r':
                setattr(self, 'rate', Decimal(str(value)))
            elif param == 't':
                if value == 0:
                    setattr(self, 'side', 'bid')
                elif value == 1:
                    setattr(self, 'side', 'ask')
            elif param  == 'a':
                setattr(self, 'amount', Decimal(str(value)))
            elif param  == 'v':
                setattr(self, 'value', Decimal(str(value)))
            elif param == 'o':
                setattr(self, 'oid', str(value))
        if not hasattr(self, 'amount'):
            setattr(self, 'amount', Decimal('0.0'))
            setattr(self, 'value', Decimal('0.0'))
                
    def __repr__(self):
        return "OrderUpdate(side={side}, timestamp={timestamp}, rate={rate}, amount={amount}, value={value})".format(
            side=self.side,
            timestamp=self.timestamp,
            rate=self.rate,
            amount= self.amount,
            value=self.value,
            oid=self.oid)



class TradeUpdate(BaseModel):
    def __init__(self, **kwargs):
        for (param, value) in kwargs.items():
            if param == 'r':
                setattr(self, 'rate', Decimal(str(value)))
            elif param  == 'a':
                setattr(self, 'amount', Decimal(str(value)))
            elif param  == 'v':
                setattr(self, 'value', Decimal(str(value)))
            elif param  == 'i':
                setattr(self, 'tid', value)
            
                
    def __repr__(self):
        return "TradeUpdate(tid={tid}, amount={amount}, rate={rate},value={value})".format(
            tid=self.tid,
            rate=self.rate,
            amount= self.amount,
            value=self.value)


class StreamUpdate(object):
    def __init__(self, json_dict):
        self.channel = json_dict['type']
        self.sequence_number = None
        if 'sequence' in json_dict:
            self.sequence_number = int(json_dict['sequence'])
        self.updates = []
        if 'payload' in json_dict:
            if self.channel == 'diff-orders':
                self.updates = self._build_diff_order_updates(json_dict['payload'])
            elif self.channel == 'trades':
                self.updates = self._build_trade_updates(json_dict['payload'])
            elif self.channel == 'orders':
                self.updates = self._build_order_updates(json_dict['payload'])

    def _build_object_updates(self, payload, objcls):
        obj_list = []
        for elem in payload:
            elobj = objcls(**elem)
            obj_list.append(elobj)
        return obj_list

            
    def _build_trade_updates(self, payload):
        return self._build_object_updates(payload, TradeUpdate)
        
    def _build_diff_order_updates(self, payload):
        return self._build_object_updates(payload, OrderUpdate)

    def _build_order_updates(self, payload):
        asks = self._build_object_updates(payload['asks'], OrderUpdate)
        bids = self._build_object_updates(payload['bids'], OrderUpdate)
        return asks+bids
