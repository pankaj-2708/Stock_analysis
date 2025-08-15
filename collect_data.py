from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import pandas as pd
import requests
from fake_useragent import UserAgent
import time


# collecting html
def collecthtml(url):
    response=requests.get(url)
    with open("data.html",'w',encoding='utf-8') as f:
        f.write(response.text)


# all companies list
with open("com.txt",'r') as f:
    response=f.read()
allComp=response.split(',\\n')
# print(len(allComp))

def getCompName():
    with open("data.html",'r') as f:
        html=f.read()
    soup=BeautifulSoup(html,'html.parser')
    return soup.find(class_="margin-0 show-from-tablet-landscape").text.replace(" Ltd","")[:16]

# getting key metrics
def getKeymetrics(company_name='BANKINDIA'):
    
    collecthtml(f"https://www.screener.in/company/{company_name}/consolidated/")

    with open("data.html",'r',encoding='utf-8') as f:
        html=f.read()
    
    soup=BeautifulSoup(html,'html.parser')
    metrics_name=soup.find_all(class_="name")
    metrics_value=soup.find_all(class_="nowrap value")
    metrics_name=[i.text.replace("\n","").strip() for i in metrics_name]
    metrics_value=[" ".join(i.text.replace("\n","").replace("â‚¹","").strip().split()) for i in metrics_value]
    
    collecthtml(f"https://www.alphaspread.com/security/nse/{company_name.lower()}/dcf-valuation/base-case")
    
    with open("data.html",'r',encoding='utf-8') as f:
        html=f.read()
        
    soup=BeautifulSoup(html,'html.parser')
    metrics_name.append("Intrinsic value (DCF method)")
    metrics_name.append("Status ")
    
    dcf=soup.find(class_="dcf-value-color")
    status=soup.find(class_="opacity-90 space-no-wrap")
    metrics_value.append(dcf.text.replace("\n","").replace("\t","").replace(" ","").replace(",",""))
    metrics_value.append(status.text.replace("\n","").replace("\t","").replace(" ","").replace(",",""))
    
    metrics_name.append("P/B ratio")
    try:
        metrics_value.append(round(float(metrics_value[1].replace(",",""))/float(metrics_value[4].replace(",","")),2))
    except Exception as E:
        print(E,company_name)
        metrics_value.append(-1)
    metrics_value=['None' if type(i)==str and len(i)==0 else i for i in metrics_value]
    return [metrics_name,metrics_value] 


#pros and cons
def getpts(company_name):
    collecthtml(f"https://www.screener.in/company/{company_name}/")
    
    with open("data.html",'r',encoding='utf-8') as f:
        html=f.read()
    soup=BeautifulSoup(html,'html.parser')
    pros=[i.text for i in soup.find(class_="pros").find("ul").find_all("li")]
    cons=[i.text for i in soup.find(class_="cons").find("ul").find_all("li")]
    return pros,cons



# cagr related data
def getCAGR(company_name):
    with open("data.html",'r',encoding='utf-8') as f:
        html=f.read()
    soup=BeautifulSoup(html,'html.parser')
    
    tables=soup.find_all(class_="ranges-table")
    colum_names=[]
    
    values=[[],[],[],[]]
    index=[i.text.replace("\n","").split(":")[0] for i in tables[0].find_all("tr")[1:]]
    for i in range(len(tables)):
        colum_names.append(tables[i].find('th').text)
        val=[i.text.replace("\n","").split(":")[1] for i in tables[i].find_all("tr")[1:]]
        values[i]=val
        
    df=pd.DataFrame(values,columns=colum_names,index=index)
    return df
    
    
    
