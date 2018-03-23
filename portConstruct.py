#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import openpyxl
import datetime as dt
import numpy as np
import pandas as pd
import xlFuncs


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

    # turn nan fee values into 0
    csv['Fees'].replace(np.nan, 0, inplace=True)

    # sort on date
    csv.sort_values(
        by=['Date Of Transaction', 'Action', 'Number of Shares'],
        ascending=[True, False, False],
        inplace=True)

    return csv


class TransactionError(Exception):
    def __init__(self, ticker, qty, negAmt=None):
        self.ticker = ticker
        self.qty = qty
        self.negAmt = negAmt

    def __str__(self):
        if self.negAmt is not None:
            errStr = (f'Transacting {self.ticker} for {self.qty} shares '
                      f' creates a negative cash balance of {self.negAmt}.'
                      ' Please amend your transaction log.')
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

    def loadTransactions(self, fileLoc, startRow=4):
        df = readCSV(fileLoc, startRow)
        for _, row in df.iterrows():
            rowPrice = row.loc['Sale Price/Share']
            if type(rowPrice) is not float and '$' in rowPrice:
                rowPrice = rowPrice.strip('$')

            kwargs = {
                'action': row.loc['Action'],
                'datetime': row.loc['Date Of Transaction'].to_pydatetime(),
                'ticker': row.loc['Ticker'],
                'sector': row.loc['Sector'],
                'qty': float(row.loc['Number of Shares']),
                'price': float(rowPrice),
                'fees': float(row.loc['Fees'])
            }

            tx = Transaction(**kwargs)

            # if position not in dictionary, create key
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

    def _buy(self, tx) -> 'Position':
        cashLeft = self.cash - (tx.price * tx.qty + tx.fees)
        if cashLeft > 0:
            self.cash = cashLeft  # Update cash position
            pos = Position(**tx.exportToPos())
            self.activePos[tx.ticker].append(pos)
        else:
            # BUG: creating negative cash balance...
            raise TransactionError(tx.ticker, tx.qty, cashLeft)

        return pos

    def _sell(self, tx) -> None:

        aggQty = sum([pos.qty for pos in self.activePos[tx.ticker]])
        qtyLeftToSell = (aggQty - tx.qty)

        if qtyLeftToSell > 0:
            while tx.qty > 0:
                tx.qty = self.sellShares(self.activePos[tx.ticker][0], tx.qty)
                pass
        else:
            raise TransactionError(tx.ticker, tx.qty)

        self.cash += tx.price * tx.qty + tx.fees

    def sellShares(self, pos, tx) -> float:
        if pos.qty - tx.qty >= 0:  # selling tx.qty shares
            qtyLeftOver = pos.qty - tx.qty
        else:
            qtyLeftOver = tx.qty - pos.qty

        soldPos = Position(**tx.exportToClosed())
        soldPos.buyDate = pos.buyDate
        soldPos.costBasis = pos.costBasis
        self.closedPos[tx.ticker].append(soldPos)
        pos.qty = qtyLeftOver

        if qtyLeftOver == 0:
            del pos
        return qtyLeftOver

    def getAggrQty(self, ticker: str) -> float:
        aggQty = 0
        for pos in self.activePos[ticker]:
            aggQty += pos.qty
        return aggQty

    def _distribute(self, tx) -> None:
        """ NOTE: if stock distribution, cost basis is as of day before"""

        if 'cash' not in tx.ticker.lower() and 'fdrxx' not in tx.ticker.lower(
        ):
            self.activePos[tx.ticker].append()
        else:
            self._infuseCash(tx)
        return

    def _infuseCash(self, tx) -> None:
        cashLeft = self.cash + tx.qty
        if cashLeft > 0:
            self.cash = cashLeft
        else:
            raise TransactionError(tx.ticker, tx.qty, cashLeft)
        return

    def getAggrPos(self, key: str) -> 'Position':
        pos = None
        for index, iPos in self.activePos[key].items():

            if index == 0:
                pos = Position(iPos.exportData())
            else:
                pos.qty += iPos.qty
                pos.costBasis += iPos.costBasis

                pos.buyDate = iPos.buyDate if iPos.buyDate <= pos.buyDate else pos.buyDate

        pos.costBasis /= len(self.activePos[key])

        return pos


class Position(object):
    def __init__(self, **kwargs):
        self.ticker = kwargs['ticker']
        self.sector = kwargs['sector']

        self.qty = kwargs['qty']
        self.costBasis = kwargs['costBasis']
        self.costSold = kwargs['costSold']

        self.buyDate = kwargs['buyDate']
        self.sellDate = kwargs['sellDate']

    def exportData(self) -> dict:
        return self.__dict__


