# Get Your ClickBank Transactions Into Sqlite With Python

[Clickbank](http://www.clickbank.com) is an amazing service that allows anyone to easily to either as a publisher create and sell information products or as an advertiser sell other peoples products for a commission. Clickbank handles the credit card transactions, and refunds while affiliates can earn as much as 90% of the price of the products as commission. It's a pretty easy to use system and I have used it both as a publisher and as an affiliate to make significant amounts of money online.

The script I have today is a Python program that uses Clickbank's REST API to download the latest transactions for your affiliate IDs and stuffs the data into a database.

The reason for doing this is that it keeps the data **in your control** and allows you to more easily see all of the transactions for all your accounts in one place without having to go to clickbank.com and log in to your accounts constantly. I'm going to be including this data in my Business Intelligence Dashboard Application

One of the new things I did while writing this script was made use of [SQLAlchemy](http://www.sqlalchemy.org) to abstract the database. This means that it should be trivial to convert it over to use MySQL - just change the connection string.

Also you should note that to use this script you'll need to get the **"Clerk API Key"** and the **"Developer API Key"** from your Clickbank account. To generate those keys go to the Account Settings tab from the account dashboard. If you have more than one affiliate ID then you'll need one Clerk API Key per affiliate ID.

This is the biggest script I have shared on this site yet. I hope someone finds it useful.

Here's the code:

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# (C) 2009 HalOtis Marketing
# written by Matt Warren
# http://halotis.com/

import csv
import httplib
import logging

from sqlalchemy import Table, Column, Integer, String, MetaData, Date, DateTime, Float
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

LOG_FILENAME = 'ClickbankLoader.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,filemode='w')

#generate these keys in the Account Settings area of ClickBank when you log in.
ACCOUNTS = [{'account':'YOUR_AFFILIATE_ID',  'API_key': 'YOUR_API_KEY' },]
DEV_API_KEY = 'YOUR_DEV_KEY'

CONNSTRING='sqlite:///clickbank_stats.sqlite'

Base = declarative_base()
class ClickBankList(Base):
    __tablename__ = 'clickbanklist'
    __table_args__ = (UniqueConstraint('date','receipt','item'),{})

    id                 = Column(Integer, primary_key=True)
    account            = Column(String)
    processedPayments  = Column(Integer)
    status             = Column(String)
    futurePayments     = Column(Integer)
    firstName          = Column(String)
    state              = Column(String)
    promo              = Column(String)
    country            = Column(String)
    receipt            = Column(String)
    pmtType            = Column(String)
    site               = Column(String)
    currency           = Column(String)
    item               = Column(String)
    amount             = Column(Float)
    txnType            = Column(String)
    affi               = Column(String)
    lastName           = Column(String)
    date               = Column(DateTime)
    rebillAmount       = Column(Float)
    nextPaymentDate    = Column(DateTime)
    email              = Column(String)

    format = '%Y-%m-%dT%H:%M:%S'

    def __init__(self, account, processedPayments, status, futurePayments, firstName, state, promo, country, receipt, pmtType, site, currency, item, amount , txnType, affi, lastName, date, rebillAmount, nextPaymentDate, email):
        self.account            = account
        if processedPayments != '':
            self.processedPayments  = processedPayments
        self.status             = status
        if futurePayments != '':
            self.futurePayments     = futurePayments
        self.firstName          = firstName
        self.state              = state
        self.promo              = promo
        self.country            = country
        self.receipt            = receipt
        self.pmtType            = pmtType
        self.site               = site
        self.currency           = currency
        self.item               = item
        if amount != '':
            self.amount             = amount
        self.txnType            = txnType
        self.affi               = affi
        self.lastName           = lastName
        self.date               = datetime.strptime(date[:19], self.format)
        if rebillAmount != '':
            self.rebillAmount       = rebillAmount
        if nextPaymentDate != '':
            self.nextPaymentDate    = datetime.strptime(nextPaymentDate[:19], self.format)
        self.email              = email

    def __repr__(self):
        return "<clickbank ('%s - %s - %s - %s')>" % (self.account, self.date, self.receipt, self.item)

def get_clickbank_list(API_key, DEV_key):
    conn = httplib.HTTPSConnection('api.clickbank.com')
    conn.putrequest('GET', '/rest/1.0/orders/list')
    conn.putheader("Accept", 'text/csv')
    conn.putheader("Authorization", DEV_key+':'+API_key)
    conn.endheaders()
    response = conn.getresponse()

    if response.status != 200:
        logging.error('HTTP error %s' % response)
        raise Exception(response)

    csv_data = response.read()

    return csv_data

def load_clickbanklist(csv_data, account, dbconnection=CONNSTRING, echo=False):
    engine = create_engine(dbconnection, echo=echo)

    metadata = Base.metadata
    metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    data = csv.DictReader(iter(csv_data.split('\n')))

    for d in data:
        item = ClickBankList(account, **d)
        #check for duplicates before inserting
        checkitem = session.query(ClickBankList).filter_by(date=item.date, receipt=item.receipt, item=item.item).all()

        if not checkitem:
            logging.info('inserting new transaction %s' % item)
            session.add(item)

    session.commit()

if  __name__=='__main__':
    try:
        for account in ACCOUNTS:
            csv_data = get_clickbank_list(account['API_key'], DEV_API_KEY)
            load_clickbanklist(csv_data, account['account'])
    except:
        logging.exception('Crashed')
```
