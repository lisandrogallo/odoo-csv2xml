# -*- coding: utf-8 -*-

import re
import sys
from os import chdir, path
import glob

# delimiter used in the CSV file(s)
DELIMITER = ","

# 4 spaces tabulation
TAB = 4 * ' '

def reference_match(field, regex=re.compile(r'([a-z]*_id\/id)$')):
    return regex.match(field)

# The optional command-line argument maybe a CSV file or a folder
if len(sys.argv) == 2:
    arg = sys.argv[1].lower()
    # If a CSV file then convert only that file
    if arg.endswith('.csv'):
        csvFiles = [arg]
    # If a folder path then convert all CSV files in the that folder
    else:
        chdir(arg)
        csvFiles = glob.glob('*.csv')
# If no command-line argument then convert all CSV files in the current folder
elif len(sys.argv) == 1:
    csvFiles = glob.glob('*.csv')
else:
    sys.exit()

for csvFileName in csvFiles:
    xmlFile = csvFileName[:-4] + '.xml'

    # Read the CSV file as binary data in case there are non-ASCII characters
    csvFile = open(csvFileName, 'rb')
    csvData = csvFile.readlines()
    csvFile.close()
    tags = csvData.pop(0).strip().replace(' ', '_').split(DELIMITER)
    xmlData = open(xmlFile, 'w')
    xmlData.write('<?xml version="1.0" encoding="utf-8"?>' + '\n')

    # There must be only one top-level tag
    xmlData.write('<openerp>' + '\n')
    xmlData.write(TAB + '<data noupdate="0">' + '\n')


    for row in csvData:
        rowData = row.strip().split(delimiter)
        xmlData.write('\n' + tab*2 + '<record id="' + rowData[0] +
                      '" model="' + csvFileName[:-4] + '">' + '\n')

        for i in range(1, len(tags)):

            if tags[i]:
                if reference_match(tags[i]) and rowData[i]:
                    xmlData.write(TAB*3 + '<field name="' +
                                  tags[i].split('/', 1)[0] +
                                  '"' + ' ref="' + rowData[i] + '"/>' + '\n')
                else:
                    xmlData.write(TAB*3 + '<field name="' +
                                  tags[i].split('/', 1)[0] +
                                  '">' + rowData[i] + '</field>' + '\n')

        xmlData.write(TAB*2 + '</record>' + '\n')

    xmlData.write('\n' + TAB + '</data>' + '\n')
    xmlData.write('</openerp>' + '\n')
    xmlData.close()
