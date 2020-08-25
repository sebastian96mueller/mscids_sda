#!/usr/bin/env python3

import http.client as http
import os
import numpy as np
import json
import time


class RequestTeamStatistics:
    """

    """
    def __init__(self, competitor: int):
        self.competitor: int = competitor
        self.json: bool = True  # alternative: False for xml
        self.api_key: str = os.environ['sportradar_api_key']
        self.api_url: str = "api.sportradar.us"

        # Create variables
        self.matches_played = self.team_statistic_per_team("matches_played")
        self.matches_won = self.team_statistic_per_team("matches_won")

    def request_response(self):
        """
        Returns the whole api response.
        :return: dict
        """

        conn = http.HTTPSConnection(self.api_url, timeout=10)
        api_string = \
            f"https://api.sportradar.us/soccer-t3/eu/en/teams/sr:competitor:{self.competitor}" \
            f"/profile.{'json' if self.json else 'xml'}?api_key={self.api_key}"

        try:
            conn.request("GET", api_string)
            response = conn.getresponse()
            data = response.read().decode("utf-8")
            json_data: dict = json.loads(data)
            self.sleeper()
            return json_data
        except http.HTTPException as e:
            print(e)

    def team_statistic_per_team(self, team_statistic):
        """
        Slices the api response and returns wins/number of games.
        The format of the api response is: statistics > seasons > counter > statistics > matches_played

        Possible team_statistic values:
        matches_played
        matches_won
        matches_drawn
        matches_lost
        goals_scored
        goals_conceded
        group_position

        :return: sum_of_team_statistic
        """

        # Slice api response for statistics
        data = self.request_response()["statistics"]
        number_of_seasons: int = len(data["seasons"])

        sum_of_team_statistic: int = 0
        # Loop over each season to sum up matches_played and matches_won
        try:
            for i in range(number_of_seasons):
                current_season: int = data["seasons"][i]["statistics"][team_statistic]
                sum_of_team_statistic += current_season
        except KeyError as e:
            print("Slice error with: ", e)

        return sum_of_team_statistic

    def win_rate(self):
        """
        Calculates the win rate
        """
        return self.matches_won / self.matches_played

    def coin_toss(self):
        """
        Coin toss.
        Returns the std!
        """
        return np.sqrt(0.5 * (0.5 / self.matches_played))

    def real_vs_skill(self):
        """
        Real and skill
        """
        skill = self.win_rate() - self.coin_toss()
        real = skill + self.coin_toss()

        return real, skill

    @staticmethod
    def sleeper():
        time.sleep(1.01)


if __name__ == "__main__":
    team_1 = RequestTeamStatistics(1)
    print(team_1.win_rate())
    print(team_1.coin_toss())
    print(team_1.real_vs_skill())
