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
import string


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

                if iPos.buyDate <= pos.buyDate:
                    pos.buyDate = iPos.buyDate

        pos.costBasis /= len(self.activePos[key])

        return pos

    def getBySector(self, sector: str = None) -> list:
        openPositions = []
        for k, _ in self.activePos:
            if k != []:
                if (self.activePos[k][0].sector == sector or
                        sector == 'All'):
                    openPositions.append(self.activePos[k])
        return openPositions


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


class currentWriter():
    """currentWriter writes data about current positions
        to an excel worksheet."""

    def __init__(
        self,
        port,
        sheet,
        sectorWanted,
        functioner,
        dateof,
        datefrom,
    ):
        self.port = port
        self.sheet = sheet
        self.functioner = functioner
        self.i = 0  # row index
        self.dateof = dateof
        self.datefrom = datefrom
        self.sector = sectorWanted

    def Write(self, sheet) -> int:
        # Write headers
        self._headers(sheet)

        # Write position data
        if self.sector == 'All':
            self._row(
                sheet,
                [
                    # First data block (A:J)
                    'FDRXX',
                    'Fidelity Government Cash Reserves Shs of Benef Interest',
                    '=#N/A',
                    port.cash,
                    1.00,
                    port.cash,
                    1.00,
                    port.cash,
                    0,
                    0,
                    # Second data block (K:M)
                    '',
                    1.00,
                    # TODO: get Beginning cash value
                    '',
                    # Third data block (S:Z)
                    '', 0, 0,
                    # TODO: get weight of cash
                    '',
                    0, 0, 0, 0,
                ]
            )
        data = self.port.getBySector(self.sector)
        for posList in data:
            self._data(sheet, posList)

        # Write total row
        self._total(sheet)

        return self.i

    def _headers(self, sheet) -> None:
        # Write meta-headers.
        sheet['A2:B2'] = 'Holdings as of: {0}'.format(
            self.dateof.strftime('%m-%d-%Y'))
        sheet['G2:J2'] = 'Current Value'
        sheet['O2:R2'] = 'Dividends'
        sheet['T2:W2'] = 'Year to Date Performance'
        sheet['X2:Z2'] = 'Beta'

        # Write headers.
        __headers = [
            # First Header Block (A:J)
            'Ticker', 'Security Name', 'Date Acquired',
            'Cost Basis Total', 'Price', 'Market Value',
            'HPR $', 'HPR %',

            # Second Header Block (K:M)
            '', 'Price', 'Market Value'

            # Third Header Block (N:R)
            '', 'Div Paid YTD', 'TOtal Dividends Collected YTD',
            'Most Recent Dividend Payment', 'Div Date',

            # Fourth Header Block (S:Z)
            '', 'YTD ($)', 'YTD (%)',
            'Stock Weight in Sector', 'Contribution to YTD Sector Return',
            '1 Year', '3 Year', '5 Year',
        ]
        self.i = 3
        self._row(sheet, __headers, 3)
        return None

    def _data(self, sheet, posList) -> None:
        """Write current holdings of a sector to excel sheet."""
        try:
            firstPos = posList[0]
        except IndexError:
            return

        aggrQty = self.port.getAggrQty(firstPos.ticker)
        # Write first block of values to excel sheet.
        row = [
            # First block of data --------------

            # Ticker
            firstPos.ticker,

            # Company Name
            '=' + self.functioner.compName(firstPos.ticker),

            # Earliest Date Bought
            min([pos.buyDate for pos in posList]).strftime('%m/%d/%Y'),

            # Total Quantity
            sum([pos.qty for pos in posList]),

            # Avg Cost Basis
            sum([pos.costBasis * (pos.qty / aggrQty) for pos in posList]),

            # Total Cost Basis
            sum([pos.qty * pos.costBasis for pos in posList]),

            # Current Price
            '=' + self.functioner.histPrice(firstPos.ticker),

            # Market Value
            f'=D{self.i}*G{self.i}',

            # HPR ($)
            f'==H{self.i}*F{self.i}',

            # HPR (%)
            f'==I{self.i}*F{self.i}',

            '',
            # Second block of data --------------

            # Beginning of Period Price
            self.functioner.histPrice(firstPos.ticker, self.datefrom),

            # Beginning of Period Market Value
            f'=L{self.i}*D{self.i}', '',

            # Third block of data --------------

            # Divs Paid YTD
            self.functioner.dividends(
                firstPos.ticker, startDate=self.datefrom),

            # Total Dividends Collected YTD
            sum([self.functioner.dividends(pos)
                 for pos in posList]),

            # TODO:  Most Recent Dividend Payment
            '',

            # TODO:  Most Recent Dividend Date
            '', '',

            # Fourth block of data --------------

            # YTD ($)
            f'=IFERROR(H{self.i}+P{self.i}-M{self.i}, \"\")',

            # YTD (%)
            f'=IFERROR((T{self.i}+P{self.i})/M{self.i}, \"\")',

            # TODO: stock weight in sector
            '',

            # contribution to sector return ytd
            f'=IFERROR(U{self.i}*V{self.i}), \"\")',

            # Beta 1-Year
            self.functioner.beta(
                firstPos.ticker, dateAsOf=self.dateof, betaYr=1),

            # Beta 3-Year
            self.functioner.beta(
                firstPos.ticker, dateAsOf=self.dateof, betaYr=3),

            # Beta 5-Year
            self.functioner.beta(
                firstPos.ticker, dateAsOf=self.dateof, betaYr=5),

            # ESG
            self.functioner.esg(firstPos.ticker),
        ]
        self._row(sheet, row, self.i)

        return None

    def _total(self, sheet) -> None:
        sheet[f'A{self.i}:B{self.i}'] = "TOTALS"

        # Write column sums
        self.__writeTotals(sheet, 'fhimopqtuvw', 4, self.i)

        # Write other columns
        # 1yr beta
        sheet[f'X{self.i}'] = f'=sumproduct(v4:v{self.i-1}, x4:x{self.i-1})'

        # 3yr beta
        sheet[f'X{self.i}'] = f'=sumproduct(v4:v{self.i-1}, y4:y{self.i-1})'

        # 5yr beta
        sheet[f'X{self.i}'] = f'=sumproduct(v4:v{self.i-1}, z4:z{self.i-1})'

        return None

    def __writeTotals(self, sheet, cols, startRow, endRow) -> None:
        for col in cols:
            totalValue = f'=sum({col}{startRow}:{col}{endRow-1})'
            sheet[f'{col}{endRow}'] = totalValue

        return None

    def _row(self, sheet, vals: list) -> None:
        for j in len(vals):
            sheet[f'{string.ascii_lowercase[j]}{self.i}'] = vals[j]
        self.i += 1

        return None


