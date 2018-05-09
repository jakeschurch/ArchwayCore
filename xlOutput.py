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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import absolute_import
import re


def mapKeys(mapInp, *inp):
    out = []
    for key in inp:
        if key in mapInp:
            if key != u'*':
                out.append(mapInp[key])
            else:
                return mapKeys(mapInp, *[unicode(i) for i in xrange(0, 11)])
        else:
            if len(key) > 2:
                raise ValueError(
                    u'Please re-enter sector values in a valid format.')
            else:
                print f'Passed value is invalid: \'{key}\'. Ignoring.'
    return set(out)


def askForSectors():
    sectors = {
        u'*': u'All',
        u'0': u'Consumer Discretionary',
        u'1': u'Consumer Staples',
        u'2': u'Energy',
        u'3': u'Financials',
        u'4': u'Healthcare',
        u'5': u'Industrials',
        u'6': u'Materials',
        u'7': u'Real Estate',
        u'8': u'Technology',
        u'9': u'Telecom',
        u'10': u'Utilities'
    }
    # promptString = 'Please enter a comma or space-seperated list of desired sector values:\n\n'
    # for key, val in sectors.items():
    #     promptString += f'\t{key}:\t{val}\n'
    # promptSectors = input(promptString)

    promptSectors = u'* ,     0 , 1  a  1 1 1  1'
    promptSectors = re.sub(u'[\s,]+', u' ', promptSectors)
    desiredSectors = promptSectors.split(u' ')

    print mapKeys(sectors, *desiredSectors)
    if u'*' in promptSectors:
        print True
