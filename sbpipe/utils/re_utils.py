#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of sbpipe.
#
# sbpipe is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# sbpipe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with sbpipe.  If not, see <http://www.gnu.org/licenses/>.
#
#
#
# $Revision: 2.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-07-13 12:14:32 $


# Regular expressions utils
import re


def nat_sort_key(str):
    """
    The key to sort a list of strings alphanumerically (e.g. "file10" is correctly placed after "file2")
    
    :param str: the string to sort alphanumerically in a list of strings
    :return: the key to sort strings alphanumerically
    """
    _nsre = re.compile('([0-9]+)')
    return [int(str) if str.isdigit() else str.lower()
            for str in re.split(_nsre, str)]


def escape_special_chars(text):
    """
    Escape ^,%, ,[,],(,),{,} from text
    
    :param text: the command to escape special characters inside
    :return: the command with escaped special characters
    """
    text = text.replace('^', '\\^')
    text = text.replace('%', '\\%')
    text = text.replace(' ', '\\ ')
    text = text.replace('[', '\\[')
    text = text.replace(']', '\\]')
    text = text.replace('(', '\\(')
    text = text.replace(')', '\\)')
    text = text.replace('{', '\\{')
    text = text.replace('}', '\\}')
    return text

