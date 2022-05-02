from django.http import HttpResponse


def view(request, slug):
    return HttpResponse(slug)
