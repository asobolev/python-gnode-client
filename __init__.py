#!/usr/bin/env Python

"""
Gnode Python(TM) client
~~~~~~~~~~~~

:copyright: (c) 2012 by German Neuroinformatics Node (www.g-node.org)
:license: Permission is hereby granted, free of charge, to any person 
obtaining a copy of this software and associated documentation files
(the"Software"), to deal in the Software without restriction, including 
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

__title__ = 'gnode-client'
__version__ = 'dev'
__author__ = 'Michael Pereira (michael.fsp@gmail.com), Andrey Sobolev \
(sobolev.andrey@gmail.com), Thomas Wachtler (wachtler@bio.lmu.de)'
__copyright__ = 'Copyright 2012 by German Neuroinformatics Node \
 (www.g-node.org)'

import requests

import errors, utils, files, permissions

#NOTE!!!!: using simplejson.JSONDecodeError makes simplejson a mandatory
#	requirement since json doesn't have that error!!!
#	TODO: whether there are other functionalities that json doesn't have or
#		simply decide that simplejson can be a requirement!

#TODO: Move the authentication here authentication method here.
#TODO: the global parameters like URL should obviously also come here.