class PosWriter(object):
    def __init__(self,
                 port,
                 funcsWanted='factset',
                 endDate=dt.datetime.today(),
                 startDate=dt.datetime.today() - dt.timedelta(days=365)):
        self.rowIndex = 4
        self.Functioner = xlFuncs.xlFunctionSelector(startDate, endDate,
                                                     funcsWanted)
        self.port = port
        self.endDate = endDate
        self.startDate = startDate

    def make(self):
        wb = openpyxl.load_workbook('../data_files/template.xlsx')
        ws = wb.copy_worksheet('currentHoldings')
        ws.name = 'Current AIF Holdings'

        ws['A1'] = 'Date Updated as of: {0}'.format(self.endDate)

        self.writeCash(ws, self.port)
        for _, posList in self.port.activePos:
            # aggPos = self.port.getAggrPos(pos.ticker)
            self.write(posList, 'Current AIF Holdings')
            self.writeTotalRow('Current AIF Holdings')

        # after all position lists have been written, output portfolio weights.

        for n in range(4, self.rowIndex + 1):
            # Portfolio Weight
            ws['K' + n] = '=J{0}/J{1}'.format(n, self.rowIndex)

        wb.save(ws)

    def write(self, posList, sheet):
        firstPos = posList[0]
        _aggrQty = self.port.getAggrQty(firstPos.ticker)

        # Ticker
        sheet['A' + self.rowIndex] = firstPos.ticker

        # Company Name
        sheet['B' + self.rowIndex] = self.Functioner.compName(firstPos.ticker)

        # Total Quantity
        sheet['C' + self.rowIndex] = sum([pos.qty for pos in posList])

        # Average Cost Basis per share
        sheet['D' + self.rowIndex] = sum(
            [pos.costBasis * (pos.qty / _aggrQty) for pos in posList])

        # Total Cost Basis
        sheet['E' + self.rowIndex] = sum(
            [pos.qty * pos.costBasis for pos in posList])

        # Earliest Date Bought
        sheet['F' + self.rowIndex] = min([pos.costBasis for pos in posList])

        # Sector
        sheet['G' + self.rowIndex] = firstPos.sector

        # Subsector
        sheet['H' + self.rowIndex] = self.Functioner.subsector(firstPos.ticker)

        # Current Price
        sheet['I' + self.rowIndex] = self.Functioner.histPrice(firstPos.ticker)

        # Current Position Value
        sheet['J' + self.rowIndex] = '=I{0}*C{0}{1}'.format(
            self.rowIndex, ' '.join([
                '+' + self.Functioner.dividends(pos.ticker) for pos in posList
            ]))

        # 3-Year Beta
        sheet['L' + self.rowIndex] = self.Functioner.beta(firstPos.ticker)

        # ESG - Rankings
        sheet['M' + self.rowIndex] = self.Functioner.esg(firstPos.ticker)

        # # MktCap Size TODO
        # sheet['N' + self.rowIndex]

        # Price/Earnings Ratio
        sheet['O' + self.rowIndex] = self.Functioner.peRatio(firstPos.ticker)

        self.index += 1

    def writeCash(self, sheet, port):
        # Ticker
        sheet['A' + self.rowIndex] = "FDRXX"

        # Company Name
        sheet[
            'B' + self.
            rowIndex] = 'Fidelity Government Cash Reserves Shs of Benef Interest'

        # Total Quantity
        sheet['C' + self.rowIndex] = port.Cash

        # Average Cost Basis per share
        sheet['D' + self.rowIndex] = 1

        # Total Cost Basis
        sheet['E' + self.rowIndex] = self.cash

        # Earliest Date Bought REVIEW
        sheet['F' + self.rowIndex] = ''

        # Sector
        sheet['G' + self.rowIndex] = 'Cash'

        # Subsector
        sheet['H' + self.rowIndex] = 'Cash'

        # Current Price
        sheet['I' + self.rowIndex] = port.Cash

        self.rowIndex += 1

    def writeTotalRow(self, sheet):
        # Ticker
        sheet['A' + self.rowIndex] = "Total"

        # Total Cost Basis
        sheet['E' + self.rowIndex] = '=sum(E4:E{0})'.format(self.rowIndex - 1)

        # Current Value of Position
        sheet['J' + self.rowIndex] = '=sum(J4:J{0})'.format(self.rowIndex - 1)
