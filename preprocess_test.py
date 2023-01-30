import unittest
import pandas as pd
import requests
import os
from bs4 import BeautifulSoup

class MaharashtraExpenseDataLoader:
    # same class code

    class TestMaharashtraExpenseDataLoader(unittest.TestCase):
        def test_download(self):
            years = [2019, 2020, 2021, 2022]
            loader = MaharashtraExpenseDataLoader(years)
            loader.download()
            self.assertEqual(len(loader.df_list), 4)
            for df in loader.df_list:
                self.assertIsInstance(df, pd.DataFrame)

    def test_process(self):
        years = [2019, 2020, 2021, 2022]
        loader = MaharashtraExpenseDataLoader(years)
        loader.download()
        loader.process()
        self.assertIsInstance(loader.final_df, pd.DataFrame)
        self.assertEqual(loader.final_df.columns.tolist(), ['Item', "Last-to-last year's actual", 'Last year BE', 'Last year RE', '% change (last year BE v/s RE)', 'This year BE','% change (last year RE v/s this year BE)', 'Year'])
        self.assertFalse(loader.final_df['Item'].str.contains('%').any())
        for col in ["Last-to-last year's actual", 'Last year BE', 'Last year RE', 'This year BE']:
            self.assertTrue(pd.api.types.is_numeric_dtype(loader.final_df[col].dtype))

    def test_save(self):
        years = [2019, 2020, 2021, 2022]
        loader = MaharashtraExpenseDataLoader(years)
        loader.download()
        loader.process()
        filename = "test_maharashtra_expense_data.csv"
        loader.save(filename)
        self.assertTrue(os.path.exists(filename))
        os.remove(filename)

if __name__ == '__main__':
    unittest.main()
