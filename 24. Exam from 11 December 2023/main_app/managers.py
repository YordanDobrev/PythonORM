from django.db import models


class TennisPlayerManager(models.Manager):
    def get_tennis_players_by_wins_count(self):
        return self.annotate(
            win_count=models.Count('wins')
        ).order_by(
            "-win_count", "full_name"
        )
