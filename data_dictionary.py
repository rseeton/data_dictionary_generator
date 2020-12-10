#Pythond script to generate dataloader from delimited file
#Arg parsing:       https://towardsdatascience.com/learn-enough-python-to-be-useful-argparse-e482e1764e05
#Pandas read csv:   https://www.shanelynn.ie/python-pandas-read_csv-load-data-from-csv-files/
#list index & value https://stackoverflow.com/questions/38387529/how-to-iterate-over-pandas-series-generated-from-groupby-size
#create new pandas  https://stackoverflow.com/questions/20638006/convert-list-of-dictionaries-to-a-pandas-dataframe
#series valuecounts https://www.w3resource.com/pandas/series/series-value_counts.php

import pandas as pd
import argparse

from utility_functions import check_boolean_column

distribution_reporting_limit_float=5      #If more than X floats, don't report distribution percentages
distribution_reporting_limit_varchar=10   #If more than X varchars, don't report distribution percentages

data = {} # To accomodate spreadsheets with multiple tabs

parser = argparse.ArgumentParser(description='Generate Datasource Layout from file')
parser.add_argument('filename', type=str, help='Input dir to be parsed')
parser.add_argument('delim',  type=str, nargs='?', default=',', help='File Delimiter [comma|semi-colon|tab|pipe|xls] defaults to comma')
parser.add_argument('header', type=int, nargs='?', default='0', help='Number of header record rows (assumes first row represents column headers')
args = parser.parse_args()
print(args.filename)

if args.delim == '' or args.delim == ',':
    data[args.filename] = pd.read_csv(args.filename, delimiter=',', header=args.header)
elif args.delim == 'tab':
    data[args.filename] = pd.read_csv(args.filename, delimiter='\t', header=args.header)
elif args.delim =='semi-colon':
    data[args.filename] = pd.read_csv(args.filename, delimiter=';', header=args.header)
elif args.delim == 'pipe':
    data[args.filename] = pd.read_csv(args.filename, delimiter='|', header=args.header)
elif args.delim == 'xls':
    excel_data=True
    with pd.ExcelFile(args.filename) as xls:
        print(xls.sheet_names)
        data = {}
        for x in xls.sheet_names:
            data[x] = pd.read_excel(xls, x, index_col=None, na_values=['NA'])
else:
    print ('Delimiter not recognized')
    exit()

#data_layout = {'Column_Name','Data_Type','Allow_Nulls','Count','Count_NaN','Max','Min','Values'}
data_dictionary = pd.DataFrame()


for x in data:
    print('Worksheet Name: {}'.format(x))
    types = data[x].dtypes
    allow_defaults = False
    for column_name, v in types.items():
        value_counts= ''
        field_max=''
        field_min=''
        default_value = ''
        items_list=[]
        allow_nulls = False
        print('\tColumn {}'.format(column_name))
        if v == 'float64':
            data_type='FLOAT'
        elif v == 'int64':
            data_type='INTEGER'
        elif v == 'object':
            data_type='VARCHAR'
        else:
            data_type='VARCHAR'

        unique_list = data[x][column_name].unique()
        if check_boolean_column(unique_list):
            data_type='BOOLEAN'
        elif column_name[-5:].upper() == '_DATE':
            data_type='DATE'
        print('\t\tType: {}'.format(data_type))
        if (((data_type == 'VARCHAR' ) and (len(data[x][column_name].unique()) <= distribution_reporting_limit_varchar )) or ((data_type == 'FLOAT') and (len(data[x][column_name].unique()) <= distribution_reporting_limit_float)) or (data_type == 'BOOLEAN')):
            print('\t\tDistribution:')
            value_counts = data[x][column_name].value_counts(normalize=True, sort=True, ascending=False, bins=None, dropna=False)
            print(type(value_counts.items()))
            for item, amount in value_counts.items():  
                items_list.append(item)
                print('\t\t\t{} ({:.2f}%)'.format(item, amount*100))
        else:
            print('\t\tDistrubution: VARCHAR with count > {} or FLOAT with count > {}, no details shown'.format( distribution_reporting_limit_varchar,  distribution_reporting_limit_float))

        count_total=len(data[x][column_name])
        count_nan  =data[x][column_name].isna().sum()
        if count_nan > 0:
            allow_nulls=True
        print('\t\tCount        :{}'.format(count_total))
        print('\t\tCount (NaN)  :{}'.format(count_nan))
        if data_type not in ('BOOLEAN','VARCHAR'):
            field_max=data[x][column_name].max()
            field_min=data[x][column_name].min()
            print('\t\tMax Value    :{}'.format(field_max))
            print('\t\tMin Value    :{}'.format(field_min))
        #print ('Field_Name'+column_name,'Data_Type'+data_type,'Allow_Nulls'+str(allow_nulls),'Default_Value'+default_value,'Allow_Defaults'+str(allow_defaults) )
        new_row = {'Column_Name':column_name, 'Data_Type':data_type, 'Allow_Nulls':allow_nulls,'Count':count_total,'Count_NaN':count_nan,'Max':field_max,'Min':field_min,'Values':items_list}
        data_dictionary = data_dictionary.append(new_row, ignore_index=True)

    data_dictionary.set_index('Column_Name',inplace=True)
    print(data_dictionary)

    html = data_dictionary.to_html()
    text_file = open("index.html", "w")
    text_file.write(html)
    text_file.close()