class realizedWriter():
    def __init__(
        self,
        closed,
        functioner,
        iLast,
        dateof,
        datefrom,
    ):
        self.iLast = iLast + 3
        self.closed = closed
        self.functioner = functioner
        self.i = iLast + 3  # row index
        self.dateof = dateof
        self.datefrom = datefrom

    def Write(self, sheet) -> int:

        # Write headers
        self._headers(sheet)

        # Write realized holding data
        self._data(sheet)

        # Write totals
        self._total(sheet)

        return self.i

    def _headers(self, sheet) -> None:
        # Write meta-headers
        asOf = f'Realized Holdings as of: {self.dateof.strftime("%m-%d-%Y")}'
        sheet[f'A{self.i}:B{self.i}'] = asOf
        sheet[f'F{self.i}:G{self.i}'] = 'Beginning of Year'
        sheet[f'H{self.i}:I{self.i}'] = 'At Sale'
        self.i += 1

        # Write Headers
        headers = [
            'Ticker',
            'Security Name',
            'Date Acquired',
            'Date Sold',
            'Quantity',
            'Price',
            'Market Value',
            'Price',
            'Market Value',
            'Dividends Collected',
            'YTD ($)',
            'YTD (%)',
        ]
        self._row(sheet, headers)

        return None

    def _data(self, sheet) -> None:
        for pos in self.closed:
            self._row(sheet, self.__outputPos(pos))

        return None

    def __outputPos(self, pos: Position) -> list:
        divs = self.functioner.dividends(pos.ticker, pos.buyDate, pos.sellDate)
        return [
            pos.ticker,
            self.functioner.compName(pos.ticker),
            pos.buyDate, pos.sellDate,
            pos.qty, pos.costBasis, f'=d{self.i}*e{self.i}',
            pos.costSold, f'=f{self.i}*e{self.i}',
            f'{divs}*e{self.i}', f'=(i{self.i}+j{self.i})-g{self.i}',
            f'=K{self.i}/G{self.i}',
        ]

    def _total(self, sheet) -> None:
        sheet[f'A{self.i}'] = 'TOTALS'
        self.__writeTotals(sheet, 'gijk', self.iLast, self.i)

    def __writeTotals(self, sheet, col, startRow, endRow):
        for col in cols:
            totalValue = f'=sum({col}{startRow}:{col}{endRow-1})'
            sheet[f'{col}{endRow}'] = totalValue

        return None

    def _row(self, sheet, vals: list) -> None:
        for j in len(vals):
            sheet[f'{string.ascii_lowercase[j]}{self.i}'] = vals[j]
        self.i += 1

        return None


