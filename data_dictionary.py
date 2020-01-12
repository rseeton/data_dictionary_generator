#Pythond script to generate dataloader from delimited file
#Arg parsing:       https://towardsdatascience.com/learn-enough-python-to-be-useful-argparse-e482e1764e05
#Pandas read csv:   https://www.shanelynn.ie/python-pandas-read_csv-load-data-from-csv-files/
#list index & value https://stackoverflow.com/questions/38387529/how-to-iterate-over-pandas-series-generated-from-groupby-size
#create new pandas  https://stackoverflow.com/questions/20638006/convert-list-of-dictionaries-to-a-pandas-dataframe


import pandas as pd
import argparse

data = {} # To accomodate spreadsheets with multiple tabs

parser = argparse.ArgumentParser(description='Generate Datasource Layout from file')
parser.add_argument('filename', type=str, help='Input dir to be parsed')
parser.add_argument('delim',  type=str, nargs='?', default=',', help="File Delimiter [comma|semi-colon|tab|pipe|xls] defaults to comma")
parser.add_argument('header', type=int, nargs='?', default='0', help="Number of header record rows (assumes first row represents column headers")
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
    print ("Delimiter not recognized")
    exit()

# Preview the first 5 lines of the loaded data
for x in data:
    print(x)

    types = data[x].dtypes
    default_value = ''
    allow_defaults = False
    a = []
    for column_name, v in types.items():
        allow_nulls = True
        print('\tColumn', column_name)
        if v == 'float64':
            data_type='FLOAT'
        elif v == 'int64':
            data_type='INTEGER'
        elif v == 'object':
            data_type='VARCHAR'
        else:
            data_type='VARCHAR'

        #If indicator column then default to 'N'
        if column_name[-4:].upper() == '_IND' or column_name[-4:].upper() == 'FLAG' :
            allow_defaults = True
            default_value  = 'N'
        elif column_name[-5:].upper() == '_DATE':
            data_type='DATE'
        #
        #print ('Field_Name'+column_name,'Data_Type'+data_type,'Allow_Nulls'+str(allow_nulls),'Default_Value'+default_value,'Allow_Defaults'+str(allow_defaults) )
        a.append({'Field_Name' : column_name,'Data_Type' : data_type,'Allow_Nulls' : allow_nulls,'Default_Value' : default_value,'Allow_Defaults' : allow_defaults}) 
        print('\t\tType:', data_type)
        if len(data[x][column_name].unique()) <= 10:
            print('\t\tUnique: ',data[x][column_name].unique())
        if data_type !=  "VARCHAR":
            print('\t\tMax :', data[x][column_name].max())
            print('\t\tMin :', data[x][column_name].min())


    layout_data = pd.DataFrame(a)

    #Create layout dataframe
    layout_header = pd.DataFrame(columns=['Field_Name','Description','Title','Data_Type','Size','Allow_Nulls','Allow_Defaults','Default_Value','Synthetic_Content','Lookup_Source','Value_Field','Description_Field','Parent_Fields','Display_Format','Show_Subtotal','Aggregated_Function','Is_Count_Field_For','Is_Hidden','Field_Type','Default_Instance_Key_Value_Formula','Generate_Auto_Unique_Id','Data_Permission_Entity','Join_Source_For_Permissions','Join_Field_For_Permissions'])

    layout=pd.concat([layout_header, layout_data], axis=1, sort=False)
    #print(layout)
