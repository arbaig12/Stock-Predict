from bs4 import BeautifulSoup
import time
import requests
import random


class Stock_Info:
    def __init__(self):
        # Instance variables to store stock data
        self.dates = []
        self.open_price = []
        self.high = []
        self.low = []
        self.close = []
        self.adj_close = []
        self.volume = []
        self.div_date = []
        self.dividend = []
        self.current_price = 0

        # Initialize stock data
        self.get_stock_data()

    def random_header(self): #return a random header to reduce bot strike
        headers = [
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Referer': 'https://www.google.com/'
            },
            {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Referer': 'https://www.bing.com/'
            },
            {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
                'Accept-Language': 'en-GB,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Referer': 'https://www.yahoo.com/'
            },
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
                'Accept-Language': 'en-US,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Referer': 'https://www.duckduckgo.com/'
            }
        ]
        return random.choice(headers)

    def sort(self, element, number):     #organize numbers into correct listings
        if number == 0:
            self.dates.append(element)
        elif number == 2:
            self.open_price.append(element)
        elif number == 4:
            self.high.append(element)
        elif number == 6:
            self.low.append(element)
        elif number == 8:
            self.close.append(element)
        elif number == 10:
            self.adj_close.append(element)
        else:
            self.volume.append(int(element.replace(',', '')))

    def iterate(self, table):      #iterate over tr containing all elements
        count = 0
        for date in table:
            count1 = 0
            for elem in date:
                if count > 0 and count1 % 2 == 0:
                    sample = elem.text
                    if len(date) < 7:            # filtering out inputs where the dividends occurs in table
                        if count1 == 0:
                            self.div_date.append(sample)
                        elif count1 == 2:
                            self.dividend.append(sample)
                    else:
                        self.sort(sample, count1)
                count1 += 1
            count += 1

    def init_scrape(self):     #begin query from today to 5 years ago
        stock_name = input("Enter stock name: ").upper()
        current_time = int(time.time())
        five_ago = current_time - ((24 * 60 * 60) * (4 * 365 + 366))  # Five years ago
        url = f'https://finance.yahoo.com/quote/{stock_name}/history/?period1={five_ago}&period2={current_time}'
        return requests.get(url, headers=self.random_header())

    def get_stock_data(self):     # main function of file which filters the page html elements
        holder = []
        flag = False
        try:
            response = self.init_scrape()
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')
                test = soup.find_all('main')
                sections = test[0].find_all('tr')
                maybe = test[0].find_all('span')
                no_results = test[0].find_all('h2')   # Check to see if the input stock was valid
                for nr in no_results:
                    empty = nr.get_text().split()[0]
                    if empty == "Symbols":
                        print("Invalid stock name or page not found. Please Try Again")
                        self.get_stock_data()
                        return
                for may in maybe:
                    try:
                        num = float(may.get_text().strip())
                        holder.append(num)
                    except ValueError:
                        pass
                if not flag:
                    self.current_price = holder[0]
                    self.iterate(sections)
                else:
                    print("Invalid stock name or page not found. Please Try Again")
                    self.get_stock_data()
            else:
                raise ValueError("Invalid stock name or page not found. Please Try Again")
        except (requests.exceptions.RequestException, ValueError) as e:
            print(e)
            self.get_stock_data()



stock_info = Stock_Info()