class alphaWriter():
    def __init__(
        self,
        currentEndRow: int,
        realizedEndRow: int,
    ):
        self.iCurrent = currentEndRow
        self.iRealized = realizedEndRow
        self.i = realizedEndRow + 4

    def Write(self, sheet: "Worksheet"):
        self._headers(sheet)
        self._data(sheet)
        self._totals(sheet)

        return None

    def _headers(self, sheet) -> None:
        # Write meta-headers
        sheet[f'A{self.i}:B{self.i}'] = 'Year to Date Alpha'
        sheet[f'C{self.i}:G{self.i}'] = 'Beginning of Period/Purchase'
        sheet[f'F{self.i}:G{self.i}'] = 'Current Value/Sale'
        self.i += 1

        headers = [
            'Ticker',
            'Security Name',
            'Realized',
            'Market Value',
            'Weight',
            'Market Value',
            'Weight',
            'YTD ($) w/ Dividends',
            'YTD (%) w/ Dividends',
            'Weighted Contribution to Return',
            '',
            'YTD', 'Benchmark', 'Alpha',
        ]
        self._row(sheet, headers)

        return None

    def _data(self, sheet) -> None:
        # Write Current Data
        currentStart = 4
        for i in range(currentStart, self.iCurrent):
            self._row(
                sheet,
                [
                    f'=A{i}',
                    f'=B{i}',
                    '',
                    f'=M{i}',
                    # TODO: beginning weight
                    '',
                    f'=H{i}',
                    # TODO:  current market weight
                    '',
                    f'=T{i}',
                    f'=H{self.i}/D{self.i}',
                    f'=G{self.i}/I{self.i}',
                ]
            )

        # Write realized data
        realizedStart = self.iCurrent + 6
        for i in range(realizedStart, self.iRealized):
            self._row(
                sheet,
                [
                    f'=A{i}',
                    f'=B{i}',
                    '',
                    f'=M{i}',
                    # TODO: beginning weight
                    '',
                    f'=H{i}',
                    # TODO:  current market weight
                    '',
                    f'=T{i}',
                    f'=H{self.i}/D{self.i}',
                    f'=G{self.i}/I{self.i}',
                ]
            )

        return None

    def _total(self, sheet) -> None:
        alphaStart = self.iRealized + 6

        # Write total row.
        sheet[f'A{self.i}'] = 'TOTALS'
        self._row(
            sheet,
            [
                '',
                '',
                '',
                f'=sum(D{alphaStart}:D{self.i-1})',
                f'=sum(E{alphaStart}:E{self.i-1})',
                f'=sum(F{alphaStart}:F{self.i-1})',
                f'=sum(G{alphaStart}:G{self.i-1})',
                f'=sum(H{alphaStart}:H{self.i-1})',
                f'=H{self.i}/D{self.i}',
            ]
        )
        # Write relative return data
        sheet[f'L{alphaStart}'] = f'J{self.i-1}'
        # TODO: relative return against benchmark
        sheet[f'M{alphaStart}'] = 'TODO:'
        sheet[f'N{alphaStart}'] = f'L{alphaStart}-M{alphaStart}'

        return None

    def _row(self, sheet: 'Worksheet', vals: list):
        for j in len(vals):
            sheet[f'{string.ascii_lowercase[j]}{self.i}'] = vals[j]
        self.i += 1

        return None


class ExcelWriter(object):
    sectorMap = {
        '*': 'All',
        '0': 'Consumer Discretionary',
        '1': 'Consumer Staples',
        '2': 'Energy',
        '3': 'Financials',
        '4': 'Healthcare',
        '5': 'Industrials',
        '6': 'Materials',
        '7': 'Real Estate',
        '8': 'Technology',
        '9': 'Telecom',
        '10': 'Utilities'
    }

    def __init__(
            self,
            port,
            sectorsWanted=['*'],
            funcsWanted='factset',
            endDate=dt.datetime.today(),
            startDate=dt.datetime.today() - dt.timedelta(days=365)
    ):
        self.sectors = []
        for Id in sectorsWanted:
            self.sectors.append(self.sectorMap[Id])

        self.rowIndex = 0
        self.Functioner = xlFuncs.xlFunctionSelector(startDate, endDate,
                                                     funcsWanted)
        self.port = port
        self.endDate = endDate
        self.startDate = startDate
        self.realizedIndex = 4

    def Write(self):
        templatePath = os.path.abspath('data_files/template.xlsx')
        wb = openpyxl.load_workbook(templatePath)

        for sector in self.sectors:
            sectorSheet = wb.copy_worksheet(wb['Sheet1'])
            sectorSheet.title = sector if sector != 'All' else 'Archway Fund'

            # Write Current Holding Data
            current = currentWriter(
                self.port, sectorSheet, sector, self.Functioner,
                self.startDate, self.endDate
            )
            iCurrentEnd = current.Write(sectorSheet)

            # Write Realized Holding Data
            realized = realizedWriter(
                self.port.closed, self.Functioner,
                iCurrentEnd, self.startDate, self.endDate,
            )
            iRealizedEnd = realized.Write(sectorSheet)

            # Write YTD Alpha Data
            alpha = alphaWriter(
                iCurrentEnd, iRealizedEnd,
            )
            alpha.Write(sectorSheet)

        wb.save('portOutput.xlsx')
        # TODO: option to specify output path
