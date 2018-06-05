from __future__ import division
from bs4 import BeautifulSoup
import urllib2
import csv, copy, os
from lxml import etree
import numpy as np

currDir = os.path.dirname(os.path.realpath(__file__))

allCompaniesCSV = currDir + "/nasdaqCompaniesFullList.csv"
nasdaqSubList = currDir + "/nasdaqSubList.csv"
testUrl = currDir + "/testlist.csv"
#This class gets stock info from a market they are listed (Nasdaq, NYSE ...)
class stockInfo:

    #Holds urlib request, a website andother data if required to send to the website(see docs)
    webSite = None#urllib2.Request("https://www.nasdaq.com/screening/company-list.aspx")
    urlIndex = 8
    
    bs4BeautifulSoup = None
    #Array of stocks.
    stocks = []

    #url = "https://www.nasdaq.com/screening/company-list.aspx"
    def __init__(self):
        # self.setUrlLib()
        # self.setBS4()
        self.storeStockInfo(allCompaniesCSV)
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
    
    #Gets stock info from a csv file which contains, ["Symbol","Name","LastSale","MarketCap","IPOyear","Sector","industry","Summary Quote"]
    def storeStockInfo(self,csvURL):
        
        with open(csvURL) as f:
            next(f)
            reader = csv.reader(f, dialect='excel', delimiter=',')
            i = 0
            for row in reader:
                print( row )
                print("Num row: %i" %i)
                _stock = self.getCompanyStockInfo(row[self.urlIndex], row[1], row[0])
                #If the stock info is found.
                if _stock is not None:
                    self.stocks.append(_stock)
                #del _stock
                # print("Stock Info################")
                # _stock.printInfo()
                
                i = i+1
            
            #self.printStocks()
        return

    #Company stock info from site
    def getCompanyStockInfo(self, url, stockName, stockSymbol):
        try:
            req = urllib2.Request(url)
            bs4NasdaqCompanyInfo = BeautifulSoup( urllib2.urlopen(req) , 'lxml')
        except:
            print("%s is an invalid URL for stock Name %s." %(url, stockName))
            return None
        #col = bs4NasdaqCompanyInfo.find('div', attrs={'id':'left-column-div'}) 
        
        _stock = stock(stockName,stockSymbol,url)

        #Go through each column         
        for col in bs4NasdaqCompanyInfo.find_all('div', attrs={'class':'column span-1-of-2'}):
            #Go through each row
            for row in col.find_all('div', attrs={'class':'table-row'}):
                #Ensure this is called out here to ensure the row is in scope, other wise name memory issues.
                _row = tableRow()

                #Go through each cell in the row, and store the values in this case there is a property name, and its integer value.
                for cell in row.find_all('div', attrs={'class':'table-cell'}):
                    
                    #Initialize a row to modify later.
                    
                    #This is the bold text/text portion.
                    names = cell.find_all('b')
                    
                    for name in names:
                        _name = name.string
                        #print(_name)
                        if _name is not None:
                            #Strip with no args removes white spaces.
                            _row.setName(_name.encode('utf-8').strip())
                    
                    if cell.string is not None:
                        val = cell.string
                        # try:
                        #     _row.modRow(None, float(cell.string))
                        # except ValueError:
                        #     print "Not a float"                        
                        #print(cell.string)
                        _row.setValue( val.encode('utf-8').strip())
                        #print("%s value is %s" %(stockName,val.encode('utf-8').strip() ))
                #Store each row of info
                _stock.addInfo(_row)
                
        #_stock.printInfo()
        # prop = "Beta"
        # val = _stock.getProperty(prop)
        # if val is not None:
        #     print("Found %s with value: %f." %(prop, float(val)))
        # highlow = _stock.getyearHighLow()
        # todayHighLow=_stock.gettodayHighLow()
        # print("Year High: %f, Year Low: %f." %(highlow[0], highlow[1]))
        # print("Today High: %f, Today Low: %f." %(todayHighLow[0], todayHighLow[1]))
        
        return _stock

    def getMostVoalatile(self):
        diffstoday = []
        diffsyear = []
        _stocks = []
        for _stock in self.stocks:
            assert isinstance(_stock, stock)
            highlow = _stock.getyearHighLow()
            todayHighLow=_stock.gettodayHighLow()
            todayHigh = None
            todayLow = None
            yearHigh = None
            yearLow = None
            try:
                todayHigh = todayHighLow[0]
                todayLow = todayHighLow[1]
                yearHigh = highlow[0]
                yearLow = highlow[1]
            except:
                print("No high or low data for %s." %(_stock.stockName))
                continue
            yeardiff = (yearHigh - yearLow) / ( (yearHigh + yearLow) / 2 ) * 100
            todaydiff =  (todayHigh - todayLow) / ((todayHigh + todayLow) / 2 ) * 100

            print("Today high: %f, Today Low: %f, Volatility: %f for company %s." %(todayHigh, todayLow, todaydiff, _stock.stockUrl))
            print("Year high: %f, Year Low: %f, Volatility: %f for company %s." %(yearHigh, yearLow, yeardiff,_stock.stockUrl))
            #print("%f year dif for %s company." %(yeardiff, _stock.stockName))
            try:
                assert isinstance(yeardiff, float)
                assert isinstance(todaydiff, float)
                
                diffstoday.append(todaydiff)
                diffsyear.append(yeardiff)
                _stocks.append(_stock)
            except:
                #To maintain the order.
                diffstoday.append(0)
                diffsyear.append(0)                
                print("%s stock does not hav a high low info." %_stock.stockName)

        
        npdiffstoday = np.array(diffstoday)
        npdiffsyear = np.array(diffsyear)

        self.storeYearAndDayVolatilityInfo(_stocks,npdiffstoday, npdiffsyear)
        # index = np.argsort(npdiffstoday)[:len(diffstoday)]
        # # print(diffstoday)
        # for i in index:
        #     # print(index)
        #     _stock = _stocks[i]
        #     assert isinstance(_stock, stock)
        #     print("%s Stock has %f volatility."%(_stock.stockName, npdiffstoday[i]))
        return

    def storeYearAndDayVolatilityInfo(self, _stocks,npdiffstoday,npdiffsyear):
        
        with open(currDir + "/data/yearInfo.csv",'w+') as yearFile:
            with open(currDir + "/data/todayInfo.csv", 'w+') as todayFile:
                todayCSV = csv.writer(todayFile, dialect='excel', delimiter=',')
                yearCSV = csv.writer(yearFile, dialect='excel', delimiter=',')
                row = ['Company Name', "Stock Volatility today as a percent of company average stock today", "StockURL"]
                todayCSV.writerow(row)
                row = ['Company Name', "Stock Volatility yearly as a percent of company average stock this year", "StockURL"]
                yearCSV.writerow(row)

                index = (np.argsort(npdiffstoday)[:len(npdiffstoday)])[::-1]
                # print(diffstoday)
                for i in index:
                    
                    # print(index)
                    _stock = _stocks[i]
                    assert isinstance(_stock, stock)
                    #print("%s Stock has %f volatility."%(_stock.stockName, npdiffstoday[i]))                
                    row = [_stock.stockName, str(npdiffstoday[i]), _stock.stockUrl]
                    todayCSV.writerow(row)

                index = (np.argsort(npdiffsyear)[:len(npdiffsyear)])[::-1]
                for i in index:
                    
                    # print(index)
                    _stock = _stocks[i]
                    assert isinstance(_stock, stock)
                    #print("%s Stock has %f volatility."%(_stock.stockName, npdiffstoday[i]))                
                    row = [_stock.stockName, str(npdiffsyear[i]), _stock.stockUrl]
                    yearCSV.writerow(row)
                                
        yearFile.close()
        todayFile.close()
        return

    def printStocks(self):
        for _stock in self.stocks:
            assert isinstance(_stock, stock)
            print("################################################################")
            _stock.printInfo()

