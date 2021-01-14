#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

from __future__ import absolute_import

import hashlib
import hmac
import json
import time
import requests
from future.utils import iteritems

try:
    basestring
except NameError:
    from past.builtins import basestring

try:
    from urllib.parse import urlparse, urlencode
except ImportError:
    from urlparse import urlparse
    from urllib import urlencode


from bitso import (ApiError, ApiClientError, Ticker, OrderBook, Balances, Fees, Trade, UserTrade, Order, TransactionQuote, TransactionOrder, LedgerEntry, FundingDestination, Withdrawal, Funding, AvailableBooks, AccountStatus, AccountRequiredField)


def current_milli_time():
    nonce =  str(int(round(time.time() * 1000000)))
    return nonce
    

class Api(object):
    """A python interface for the Bitso API

    Example usage:
      To create an instance of the bitso.Api class, without authentication:
      
        >>> import bitso
        >>> api = bitso.Api()
      
      To get the Bitso price ticker:
      
        >>> ticker = api.ticker()
        >>> print ticker.ask
        >>> print ticker.bid

      To use the private endpoints, initiate bitso.Api with a client_id,
      api_key, and api_secret (see https://bitso.com/developers?shell#private-endpoints):
      
        >>> api = bitso.Api(API_KEY, API_SECRET)
        >>> balance = api.balance()
        >>> print balance.btc_available
        >>> print balance.mxn_available
    """
    
    def __init__(self, key=None, secret=None, timeout=0):
        """Instantiate a bitso.Api object.
        
        Args:
          key:
            Bitso API Key 
          secret:
            Bitso API Secret

  
        """
        self.base_url_v2 = "https://bitso.com/api/v2"
        self.base_url = "https://bitso.com/api/v3"
        self.key = key
        self._secret = secret
        self.timeout = timeout

    def available_books(self):
        """
        Returns:
          A list of bitso.AvilableBook instances
        """
        url = '%s/available_books/' % self.base_url
        resp = self._request_url(url, 'GET')
        return AvailableBooks._NewFromJsonDict(resp)

        
    def ticker(self, book=None):
        """Get a Bitso price ticker.

        Args:
          book (str, optional):
            Specifies which book to use. 
            
        Returns:
          A bitso.Ticker instance.
        
        """
        url = '%s/ticker/' % self.base_url
        parameters = {}
        if book is not None:
            parameters['book'] = book
        resp = self._request_url(url, 'GET', params=parameters)
        if book is None:
            return [Ticker._NewFromJsonDict(x) for x in resp['payload']]
        return Ticker._NewFromJsonDict(resp['payload'])
    



    def order_book(self, book, aggregate=True):
        """Get a public Bitso order book with a 
        list of all open orders in the specified book
        

        Args:
          book (str):
            Specifies which book to use. Default is btc_mxn
          aggregate (bool):
            Specifies if orders should be aggregated by price
            
        Returns:
          A bitso.OrderBook instance.
        
        """

        url = '%s/order_book/' % self.base_url
        parameters = {}
        parameters['book'] = book
        parameters['aggregate'] = aggregate
        resp = self._request_url(url, 'GET', params=parameters)
        return OrderBook._NewFromJsonDict(resp['payload'])

    def trades(self, book, **kwargs):
        """Get a list of recent trades from the specified book.

        Args:
          book (str):
            Specifies which book to use. Default is btc_mxn

          marker (str, optional):
            Returns objects that are older or newer (depending on 'sort') than the object which
            has the marker value as ID
          limit (int, optional):
            Limit the number of results to parameter value, max=100, default=25
          sort (str, optional):
            Sorting by datetime: 'asc', 'desc'
            Defuault is 'desc'

            
        Returns:
          A list of bitso.Trades instances.        
        """

        url = '%s/trades/' % self.base_url
        parameters = {}
        parameters['book'] = book        
        if 'marker' in kwargs:
            parameters['marker'] = kwargs['marker']
        if 'limit' in kwargs:
            parameters['limit'] = kwargs['limit']
        if 'sort' in kwargs:
            parameters['sort'] = kwargs['sort']
        resp = self._request_url(url, 'GET', params=parameters)
        return [Trade._NewFromJsonDict(x) for x in resp['payload']]


        
    def account_status(self):
        """
        Get a user's account status.

        Returns:
          A bitso.AccountStatus instance.        
        """
        url = '%s/account_status/' % self.base_url
        resp = self._request_url(url, 'GET', private=True)
        return AccountStatus._NewFromJsonDict(resp['payload'])

        
    def account_required_fields(self):
        """
        This endpoint returns a list of required fields and their 
        descriptions for use in the [Account Creation] endpoint.

        Returns:
          A Dictionary qith required fields and descriptions        
        """
        url = '%s/account_required_fields/' % self.base_url
        resp = self._request_url(url, 'GET')
        return [AccountRequiredField._NewFromJsonDict(x) for x in resp['payload']]


    def create_account(self, **kwargs):
        """This endpoint creates a new Bitso user account.
                
        Args:
          All parameters as returned by the [account_required_fields] endpoint
          are required

            
        Returns:
          A dictionary with client_id, and account_level
        """

        url = '%s/accounts/' % self.base_url
        resp = self._request_url(url, 'POST', params=kwargs)
        return resp['payload']

    
    def register_phone(self, phone_number):
        """This endpoint is used to register Mobile phone number for verification.

                
        Args:
          phone_number(str):
            Mobile phone number to register (10 digits)
            
        Returns:
          A Dictinoary object       
        """

        url = '%s/phone_number/' % self.base_url
        parameters = {'phone_number': phone_number}
        resp = self._request_url(url, 'POST', params=parameters, private=True)
        return resp['payload']


    def verify_phone(self, verification_code):
        """This endpoint is used to verify a registered mobile phone number

                
        Args:
          verification_code(str):
            Verification code sent by SMS when registering a phone
            with the [register_phone] endpoint
            
        Returns:
          A Dictinoary object       
        """

        url = '%s/phone_verification/' % self.base_url
        parameters = {'verification_code': verification_code}
        resp = self._request_url(url, 'POST', params=parameters, private=True)
        return resp['payload']

    
    def balances(self):
        """Get a user's balance.

        Returns:
          A list of bitso.Balance instances.        
        """

        url = '%s/balance/' % self.base_url
        resp = self._request_url(url, 'GET', private=True)
        return Balances._NewFromJsonDict(resp['payload'])

  
    def fees(self):
        """Get a user's fees for all availabel order books.

        Returns:
          A list bitso.Fees instances.        
        """

        url = '%s/fees/' % self.base_url
        resp = self._request_url(url, 'GET', private=True)
        return Fees._NewFromJsonDict(resp['payload'])



    def ledger(self, operations='', marker=None, limit=25, sort='desc'):
        """Get the ledger of user operations 

        Args:
          operations (str, optional):
            They type of operations to include. Enum of ('trades', 'fees', 'fundings', 'withdrawals')
            If None, returns all the operations.
          marker (str, optional):
            Returns objects that are older or newer (depending on 'sort') than the object which
            has the marker value as ID
          limit (int, optional):
            Limit the number of results to parameter value, max=100, default=25
          sort (str, optional):
            Sorting by datetime: 'asc', 'desc'
            Defuault is 'desc'

        Returns:
          A list bitso.LedgerEntry instances.
        """
        url = '%s/ledger/%s' % (self.base_url, operations)
        parameters = {}
        if marker:
            parameters['marker'] = marker
        if limit:
            parameters['limit'] = limit
        if sort:
            parameters['sort'] = sort

        #headers = self._build_auth_header('GET', self._build_url(url, parameters))
        resp = self._request_url(url, 'GET', params=parameters, private=True)
        return [LedgerEntry._NewFromJsonDict(entry) for entry in resp['payload']]


    def withdrawals(self, wids=[], marker=None, limit=25, sort='desc'):
        """Get the ledger of user operations 

        Args:
          wids (list, optional):
            Specifies which withdrawal objects to return
          marker (str, optional):
            Returns objects that are older or newer (depending on 'sort') than the object which
            has the marker value as ID
          limit (int, optional):
            Limit the number of results to parameter value, max=100, default=25
          sort (str, optional):
            Sorting by datetime: 'asc', 'desc'
            Defuault is 'desc'

        Returns:
          A list bitso.Withdrawal instances.
        """
        if isinstance(wids, basestring):
            wids = [wids]
        
        url = '%s/withdrawals/' % (self.base_url)
        if wids:
            url+='%s/' % ('-'.join(wids))
        parameters = {}
        if marker:
            parameters['marker'] = marker
        if limit:
            parameters['limit'] = limit
        if sort:
            parameters['sort'] = sort
        resp = self._request_url(url, 'GET', params=parameters, private=True)
        return [Withdrawal._NewFromJsonDict(entry) for entry in resp['payload']]


    def fundings(self, fids=[], marker=None, limit=25, sort='desc'):
        """Get the ledger of user operations 

        Args:
          fids (list, optional):
            Specifies which funding objects to return
          marker (str, optional):
            Returns objects that are older or newer (depending on 'sort') than the object which
            has the marker value as ID
          limit (int, optional):
            Limit the number of results to parameter value, max=100, default=25
          sort (str, optional):
            Sorting by datetime: 'asc', 'desc'
            Defuault is 'desc'

        Returns:
          A list bitso.Funding instances.
        """
        if isinstance(fids, basestring):
            fids = [fids]
        
        url = '%s/fundings/' % (self.base_url)
        if fids:
            url+='%s/' % ('-'.join(fids))
        parameters = {}
        if marker:
            parameters['marker'] = marker
        if limit:
            parameters['limit'] = limit
        if sort:
            parameters['sort'] = sort
        resp = self._request_url(url, 'GET', params=parameters, private=True)
        return [Funding._NewFromJsonDict(entry) for entry in resp['payload']]


    
    def order_trades(self, oid):
        url = '%s/order_trades/%s' % (self.base_url, oid)
        resp = self._request_url(url, 'GET', params={}, private=True)
        return [UserTrade._NewFromJsonDict(x) for x in resp['payload']]

        
    def user_trades(self, tids=[], book=None, marker=None, limit=25, sort='desc'):
        """Get a list of the user's transactions

        Args:
           book (str):
            Specifies which order book to get user trades from. 
          marker (str, optional):
            Returns objects that are older or newer (depending on 'sort') than the object which
            has the marker value as ID
          limit (int, optional):
            Limit the number of results to parameter value, max=100, default=25
          sort (str, optional):
            Sorting by datetime: 'asc', 'desc'
            Defuault is 'desc'
         
        Returns:
          A list bitso.UserTrade instances.        
        """

        url = '%s/user_trades/' % self.base_url
        if isinstance(tids, int):
            tids = str(tids)
        if isinstance(tids, basestring):
            tids = [tids]
        tids = map(str, tids)
        if tids:
            url+='%s/' % ('-'.join(tids))            
        parameters = {}
        if book:
            parameters['book'] = book
        if marker:
            parameters['marker'] = marker
        if limit:
            parameters['limit'] = limit
        if sort:
            if not isinstance(sort, basestring) or sort.lower() not in ['asc', 'desc']:
                 raise ApiClientError({u'message': u"sort is not 'asc' or 'desc' "})
            parameters['sort'] = sort
        resp = self._request_url(url, 'GET', params=parameters, private=True)
        return [UserTrade._NewFromJsonDict(x) for x in resp['payload']]
    

    def open_orders(self, book=None):
        """Get a list of the user's open orders

        Args:
          book (str):
            Specifies which book to use. Default is btc_mxn
            
        Returns:
          A list of bitso.Order instances.        
        """
        url = '%s/open_orders/' % self.base_url
        url+='?book=%s' % book
        parameters = {}
        resp = self._request_url(url, 'GET', params=parameters, private=True)
        return [Order._NewFromJsonDict(x) for x in resp['payload']]


    def lookup_order(self, oids):
        """Get a list of details for one or more orders

        Args:
          order_ids (list):
            A list of Bitso Order IDs
            
        Returns:
          A list of bitso.Order instances.        
        """
        if isinstance(oids, basestring):
            oids = [oids]
        url = '%s/orders/' % self.base_url
        if oids:
            url+='%s/' % ('-'.join(oids))
        resp = self._request_url(url, 'GET', private=True)
        return [Order._NewFromJsonDict(x) for x in resp['payload']]

    def cancel_order(self, oids):
        """Cancels an open order

        Args:
          order_id (str):
            A Bitso Order ID.
            
        Returns:
          A list of Order IDs (OIDs) for the canceled orders. Orders may not be successfully cancelled if they have been filled, have been already cancelled, or the OIDs are incorrect.        
        """
        if isinstance(oids, basestring):
            oids = [oids]        
        url = '%s/orders/' % self.base_url
        url+='%s/' % ('-'.join(oids))
        resp = self._request_url(url, 'DELETE', private=True)
        return resp['payload']

    def place_order(self, **kwargs):
        """Places a buy limit order.

        Args:
          book (str):
            Specifies which book to use. 
          side (str):
            the order side (buy or sell) 
          order_type (str):
            Order type (limit or market)
          major (str):
            The amount of major currency for this order. An order could be specified in terms of major or minor, never both.
          minor (str):
            The amount of minor currency for this order. An order could be specified in terms of major or minor, never both.
          price (str):
            Price per unit of major. For use only with limit orders.


        Returns:
          A bitso.Order instance.        
        """

        if kwargs.get('book') is None:
            raise ApiClientError({u'message': u'book not specified.'})
        if kwargs.get('side') is None:
            raise ApiClientError({u'message': u'side not specified.'})
        if kwargs.get('order_type') is None:
            raise ApiClientError({u'message': u'order type not specified.'})

        url = '%s/orders/' % self.base_url
        parameters = {}
        parameters['book'] = kwargs.get('book')
        parameters['type'] = kwargs.get('order_type')
        parameters['side'] = kwargs.get('side')
        if 'major' in kwargs:
            parameters['major'] = str(kwargs['major']).encode('utf-8')
        if 'minor' in kwargs:
            parameters['minor'] = str(kwargs['minor']).encode('utf-8')
        if 'price' in kwargs:
            parameters['price'] = str(kwargs['price']).encode('utf-8')

        resp = self._request_url(url, 'POST', params=parameters, private=True)
        return resp['payload']



    def funding_destination(self, fund_currency):
        """Returns account funding information for specified currencies.

        Args:
          fund_currency (str):
            Specifies which book to use. 

        
        Returns:
          A bitso.Funding Destination instance.      
        """
        url = '%s/funding_destination/' % self.base_url
        parameters = {}
        parameters['fund_currency'] = fund_currency
        resp = self._request_url(url, 'GET', params=parameters, private=True)
        return FundingDestination._NewFromJsonDict(resp['payload']) 
    

    def btc_withdrawal(self, amount, address):
        """Triggers a bitcoin withdrawal from your account

        Args:
          amount (str):
            The amount of BTC to withdraw from your account
          address (str):
            The Bitcoin address to send the amount to
        
        Returns:
          ok      
        """
        url = '%s/bitcoin_withdrawal/' % self.base_url
        parameters = {}
        parameters['amount'] = str(amount).encode('utf-8')
        parameters['address'] = address
        resp = self._request_url(url, 'POST', params=parameters, private=True)
        return Withdrawal._NewFromJsonDict(resp['payload'])


    def eth_withdrawal(self, amount, address):
        """Triggers an ether withdrawal from your account

        Args:
          amount (str):
            The amount of BTC to withdraw from your account
          address (str):
            The Bitcoin address to send the amount to
        
        Returns:
          ok      
        """
        url = '%s/ether_withdrawal/' % self.base_url
        parameters = {}
        parameters['amount'] = str(amount).encode('utf-8')
        parameters['address'] = address
        resp = self._request_url(url, 'POST', params=parameters, private=True)
        return Withdrawal._NewFromJsonDict(resp['payload'])

    
    def ripple_withdrawal(self, currency, amount, address):
        """Triggers a ripple withdrawal from your account

        Args:
          currency (str):
            The currency to withdraw
          amount (str):
            The amount of BTC to withdraw from your account
          address (str):
            The ripple address to send the amount to
        
        Returns:
          ok      
        """

        url = '%s/ripple_withdrawal/' % self.base_url
        parameters = {}
        parameters['currency'] = str(currency).encode('utf-8')
        parameters['amount'] = str(amount).encode('utf-8')
        parameters['address'] = address
        resp = self._request_url(url, 'POST', params=parameters, private=True)
        return Withdrawal._NewFromJsonDict(resp['payload'])

    
    def spei_withdrawal(self, amount=None, first_names=None, last_names=None, clabe=None, notes_ref=None, numeric_ref=None):
        """Triggers a SPEI withdrawal from your account.
        These withdrawals are immediate during banking hours for some banks (M-F 9:00AM - 5:00PM Mexico City Time), 24 hours for others.


        Args:
          amount (str):
            The amount of MXN to withdraw from your account
          recipient_given_names (str):
            The recipient's first and middle name(s)
          recipient_family_names (str):
            The recipient's last names
          clabe (str):
            The CLABE number where the funds will be sent to
            https://en.wikipedia.org/wiki/CLABE
          notes_ref (str):
            The alpha-numeric reference number for this SPEI
          numeric_ref (str):
            The numeric reference for this SPEI
        
        Returns:
          ok      
        """

        
        url = '%s/spei_withdrawal/' % self.base_url
        parameters = {}
        parameters['amount'] = str(amount).encode('utf-8')
        parameters['recipient_given_names'] = first_names
        parameters['recipient_family_names'] = last_names
        parameters['clabe'] = clabe
        parameters['notes_ref'] = notes_ref
        parameters['numeric_ref'] = numeric_ref
        resp = self._request_url(url, 'POST', params=parameters, private=True)
        return Withdrawal._NewFromJsonDict(resp['payload'])


    def debit_card_withdrawal(self, amount=None, first_names=None, last_names=None, card_number=None, bank_code=None):
        """Triggers a Debit Cards withdrawal from your account. These withdrawals are immediate during banking hours for some 
        banks (M-F 9:00AM - 5:00PM Mexico City Time), 24 hours for others.



        Args:
          amount (str):
            The amount of MXN to withdraw from your account
          recipient_given_names (str):
            The recipient's first and middle name(s)
          recipient_family_names (str):
            The recipient's last names
          clabe (str):
            The CLABE number where the funds will be sent to
            https://en.wikipedia.org/wiki/CLABE
          notes_ref (str):
            The alpha-numeric reference number for this SPEI
          numeric_ref (str):
            The numeric reference for this SPEI
        
        Returns:
          ok      
        """

        
        url = '%s/debit_card_withdrawal/' % self.base_url
        parameters = {}
        parameters['amount'] = str(amount).encode('utf-8')
        parameters['recipient_given_names'] = first_names
        parameters['recipient_family_names'] = last_names
        parameters['card_number'] = card_number
        parameters['bank_code'] = bank_code
        resp = self._request_url(url, 'POST', params=parameters, private=True)
        return Withdrawal._NewFromJsonDict(resp['payload'])

    
    def phone_withdrawal(self, amount=None, first_names=None, last_names=None, phone_number=None, bank_code=None):
        """Triggers a withdrawal from your account to a phone number. (Phone number must be registered for SPEI Transfers with their corresponding bank) These withdrawals are immediate during banking hours for some banks (M-F 9:00AM - 5:00PM Mexico City Time), 24 hours for others.

        Args:
          amount (str):
            The amount of MXN to withdraw from your account
          recipient_given_names (str):
            The recipient's first and middle name(s)
          recipient_family_names (str):
            The recipient's last names
          clabe (str):
            The CLABE number where the funds will be sent to
            https://en.wikipedia.org/wiki/CLABE
          notes_ref (str):
            The alpha-numeric reference number for this SPEI
          numeric_ref (str):
            The numeric reference for this SPEI
        
        Returns:
          ok      
        """

        
        url = '%s/phone_withdrawal/' % self.base_url
        parameters = {}
        parameters['amount'] = str(amount).encode('utf-8')
        parameters['recipient_given_names'] = first_names
        parameters['recipient_family_names'] = last_names
        parameters['phone_number'] = phone_number
        parameters['bank_code'] = bank_code
        resp = self._request_url(url, 'POST', params=parameters, private=True)
        return Withdrawal._NewFromJsonDict(resp['payload'])


    
    
    
    def bank_codes(self):
        """Gets codes for banks to be used in debit_card_withdrawal/phone_number_withdrawal

        Returns:
          A Dictinoary with the name of each bank as keys and it's corresponding key as values
        """

        url = '%s/mx_bank_codes/' % self.base_url
        resp = self._request_url(url, 'GET', private=True)
        banks = {}
        for bank_item in resp['payload']:
            banks[bank_item['name']] = bank_item['code']
        return banks

        
    

    def transfer_quote(self, amount=None, btc_amount=None, currency=None):
        """Get a quote for a transfer for various Bitso Outlets.

        Args:
          btc_amount (str):
            Mutually exclusive with amount. Either this, or amount should
            be present in the request. The total amount in Bitcoins, as
            provided by the user. NOTE: The amount is in BTC format
            (900mbtc = .9 BTC).
          amount (str):
            Mutually exclusive with btc_amount. Either this, or btc_amount
            should be present in the request. The total amount in Fiat currency.
            Use this if you prefer specifying amounts in fiat instead of BTC.
          currency (str):
            An ISO 4217 fiat currency symbol (ie, "MXN"). If btc_amount is
            provided instead of amount, this is the currency to which the BTC
            price will be converted into. Otherwise, if amount is specified
            instead of btc_amount, this is the currency of the specified amount.
        
        Returns:
          A bitso.TransactionQuote instance.         
        """
        
        if currency is None:
            raise ApiClientError({u'message': u"Currency symbol not specified"})
        if amount is None and btc_amount is None:
            raise ApiClientError({u'message': u"Neither 'amount' nor 'btc_amount' are specified"})
        if amount is not None and btc_amount is not None:
            raise ApiClientError({u'message': u"'amount' and 'btc_amount' are mutually exclusive. Pick one"})
        
        url = '%s/transfer_quote' % self.base_url
        parameters = {}
        if amount:
            parameters['amount'] = str(amount).encode('utf-8')
        elif btc_amount:
            parameters['btc_amount'] = str(btc_amount).encode('utf-8')

        parameters['currency'] = currency
        parameters['full'] = True
        resp = self._request_url(url, 'POST', params=parameters, private=True)
        return TransactionQuote._NewFromJsonDict(resp['payload']) 



    def transfer_create(self,
                        amount=None,
                        btc_amount=None,
                        currency=None,
                        rate = None,
                        payment_outlet=None,
                        **kwargs):
        """Request a currency transfer using quoted Bitso transer outlet

        Args:
          btc_amount (str):
            Mutually exclusive with amount. Either this, or amount should
            be present in the request. The total amount in Bitcoins, as
            provided by the user. NOTE: The amount is in BTC format
            (900mbtc = .9 BTC).
          amount (str):
            Mutually exclusive with btc_amount. Either this, or btc_amount
            should be present in the request. The total amount in Fiat currency.
            Use this if you prefer specifying amounts in fiat instead of BTC.
          currency (str):
            An ISO 4217 fiat currency symbol (ie, "MXN"). If btc_amount is
            provided instead of amount, this is the currency to which the BTC
            price will be converted into. Otherwise, if amount is specified
            instead of btc_amount, this is the currency of the specified amount.
          rate (str):
            This is the rate (e.g. BTC/MXN), as acquired from the
            transfer_quote method. You must request a quote in this way before
            creating a transfer.
          payment_outlet (str):
            The outlet_id as provided by quote method. 
          required fields parameters: (str):
            Each of the other 'required_fields', as stipulated in the TransferQuote
            for the chosen payment_outlet.

        
        Returns:
          A bitso.TransactionQuote instance.         
        """
        
        
        if currency is None:
            raise ApiClientError({u'message': u"'currency' not specified"})
        if amount is None and btc_amount is None:
            raise ApiClientError({u'message': u"Neither 'amount' nor 'btc_amount' are specified"})
        if amount is not None and btc_amount is not None:
            raise ApiClientError({u'message': u"'amount' and 'btc_amount' are mutually exclusive. Pick one"})
        if rate is None:
            raise ApiClientError({u'message': u"'rate' not specified"})
        if payment_outlet is None:
            raise ApiClientError({u'message': u"'payment_outlet' not specified"})


        url = '%s/transfer_create' % self.base_url
        parameters = {}
        if amount:
            parameters['amount'] = str(amount).encode('utf-8')
        elif btc_amount:
            parameters['btc_amount'] = str(btc_amount).encode('utf-8')

        parameters['currency'] = currency
        parameters['rate'] = str(rate).encode('utf-8')
        parameters['payment_outlet'] = payment_outlet
        for k, v in iteritems(kwargs):
            parameters[k] = str(v).encode('utf-8')
        resp = self._request_url(url, 'POST', params=parameters, private=True)
        return TransactionOrder._NewFromJsonDict(resp['payload']) 

             
    def transfer_status(self, transfer_id):
        """Request status for a transfer order 

        Args:
          transfer_id (str):
            Bitso Transfer Order ID (As returned by transfer_create
            method.

        """
        if transfer_id is None:
            raise ApiClientError({u'message': u"'transfer_id' not specified"})
        url = '%s/transfer/%s' % (self.base_url, transfer_id)
        parameters = {}
        resp = self._request_url(url, 'GET', params=parameters, private=True)
        return TransactionOrder._NewFromJsonDict(resp['payload'])

    
    def _build_auth_payload(self):
        parameters = {}
        parameters['key'] = self.key
        parameters['nonce'] = str(int(time.time()))
        msg_concat = parameters['nonce']+self.client_id+self.key
        parameters['signature'] = hmac.new(self._secret.encode('utf-8'),
                                           msg_concat.encode('utf-8'),
                                           hashlib.sha256).hexdigest()
        return parameters

    def _build_auth_header(self, http_method, url, json_payload=''):
        if json_payload == {} or json_payload=='{}':
            json_payload = ''
        url_components = urlparse(url)
        request_path = url_components.path
        if url_components.query != '':
            request_path+='?'+url_components.query
        nonce = current_milli_time()
        msg_concat = nonce+http_method.upper()+request_path+json_payload
        signature = hmac.new(self._secret.encode('utf-8'),
                                 msg_concat.encode('utf-8'),
                                 hashlib.sha256).hexdigest()
        return {'Authorization': 'Bitso %s:%s:%s' % (self.key, nonce, signature)}

    
    def _request_url(self, url, verb, params=None, private=False):
        headers=None
        if params == None:
            params = {}
        params = {k: v.decode("utf-8") if isinstance(v, bytes) else v for k, v in params.items()}
        if private:
            headers = self._build_auth_header(verb, url, json.dumps(params))
        if verb == 'GET':
            url = self._build_url(url, params)
            if private:
                headers = self._build_auth_header(verb, url)
            try:
                resp = requests.get(url, headers=headers, timeout=self.timeout)
            except requests.RequestException as e:
                raise
        elif verb == 'POST':
            try:
                resp = requests.post(url, json=params, headers=headers, timeout=self.timeout)
            except requests.RequestException as e:
                raise
        elif verb == 'DELETE':
            try:
                resp = requests.delete(url, headers=headers, timeout=self.timeout)
            except requests.RequestException as e:
                raise
        content = resp.content
        data = self._parse_json(content if isinstance(content, basestring) else content.decode('utf-8'))
        return data

    def _build_url(self, url, params):
        if params and len(params) > 0:
            url = url+'?'+self._encode_parameters(params)
        return url

    def _encode_parameters(self, parameters):
        if parameters is None:
            return None
        else:
            param_tuples = []
            for k,v in parameters.items():
                if v is None:
                    continue
                if isinstance(v, (list, tuple)):
                    for single_v in v:
                        param_tuples.append((k, single_v))
                else:
                    param_tuples.append((k,v))
            return urlencode(param_tuples)


         
    def _parse_json(self, json_data):
        try:
            data = json.loads(json_data)
            self._check_for_api_error(data)
        except:
            raise
        return data

    def _check_for_api_error(self, data):
        if data['success'] != True:
            raise ApiError(data['error'])
        if 'error' in data:
            raise ApiError(data['error'])
        if isinstance(data, (list, tuple)) and len(data)>0:
            if 'error' in data[0]:
                raise ApiError(data[0]['error'])
        

     
     

