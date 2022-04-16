import requests
import time
import numpy
from datetime import datetime

def read_current_ids():
    current_ids = numpy.genfromtxt('data/ids.txt')
    
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
    with open('data/ids.txt','a') as f:
        for i in ids_clean:
            f.write(str(i))
            f.write('\n')
            
    f.close()

if __name__=='__main__':
	niter = 100
	n = 0
	while n < niter:
	    n+=1
	    print(f'n/nIter = {str(n)}/{str(niter)}')
	    write_ids()
	    time.sleep(30)
