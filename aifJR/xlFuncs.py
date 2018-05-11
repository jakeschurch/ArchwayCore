#!/usr/bin/env python
# -*- coding: future_fstrings -*-

from __future__ import absolute_import
import datetime as dt


class xlFunctionSelector(object):
    today = dt.date.today()
    fiscalYearEnd = dt.date(year=today.year - 1, month=12, day=31)
    oneYearAgo = today - dt.timedelta(days=365)

    bbDateFormat = u'%Y%m%d'
    factsetDateFormat = u'%m/%d/%Y'

    def __init__(
        self,
        startDate,
        endDate,
        funcsWanted=u'factset'
    ):
        self.funcsWanted = funcsWanted
        self.startDate = startDate
        self.endDate = endDate

        if self.funcsWanted == u'factset':
            self.__formatDates(self.factsetDateFormat)
        else:  # Set bloomberg format
            self.__formatDates(bbDateFormat)

    def __formatDates(self, format):
        self.today = self.today.strftime(format)
        self.fiscalYearEnd = self.fiscalYearEnd.strftime(format)
        self.oneYearAgo = self.oneYearAgo.strftime(format)
        self.startDate = self.startDate.strftime(format)
        self.endDate = self.endDate.strftime(format)

    def _abstractFactsetFunc(self, ticker, field):
        return f'fds(\"{ticker}\", \"{field}\")'

    def _abstractBloombergFunc(self, ticker, field, params=None, hist=False):
        params = u', ' + params if params is not None else None
        func = u'bdh' if hist else u'bdp'
        return f'{func}(\"{ticker}\", \"{field}\" {params})'

    def sedolID(self, ticker):
        if self.funcsWanted == u'factset':
            return self._abstractFactsetFunc(ticker, u'FF_SEDOL')
        else:
            return self._abstractBloombergFunc(ticker, u'ID_SEDOL1')

    def subsector(self, ticker):
        if self.funcsWanted == u'factset':
            return self._abstractFactsetFunc(ticker, u'FG_GICS_INDUSTRY')
        else:
            return self._abstractBloombergFunc(
                ticker, u'GICS_INDUSTRY_NAME', params=u'\"Fill\",\"Fund\"')

    def compName(self, ticker):
        if self.funcsWanted == u'factset':
            return self._abstractFactsetFunc(ticker, u"FG_COMPANY_NAME")
        else:
            return self._abstractBloombergFunc(ticker, u"LONG_COMP_NAME")

    def histPrice(self, ticker, dateAsOf=today):
        if self.funcsWanted == u'factset':
            return self._abstractFactsetFunc(
                ticker, f"FG_PRICE({dateAsOf},{dateAsOf})")
        else:
            params = f'{self.endDate}, {self.endDate}, \"Days\",\"A\"'
            return self._abstractBloombergFunc(
                ticker, u"PX_LAST", hist=True, params=params)

    def beta(self, ticker, dateAsOf=today, betaYr=3):
        if self.funcsWanted == u'factset':
            return self._abstractFactsetFunc(
                ticker, f"P_BETA_PR({dateAsOf},,,\"\"{betaYr}YR\"\")")
        else:
            # REVIEW: does this have to be same date?
            params = u'\"BETA_RAW_OVERRIDEABLE\", \"BETA_OVERRIDE_START_DT\", '
            paramsStart = f'TEXT(BaddPeriods({self.startDate}), \"NUMBEROFPERIODS=-3\", \"PER=Y\"), \"YYYYMMDD\"), '
            paramsEnd = f'TEXT(BaddPeriods({self.endDate}), \"NUMBEROFPERIODS=-3\", \"PER=Y\"), \"YYYYMMDD\")'

            return self._abstractBloombergFunc(
                ticker, u'EQY_Beta', params=params + paramsStart + paramsEnd)

    def peRatio(self, ticker):
        if self.funcsWanted == u'factset':
            return self._abstractFactsetFunc(ticker, u'FF_PE(CURR,0)')
        else:
            return self._abstractBloombergFunc(ticker, u'BEST_PE_RATIO')

    def lastDivDate(self, ticker):
        if self.funcsWanted == u'factset':
            return self._abstractFactsetFunc(
                ticker, f'P_DIVS_PD(0,,,,'u'\"\"PAYDATE\"\")")')
        else:
            return self._abstractBloombergFunc(ticker, u'DVD_PAY_DT')

    def lastDiv(self, ticker):
        if self.funcsWanted == u'factset':
            return self._abstractFactsetFunc(
                ticker, f'P_DIVS_PD(0)')
        else:
            return self._abstractBloombergFunc(ticker, u'LAST_DPS_GROSS')

    def dividends(self, ticker, startDate=None, endDate=None):
        if startDate is None:
            startDate = self.fiscalYearEnd
        if endDate is None:
            endDate = self.endDate

        if self.funcsWanted == u'factset':
            return self._abstractFactsetFunc(
                ticker, f'P_DIVS_PD_R({startDate},{endDate},,,,'u'\"\"TOTAL\"\")")')

        else:
            startDateList = startDate.split(u'/')
            endDateList = endDate.split(u'/')

            startParams = f'\"DVD_START_DT\", {startDateList[2]}{startDateList[1]}{startDateList[0]}, '
            endParams = f'\"DVD_END_DT\", {endDateList[2]}{endDateList[1]}{endDateList[0]}'

            return self._abstractBloombergFunc(
                ticker, u'DVD_HIST_ALL', params=startParams + endParams)

    def gainLoss(self, pos, startDate=None):
        if startDate is None:
            startDate = self.fiscalYearEnd

        func = f'({self.histPrice(pos.ticker, self.endDate)}-{self.histPrice(pos.ticker, startDate)}+{self.dividends(pos.ticker, pos.buyDate)})'

        return func

    def mktCap(self, ticker):
        if self.funcsWanted == u'factset':
            return self._abstractFactsetFunc(ticker, u'P_MARKET_VAL_SEC(0)')
        else:
            return self._abstractBloombergFunc(ticker, u'CUR_MKT_CAP')

    def esg(self, ticker):
        if self.funcsWanted == u'factset':
            return u'=#N/A'
        else:
            return self._abstractBloombergFunc(ticker, u"CUR_MKT_CAP")
