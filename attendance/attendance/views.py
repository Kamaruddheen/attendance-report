from django.shortcuts import render


def homepage(request):
    return render(request, 'index.html')


def view_404(request, *args, **kwargs):
    return render(request, 'handler/error_404.html')


def view_403(request, *args, **kwargs):
    return render(request, 'handler/error_403.html')


def view_400(request, *args, **kwargs):
    return render(request, 'handler/error_400.html')


def view_500(request, *args, **kwargs):
    return render(request, 'handler/error_500.html')
