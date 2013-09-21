#!/usr/bin/env python
#    futubox to XMLTV - copyright 2013 Francesco Santini <francesco.santini@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
import csv
#import xml.etree.ElementTree as ET
from lxml import etree as ET
import urllib2

# CSV with channel number vs channel names
chanlistFile = 'futubox_channels.csv'
# CSV with channel number vs URL number
chanmapFile = 'futubox_chan_map.csv'
# output XML guide file
outXMLFile = 'futubox_guide.xml'
#prefix added to IDs
futuboxPrefix = 'futubox'

def convertDateTime(datestamp):
  #converts 2013-09-14T00:30:00+02:00 into 20130914003000 +0200
  return datestamp.replace('-','').replace(':','').replace('T','').replace('+',' +')
  
def getURL(chanID):
  return 'http://futubox.to/channels/' + str(chanID) + '/programmes.xml'
  
# load channel list and generate chan XML
tv = ET.XML('<?xml version="1.0" encoding="utf-8" ?>\n<tv></tv>')
chanNames = []
with open(chanlistFile, 'rb') as csvfile:
  chanreader = csv.reader(csvfile, delimiter=',')
  for row in chanreader:
    chanNames.append(row[1] or '')
    
for chanID, chanName in enumerate(chanNames):
  if chanName != '':
    chanElement = ET.SubElement(tv, 'channel', {'id': futuboxPrefix + str(chanID+1)})
    dnameElement = ET.SubElement(chanElement, 'display-name')
    dnameElement.text = chanName

# load channel IDs
chanURLs = []
with open(chanmapFile, 'rb') as csvfile:
  chanreader = csv.reader(csvfile, delimiter=',')
  for row in chanreader:
    chanURLs.append(row[1] or '')
   
# read URLs
for chanID, chanURL in enumerate(chanURLs):
  if not chanURL: continue
  print 'Reading', chanURL
  chanXML = urllib2.urlopen(getURL(chanURL))
  futuboxXML = ET.parse(chanXML)
  progs = futuboxXML.find('programmes')
  for prog in progs.findall('programme'):
    start = convertDateTime(prog.find('start-at').text)
    end = convertDateTime(prog.find('end-at').text)
    title = prog.find('title').text
    if not title: continue
    progXMLOut = ET.SubElement(tv, 'programme', {'start': start, 'stop': end, 'channel': futuboxPrefix + str(chanID+1)})
    progXMLTitle = ET.SubElement(progXMLOut, 'title')
    progXMLTitle.text = title.strip()
  chanXML.close()
  
with open(outXMLFile, 'wb') as guideXML:
  guideXML.write(ET.tostring(tv,pretty_print = True,encoding='utf-8',xml_declaration=True))