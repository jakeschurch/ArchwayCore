#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime as dt


class xlFunctionSelector(object):
    today = dt.date.today()
    fiscalYearEnd = dt.date(year=today.year - 1, month=12, day=31)
    oneYearAgo = today - dt.timedelta(days=365)

    bbDateFormat = '%Y%m%d'
    factsetDateFormat = '%m/%d/%Y'

    def __init__(self, startDate, endDate, funcsWanted='factset'):
        self.funcsWanted = funcsWanted
        self.startDate = startDate
        self.endDate = endDate

        if self.funcsWanted == 'factset':
            self.__formatDates(self.factsetDateFormat)
        else:  # Set bloomberg format
            self.__formatDates(bbDateFormat)

    def __formatDates(self, format: str) -> None:
        self.today = self.today.strftime(format)
        self.fiscalYearEnd = self.fiscalYearEnd.strftime(format)
        self.oneYearAgo = self.oneYearAgo.strftime(format)
        self.startDate = self.startDate.strftime(format)
        self.endDate = self.endDate.strftime(format)

    def _abstractFactsetFunc(self, ticker, field):
        return f'fds(\"{ticker}\", \"{field}\")'

    def _abstractBloombergFunc(self, ticker, field, params=None, hist=False):
        params = ', ' + params if params is not None else None
        func = 'bdh' if hist == True else 'bdp'
        return f'{func}(\"{ticker}\", \"{field}\" {params})'

    def sedolID(self, ticker):
        if self.funcsWanted == 'factset':
            return self._abstractFactsetFunc(ticker, 'FF_SEDOL')
        else:
            return self._abstractBloombergFunc(ticker, 'ID_SEDOL1')

    def sector(self, ticker):
        if self.funcsWanted == 'factset':
            return self._abstractFactsetFunc(ticker, 'FG_GICS_INDUSTRY')
        else:
            return self._abstractBloombergFunc(
                ticker, 'GICS_INDUSTRY_NAME',
                params='\"Fill\",\"Fund\"')

    def compName(self, ticker):
        if self.funcsWanted == 'factset':
            return self._abstractFactsetFunc(ticker, "FG_COMPANY_NAME")
        else:
            return self._abstractBloombergFunc(ticker, "LONG_COMP_NAME")

    def histPrice(self, ticker, dateAsOf=today):
        if self.funcsWanted == 'factset':
            return self._abstractFactsetFunc(
                ticker, f"FG_PRICE({dateAsOf},{dateAsOf})")
        else:
            params = f'{self.endDate}, {self.endDate}, \"Days\",\"A\"'
            return self._abstractBloombergFunc(
                ticker, "PX_LAST", hist=True, params=params)

    def beta(self, ticker, dateAsOf=today):
        if self.funcsWanted == 'factset':
            return self._abstractFactsetFunc(
                ticker, f"P_BETA_PR({dateAsOf},,,\"\"3YR\"\")")
        else:
            # REVIEW: does this have to be same date?
            params = '\"BETA_RAW_OVERRIDEABLE\", \"BETA_OVERRIDE_START_DT\", '
            paramsStart = f'TEXT(BaddPeriods({self.startDate}), \"NUMBEROFPERIODS=-3\", \"PER=Y\"), \"YYYYMMDD\"), '
            paramsEnd = f'TEXT(BaddPeriods({self.endDate}), \"NUMBEROFPERIODS=-3\", \"PER=Y\"), \"YYYYMMDD\")'

            return self._abstractBloombergFunc(
                ticker, 'EQY_Beta', params=params + paramsStart + paramsEnd)

    def peRatio(self, ticker):
        if self.funcsWanted == 'factset':
            return self._abstractFactsetFunc(ticker, 'FF_PE(CURR,0)')
        else:
            return self._abstractBloombergFunc(ticker, 'BEST_PE_RATIO')

    def dividends(self, ticker):
        if self.funcsWanted == 'factset':
            return self._abstractFactsetFunc(
                ticker, f"P_DIVS_PD_R({self.startDate},{self.endDate},,,,"
                "TOTAL"
                ")")
        else:
            startDateList = self.startDate.split('/')
            endDateList = self.endDate.split('/')
            startParams = f'\"DVD_START_DT\", {startDateList[2]}{startDateList[1]}{startDateList[0]}, '
            endParams = f'\"DVD_END_DT\, {endDateList[2]}{endDateList[1]}{endDateList[0]}'

            return self._abstractBloombergFunc(
                ticker, 'DVD_HIST_ALL', params=startParams + endParams)

    def mktCap(self, ticker):
        if self.funcsWanted == 'factset':
            return self._abstractFactsetFunc(ticker, 'P_MARKET_VAL_SEC(0)')
        else:
            return self._abstractBloombergFunc(ticker, 'CUR_MKT_CAP')

    def esg(self, ticker):
        if self.funcsWanted == 'factset':
            return '=#N/A'
        else:
            return self._abstractBloombergFunc(ticker, "CUR_MKT_CAP")


if __name__ == '__main__':
    today = dt.date.today()
    bbDateFormat = '%Y%m%d'
    print(today.strftime(bbDateFormat))
