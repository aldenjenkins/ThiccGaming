# coding: utf-8
from django.shortcuts import render, get_object_or_404
#from social.apps.django_app.default.models import UserSocialAuth
from social_django.models import UserSocialAuth
from djangobb_forum.models import Profile
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import time
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.urls import reverse
from .forms import BanForm, UnbanForm, CommentForm, RebanForm
from .models import Ban, Comment
from django.contrib.auth.decorators import login_required
from django.db.models import Q


# Base steamid
steamid64ident = 76561197960265728

def getSteam64FromString(steamid):
    steam64id = 76561197960265728  
    id_split = steamid.split(":")
    try:
        steam64id += int(id_split[2]) * 2  # again, not sure why multiplying by 2...
    except (IndexError, ValueError):
        return "Invalid Steam ID"
    if id_split[1] == "1":
        steam64id += 1
    return steam64id

def getSteam3FromString(steamid):
    # X = int(steamid[6:7])
    Y = int(steamid[8:9])
    Z = int(steamid[10:])
    steam3 = "[U:{}:{}]".format( Y, Z*2 + Y )
    return steam3

def commid_to_steamid(commid):
    steamid = []
    steamid.append('STEAM_0:')
    steamidacct = int(commid) - steamid64ident
    steamid.append('0:') if steamidacct % 2 == 0 else steamid.append('1:')
    steamid.append(str(steamidacct // 2))
    return ''.join(steamid)

def commid_to_steam3(commid):
    difference = int(commid) - steamid64ident
    Y = 0 if difference % 2 == 0 else 1
    # return "[U:{}:{}]".format( Y, difference + Y)
    return "[U:{}:{}]".format(Y, difference)


def index(request):
    unban_form = UnbanForm()
    comment_form = CommentForm()
    reban_form = RebanForm()
    query = request.GET.get('q')
    if query:
        bans = Ban.objects.filter(Q(name__icontains=query) | Q(authid=query)).distinct()
    else:
        bans = Ban.objects.all()
    num_bans = bans.count()

    # Show 16 bans per page.
    paginator = Paginator(bans, 16)  
    page = request.GET.get('page')
    try:
        bans = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        bans = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        bans = paginator.page(paginator.num_pages)

    # Get the logged-in user
    if request.user.is_authenticated():
        username = request.user.username
    else:
        username = ""

    for ban in bans:
        parseBan(ban)

    return render(request, 'bans/ban_list.html', {'bans': bans,
                                                  'num_bans': num_bans,
                                                  'username': username,
                                                  'unban_form': unban_form,
                                                  'reban_form': reban_form,
                                                  'comment_form': comment_form})


def search(request):
    unban_form = UnbanForm()
    comment_form = CommentForm()
    reban_form = RebanForm()
    if not 'user' in request.GET or (request.GET.get("user") == ""):
        messages.error(request, _("Please specify a user to search for."))
        return render(request, 'bans/ban_search.html')
    else:
        try:

            bans = Ban.objects.filter(authid=request.GET.get("user"))
            count = bans.count()
            socialAuthUserID = UserSocialAuth.objects.get(uid=request.GET.get("user")).user_id
            # name = Profile.objects.get(user_id=socialAuthUserID).user.username
        except UserSocialAuth.DoesNotExist:

            if count == 0:
                messages.error(request, _("This user does not exist."))
                return render(request, 'bans/ban_search.html')
            messages.warning(request, _("This user's STEAM account is not linked to a Thicc Gaming Account."))

        if count == 0:
            messages.warning(request, _("This user has no previous bans."))
            return render(request, 'bans/ban_search.html')

        else:
            paginator = Paginator(bans, 16)  # Show 12 contacts per page.
            page = request.GET.get('page')

            try:
                bans = paginator.page(page)

            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                bans = paginator.page(1)

            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                bans = paginator.page(paginator.num_pages)

            current_url = request.get_full_path()
            if '&' in current_url:
                current_url = current_url[:current_url.index('&')]

            for ban in bans:
                parseBan(ban)

            return render(request, 'bans/ban_search.html', {'bans': bans,
                                                            'count': count,
                                                            # 'name': name,
                                                            'full_path': current_url,
                                                            'unban_form': unban_form,
                                                            'reban_form': reban_form,
                                                            'comment_form': comment_form,})


def parseBan(ban):

    # Set the ban's respective user
    ban.steam3 = commid_to_steam3(ban.authid)
    ban.steamID = commid_to_steamid(ban.authid)
    try:
        socialAuthUserID = UserSocialAuth.objects.get(uid=ban.authid).user_id
        ban.user = Profile.objects.get(user_id=socialAuthUserID)
    except UserSocialAuth.DoesNotExist:
        ban.nouser = "STEAM account not linked to a Thicc Gaming account."

    # Format the ban's length
    c = ban.length
    days = int(c / 86400)
    hours = int(c / 3600) % 24
    minutes = int(c / 60) % 60
    seconds = int(c % 60)
    if days != 0 and hours != 0 and minutes != 0:
        ban.length = "{} d, {} hr, {} min".format(days, hours, minutes)
    elif days != 0 and hours != 0:
        ban.length = "{} d, {} hr".format(days, hours)
    elif days != 0:
        ban.length = "{} d".format(days)
    elif hours != 0 and minutes != 0:
        ban.length = "{} hr, {} min".format(hours, minutes, seconds)
    elif hours != 0:
        ban.length = "{} hr".format(hours)
    elif minutes != 0 and seconds != 0:
        ban.length = "{} min, {} sec".format(minutes, seconds)
    elif minutes != 0:
        ban.length = "{} min".format(minutes)
    elif seconds != 0:
        ban.length = "{} sec".format(seconds)
    else:
        ban.length = "Permanent"

    # Get the datetime of the created and end epochs
    ban.createdDate = time.strftime('%m-%d-%Y %H:%M:%S', time.localtime(ban.created))
    ban.endDate = time.strftime('%m-%d-%Y %H:%M:%S', time.localtime(ban.ends))

    # Get the total bans for the user
    ban.totalBans = Ban.objects.filter(authid=ban.authid).count()

    # Set ban's respective admin forum-profile.
    if ban.aid != 0:
        try:
            ban.adminUser = Profile.objects.get(user_id=ban.aid)
        except Profile.DoesNotExist:
            ban.adminUser = ""

    # Set ban's expired state.
    if ban.ends < int(time.time()) and ban.length != "Permanent":
         ban.expired = True
    else:
         ban.expired = False

    # Set ban's game.
    if ban.sid    == 1:
         ban.game  = "Left 4 THICC 2"
         ban.topic = 16

    elif ban.sid  == 2:
         ban.game  = "THICC | ZS"
         ban.topic = 16

    elif ban.sid  == 3:
         ban.game  = "thicc Scape"
         ban.topic = 16

    elif ban.sid  == 4:
         ban.game  = "THICC | JB"
         ban.topic = 16

    elif ban.sid  == 5:
         ban.game  = "THICC WoW"
         ban.topic = 16

    else:
         ban.game  = "Thicc Scape"
         ban.topic = 16

    if ban.RemoveType == 'U':
        ban.unbanned = True
        ban.RemovedOn = time.strftime('%m-%d-%Y %H:%M:%S', time.localtime(ban.RemovedOn))
        try:
            ban.unbannedAdmin = Profile.objects.get(user_id=ban.RemovedBy)
        except Profile.DoesNotExist:
            ban.unbannedAdmin = "Admin has since been removed."

    # Get this ban's comments
    ban.commentss = Comment.objects.filter(ban=ban)
    if ban.commentss.count() == 0:
        ban.commentss = False


@login_required
def unban(request, bid):
    ban = get_object_or_404(Ban, bid=bid)
    if request.method == 'POST':
        if not request.user.is_superuser:
            # messages.error(request, "You are not a staff member. This action has been logged.")
            return HttpResponseRedirect(reverse('bans:index'))
        else:
            # ban = get_object_or_404(Ban, bid=bid)
            form = UnbanForm(request.POST, instance=ban)
            if form.is_valid():
                ban = form.save(commit=False)
                ban.RemovedBy = request.user.id
                ban.RemovedOn = time.time()
                ban.RemoveType = 'U'
                ban.save()

    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('bans:index'))


@login_required
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@login_required
def ban(request):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == "POST":
            form = BanForm(request.POST)
            if form.is_valid():
                ban = form.save(commit=False)
                ban.aid = request.user.id
                ban.created = int(time.time())
                ban.ends = ban.created + ban.length
                ban.adminIp = get_client_ip(request)
                ban.RemovedBy = 0
                ban.RemovedOn = 0
                ban.type = 0
                ban.save()
                messages.success(request, "Ban successfully added.")
            else:
                return render(request, 'bans/ban_details.html', {'form': form})

        else:
            form = BanForm()
            return render(request, 'bans/ban_details.html', {'form':form})

    else:
        form = BanForm()
        return render(request, 'bans/ban_details.html', {'form':form})

    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('bans:index'))


@login_required
def comment(request, bid):
    if request.user.is_authenticated and request.user.is_staff:
        ban = get_object_or_404(Ban, bid=bid)
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.ban = ban
                comment.commenter= request.user
                comment.created = int(time.time())
                comment.ip = get_client_ip(request)
                comment.save()
                messages.success(request, "Comment successfully added.")

    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('bans:index'))


@login_required
def reban(request, bid):
    if request.user.is_authenticated and request.user.is_staff:
        ban = get_object_or_404(Ban, bid=bid)
        if request.method == 'POST':
            form = RebanForm(request.POST)
            if form.is_valid():
                newban = form.save(commit=False)
                newban.name = ban.name
                newban.authid = ban.authid
                newban.uid = 0
                newban.created = int(time.time())
                newban.ends = newban.created + newban.length
                newban.aid = request.user.id
                newban.adminip = get_client_ip(request)
                newban.sid = ban.sid
                newban.type = 0
                newban.RemovedBy = 0
                newban.RemovedOn = 0
                if ban.ip:
                    newban.ip = ban.ip
                newban.save()

    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('bans:index'))
