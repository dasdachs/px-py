"""
This is an update from https://github.com/zejn/pcaxis
"""
"""
usage:

from pcaxis import axis_parser

axis_parser.parseString('...')
axis_parser.parseFile(open(fn))


or run with python axis.py <dataset>
"""

import codecs
import pyparsing
from pyparsing import Keyword, Word, alphas, nums, alphanums, Regex, Literal, OneOrMore, Suppress, Group, Dict, Optional, White

NEWLINE = Literal("\n") | Literal("\r\n")
EQUAL = Suppress(Literal('='))
QUOTE = Suppress(Literal('"'))
SEMI = Suppress(Literal(";"))
BPAREN = Suppress(Literal("("))
EPAREN = Suppress(Literal(")"))
COMMA = Suppress(Literal(","))
YES = Literal("YES")
NO = Literal("NO")
INTEGER = Word(nums+'-', nums)
INTEGER.setParseAction(lambda x: int(x[0]))
FLOAT = Regex('-?[\d\.]+')
FLOAT.setParseAction(lambda x: float(x[0]))
NONQUOTE = Regex('[^"]+')
QSTRING = QUOTE + NONQUOTE + QUOTE # quoted string
MLQSTRING = OneOrMore(QSTRING | NEWLINE) # multiline quoted string
DATE = QUOTE + Word(nums + ': ', exact=14) + QUOTE

BQ = EQUAL + QUOTE
EQ = QUOTE + SEMI
BPQ = BPAREN + QUOTE
EPQ = QUOTE + EPAREN

tlist = Keyword("TLIST") + Group(BPAREN + Word("AHQMW1") + ((COMMA + QSTRING + Literal("-") + QSTRING + EPAREN) | (EPAREN + OneOrMore(QSTRING | COMMA))))

axis_version = Keyword("AXIS-VERSION") + BQ + Word(nums) + EQ
charset = Keyword("CHARSET") + BQ + Literal("ANSI") + EQ
codes = Keyword("CODES") + BPAREN + QSTRING + EPAREN + EQUAL + Group(OneOrMore(QSTRING | NEWLINE | COMMA)) + SEMI
contact = Keyword("CONTACT") + Optional(BPAREN + QSTRING + EPAREN) + EQUAL + MLQSTRING + SEMI
contents = Keyword("CONTENTS") + EQUAL + QSTRING + SEMI
copyright = Keyword("COPYRIGHT") + EQUAL + (YES | NO) + SEMI
creation_date = Keyword("CREATION-DATE") + EQUAL + DATE + SEMI

DATA_VALUES = Regex('[^;]+')
#DATA_VALUES.setParseAction(parseData)
data = Keyword("DATA") + EQUAL + Optional(Suppress(White())) + DATA_VALUES + SEMI

