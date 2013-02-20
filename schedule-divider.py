#!/usr/bin/env python

print 'Content-Type: text/html'
print

import sys
import httplib
import cgi
import urllib
import re
import pdb
from datetime import date

debugmode = 0

def monthlookup(abbr):
	mon = {};
	mon['Jan'] = 1 #guessing
	mon['Feb'] = 2 #guessing
	mon['Mar'] = 3 #guessing
	mon['Apr'] = 4
	mon['May'] = 5
	mon['Jun'] = 6
	mon['Jul'] = 7
	mon['Aug'] = 8
	mon['Sept'] = 9
	mon['Oct'] = 10 #guessing
	mon['Nov'] = 11 #guessing
	mon['Dec'] = 12 #guessing
	return mon[abbr]

if __name__ == '__main__':

	params = {}
	fieldStorage = cgi.FieldStorage()

	if debugmode==0:
		for key in fieldStorage.keys():
			params[key] = fieldStorage[key].value	
		year = params['year']
		divisions = params['divisions']
	else:
		year = 2012
		divisions = 5

	base_url = 'http://espn.go.com/mlb/teams/printSchedule/_/team/phi/season/'
	content_full = urllib.urlopen(base_url + str(year)).read()

	# remove line breaks, because regex fails with line breaks
	content = re.sub(ur"[\r\n]+","", content_full)

	regex = ur"\<tr\>(.+?)\<\/tr\>"
	#tr = re.findall('\<tr\>(.+?)\</tr\>', content)
	tr = re.findall(regex, content)

	dates = []
	times = []
	opps = []
	rownum = 0
	for currow in tr:
		# skip header rows
		if rownum == 0 or rownum == 1:
			rownum += 1
			continue

		m = re.search('size=1>at', currow)
		if m:
			rownum += 1
			continue

		td = re.findall('<td(.+?)</td>', currow)
		cellnum = 0
		for curcell in td:
			# first cell (date) is bold
			if cellnum==0:
				m = re.search('<b>(.+?)</b>', curcell)
				#pdb.set_trace()
				if m:
					m2 = re.search('([A-Za-z]*).?', m.group(1))
					if m2:
						monthnum =  monthlookup(m2.group(1))

					m3 = re.search('([0-9].*)', m.group(1))
					if m3:
						daynum = m3.group(1)
					dates.append(date(int(year), int(monthnum), int(daynum)))

			else:
				m = re.search('<font class=verdana size=1>(.+?)</font>', curcell)
				if m:
					if cellnum==1:
						curopp = m.group(1)
						opps.append(curopp)
					elif cellnum==2:
						curtime = m.group(1)
						times.append(curtime)
			cellnum += 1

		rownum += 1

	print "<html>"
	print "<head></head>"
	print "<body>"
	print "<table border=1>"

	# headings
	print "<tr>"
	for curdivision in range(1, int(divisions)+1):
		print "<th colspan=5>Partner " + str(curdivision) + "</th>"
	print "</tr>"
	
	print "<tr>"
	for curgame in range(len(dates)):
		print "<td>" + dates[curgame].strftime("%b %d") + "</td>"
		print "<td>" + dates[curgame].strftime("%a") + "</td>"
		print "<td>" + times[curgame] + "</td>"
		print "<td>" + opps[curgame] + "</td>"
		print "<td> </td>"
		if (curgame+1) % int(divisions) == 0:
			print "</tr>"
			print "<tr>"

	print "</tr>"
	print "</table>"
	print "</body>"
	print "</html"

	print "<p>"
	print "<hr />"
	print "<p>"
	print "<a href='/scheduler/schedule-divider.html'>Regenerate</a>"
	print "<p>"
	print "<a href='http://funnyphillies.com'>Go to Funny Phillies for some laughs</a>"