#Stores major nasdaq stock information. Parses from rows of data.
class nasdaqStockInfo:

    stocks = []

    def __init__(self):
        return

#Stores a row of a table.
class rowManager:

    #Array of rows.
    rows = None
    def __init__(self):
        #del self.rows[:]
        self.rows = []
        return

    def insertRow(self, row):
        self.rows.append(row)
        return

    def getRows(self):
        return self.rows
    
    def getLength(self):
        return len(self.rows)
    
class tableRow:
    name = None
    value = None

    def __init__(self, name=None, value=None):
        self.setName(name)
        self.setValue(value)
        return

    def modRow(self, name, value):
        self.setName(name)
        self.setValue(value)
        return

    def setName(self, name):
        if name is not None:
            self.name = name
        #print("Name is None")

    def setValue(self, value):
        self.value = value

    def getName(self):
        return self.name
    
    def getValue(self):
        return self.value

class stock:
    #Stock Nasdaq URL
    stockUrl = None
    #Stock Name
    stockName=None
    stockSymbol=None
    #Info Manager, stores array of rows, which in turns contains information of the stock in [property, value] format.
    _rowManager=None
    
    def __init__(self, stockName, stockSymbol, stockURL):
        self.stockName = stockName
        self.stockUrl = stockURL
        self.stockSymbol = stockSymbol
        self._rowManager=rowManager()

        #print(self._rowManager.getLength())
        return

    def addInfo(self, info):
        assert isinstance(self._rowManager, rowManager)
        assert isinstance(info, tableRow)
        self._rowManager.insertRow(info)
        #print(info.getValue())
        return
    
    def getProperty(self, _property):
        for row in self._rowManager.getRows():
            assert isinstance(row, tableRow)
            if row.getName() == _property:
                return row.getValue()
        
        return None

    def getyearHighLow(self):
        prop = self.getProperty("52 Week High / Low")
        if prop is None:
            return None

        props = prop.split("/")
        data = []
        highLow = []
        for _prop in props:
            props = _prop.split("$")
            for _prop in props:
                #Have to decode utf-8 otherwise html extracted from the beutiful soup is off.
                _prop = _prop.decode('utf-8')
                props = _prop.split(' ')
                for _prop in props:                    
                    if _prop is not ' ':
                        data.append(_prop.lstrip())

        try:
            highLow.append(float(data[1]))
            highLow.append(float(data[3]))
        except:
            print("Could not find a high or low for today, company: %s." %(self.stockName))
            return None
        return highLow

    def gettodayHighLow(self):
        prop = self.getProperty("Today's High / Low")
        if prop is None:
            return None
            
        props = prop.split("/")
        data = []
        highLow = []
        for _prop in props:
            props = _prop.split("$")
            for _prop in props:
                #Have to decode utf-8 otherwise html extracted from the beutiful soup is off.
                _prop = _prop.decode('utf-8')
                props = _prop.split(' ')
                for _prop in props:                    
                    if _prop is not ' ':
                        
                        data.append(_prop.lstrip())
        try:
            highLow.append(float(data[1]))
            highLow.append(float(data[3]))
        except:
            print("Could not find a high or low for today, company: %s." %(self.stockName))
        return highLow

    def printInfo(self):
        for row in self._rowManager.getRows():
            assert isinstance(row, tableRow)
            print("%s: %s" %(row.getName(), row.getValue()))
        return

if __name__=="__main__":
    stockinfo = stockInfo()

    #stockinfo.getCompanyStockInfo("https://www.nasdaq.com/symbol/amd", "AMD","AMD")
    stocks = []
    stockinfo.getMostVoalatile()

        
        
        
        
