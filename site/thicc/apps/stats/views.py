from django.shortcuts import render
from django.views.generic.list import ListView
from djangobb_forum

def StatsListView(ListView):
    
    model = Profile

    def get_queryset():
        return Profile.objects.all().order_by('stat_count')
