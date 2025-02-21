import requests
import json
import log
import pandas as pd


class ActiveFixtures:

    def __init__(self):
        self.data_url = 'https://api.s6.sbgservices.com/round/active'
        self.response_data = None
        self.content = None
        self.fixtures_df = pd.DataFrame()

    def _request_active_games(self):
        try:
            self.request_data = requests.get(self.data_url)
            return self.request_data
        except Exception as err:
            message = f'Failed to get data from source, error {err}'
            log.logit(message)

    def _check_response(self, response_data):
        try:
            if response_data.status_code != 200:
                message = f'Failed to get source data CODE : {response_data.status_code}'
                log.logit(message)
        except Exception as err:
            message = f'Failed to determine response code : {err}'
            log.logit(message)

    def _get_content(self, response_data):
        try:
            content = json.loads(response_data.content)
            return content
        except Exception as err:
            message = f'Failed to get content : {err}'
            log.logit(message)

    def _get_fixtures(self, content):
        fixtures_df = pd.DataFrame()
        for match_data in content['scoreChallenges']:
            row_df = pd.DataFrame(data={'competition': match_data['match']['competitionName'],
                                        'home_team': match_data['match']['homeTeam']['name'],
                                        'away_team': match_data['match']['awayTeam']['name']}, index=[0])
            fixtures_df = pd.concat([fixtures_df, row_df])
        return fixtures_df.reset_index(drop=True)

    def convert_names(self, team_name):
        match team_name:
            case 'Spurs':
                return 'Tottenham'
            case 'Nottm Forest':
                return "Nott'm Forest"
        return team_name

    def get_data(self):
        self.response_data = self._request_active_games()
        self._check_response(self.response_data)
        self.content = self._get_content(self.response_data)
        self.fixtures_df = self._get_fixtures(self.content)
        self.fixtures_df['home_team'] = self.fixtures_df['home_team'].apply(
            self.convert_names)
        self.fixtures_df['away_team'] = self.fixtures_df['away_team'].apply(
            self.convert_names)
        return self.fixtures_df
