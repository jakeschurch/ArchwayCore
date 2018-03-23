#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xlFuncs
import portConstruct as pt
import datetime as dt
import os
def main():
    portBuilder = pt.PortfolioBuilder()
    portBuilder.loadTransactions(r'/home/jake/Desktop/Attribution.csv')
    print(os.path.abspath('../data_files'))
    today = dt.datetime.today()
    fiscalYearEnd = dt.date(year=today.year - 1, month=12, day=31)

    posWriter = pt.PosWriter(portBuilder, 'factset', endDate=today, startDate=fiscalYearEnd)
    posWriter.make()

if __name__ == '__main__':
    main()
