from django.shortcuts import render
from django.views.generic import View
from game_info.models import Player
import time

def index(request):
    current_players = get_current_players()
    return render(request, 'gmod/gmod.html', {'current_players' : current_players})


def get_current_players():
    try:
        # query_results = ScapePlayer.objects.all().order_by('-duration')
        real_results = []
        query_results = Player.objects.all()
        for player in query_results:
            if "mod" in player.server.title.lower():
                # sec = timedelta(seconds=player.duration)
                # d = datetime(1, 1, 1) + sec
                #
                # # print("DAYS:HOURS:MIN:SEC")
                # player.duration = ("%d:%d:%d:%d" % (d.day - 1, d.hour, d.minute, d.second))
                a = int(player.duration)  # last epoch recorded
                # b = int(time.time())  # current epoch time
                # c = b - a  # returns seconds
                days = int(a / 864000)
                hours = int(a / 3600 % 24)
                minutes = int(a / 60 % 60)
                seconds = int(a % 60)
                player.duration = "{} days, {} hours, {} minutes, {} seconds.".format(days, hours, minutes, seconds)
                real_results.append(player)
    except Player.DoesNotExist:
        real_results = "None"
    return real_results
