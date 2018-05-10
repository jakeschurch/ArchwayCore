#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
import portConstruct as pt
import transactions as Tx
import datetime as dt
import gi
gi.require_version(u'Gtk', u'3.0')
from gi.repository import Gtk

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


today = dt.datetime.today()


class Handler(object):

    @staticmethod
    def sendError(builder, errMsg):
        err_dialogue = builder.get_object(u'error_dialogue')
        err_dialogue.format_secondary_text(errMsg)

        err_dialogue.show()

        response = err_dialogue.run()
        if response != u'':
            err_dialogue.hide()

    @staticmethod
    def setup(builder):
        endDate = builder.get_object(u'entry_enddate')
        endDate.set_text(
            today.strftime(u'%m/%d/%Y')
        )

    @staticmethod
    def checkSectors(builder):
        sectorsWanted = []
        if builder.get_object(u'checkbtn_all').get_active():
            sectorsWanted.append(u'All')
            return

        if builder.get_object(u'checkbtn_telecom').get_active():
            sectorsWanted.append(u'Telecom')

        if builder.get_object(u'checkbtn_realestate').get_active():
            sectorsWanted.append(u'Real Estate')

        if builder.get_object(u'checkbtn_industrials').get_active():
            sectorsWanted.append(u'Industrials')

        if builder.get_object(u'checkbtn_financials').get_active():
            sectorsWanted.append(u'Financials')

        if builder.get_object(u'checkbtn_staples').get_active():
            sectorsWanted.append(u'Consumer Staples')

        if builder.get_object(u'checkbtn_utilites').get_active():
            sectorsWanted.append(u'Utilites')

        if builder.get_object(u'checkbtn_tech').get_active():
            sectorsWanted.append(u'Technology')

        if builder.get_object(u'checkbtn_materials').get_active():
            sectorsWanted.append(u'Materials')

        if builder.get_object(u'checkbtn_healthcare').get_active():
            sectorsWanted.append(u'Health Care')

        if builder.get_object(u'checkbtn_energy').get_active():
            sectorsWanted.append(u'Energy')

        if builder.get_object(u'checkbtn_discretionary').get_active():
            sectorsWanted.append(u'Consumer Discretionary')

        return sectorsWanted

    @staticmethod
    def getData(builder):
        wordsOfEncouragement = u'Please try again.'

        txLogFile = builder.get_object(u'transactionLog_txtbox').get_text()

        if txLogFile == u'':
            errMsg = u'Location of Tx log file given is invalid. '
            Handler().sendError(builder, errMsg + wordsOfEncouragement)
            return

        if builder.get_object(u'radiobutton_factset').get_active():
            functype = u'factset'
        else:
            functype = u'bloomberg'

        outputLoc = builder.get_object(u'outputFolder_txtbox').get_text()
        if outputLoc == u'':
            errMsg = u'Location of output file destination given is invalid. '
            Handler().sendError(builder, errMsg + wordsOfEncouragement)
            return

        if builder.get_object(u'switch_sectorholdings').get_active():
            getSectorHoldings = True
            sectorsWanted = Handler().checkSectors(builder)

            if sectorsWanted == []:
                errMsg = u'No sectors were selected. '
                Handler().sendError(builder, errMsg + wordsOfEncouragement)
                return
        else:
            getSectorHoldings = False
            sectorsWanted = None

        if builder.get_object(u'switch_transactionlog').get_active():
            getTxLog = True
        else:
            getTxLog = False

        return {
            u'getSectorHoldings': getSectorHoldings,
            u'getTxLog': getTxLog,
            u'fileLoc': txLogFile,
            u'outputLoc': outputLoc,
            u'funcType': functype,
            u'startDate': builder.get_object(u'entry_startdate').get_text(),
            u'endDate': builder.get_object(u'entry_enddate').get_text(),
            u'sectorsWanted': sectorsWanted,
        }

    def on_main_window_Destroy(self, *args):
        Gtk.main_quit()

    def on_button_run_clicked(self, button):
        global builder
        userInputs = Handler().getData(builder)
        print(userInputs)
        run(
            getSectorHoldings=userInputs[u'getSectorHoldings'],
            getTxLog=userInputs[u'getTxLog'],
            fileLoc=userInputs[u'fileLoc'],
            outputLoc=userInputs[u'outputLoc'],
            funcType=userInputs[u'funcType'],
            startDate=userInputs[u'startDate'],
            endDate=userInputs[u'endDate'],
            sectorsWanted=userInputs[u'sectorsWanted']
        )

    def on_file_chooser_button_file_set(self, button):
        set_file = button.get_filename()
        txLogBox = builder.get_object(u'transactionLog_txtbox')
        txLogBox.set_text(set_file)

    def on_folder_chooser_button_file_set(self, button):
        set_folder = button.get_filename()
        outputFolderBox = builder.get_object(u'outputFolder_txtbox')
        outputFolderBox.set_text(set_folder)

    def on_checkbtn_all_toggled(self, button):
        if button.get_active():
            builder.get_object(u'checkbtn_telecom').set_active(True)
            builder.get_object(u'checkbtn_realestate').set_active(True)
            builder.get_object(u'checkbtn_industrials').set_active(True)
            builder.get_object(u'checkbtn_financials').set_active(True)
            builder.get_object(u'checkbtn_staples').set_active(True)
            builder.get_object(u'checkbtn_utilites').set_active(True)
            builder.get_object(u'checkbtn_tech').set_active(True)
            builder.get_object(u'checkbtn_materials').set_active(True)
            builder.get_object(u'checkbtn_healthcare').set_active(True)
            builder.get_object(u'checkbtn_energy').set_active(True)
            builder.get_object(u'checkbtn_discretionary').set_active(True)
        else:
            builder.get_object(u'checkbtn_telecom').set_active(False)
            builder.get_object(u'checkbtn_realestate').set_active(False)
            builder.get_object(u'checkbtn_industrials').set_active(False)
            builder.get_object(u'checkbtn_financials').set_active(False)
            builder.get_object(u'checkbtn_staples').set_active(False)
            builder.get_object(u'checkbtn_utilites').set_active(False)
            builder.get_object(u'checkbtn_tech').set_active(False)
            builder.get_object(u'checkbtn_materials').set_active(False)
            builder.get_object(u'checkbtn_healthcare').set_active(False)
            builder.get_object(u'checkbtn_energy').set_active(False)
            builder.get_object(u'checkbtn_discretionary').set_active(False)


