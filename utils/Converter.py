import json

#  ResponseToQuerry function which has a parameter (Which takes Model response as a input) and returns querry and error.
def ResponseToQuerry(response):
  try:
    ConvertedJson = json.loads(response)
    sqlquery,error = ConvertedJson['query'],ConvertedJson['error']
    query,error = sqlquery,error  
    return query,error
  except:
    return 0,response
  