from django.shortcuts import render
from game_info.models import Player


def index(request):
    current_players = get_current_players()
    return render(request, 'l4d2/l4d2.html', {'current_players': current_players})


def banner(request):
    return render(request, 'l4d2/banner.html')


def get_current_players():
    try:
        # query_results = ScapePlayer.objects.all().order_by('-duration')
        real_results = []
        query_results = Player.objects.all()
        for player in query_results:
            if "4" in player.server.title:
                # sec = timedelta(seconds=player.duration)
                # d = datetime(1, 1, 1) + sec
                #
                # # print("DAYS:HOURS:MIN:SEC")
                # player.duration = ("%d:%d:%d:%d" % (d.day - 1, d.hour, d.minute, d.second))
                a = int(player.duration)  # last epoch recorded
                # b = int(time.time())  # current epoch time
                # c = b - a  # returns seconds
                days = int(a / 86400)
                hours = int(a / 3600 % 24)
                minutes = int(a / 60 % 60)
                seconds = int(a % 60)
                player.duration = "{} days, {} hours, {} minutes, {} seconds.".format(days, hours, minutes, seconds)
                real_results.append(player)
    except Player.DoesNotExist:
        real_results = "None"
    return real_results
