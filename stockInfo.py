from bs4 import BeautifulSoup
import urllib2
import csv
from lxml import etree

allCompaniesCSV = "/home/ahmad/Software/programs/finance/nasdaqCompaniesFullList.csv"
nasdaqSubList = "/home/ahmad/Software/programs/finance/nasdaqSubList.csv"

#This class gets stock info from a market they are listed (Nasdaq, NYSE ...)
class stockInfo:

    #Holds urlib request, a website andother data if required to send to the website(see docs)
    webSite = None#urllib2.Request("https://www.nasdaq.com/screening/company-list.aspx")
    
    
    bs4BeautifulSoup = None
    

    url = "https://www.nasdaq.com/screening/company-list.aspx"
    def __init__(self):
        # self.setUrlLib()
        # self.setBS4()
        return

    def setUrlLib(self):
        url = "https://www.nasdaq.com/screening/company-list.aspx"
        self.webSite = urllib2.Request(url)
        assert isinstance(self.webSite, urllib2.Request)
        return self.webSite

    def getUrlLib(self):
        return self.webSite

    def setBS4(self):
        self.bs4BeautifulSoup = BeautifulSoup(urllib2.urlopen(self.webSite),'lxml')
        assert isinstance(self.bs4BeautifulSoup, BeautifulSoup)
        return

    def getWebHTML(self):
        return self.bs4BeautifulSoup


    #Gets the URLs for each letter of the companies listed on NASDAq
    def getAllCompaniesURLs(self):
        ctgURLS = []
        for ctg in self.bs4BeautifulSoup.find_all('div', attrs={'id':'alpha-list'}):
            for a in ctg.find_all('a'):
                ctgURLS.append(a.get('href'))
        return ctgURLS

    #Takes in parameters, URLs to each companies stock info.
    def getStockInfoForCompanies(self):
        ctgUrls = self.getAllCompaniesURLs()

        for url in ctgUrls:
            self.getCompanyStockInfo(url)
        return
    
    #Company stock info from site
    def getCompanyStockInfo(self, url):
        req = urllib2.Request(url)
        bs4NasdaqCompanyInfo = BeautifulSoup( urllib2.urlopen(req) , 'lxml')

        #col = bs4NasdaqCompanyInfo.find('div', attrs={'id':'left-column-div'}) 
    

        #Go through each column         
        for col in bs4NasdaqCompanyInfo.find_all('div', attrs={'class':'column span-1-of-2'}):
            #Go through each row
            for row in col.find_all('div', attrs={'class':'table-row'}):
                #Go through each cell in the row, and store the values
                for cell in row.find_all('div', attrs={'class':'table-cell'}):
                    
                    _row = tableRow(info.string, )
                    for info in cell.find_all('b'):
                        print(info.string)

                    # for info in cell.find_all('div'):
                    #     print(cell.string)
                    if cell.string is not None:
                        print(cell.string)
                print("End Row")
        #print(col)
        #print(bs4NasdaqCompanyInfo)
        return

#Stores major nasdaq stock information. Parses from rows of data.
class nasdaqStockInfo:

    rows = []

    def __init__(self, rows):
        return

#Stores a row of a table.
class rowManager:

    #Array of rows.
    rows = []
    def __init__(self):
        return

    def insertRow(self, row):
        self.rows.append(row)
        return

    def getRows(self):
        return self.rows
    
class tableRow:
    name = None
    value = None

    def __init__(self, name, value):
        self.name = name
        self.value = value
        return

    def modRow(self, name, value):
        self.name = name
        self.value = value
        return


class cellInfo:
    def __init__(self):
        return

if __name__=="__main__":
    stockinfo = stockInfo()

    stockinfo.getCompanyStockInfo("https://www.nasdaq.com/symbol/amd")