builder = Gtk.Builder()


def main():

    builder.add_from_file(u"gui.glade")
    builder.connect_signals(Handler())

    global window
    window = builder.get_object(u"main_window")
    window.show()
    Handler().setup(builder)
    Gtk.main()


def parseDates(startDate, endDate):
    # Should be in format 'MONTH/DAY/4-Digit Year'
    splitStart = startDate.split(u'/')

    try:
        parsedStart = dt.datetime(
            year=int(splitStart[2]),
            month=int(splitStart[0]),
            day=int(splitStart[1])
        )
    except:
        Handler().sendError(
            builder, 'Start Date is not in `mm-dd-yyy` format.'
        )

    splitEnd = endDate.split(u'/')
    try:
        parsedEnd = dt.datetime(
            year=int(splitEnd[2]),
            month=int(splitEnd[0]),
            day=int(splitEnd[1])
        )
    except:
        Handler().sendError(
            builder, 'End Date is not in `mm-dd-yyy` format.'
        )

    return parsedStart, parsedEnd


def run(
    getSectorHoldings,
    getTxLog,
    fileLoc,
    outputLoc,
    funcType,
    startDate,
    endDate,
    sectorsWanted
):

    startDate, endDate = parseDates(startDate, endDate)
    fiscalYearEnd = dt.datetime(year=today.year - 4, month=12, day=31)

    fileLoc = fileLoc.encode(u'string-escape')
    outputLoc = outputLoc.encode(u'string-escape')

    transactions = Tx.LoadTx(
        pt.readCSV(fileLoc, 0), startDate, endDate,
    )

    if getSectorHoldings:
        portBuilder = pt.PortfolioBuilder()
        portBuilder.loadTransactions(transactions)

        xlWriter = pt.ExcelWriter(
            portBuilder,
            [u'*'],
            funcType, endDate=endDate, startDate=fiscalYearEnd)
        xlWriter.Write()


if __name__ == u'__main__':
    main()
