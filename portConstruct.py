#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2018 Jake Schurch
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import openpyxl
import transactions as Tx
import datetime as dt
import numpy as np
import pandas as pd
import xlFuncs
import os


def readCSV(fileLoc, startRow=0) -> pd.DataFrame:
    csv = pd.read_csv(
        fileLoc, header=startRow, skip_blank_lines=True, memory_map=True)
    csv.dropna(inplace=True, thresh=4)

    # strip whitespace from column headers
    csv.rename(columns=lambda x: x.strip(), inplace=True)

    # recode date column
    for header in csv.columns:
        if 'date' in header.lower():
            csv[header] = csv[header].apply(
                lambda x: pd.to_datetime(str(x), format='%m/%d/%Y'))

    # turn nan fee values into 0
    csv['Fees'].replace(np.nan, 0, inplace=True)

    # sort on date
    csv.sort_values(
        by=['Date Of Transaction', 'Action', 'Number of Shares'],
        ascending=[True, True, False],
        inplace=True)
    print(csv.head())
    return csv


class PortfolioBuilder(object):
    def __init__(self):
        self.cash = 0
        self.activePos = {}
        self.closedPos = []
        self.holdings = []

    def __str__(self):
        print("Active Positions:")
        for pos in self.activePos:
            print(f'\t{pos}')
            for tx in self.activePos[pos]:
                print(f'\t\t{tx.__dict__}')

    def loadTransactions(
            self, fileLoc, startRow, startDate, endDate):
        allTx = Tx.LoadTx(
            readCSV(fileLoc, startRow)
        )
        for tx in allTx:
            if tx.datetime >= startDate and tx.datetime <= endDate:
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
        if cashLeft < 0:
            print(Tx.TransactionError(tx.ticker, tx.qty, cashLeft))

        self.cash = cashLeft  # Update cash position
        pos = Position(**tx.exportToPos())

        if tx.ticker not in self.activePos:
            self.activePos[tx.ticker] = []
        self.activePos[tx.ticker].append(pos)

        return pos

    def _sell(self, tx) -> None:
        aggQty = sum([pos.qty for pos in self.activePos[tx.ticker]])

        qtyLeftToSell = (aggQty - tx.qty)

        if qtyLeftToSell >= 0:
            self.cash += tx.price * tx.qty + tx.fees
            while tx.qty > 0:
                tx.qty = self.sellShares(self.activePos[tx.ticker], tx)
            return
        else:
            raise Tx.TransactionError(tx.ticker, tx.qty)

    def sellShares(self, posList, tx) -> float:
        pos = posList[0]

        if pos.qty > tx.qty:  # selling tx.qty shares
            qtyToSell = tx.qty
            tx.qty -= tx.qty
        else:
            qtyToSell = pos.qty
            tx.qty -= pos.qty
        leftOver = tx.qty

        soldPos = Position(**tx.exportToClosed())
        soldPos.qty = qtyToSell
        soldPos.buyDate = pos.buyDate
        soldPos.costBasis = pos.costBasis

        self.closedPos.append(soldPos)
        pos.qty -= qtyToSell

        if pos.qty == 0:
            del posList[0]
            # posList = posList[0:]
        return leftOver

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
            self._infuseCash(tx.qty)
        return

    def _infuseCash(self, amount) -> None:
        self.cash += amount

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

    def __str__(self) -> str:
        return str(self.__dict__)


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
        self.realizedIndex = 4

    def make(self):
        templatePath = os.path.abspath('data_files/template.xlsx')
        wb = openpyxl.load_workbook(templatePath)
        ws = wb.copy_worksheet(wb['currentHoldings'])
        ws.title = 'aifHoldings'

        ws['A1'] = 'Date Updated as of: {0}'.format(self.endDate)

        self.writeCash(ws, self.port)
        for _, posList in self.port.activePos.items():
            # aggPos = self.port.getAggrPos(pos.ticker)
            self.write(posList, ws)
        self.writeTotalRow(ws)

        # after all position lists have been written, output portfolio weights.

        for n in range(4, self.rowIndex + 1):
            # Portfolio Weight
            ws['K' + str(n)] = '=J{0}/J{1}'.format(n, self.rowIndex)

        # Create Realized Holdings Sheet
        realizedSheet = wb.copy_worksheet(wb['currentHoldings'])
        realizedSheet['A1'] = 'Date Updated as of: {0}'.format(
            self.endDate.strftime('%m-%d-%Y'))
        realizedSheet.title = "Realized Holdings"
        for pos in self.port.closedPos:
            self.makeRealized(pos, realizedSheet)

        wb.save('portOutput.xlsx')

    def makeRealized(self, pos, sheet):
        # TODO: test

        # Ticker
        sheet['A' + str(self.realizedIndex)].value = pos.ticker

        # Sector
        sheet['B{0}'.format(self.realizedIndex)].value = pos.sector

        # Name
        sheet['C{0}'.format(
            self.realizedIndex)].value = '=' + self.Functioner.compName(
                pos.ticker)

        # DateBought
        sheet['D{0}'.format(
            self.realizedIndex)].value = pos.buyDate.strftime('%m/%d/%Y')

        # DateSold
        sheet['E{0}'.format(
            self.realizedIndex)].value = pos.sellDate.strftime('%m/%d/%Y')

        # CostBasis
        sheet['F{0}'.format(self.realizedIndex)].value = pos.costBasis

        # YTD Value
        sheet['G{0}'.format(
            self.realizedIndex)].value = '=' + self.Functioner.gainLoss(
                pos)

        # Shares Sold
        sheet['H{0}'.format(self.realizedIndex)].value = pos.qty

        # Sale Price
        sheet['I{0}'.format(self.realizedIndex)].value = pos.costSold

        # Sale Value
        sheet['J{0}'.format(self.realizedIndex)].value = '=I{0}*H{0}'.format(
            self.realizedIndex)

        # Gain/Loss($)
        sheet['K{0}'.format(
            self.realizedIndex)].value = '=' + self.Functioner.gainLoss(
                pos, pos.buyDate) + f'*{pos.qty}'

        # Gain/Loss(%)
        sheet['L{0}'.format(
            self.realizedIndex)].value = '=' + self.Functioner.gainLoss(
                pos,
                pos.buyDate) + f'/{self.Functioner.histPrice(pos.buyDate)}'

        self.realizedIndex += 1

    def write(self, posList, sheet):
        try:
            firstPos = posList[0]
        except IndexError:
            return

        _aggrQty = self.port.getAggrQty(firstPos.ticker)

        # Ticker
        sheet['A' + str(self.rowIndex)].value = firstPos.ticker

        # Company Name
        sheet['B{0}'.format(
            self.rowIndex)].value = '=' + self.Functioner.compName(
                firstPos.ticker)

        # Total Quantity
        sheet['C{0}'.format(self.rowIndex)].value = sum(
            [pos.qty for pos in posList])

        # Average Cost Basis per share
        sheet['D{0}'.format(self.rowIndex)].value = sum(
            [pos.costBasis * (pos.qty / _aggrQty) for pos in posList])

        # Total Cost Basis
        sheet['E{0}'.format(self.rowIndex)].value = sum(
            [pos.qty * pos.costBasis for pos in posList])

        # Earliest Date Bought
        earliestDate = min([pos.buyDate for pos in posList])

        # if earliestDate < dt.datetime(year=2016, month=1, day=1):
        #     earliestDate = "Before Jan 1, 16"
        # else:
        earliestDate = earliestDate.strftime('%m/%d/%Y')
        sheet['F{0}'.format(self.rowIndex)].value = earliestDate

        # Sector
        sheet['G{0}'.format(self.rowIndex)].value = firstPos.sector

        # Subsector
        sheet['H{0}'.format(
            self.rowIndex)].value = '=IFNA(' + self.Functioner.subsector(
                firstPos.ticker) + ',\"Fund\")'

        # Current Price
        sheet['I{0}'.format(
            self.rowIndex)].value = '=' + self.Functioner.histPrice(
                firstPos.ticker)

        # Current Position Value
        sheet['J{0}'.format(self.rowIndex)].value = '=(I{0}*C{0}){1}'.format(
            self.rowIndex, ' '.join([
                '+' + self.Functioner.dividends(pos.ticker) for pos in posList
            ]))

        # 3-Year Beta
        sheet['L{0}'.format(self.rowIndex)].value = '=' + self.Functioner.beta(
            firstPos.ticker)

        # ESG - Rankings
        sheet['M{0}'.format(self.rowIndex)].value = self.Functioner.esg(
            firstPos.ticker)

        # # MktCap Size TODO
        # sheet['N{0}'.format(self.rowIndex)].value

        # Price/Earnings Ratio
        sheet['O{0}'.format(
            self.rowIndex)].value = '=IFNA(' + self.Functioner.peRatio(
                firstPos.ticker) + ',\"NA\"'

        self.rowIndex += 1

    def writeCash(self, sheet, port):
        # Ticker
        sheet['A{0}'.format(self.rowIndex)].value = "FDRXX"

        # Company Name
        sheet['B' + str(
            self.rowIndex
        )] = 'Fidelity Government Cash Reserves Shs of Benef Interest'

        # Total Quantity
        sheet['C{0}'.format(self.rowIndex)].value = port.cash

        # Average Cost Basis per share
        sheet['D{0}'.format(self.rowIndex)].value = 1

        # Total Cost Basis
        sheet['E{0}'.format(self.rowIndex)].value = port.cash

        # Earliest Date Bought REVIEW
        sheet['F{0}'.format(self.rowIndex)].value = ''

        # Sector
        sheet['G{0}'.format(self.rowIndex)].value = 'Cash'

        # Subsector
        sheet['H{0}'.format(self.rowIndex)].value = 'Cash'

        # Current Price
        sheet['I{0}'.format(self.rowIndex)].value = port.cash

        sheet['J{0}'.format(self.rowIndex)].value = port.cash

        self.rowIndex += 1

    def writeTotalRow(self, sheet):
        # Ticker
        sheet['A{0}'.format(self.rowIndex)].value = "Total"

        # Total Cost Basis
        sheet['E{0}'.format(
            self.rowIndex)].value = '=sum(E4:E{0})'.format(self.rowIndex - 1)

        # Current Value of Position
        sheet['J{0}'.format(
            self.rowIndex)].value = '=sum(J4:J{0})'.format(self.rowIndex - 1)
