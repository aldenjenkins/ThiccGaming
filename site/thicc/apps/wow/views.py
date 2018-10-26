from django.shortcuts import render


def index(request):
    return render(request, 'wow/wow.html')
