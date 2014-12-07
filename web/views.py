from django.shortcuts import render


def home(request):
    if request.method == "GET":
        pass

    return render(request, 'index.html', {})