from score_models.score_generator import random_score_list_generator
from data_processing.game_data import LeagueGame, collapse_to_model_list
from datetime import datetime
import pandas as pd
import joblib
import log
import numpy as np


MAX = 4
MIN = 0
TODAY = datetime.now().strftime('%Y-%m-%d')


def random_prediction(fixtures_df, max, min):

    random_scores = random_score_list_generator(len(fixtures_df), max, min)
    random_score_df = pd.DataFrame(random_scores, columns=['random_home_score',
                                                           'random_away_score'])
    full_data_df = pd.concat([fixtures_df, random_score_df], axis=1)
    return full_data_df


def generate_raw_data(competition, competition_data):
    if competition == 'Champions League':
        return competition_data.champions_league
    elif competition == 'FA Cup':
        return competition_data.facup_data
    elif competition == 'EFL Cup':
        return competition_data.eflcup_data
    elif competition == 'Europa League':
        return competition_data.europa_data
    elif competition == 'Confrence League':
        return competition_data.confrence_data
    else:
        return competition_data.league_data


def generate_model_data(competition, raw_data, home_team, away_team):
    if competition == 'Champions League':
        return pd.DataFrame()
    elif competition == 'FA Cup':
        return pd.DataFrame()
    elif competition == 'Europa League':
        return pd.DataFrame()
    elif competition == 'Confrence League':
        return pd.DataFrame()
    elif competition == 'EFL Cup':
        return pd.DataFrame()
    else:
        league_game = LeagueGame(home_team, away_team, TODAY, raw_data)
        league_game.generate_game_data()
        return league_game


def predictor(model, features, model_type):
    try:
        if model_type == 'tensorflow':
            features = pd.DataFrame(features).transpose()
            prediction = model.predict(features).flatten()
        else:
            prediction = model.predict(features)

        if prediction[0] <= 0.0:
            pred = 0.0
        else:
            pred = prediction[0]
        score = int(round(pred, 0))
    except Exception as err:
        message = f'failed to predict score : {err}'
        log.logit(message)
        score = -1
    return score


def prediction(fixtures_df, competition_data, model_type):
    output_df = pd.DataFrame()
    fixtures_list = list(fixtures_df.itertuples(index=False))
    for fixture in fixtures_list:
        raw_data = generate_raw_data(fixture[0], competition_data)
        if len(raw_data) > 0:
            model_data = generate_model_data(
                fixture[0], raw_data, fixture[1], fixture[2])
            home_features = collapse_to_model_list(model_data.home_team_data)
            away_features = collapse_to_model_list(model_data.away_team_data)
            partial_directory = './score_models/'

            if fixture[0] == 'Champions League':
                comp_directory = partial_directory + 'cl/'
                continue
            elif fixture[0] == 'Europa League':
                comp_directory = partial_directory + 'eu/'
                continue
            elif fixture[0] == 'Confrence League':
                comp_directory = partial_directory + 'conf/'
                continue
            elif fixture[0] == 'FA Cup':
                comp_directory = partial_directory + 'fa/'
                continue
            elif fixture[0] == 'EFL Cup':
                comp_directory = partial_directory + 'cup/'
                continue
            else:
                comp_directory = partial_directory + 'league/'

            home_model_path = comp_directory + model_type + '/home_model.joblib'
            away_model_path = comp_directory + model_type + '/away_model.joblib'

            home_model = joblib.load(home_model_path)
            away_model = joblib.load(away_model_path)

            home_score = predictor(home_model, home_features, model_type)
            away_score = predictor(away_model, away_features, model_type)

        else:
            home_score = -2
            away_score = -2

        output_dic = {'competition': fixture[0],
                      'home_team': fixture[1],
                      'away_team': fixture[2],
                      'home_score': home_score,
                      'away_score': away_score
                      }
        partial_df = pd.DataFrame(output_dic, index=[0])
        output_df = pd.concat([output_df, partial_df])
    return output_df


def predict_scores(prediction_type, fixtures_df, competition_data):

    if prediction_type == 'random':
        output_df = random_prediction(fixtures_df, MAX, MIN)
    else:
        output_df = prediction(fixtures_df, competition_data, prediction_type)
    return output_df
