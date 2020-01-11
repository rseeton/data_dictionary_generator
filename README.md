# data_dictionary_generator
Python script to read a data file and generate data details

A _Data Dictionary_ is a "centralized repository of information about data such as meaning, relationships to other data, origin, usage, and format" (IBM Dictionary of Computing).

Automated inspection of a random file cannot reliably generalize about the set of files that may follow, nor can it definitively determine relationships to other data.  However, based on the data in the file, we can determine some absolute attributes of the data provide and make some educated guess as well.

This package is intended to read in a data file (delimited text, spreadsheets, etc) and then generate a report on the file specifications.

The report will include:

Column Name
Data type (Integer, Float, Text, Date*, Time*, Boolean*)


* Boolean and Date formats are best-guesses based on a combination of field name and data contents

Boolean
- Field names ending in __IND__ or __FLAG__ (or other capitalization there-of)
- Data contents for 1/0 T/F Y/N Yes/No (or combinations with NULL)
- Data Type returned will include note on field contents

Date
- Field names ending in __DATE__ (or other capitalization there-of)
- Will attempt to match to 'common' formats:
YYYY-MM-DD
MM-DD-YYYY
M-D-Y
DD-MMM-YYYY
(Will try different separators / or - or nothing)
Excel number date (Integer portion starts at 1900-01-01 = 1)

Time
- Field names ending in __TIME__ (or other capitalization there-of)
HH-MM-SS (Will try different separators / or - or : or nothing)
- Excel number time (QQQ - not sure how this is represented)


Data Dictionary: a how to and best practices (Medium Article - possible paywall)
https://medium.com/@leapingllamas/data-dictionary-a-how-to-and-best-practices-a09a685dcd61
