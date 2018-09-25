import json
import difflib
from difflib import SequenceMatcher as sm
from difflib import get_close_matches as gcm
data=json.load(open('/Users/eli/Documents/Data_science/python3/1_application/data.json'))

def translate(w):
    w= w.lower()

    if w in data:
        return data[w]
    elif w.title() in data: #if user entered "texas" this will check for "Texas" as well.
        return data[w.title()]
    elif w.upper() in data: #in case user enters words like USA or NATO
        return data[w.upper()]
    elif len(gcm(w,data.keys(),cutoff=0.80))>0:
             yn=input("You had problably a typo but we found a similar word: %s . Enter Y if yes, or N if no: " %gcm(w,data.keys(),cutoff=0.80)[0])
             if yn=='Y':
                return data[(gcm(w,data.keys(),cutoff=0.80)[0])]
             elif yn=='N':
                return "the word does not exist. Please double check it"
             else:
                return "We did not understand your query"
    else:
        return "the word does not exist. Please double check it"

k=input('Enter the key: ')
output=translate(k)
if type(output)==list:
    for i in output:
        print(i)
else:
    print(output)
