from active_fixtures import ActiveFixtures
from data_processing.competition_data import CompetitionData
import score_predictor
import numpy as np


def main():

    # Get active fixtures
    active_fixtures = ActiveFixtures()
    fixtures_df = active_fixtures.get_data()

    # Get all competitions data required
    competition_data = CompetitionData()
    competition_data.get_competition_data(
        np.unique(fixtures_df['competition']))

    # Make score predictions

    result_df = score_predictor.predict_scores(
        'tensorflow', fixtures_df, competition_data)

    print(result_df)


if __name__ == "__main__":
    main()

0.7469758064516129