# peers data
def peers_table(company='BANKINDIA'):
    chrome_options = Options()
    chrome_options.add_argument("--headless")        # Run in headless mode
    chrome_options.add_argument("--disable-gpu")     # Optional: better compatibility
    chrome_options.add_argument("--no-sandbox") 
    # Set up browser (Chrome here — make sure you have chromedriver installed)
    driver = webdriver.Chrome(options=chrome_options)

    # Go to page
    driver.get(f"https://www.screener.in/company/{company}/consolidated/")
    html = driver.page_source
    with open("data.html",'w',encoding='utf-8') as f:
            f.write(html)
    # Quit browser
    driver.quit()

    with open("data.html",'r') as f:
            html=f.read()
    
    soup=BeautifulSoup(html,'html.parser')
    peers_table=soup.find('table',{'class':'data-table'})
    th=peers_table.find_all('th')
    quaters=[" ".join(i.text.strip().replace("\n",'').strip().split()) for i in th][1:]
    ind_columns=[]
    td=peers_table.find_all('td')
    columns=[i.text.strip().replace("\n",'').strip().replace("\xa0+",'').replace("%",'') for i in td]
    i=0
    while i<len(columns):
        ind_columns.append(columns[i+1:i+11])
        i+=11

    arr=[]
    for rows in ind_columns:
        clm=rows[1:10]
        for i in range(len(clm)):
            clm[i]=float(clm[i].replace(",","")) if clm[i].replace(",","").replace(".","").replace("-","").isdigit() else None 
        arr.append([rows[0]]+clm)

    peers=pd.DataFrame(arr,columns=quaters)
    return peers




# collecting consolidated data
def collectDataConsolidated(company_name='BANKINDIA'):
    with open("data.html",'r') as f:
        html=f.read()
    soup=BeautifulSoup(html,'html.parser')

    # dfs
    quarterly_results=None
    Profit_Loss=None
    Balance_sheet=None
    Cash_flows=None
    ratios=None
    share_holding_pattern=None
    dfs=[quarterly_results,Profit_Loss,Balance_sheet,Cash_flows,ratios,share_holding_pattern]
    tables=soup.find_all('table',{'class':'data-table'})


    for k in range(1,len(dfs)+1):
         #quaterly results
        th=tables[k].find_all('th')
        quaters=[i.text.strip().replace("\n",'').strip() for i in th][1:]
        ind_columns=[]
        td=tables[k].find_all('td')
        columns=[i.text.strip().replace("\n",'').strip().replace("\xa0+",'').replace("%",'') for i in td]
        i=0
        while i<len(columns):
            ind_columns.append(columns[i:i+len(quaters)+1])
            i+=len(quaters)+1
        dict={}
        for rows in ind_columns:
            clm=rows[1:len(quaters)+1]
            for i in range(len(clm)):
                clm[i]=float(clm[i].replace(",","")) if clm[i].replace(",","").replace(".","").replace("-","").isdigit() else None 
            dict[rows[0]]=clm
        dfs[k-1]=pd.DataFrame(dict,index=quaters)
    return dfs


# collecting standalone data
def collectDataStandalone(company_name='BANKINDIA'):
    
    with open("data.html",'r') as f:
        html=f.read()
    soup=BeautifulSoup(html,'html.parser')

    # dfs
    quarterly_results=None
    Profit_Loss=None
    Balance_sheet=None
    Cash_flows=None
    ratios=None
    share_holding_pattern=None
    dfs=[quarterly_results,Profit_Loss,Balance_sheet,Cash_flows,ratios,share_holding_pattern]
    tables=soup.find_all('table',{'class':'data-table'})

    rlm=[14,13,13,13,13,13]

    for k in range(1,len(dfs)+1):
         #quaterly results
        th=tables[k].find_all('th')
        quaters=[i.text.strip().replace("\n",'').strip() for i in th][1:]
        ind_columns=[]
        td=tables[k].find_all('td')
        columns=[i.text.strip().replace("\n",'').strip().replace("\xa0+",'').replace("%",'') for i in td]
        i=0
        while i<len(columns):
            ind_columns.append(columns[i:i+len(quaters)+1])
            i+=len(quaters)+1
        dict={}
        for rows in ind_columns:
            clm=rows[1:len(quaters)+1]
            for i in range(len(clm)):
                clm[i]=float(clm[i].replace(",","")) if clm[i].replace(",","").replace(".","").replace("-","").isdigit() else None 
            dict[rows[0]]=clm
        dfs[k-1]=pd.DataFrame(dict,index=quaters)
    
    return dfs