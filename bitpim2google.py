#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Simple script to convert a CSV contact list from bitpim to
something you can import into google voice.
By Kevin Darlington (http://outroot.com)"""

import sys
import csv
import optparse

phone_type_map = {
  'cell': 'Mobile',
  'office': 'Work'
}

#===================================
def get_full_number(number):
  if number and not number.startswith('+1'):
    return '+1' + number
  return None

#===================================
def get_phone_type(type):
  if not type:
    return type
  type = phone_type_map.get(type, type)
  return type.lower().capitalize()

#===================================
if __name__ == '__main__':
  usage = 'usage: %prog <input file> [output file]'
  parser = optparse.OptionParser(usage)
  (options, args) = parser.parse_args()
  
  if len(args) < 1:
    parser.print_help()
    sys.exit(1)
  
  reader = csv.reader(open(args[0], 'r'), delimiter=',')
  writer = csv.writer(
    open(args[1] if len(args) > 1 else 'google.csv', 'wb'),
    delimiter=',',
    quoting=csv.QUOTE_MINIMAL
  )
  
  header = None
  phone_count = 0
  for row in reader:
    if reader.line_num == 1:
      header = row
      phone_count = header.count('numbers_number')
      
      tmprow = ['Name', 'Given Name', 'Nickname']
      for x in range(phone_count):
        tmprow.append('Phone %d - Type' % (x+1))
        tmprow.append('Phone %d - Value' % (x+1))
    else:
      tmprow = [
        row[header.index('names_full')],
        row[header.index('names_full')],
        row[header.index('names_nickname')]
      ]
      
      type_index = -1
      number_index = -1
      for x in range(phone_count):
        type_index = header.index('numbers_type', type_index+1)
        number_index = header.index('numbers_number', number_index+1)
        tmprow.append(get_phone_type(row[type_index]))
        tmprow.append(get_full_number(row[number_index]))
      
    writer.writerow(tmprow)
      