import numpy as np
from data_processing.historical_data import HistoricaLeague


class CompetitionData:

    def __init__(self):
        self.champions_league = None
        self.league_data = None
        self.facup_data = None
        self.eflcup_data = None
        self.confrence_data = None
        self.europa_data = None

    def get_competition_data(self, competition_list: list):
        unique_list = np.unique(competition_list)
        for competition in unique_list:
            if competition == 'Champions League':
                continue
            elif competition == 'FA Cup':
                continue
            elif competition == 'EFL Cup':
                continue
            elif competition == 'Europa League':
                continue
            elif competition == 'Confrence League':
                continue
            else:
                historical_league = HistoricaLeague()
                self.league_data = historical_league.get_data()
