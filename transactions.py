#!/usr/bin/python3
# -*- coding: utf-8 -*-

import openpyxl
import os


class TransactionError(Exception):
    def __init__(self, ticker, qty, negAmt=None):
        self.ticker = ticker
        self.qty = qty
        self.negAmt = negAmt

    def __str__(self):
        if self.negAmt is not None:
            errStr = (f'Transacting {self.ticker} for {self.qty} shares '
                      f'creates a negative cash balance of {self.negAmt}. '
                      'Please amend your transaction log.')
        else:
            errStr = (f'Cannot sell shares of {self.ticker} '
                      'because none have been recorded as of yet in the '
                      'transaction log. Please amend your transaction log.')
        return repr(errStr)


class Transaction(object):
    def __init__(self, **kwargs):
        self.ticker = kwargs['ticker']
        self.qty = kwargs['qty']
        self.price = kwargs['price']
        self.fees = kwargs['fees']
        self.sector = kwargs['sector']
        self.action = kwargs['action']
        self.datetime = kwargs['datetime']

    def exportToPos(self) -> dict:
        return {
            'ticker': self.ticker,
            'qty': self.qty,
            'costBasis': self.price,
            'sector': self.sector,
            'buyDate': self.datetime,
            'sellDate': None,
            'costSold': None,
            'dateSold': None
        }

    def exportToClosed(self) -> dict:
        return {
            'ticker': self.ticker,
            'qty': self.qty,
            'costSold': self.price,
            'sector': self.sector,
            'sellDate': self.datetime,
            'costBasis': None,
            'buyDate': None,
        }

    def __str__(self) -> str:
        print(self.__dict__)


def GetTx(txFile):
    txList = LoadTx(txFile, 0)
    cashTxList = GetCashTx(txList)
    allTx = txList + cashTxList

    return allTx


def GetCashTx(txList: list) -> list:
    cashTx = []
    for tx in txList:
        amt = tx.qty * tx.price
        if tx.Ticker != "FDRXX" and amt != 0:
            txDetails = {
                "ticker": "FDRXX",
                "qty": amt,
                "price": 1.00,
                "fees": None,
                "action": "Buy" if "sell" in tx.action.lower() else "Sell",
                "datetime": tx.datetime
            }
            cashTx.append(Transaction(**txDetails))
    return cashTx


def LoadTx(df: "dataframe", startRow=0) -> list:
    txList = []
    for _, row in df.iterrows():
        rowPrice = row.loc['Sale Price/Share']
        if type(rowPrice) is str:
            rowPrice = float(rowPrice.replace('$', ''))

        rowShares = row.loc['Number of Shares']
        if type(rowShares) is str:
            rowShares = float(rowShares.replace(',', ''))

        rowFees = row.loc['Fees']
        if type(rowFees) is str:
            rowFees = float(rowFees.replace('$', ''))

        kwargs = {
            'action': row.loc['Action'],
            'datetime': row.loc['Date Of Transaction'].to_pydatetime(),
            'ticker': row.loc['Ticker'],
            'sector': row.loc['Sector'],
            'qty': rowShares,
            'price': rowPrice,
            'fees': rowFees
        }
        txList.append(Transaction(**kwargs))
    return txList


def OutputTx(fileName, txList):
    wb = openpyxl.load_workbook(
        os.path.abspath('data_files/template.xlsx')
    )
    ws = wb.copy_worksheet(wb['transactions'])

    i = 1
    for tx in txList:
        ws['a{0}'.format(i)] = tx.action
        ws['b{0}'.format(i)] = tx.ticker
        ws['c{0}'.format(i)] = tx.qty
        ws['d{0}'.format(i)] = tx.price
        ws['e{0}'.format(i)] = tx.fees
        ws['f{0}'.format(i)] = tx.sector
        ws['g{0}'.format(i)] = tx.datetime
    i += 1


if __name__ == "__main__":
    LoadTx(None, 0)
