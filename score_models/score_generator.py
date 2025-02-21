import random
import pandas as pd


def random_score_generator(max, min):
    home_score = random.randint(min, max)
    away_score = random.randint(min, max)
    return home_score, away_score


def random_score_list_generator(score_count, max, min):
    scores_list = []
    for i in range(0, score_count):
        score = random_score_generator(max, min)
        scores_list.append(score)
    return scores_list
