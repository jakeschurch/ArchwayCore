#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import absolute_import
import string


def getCol(i, vals=[]):
    if i <= 25:
        vals.append(string.ascii_lowercase[i])
        return u''.join(vals)
    else:
        j = 0
        while (j * 26) < i:
            j += 1
        vals.append(string.ascii_lowercase[j - 1])
        i -= (26 * j-1)+1
        return getCol(i, vals)


print getCol(2)
