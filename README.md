# stockInfo
Allows users to rank volatility of stocks listed on nasdaq simply copy and paste the stocks you want to follow from nasdaqCompaniesFullList.csv to the nasdaqSubList.csv file which is used to generate the csv files present in /data directory these files contains in order from highest to lowest volatity of stocks based on today, and this year.

You can copy paste the whole nasdaq nasdaqCompaniesFullList.csv to the nasdaqSubList.csv but it will take a while.

NOTE:
Example output in /data.
When copying make sure that the format remains the same (csv don't remove any commas and paste on a new line). Don't delete the first line of the csv's.
I have used python2.7.12, there are some modules you need to pip install csv, BeautifulSoup etc..

Requirments:
apt-get install python-bs4
pip install lxml