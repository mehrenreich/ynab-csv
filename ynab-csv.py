#!/usr/bin/env python3

import os
import sys
import re
import codecs
from datetime import datetime


if len(sys.argv) != 2:
    print('Usage: %s INPUT_FILE' % __file__, file=sys.stderr)
    sys.exit(1)

input_file = sys.argv[1]

if not os.path.isfile(input_file):
    print('Input file %s not found' % input_file, file=sys.stderr)
    sys.exit(1)

with codecs.open(input_file, 'r', 'iso-8859-1') as file:
    r = re.compile(r'^"\d')
    transactions = list(filter(r.search, file.readlines()))
    print('Date;Payee;Memo;Outflow;Inflow')
    for t in transactions:
        a = {}
        fields = list(map(lambda l: l.replace('"', ''), t.split(';')))
        a['inflow'] = ''
        a['outflow'] = ''
        a['date'] = datetime.strptime(fields[0], '%d.%m.%Y')
        a['amount'] = float(fields[4].replace('.', '').replace(',', '.'))
        if a['amount'] < 0:
            a['outflow'] = a['amount'] * -1
        else:
            a['inflow'] = a['amount']
        if fields[2] == 'Wertpapiere':
            a['payee'] = 'Depot'
        else:
            a['payee'] = re.search(
                r'^([^:]+): (.*) Buchungstext', fields[3]).group(2)
        a['memo'] = re.search(r'Buchungstext: (.*)', fields[3]).group(1)
        print('%s;%s;%s;%s;%s' % (a['date'].strftime(
            '%d.%m.%Y'), a['payee'], a['memo'], a['outflow'], a['inflow']))
