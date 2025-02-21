import pandas as pd


class Team:

    def __init__(self, name, team_type, home_scores, away_scores, latest_scores, game_date):
        self.name = name
        self.team_type = team_type
        self.home_scores = home_scores
        self.away_scores = away_scores
        self.latest_scores = latest_scores
        self.game_date = game_date


def collapse_to_model_list(team_object):
    output_list = (team_object.latest_scores +
                   team_object.home_scores +
                   team_object.away_scores)

    return [output_list]


class LeagueGame:

    def __init__(self,
                 home_team,
                 away_team,
                 game_date,
                 historical_game_data,
                 historical_score_count=5):
        self.home_team = home_team
        self.away_team = away_team
        self.historical_game_data = historical_game_data
        self.game_date = game_date
        self.historical_score_count = historical_score_count

    def _get_raw_team_data(self, team, game_type='home_fixture'):
        if game_type == 'home_fixture':
            team_column = 'HomeTeam'
        else:
            team_column = 'AwayTeam'

        if game_type == 'home_fixture':
            score_column = 'FTHG'
        else:
            score_column = 'FTAG'
        team_data = self.historical_game_data[self.historical_game_data[team_column] == team]
        team_data = team_data[team_data['Date'] < self.game_date]
        team_data = team_data[['Date', score_column]]
        team_data = team_data.rename(columns={score_column: 'score'})
        team_data['game_type'] = game_type
        return team_data

    def _generate_team_fixture_data(self, team):
        home_fixtures = self._get_raw_team_data(team)
        away_fixtures = self._get_raw_team_data(team, game_type='away_fixture')
        fixtures = pd.concat([home_fixtures, away_fixtures])
        fixtures = fixtures.sort_values(['Date'], ascending=False)
        return fixtures

    def _generate_team_data(self, team_name):
        fixture_data = self._generate_team_fixture_data(team_name)
        # latest scores
        latest_scores = list(fixture_data.head(
            self.historical_score_count)['score'])

        # away scores
        away_scores = list(fixture_data[fixture_data['game_type'] == 'away_fixture'].head(
            self.historical_score_count)['score'])

        # home scores
        home_scores = list(fixture_data[fixture_data['game_type'] == 'home_fixture'].head(
            self.historical_score_count)['score'])

        return latest_scores, away_scores, home_scores

    def generate_game_data(self):
        # home team
        score_tuple = self._generate_team_data(self.home_team)

        self.home_team_data = Team(self.home_team,
                                   team_type='Home',
                                   home_scores=score_tuple[2],
                                   away_scores=score_tuple[1],
                                   latest_scores=score_tuple[0],
                                   game_date=self.game_date)

        # away team
        score_tuple = self._generate_team_data(self.away_team)
        self.away_team_data = Team(self.away_team,
                                   team_type='Away',
                                   home_scores=score_tuple[2],
                                   away_scores=score_tuple[1],
                                   latest_scores=score_tuple[0],
                                   game_date=self.game_date)
