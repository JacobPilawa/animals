import requests
import pandas as pd
import numpy as np


def get_data(steam_id,name):
    print(f'https://royale.pet/api/player/{str(steam_id)}/stats')
    response = requests.get(f'https://royale.pet/api/player/{steam_id}/stats')
    if response.status_code == 404:
        print('Error 404!')
        df = pd.DataFrame()
    else:
        # get data
        keys=[]
        groups=[]
        values=[]
        for key in response.json()['stats'].keys():
            keys.append(key)
            groups.append(response.json()['stats'][key]['group'])
            values.append(response.json()['stats'][key]['value'])
        # translate to pandas format
        dd = {'keys':keys,'groups':groups,'values':values,'name':name}
        # build df
        df = pd.DataFrame(dd)
        df = df.sort_values(by='groups')
        response.close()

    return df


def load_ids():
    ids = []
    with open('ids.txt','r') as f:
        for l in f:
            ids.append(int(l[:-2]))
    return ids


id_list = load_ids()

dfs = []

for i in id_list:
    dfs.append(get_data(i,str(i)))

merged = pd.concat(dfs)

merged

merged.loc[merged['keys'] == 'KillsSquads']

for unique_key in merged['keys'].unique():
    # get that key
    merged.loc[merged['keys'] == unique_key].hist(column='values')



len(merged['keys'].unique())

















import requests
import time
import numpy
from datetime import datetime

def read_current_ids():
    current_ids = numpy.genfromtxt('ids.txt')
    
    return current_ids

def write_ids():
    
    current_ids = read_current_ids()
    
    # request site
    r = requests.get('https://royale.pet')
    # get text
    text = r.text
	 
    r.close()
    
    # split text, taking 1 to end since we split on /player/
    splits = text.split('/player/')[1:]
    
    # store array 
    ids = []
    for s in splits:
        ids.append(int(s.split('/')[0]))
        
    # remove duplicates from request
    ids_clean = list(set(ids))
    
    # check if ids_clean[i] is already in list
    ids_clean = [i for i in ids_clean if i not in current_ids]
    
    # print if new id's were found
    if ids_clean:
        print(f'{datetime.now().strftime("%H:%M:%S")}: {len(ids_clean)} new IDs scraped!')
        
    # write to file
    with open('ids.txt','a') as f:
        for i in ids_clean:
            f.write(str(i))
            f.write('\n')
            
    f.close()

if __name__=='__main__':
	niter = 30
	n = 0
	while n < niter:
	    n+=1
	    print(f'n/nIter = {str(n)}/{str(niter)}')
	    write_ids()
	    time.sleep(60)
