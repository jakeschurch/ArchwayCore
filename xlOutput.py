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
import re


def mapKeys(mapInp, *inp):
    out = []
    for key in inp:
        if key in mapInp:
            if key != '*':
                out.append(mapInp[key])
            else:
                return mapKeys(mapInp, *[str(i) for i in range(0, 11)])
        else:
            if len(key) > 2:
                raise ValueError(
                    'Please re-enter sector values in a valid format.')
            else:
                print(f'Passed value is invalid: \'{key}\'. Ignoring.')
    return set(out)


def askForSectors():
    sectors = {
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
    # promptString = 'Please enter a comma or space-seperated list of desired sector values:\n\n'
    # for key, val in sectors.items():
    #     promptString += f'\t{key}:\t{val}\n'
    # promptSectors = input(promptString)

    promptSectors = '* ,     0 , 1  a  1 1 1  1'
    promptSectors = re.sub('[\s,]+', ' ', promptSectors)
    desiredSectors = promptSectors.split(' ')

    print(mapKeys(sectors, *desiredSectors))
    if '*' in promptSectors:
        print(True)
