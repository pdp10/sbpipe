#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 Piero Dalle Pezze
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


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

