from django.shortcuts import get_object_or_404, redirect

from main.models import Link


def view(request, slug):
    link = get_object_or_404(Link, alias=slug).link
    return redirect(link)
