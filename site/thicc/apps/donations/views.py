from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sites.shortcuts import get_current_site
from django.utils import timezone
from .forms import DonateForm
from .models import PremiumDonation
from django.db.models import F, Sum, OuterRef
from django.db.models.expressions import RawSQL
import uuid
from paypal.standard.ipn.models import PayPalIPN


class DonateView(FormView):
    template_name = 'donations/donate.html'
    form_class = DonateForm
    success_url = '/thanks/'
    choices = [(x[0], str(x[1]) + " days") for x in settings.DONATION_AMOUNTS]

    def get_context_data(self, **kwargs):
        context = super(DonateView, self).get_context_data(**kwargs)
        context['steam'] = self._get_steam()
        if self.request.user.is_authenticated():
            try:
                all_donations = PremiumDonation.objects.filter(user=self.request.user)
                if len(all_donations):
                    context['donation'] = all_donations.reverse()[0]
                else:
                    context['donation'] = PremiumDonation.objects.get(user=self.request.user)
                if context['donation'].end_time > timezone.now():
                    context['donation_ended'] = False
                else:
                    context['donation_ended'] = True
            except PremiumDonation.DoesNotExist:
                context['donation'] = None
        else:
            context['donation'] = None
        #payments = PayPalIPN.objects.filter( 
        #            custom=OuterRef('user__social_auth__uid'),
        #            payment_status='Completed',
        #        ).aggregate(total=Sum('mc_gross'))['total']
        context['recent_donations'] = PremiumDonation \
            .objects.all() \
            .order_by('-updated_at')[:10] \
            .select_related('user__forum_profile') \
            .prefetch_related('user__social_auth') 

        for don in context['recent_donations']:

            don.total_donated = PayPalIPN \
                .objects.filter(
                    custom=don.user.social_auth.first().uid
                ).aggregate(Sum('mc_gross'))['mc_gross__sum'] 

            # Don't need to try catch here because these donations must have a paypal
            # object created during its creation.
            don.latest_donation = PayPalIPN \
                .objects.filter(custom=don.user.social_auth.first().uid)[0].mc_gross

        return context


    def _get_steam(self):
        if self.request.user.is_authenticated():
            try:
                u = self.request.user.social_auth.filter(provider="steam").get()
                return u.uid
            except ObjectDoesNotExist:
                pass

        return None

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """

        steam = self._get_steam()

        domain = get_current_site(self.request).domain

        initial = {
            "business": settings.PAYPAL_RECEIVER_EMAIL,
            "item_name": "Donation",
            "invoice": str(steam)+":"+uuid.uuid4().hex,
            "notify_url": "http://" + "localhost:8000/" + reverse('paypal-ipn'),
            "return_url": "http://localhost:8000/donate",
            "cancel_return": "http://localhost:8000/donate",
            "custom": steam,  # Custom command to correlate to some function later (optional)
        }


        return initial
