from django.shortcuts import render


def index(request, item=None):
    return render(request, 'menu/index.html', {'item': item})