database = Keyword("DATABASE") + EQUAL + QSTRING + SEMI
datanotesum = Keyword("DATANOTESUM") + EQUAL + QSTRING + SEMI
datasymbol1 = Keyword("DATASYMBOL1") + EQUAL + QSTRING + SEMI
datasymbol2 = Keyword("DATASYMBOL2") + EQUAL + QSTRING + SEMI
datasymbol3 = Keyword("DATASYMBOL3") + EQUAL + QSTRING + SEMI
datasymbol4 = Keyword("DATASYMBOL4") + EQUAL + QSTRING + SEMI
datasymbol5 = Keyword("DATASYMBOL5") + EQUAL + QSTRING + SEMI
datasymbol6 = Keyword("DATASYMBOL6") + EQUAL + QSTRING + SEMI
datasymbolsum = Keyword("DATASYMBOLSUM") + EQUAL + QSTRING + SEMI
datasymbolnil = Keyword("DATASYMBOLNIL") + EQUAL + QSTRING + SEMI
decimals = Keyword("DECIMALS") + EQUAL + INTEGER + SEMI
description = Keyword("DESCRIPTION") + EQUAL + QSTRING + SEMI
descriptiondefault = Keyword("DESCRIPTIONDEFAULT") + EQUAL + YES + SEMI
directory_path = Keyword("DIRECTORY-PATH") + EQUAL + QSTRING + SEMI
domain = Keyword("DOMAIN") + BPAREN + QSTRING + EPAREN + EQUAL + QSTRING + SEMI
elimination = Keyword("ELIMINATION") + BPAREN + QSTRING + EPAREN + EQUAL + (QSTRING | YES) + SEMI
euro = Keyword("EURO") + EQUAL + QSTRING + SEMI
heading = Keyword("HEADING") + EQUAL + OneOrMore(QSTRING | COMMA) + SEMI
infofile = Keyword("INFOFILE") + EQUAL + QSTRING + SEMI
language = Keyword("LANGUAGE") + BQ + Word(alphas, exact=2) + EQ
last_updated = Keyword("LAST-UPDATED") + EQUAL + DATE + SEMI
matrix = Keyword("MATRIX") + EQUAL + QSTRING + SEMI
note = Keyword("NOTE") + EQUAL + MLQSTRING + SEMI
notex = Keyword("NOTEX") + Optional(BPAREN + QSTRING + EPAREN) + EQUAL + MLQSTRING + SEMI
precision = Keyword("PRECISION") + BPAREN + QSTRING + COMMA + QSTRING + EPAREN + EQUAL + INTEGER + SEMI
showdecimals = Keyword("SHOWDECIMALS") + EQUAL + INTEGER + SEMI
source = Keyword("SOURCE") + EQUAL + QSTRING + SEMI
stub = Keyword("STUB") + EQUAL + OneOrMore(QSTRING | COMMA) + SEMI
subject_area = Keyword("SUBJECT-AREA") + EQUAL + QSTRING + SEMI
subject_code = Keyword("SUBJECT-CODE") + EQUAL + QSTRING + SEMI
timeval = Keyword("TIMEVAL") + BPAREN + QSTRING + EPAREN + EQUAL + tlist + SEMI
title = Keyword("TITLE") + EQUAL + QSTRING + SEMI
units = Keyword("UNITS") + EQUAL + QSTRING + SEMI
valuenotex = Keyword("VALUENOTEX") + BPAREN + QSTRING + COMMA + QSTRING + EPAREN + EQUAL + MLQSTRING + SEMI
values = Keyword("VALUES") + BPAREN + QSTRING + EPAREN + EQUAL + Group(OneOrMore(QSTRING | NEWLINE | COMMA)) + SEMI
variable_type = Keyword("VARIABLE-TYPE") + BPAREN + QSTRING + EPAREN + EQUAL + QSTRING + SEMI



pcaxis_parser = OneOrMore(
	Group(axis_version("AXIS-VERSION")) | \
	Group(charset("CHARSET")) | \
	Group(codes("CODES")) | \
	Group(contact("CONTACT")) | \
	Group(contents("CONTENTS")) | \
	Group(copyright("COPYRIGHT")) | \
	Group(creation_date("CREATION-DATE")) | \
	Group(data("DATA")) | \
	Group(database("DATABASE")) | \
	Group(datanotesum("DATANOTESUM")) | \
	Group(datasymbol1("DATASYMBOL1")) | \
	Group(datasymbol2("DATASYMBOL2")) | \
	Group(datasymbol3("DATASYMBOL3")) | \
	Group(datasymbol4("DATASYMBOL4")) | \
	Group(datasymbol5("DATASYMBOL5")) | \
	Group(datasymbol6("DATASYMBOL6")) | \
	Group(datasymbolsum("DATASYMBOLSUM")) | \
	Group(datasymbolnil("DATASYMBOLNIL")) | \
	Group(decimals("DECIMALS")) | \
	Group(description("DESCRIPTION")) | \
	Group(descriptiondefault("DESCRIPTIONDEFAULT")) | \
	Group(directory_path("DIRECTORY-PATH")) | \
	Group(domain("DOMAIN")) | \
	Group(elimination("ELIMINATION")) | \
	Group(euro("EURO")) | \
	Group(heading("HEADING")) | \
	Group(infofile("INFOFILE")) | \
	Group(language("LANGUAGE")) | \
	Group(last_updated("LAST-UPDATED")) | \
	Group(matrix("MATRIX")) | \
	Group(note("NOTE")) | \
	Group(notex("NOTEX")) | \
	Group(precision("PRECISION")) | \
	Group(showdecimals("SHOWDECIMALS")) | \
	Group(source("SOURCE")) | \
	Group(stub("STUB")) | \
	Group(subject_area("SUBJECT-AREA")) | \
	Group(subject_code("SUBJECT-CODE")) | \
	Group(timeval("TIMEVAL")) | \
	Group(title("TITLE")) | \
	Group(units("UNITS")) | \
	Group(valuenotex("VALUENOTEX")) | \
	Group(values("VALUES")) | \
	Group(variable_type("VARIABLE-TYPE")) | \
	NEWLINE
	)


