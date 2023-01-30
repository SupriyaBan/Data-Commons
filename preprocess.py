import pandas as pd
from bs4 import BeautifulSoup
import requests

class MaharashtraExpenseDataLoader:
    def __init__(self, years):
        self.years = years
        self.base_url = "https://prsindia.org/budgets/states/maharashtra-budget-analysis-"
        self.df_list = []
    
    def download(self):
        for year in self.years:
            url = f"{self.base_url}{year}-{year % 100 + 1}"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            table = soup.find_all("table")[1]
            rows = [[td.text.strip() for td in tr.find_all("td")] for tr in table.find("tbody").find_all("tr")[1:]]
            data = pd.DataFrame(rows)
            data["Year"] = year
            self.df_list.append(data)

    def process(self):
        self.final_df = pd.concat(self.df_list)
        self.final_df.columns = ['Item', "Last-to-last year's actual", 'Last year BE', 'Last year RE', '% change (last year BE v/s RE)', 'This year BE','% change (last year RE v/s this year BE)', 'Year']
    
    def save(self, filename):
        self.final_df.to_csv(filename, index=False)

def main():
    """Runs the program."""
    years = [2019, 2020, 2021, 2022]
    loader = MaharashtraExpenseDataLoader(years)
    loader.download()
    loader.process()
    loader.save("maharashtra_expense_data.csv")

if __name__ == '__main__':
    main()
