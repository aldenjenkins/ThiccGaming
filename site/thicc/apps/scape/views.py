# from django.shortcuts import render
from django.views.generic.edit import FormView
from django.core.exceptions import ObjectDoesNotExist
from .forms import ScapeForm
from .models import ScapePlayer
import time
# from datetime import datetime, timedelta
# from django.http import HttpResponse


class ScapeView(FormView):
    template_name = 'scape/scape.html'
    form_class = ScapeForm
    # choices = [(x[0], str(x[1]) + " days") for x in settings.DONATION_AMOUNTS]

    def get_context_data(self, **kwargs):
        context = super(ScapeView, self).get_context_data(**kwargs)
        context['steam'] = self._get_steam()
        context['current_players'] = self._get_current_players()
        # if self.request.user.is_authenticated():
        #     try:
        #         all_donations = PremiumDonation.objects.filter(user=self.request.user)
        #         if len(all_donations):
        #             context['donation'] = all_donations.reverse()[0]
        #         else:
        #             context['donation'] = PremiumDonation.objects.get(user=self.request.user)
        #         if context['donation'].end_time > timezone.now():
        #             context['donation_ended'] = False
        #         else:
        #             context['donation_ended'] = True
        #     except PremiumDonation.DoesNotExist:
        #         context['donation'] = None
        # else:
        #     context['donation'] = None
        return context

    def _get_steam(self):
        if self.request.user.is_authenticated():
            try:
                u = self.request.user.social_auth.filter(provider="steam").get()
                return u.uid
            except ObjectDoesNotExist:
                pass

        return None

    # def get_initial(self):
    #     """
    #     Returns the initial data to use for forms on this view.
    #     """
    #
    #     steam = self._get_steam()
    #
    #     domain = get_current_site(self.request).domain
    #
    #     initial = {
    #         "business": settings.PAYPAL_RECEIVER_EMAIL,
    #         "item_name": "Donation",
    #         "invoice": str(steam)+":"+uuid.uuid4().hex,
    #         "notify_url": "http://" + "localhost:8000/" + reverse('paypal-ipn'),
    #         "return_url": "http://localhost:8000/donate",
    #         "cancel_return": "http://localhost:8000/donate",
    #         "custom": steam,  # Custom command to correlate to some function later (optional)
    #     }
    #
    #
    #     return initial

    def _get_current_players(self):
        try:
            # query_results = ScapePlayer.objects.all().order_by('-duration')
            query_results = ScapePlayer.objects.all()
            for player in query_results:
                # sec = timedelta(seconds=player.duration)
                # d = datetime(1, 1, 1) + sec
                #
                # # print("DAYS:HOURS:MIN:SEC")
                # player.duration = ("%d:%d:%d:%d" % (d.day - 1, d.hour, d.minute, d.second))
                a = player.duration  # last epoch recorded
                b = int(time.time())  # current epoch time
                c = b - a  # returns seconds
                days = c / 86400
                hours = c / 3600 % 24
                minutes = c / 60 % 60
                seconds = c % 60
                player.duration = "{} days, {} hours, {} minutes, {} seconds.".format(days, hours, minutes, seconds)
        except ScapePlayer.DoesNotExist:
            query_results = "None"
        return query_results