def parseDataLine(line, struct_len):
	dline2 = []
	
	total = 1
	for i in struct_len:
		total = total * i
	assert total == len(line), 'Line length does not match?'
	
	struct2 = list(reversed(struct_len))
	
	def divide(elements, substruct):
		
		if len(substruct) == 1:
			yield elements
		else:
			n = float(len(elements)) / substruct[0]
			assert int(n) == n, 'Should be integer'
			n = int(n)
			for i in xrange(substruct[0]):
				yield elements[i*n:(i+1)*n]
		
	
	return list(divide(line, struct2))

def parseData(d, structure):
	lines = []
	cur = 0
	total = len(d)
	
	#print structure
	struct_len = [len(i) for i in structure]
	struct_len.reverse()
	
	data_array = []
	dline = []
	while cur < total:
		#print cur
		if d[cur] == '"':
			next = cur + 1
			while next < total and d[next] != '"':
				next += 1
			dline.append(d[cur+1:next])
			cur = next + 1 + 1
		elif d[cur] == " ":
			#pass
			cur += 1
		elif d[cur] in '0123456789.-':
			next = cur
			while next < total and d[next] in '0123456789.-':
				next += 1
			dline.append(float(d[cur:next]))
			cur = next + 1
			#print dline[-1]
		elif d[cur] in '\r\n':
			while d[cur] in '\r\n':
				cur += 1
			#print dline
			# parse dline
			
			dline2 = parseDataLine(dline, struct_len)
			data_array.append(dline2)
			dline = []
	return data_array

def parsePX(data, encoding=None):
    parseresults = pcaxis_parser.parseString(data)

    if encoding is None:
        # detect encoding
        for item in parseresults:
            if item[0] == 'CHARSET':
                encoding = item[1]
                try:
                    c = codecs.lookup(encoding)
                except LookupError:
                    raise ValueError('Invalid encoding, please set charset manually by passing encoding parameter to parsePX', encoding)

    parsed_data = {}
    for item in parseresults:
        key = item[0]
        if key in ['LANGUAGE', 'CHARSET', 'AXIS-VERSION', 'CREATION-DATE',
            'SUBJECT-AREA', 'SUBJECT-CODE', 'DESCRIPTION', 'LAST-UPDATED',
            'SOURCE', 'CONTACT', 'MATRIX', 'TITLE', 'CONTENTS', 'UNITS',
            'STUB', 'DATASYMBOL1', 'DATASYMBOL2', 'DATASYMBOL3', 'DATASYMBOL4',
            'COPYRIGHT', 'DATABASE']:
            assert len(item) == 2
            parsed_data[key] = item[1].decode(encoding)
        elif key in ['DECIMALS']:
            parsed_data[key] = item[1]
        elif key in ['HEADING']:
            parsed_data[key] = item[1:]
        elif key in ['CODES']:
            codes = parsed_data.setdefault(key, {})
            codes[item[1]] = tuple(item[2])
            #print item
        elif key in ['VALUES']:
            codes = parsed_data.setdefault(key, {})
            codes[item[1]] = [i.decode(encoding) for i in tuple(item[2])]
            #print item
        elif key in ['NOTEX', 'NOTE']:
            parsed_data[key] = ''.join(item[1:])
        elif key == 'DATA':
            
            structure = []
            for k in parsed_data['HEADING']:
                nexts = parsed_data['CODES'].get(k, parsed_data['VALUES'].get(k))
                structure.append(nexts)
            pdata = parseData(item[1], structure)
            #print pdata
            parsed_data[key] = pdata
        else:
            print(item)
            print(item[0], len(item))
        
    
    return parsed_data
