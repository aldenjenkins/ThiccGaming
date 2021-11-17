from django.shortcuts import render
from django.views.generic.list import ListView
from djangobb_forum.models import Profile
from .models import UserStats
from django.db.models import Q
    

class StatsListView(ListView):
    paginate_by = 30
    context_object_name = "stats_list"

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['total_objects'] = UserStats.objects.count()
        return context_data

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return UserStats.objects.filter(Q(last_used_username__icontains=query) | Q(steam64=query)).distinct() \
                    .select_related('linked_steam',
                    'linked_steam__user',
                    'linked_steam__user__forum_profile')
        else:
            return UserStats.objects.all() \
                    .select_related('linked_steam',
                        'linked_steam__user',
                        'linked_steam__user__forum_profile')
