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

import portConstruct as pt
import datetime as dt
import tkinter as tk
from tkinter import filedialog, messagebox


class AppFrame(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        pass
        # TODO:


def main():
    portBuilder = pt.PortfolioBuilder()
    today = dt.datetime.today()
    # TEMP:
    fiscalYearEnd = dt.datetime(year=today.year - 4, month=12, day=31)

    portBuilder.loadTransactions(
        r'/home/jake/Desktop/Attribution.csv', 0, fiscalYearEnd, today
    )

    xlWriter = pt.ExcelWriter(
        portBuilder,
        ['*'],
        'factset', endDate=today, startDate=fiscalYearEnd)
    xlWriter.Write()


if __name__ == '__main__':
    main()
