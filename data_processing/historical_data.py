from datetime import datetime, timedelta
import log
import pandas as pd


class HistoricaLeague:

    def __init__(self, ):
        self.partial_url = 'https://www.football-data.co.uk/mmz4281/'
        self.league_code_list = ['E0', 'E1', 'E2', 'E3']
        self.historical_years = 3
        self.df = pd.DataFrame()
        self.url_list = None
        self.year_list = ModuleNotFoundError

    def _generate_prem_years(self):
        year_list = []
        for i in range(0, self.historical_years):
            latest_year = (datetime.today() -
                           timedelta(days=i*365)).strftime("%Y")[2:4]

            previous_year = str(int(latest_year)-1)
            year_string = previous_year + latest_year
            year_list.append(year_string)
        return year_list

    def _generate_url_list(self, year_list):
        url_list = []
        for years in year_list:
            for code in self.league_code_list:
                url = self.partial_url + years + '/' + code
                url_list.append(url)
        return url_list

    def _request_individual_data_file(self, url):
        try:
            data = pd.read_csv(url)
            return data
        except Exception as err:
            message = f'failed to get prem data : error : {err}'
            log.logit(message)

    def _request_all_data(self, url_list):
        for url in url_list:
            ind_df = self._request_individual_data_file(url)
            self.df = pd.concat([self.df, ind_df])
        return self.df

    def get_data(self):
        self.year_list = self._generate_prem_years()
        self.url_list = self._generate_url_list(self.year_list)
        self.df = self._request_all_data(self.url_list)
        self.df['Date'] = pd.to_datetime(self.df['Date'], format='%d/%m/%Y')
        return self.df
