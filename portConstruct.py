#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np


def readCSV(fileLoc, startRow=0):
    csv = pd.read_csv(
        fileLoc, header=startRow, skip_blank_lines=True, memory_map=True)
    csv.dropna(inplace=True, thresh=4)

    # strip whitespace from column headers
    csv.rename(columns=lambda x: x.strip(), inplace=True)

    # recode date column
    for header in csv.columns:
        if 'date' in header.lower():
            csv[header] = pd.to_datetime(csv[header])

    # turn nan fee vals into 0
    csv['Fees'].replace(np.nan, 0, inplace=True)

    # sort on date
    csv.sort_values(by='Date Of Transaction', ascending=True, inplace=True)
    return csv


class TransactionError(Exception):
    def __init__(self, ticker, quantity, negAmt=None):
        self.ticker = ticker
        self.quantity = quantity
        self.negAmt = negAmt

    def __str__(self):
        if self.negAmt is not None:
            errStr = (f'Transacting {self.ticker} for {self.quantity} shares '
                      f'creates a negative cash balance of {self.negAmt}. '
                      'Please ammend your transaction log.')
        else:
            errStr = (f'Cannot sell shares of {self.ticker} '
                      'because none have been recorded as of yet in the '
                      'transaction log. Please ammend your transaction log.')
        return repr(errStr)


class Transaction(object):
    def __init__(self, **kwargs):
        self.ticker = kwargs['ticker']
        self.quantity = kwargs['quantity']
        self.price = kwargs['price']
        self.fees = kwargs['fees']
        self.sector = kwargs['sector']
        self.action = kwargs['action']
        self.datetime = kwargs['datetime']

    def exportToPos(self) -> dict:
        return {
            'ticker': self.ticker,
            'quantity': self.quantity,
            'costBasis': self.price,
            'sector': self.sector,
            'buyDate': self.datetime,
            'costSold': None,
            'dateSold': None
        }

    def exportToClosed(self) -> dict:
        return {
            'ticker': self.ticker,
            'quantity': self.quantity,
            'costSold': self.price,
            'sector': self.sector,
            'sellDate': self.datetime,
            'costBasis': None,
            'buyDate': None,
        }


class Position(object):
    def __init__(self, **kwargs):
        self.ticker = kwargs['ticker']
        self.sector = kwargs['sector']

        self.quantity = kwargs['quantity']
        self.costBasis = kwargs['costBasis']
        self.costSold = kwargs['costSold']

        self.buyDate = kwargs['buyDate']
        self.sellDate = kwargs['sellDate']

    def exportData(self) -> dict:
        return self.__dict__


class PortfolioBuilder(object):
    def __init__(self):
        self.cash = 0
        self.activePos = {}
        self.closedPos = {}

        self.holdings = []

    def __str__(self):
        print("Active Positions:")
        for pos in self.activePos:
            print(f'\t{pos}')
            for tx in self.activePos[pos]:
                print(f'\t\t{tx.__dict__}')

    def loadTransactions(self, fileLoc, startRow=0):
        df = readCSV(fileLoc, startRow)
        for index, row in df.iterrows():
            kwargs = {
                'action': row.loc['Action'],
                'datetime': row.loc['Date Of Transaction'].to_pydatetime(),
                'ticker': row.loc['Ticker'],
                'sector': row.loc['Sector'],
                'quantity': float(row.loc['Number of Shares']),
                'price': float(row.loc['Sale Price/Share']),
                'fees': float(row.loc['Fees'])
            }

            tx = Transaction(**kwargs)

            # if position not in dictionary, create one
            if tx.ticker not in self.activePos.keys() and tx.ticker.lower(
            ) not in ['fdrxx', 'cash']:
                self.activePos[tx.ticker] = []

            self.executeTx(tx)

    def executeTx(self, tx) -> None:
        if 'buy' in tx.action.lower():
            self._buy(tx)
        elif 'sell' in tx.action.lower():
            self._sell(tx)
        elif 'distribution' in tx.action.lower():
            self._distribute(tx)

    def _buy(self, tx) -> Position:
        cashLeft = self.cash - (tx.price * tx.quantity + tx.fees)
        if cashLeft > 0:
            self.cash = cashLeft  # Update cash position
            pos = Position(**tx.exportToPos())
            self.activePos[tx.ticker].append(pos)
        else:
            raise TransactionError(tx.ticker, tx.quantity, cashLeft)

        return pos

    def _sell(self, tx) -> None:

        aggQty = sum([pos.quantity for pos in self.activePos[tx.ticker]])
        qtyLeftToSell = aggQty - tx.quantity
        if qtyLeftToSell > 0:
            while tx.quantity > 0:
                tx.quantity = self.sellShares(self.activePos[tx.ticker][0],
                                              tx.quantity)
                pass
        else:
            raise TransactionError(tx.ticker, tx.quantity)

        self.cash += tx.price * tx.quantity + tx.fees

    def sellShares(self, pos, tx) -> float:
        if pos.quantity - tx.quantity >= 0:  # selling tx.quantity shares
            qtyLeftOver = pos.quantity - tx.quantity
        else:
            qtyLeftOver = tx.quantity - pos.quantity

        soldPos = Position(tx.exportToClosed())
        soldPos.buyDate = pos.buyDate
        soldPos.costBasis = pos.costBasis
        self.closedPosition[tx.ticker].append(soldPos)
        pos.quantity = qtyLeftOver

        if qtyLeftOver == 0:
            del pos
        return qtyLeftOver

    def getAggrQty(self, ticker: str) -> float:
        aggQty = 0
        for pos in self.activePos[ticker]:
            aggQty += pos.quantity
        return aggQty

    def _distribute(self, tx) -> None:
        """ NOTE: if stock distribution, cost basis is as of day before"""

        if ('cash' or 'fdrxx') not in tx.ticker.lower():
            print(tx.ticker)
            self.activePos[tx.ticker].append()
        else:
            self._infuseCash(tx)
        return

    def _infuseCash(self, tx) -> None:
        cashLeft = self.cash + tx.quantity
        if cashLeft > 0:
            self.cash = cashLeft
        else:
            raise TransactionError(tx.ticker, tx.quantity, cashLeft)
        return
