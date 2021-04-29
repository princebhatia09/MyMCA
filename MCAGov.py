'script2.py'

import requests
from bs4 import BeautifulSoup
import threading,_thread
import pandas as pd
import concurrent.futures
#data csv se chunks mai looad karo, thread banao 10 aur usmai run karo yeh code 
session = requests.session()

chunksize = 10**3 # data of 10K
filename= "AN CIN List.csv"
dataFile = "AN CIN LIST_DATA.csv"
##
NEWS = open(dataFile,"a")

errorFile = open("./ErrorGivenByWebsite.csv","a")

def read_DataChunks(filename):

    final_list = []

    data  = pd.read_csv(filename, chunksize=chunksize,header=None,sep="_")
##    data1 = pd.DataFrame(data)
    
    for chunk in data:
        lst = []
        lst.append(chunk.to_string(index=False).split("\n"))
        final_list.append(lst[0])
    return final_list

def requst(lst,timeout):
    print(lst)
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate", "Cache-Control": "no-cache","Pragma": "no-cache"}
    url = "http://www.mca.gov.in/mcafoportal/checkFilingStatus.do"
    
    for loo in lst:
        loo1 = loo.strip()
        if loo1.startswith("CIN") or loo1=="0":
            continue
        
        http_proxy  = "http://5.252.161.48:8080"
        https_proxy = "https://111.125.138.147:59805"
        ftp_proxy   = "https://51.83.193.208:80"

        proxyDict = { 
              "http"  : http_proxy, 
              "https" : https_proxy}

        payload = {
            "counter":"",
            "companyName":"",
            "companyID":loo1,
            "displayCaptcha":"false",
            "submitBtn":"Submit",
            "method":"checkFillingStatus"
        }
        print(payload)
        

        #proxy to be used  when required
        try:
            response = session.post(url,headers=headers,timeout = timeout ,data=payload, allow_redirects=False)

            soup = BeautifulSoup(response.text,"html.parser")
            classPagnitaion = soup.find("p",{"class":"paginationresults"})
            print(classPagnitaion)
            findid = soup.find(id="results")

            if(findid==None):
                f.write(loo.strip()+","+"-"+","+"-"+","+"-"+","+"\n")
                continue

            findTr = findid.find_all("tr")
            findTd = [x.find_all("td") for x in findTr]
            for data in findTd:
                if len(data)==0:
                    continue
                CIN = loo.strip()
                SRN = data[0].text.strip()
                EFORM = data[1].text.strip()
                EVENT_DATA = data[2].text.strip()
                print(CIN,SRN,EFORM,EVENT_DATA)
                NEWS.write(CIN+","+SRN+","+EFORM+","+EVENT_DATA+"\n")
                NEWS.flush()

        except Exception as e:
            import traceback
            traceback.print_exc()
            errorFile.write(loo1.strip()+"\n")
            errorFile.flush()

            
if __name__=="__main__":
    import sys
    
##    read_file = pd.read_excel ('./AN CIN List.xls')
##    read_file.to_csv(filename,index=None,header=True)

    f = open("abc.txt","r")

    filename = f.read()
    # sys.stdin
    # filename = sys.stdin.read()
    # print("this is filename"+sys.stdin)
    
    max_data = len(read_DataChunks(filename))
   
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_data) as executor:
       
        future_to_url = {executor.submit(requst, lst, 60): lst for lst in read_DataChunks(filename)}
   
        for future in concurrent.futures.as_completed(future_to_url):            
            print(future.result())

        executor.shutdown()
    
