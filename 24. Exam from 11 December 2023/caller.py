import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import TennisPlayer, Tournament, Match
from django.db.models import Q, Count


def get_tennis_players(search_name=None, search_country=None):
    if search_name is None and search_country is None:
        return ""

    query_name = Q(full_name__icontains=search_name)
    query_country = Q(country__icontains=search_country)

    query = Q(query_name & query_country)

    if search_name is not None and search_country is not None:
        query = TennisPlayer.objects.filter(query_name & query_country)
    elif search_name is not None:
        query = TennisPlayer.objects.filter(query_name)
    elif search_country is not None:
        query = TennisPlayer.objects.filter(query_country)

    if not query.exists():
        return ""

    result = []

    for player in query.order_by('ranking'):
        result.append(
            f"Tennis Player: {player.full_name}, country: {player.country}, ranking: {player.ranking}"
        )

    return "\n".join(result)


def get_top_tennis_player():
    top_player = TennisPlayer.objects.get_tennis_players_by_wins_count().first()

    if top_player is None:
        return ""

    return f"Top Tennis Player: {top_player.full_name} with {top_player.win_count} wins."


def get_tennis_player_by_matches_count():
    player = TennisPlayer.objects.prefetch_related("matches").annotate(
        matches_count=Count("matches")
    ).filter(
        matches_count__gt=0
    ).order_by(
        "-matches_count",
        "ranking"
    ).first()

    if player is None:
        return ""

    return f"Tennis Player: {player.full_name} with {player.matches_count} matches played."


def get_tournaments_by_surface_type(surface=None):
    if surface is None:
        return ""

    tournaments = Tournament.objects.filter(
        surface_type__icontains=surface
    ).order_by(
        "-start_date"
    )

    if tournaments is None or not tournaments.exists():
        return ""

    result = []

    for t in tournaments:
        result.append(
            f"Tournament: {t.name}, start date: {t.start_date}, matches: {t.tour_matches.count()}"
        )

    return "\n".join(result)


def get_latest_match_info():
    latest_match = Match.objects.prefetch_related("players").order_by("-date_played", "id").first()

    if latest_match is None:
        return ""
    else:
        players = latest_match.players.order_by("full_name").values_list("full_name", flat=True)
        the_winner = latest_match.winner.full_name if latest_match.winner is not None else "TBA"

        return (f'Latest match played on: {latest_match.date_played}, '
                f'tournament: {latest_match.tournament.name}, '
                f'score: {latest_match.score}, '
                f'players: {players[0]} vs {players[1]}, '
                f'winner: {the_winner}, '
                f'summary: {latest_match.summary}')


def get_matches_by_tournament(tournament_name=None):
    if tournament_name is None:
        return "No matches found."

    matches = Match.objects.select_related("tournament", "winner").filter(
        tournament__name__exact=tournament_name
    ).order_by(
        "-date_played",
    )

    if not matches:
        return "No matches found."

    result = []

    for m in matches:
        the_winner = m.winner.full_name if m.winner is not None else "TBA"
        result.append(
            f"Match played on: {m.date_played}, score: {m.score}, winner: {the_winner}"
        )

    return "\n".join(result)


print(get_matches_by_tournament("Tournament 6"))
