def isNaN(num):
    #Non-numpy nan check...
    #https://stackoverflow.com/questions/944700/how-can-i-check-for-nan-values
    return num != num


def str2bool(v):
  #https://intellipaat.com/community/2592/converting-from-a-string-to-boolean-in-python

  if str(v).upper() in ("yes", "true", "t", "1", "y"):
    return (True)     
  elif str(v).upper() in ("yes", "true", "t", "1", "y"):
    return(False)
  else:
    return()


def check_boolean_column(v):

  #Booleans can contain pairs of values and possibly blanks/nulls (NaNs)
  #Cycle list, remove Nan and convert to upper (simplifies comparison)
  
  boolean_pairs_list= [['1.0','0.0'],['1','0'],[True,False],['Y','N'],['T','F'],['YES','NO'],['TRUE','FALSE'],['MALE','FEMALE']]
  if len(v) <= 3:
    v = [str(x).upper() for x in v if not isNaN(x)]
    v.sort(reverse=True)
    for pair in boolean_pairs_list:
      #print('BOOLEAN check: {} vs {} '.format(v,pair))
      if v == pair:
        return(True)
  return(False)

