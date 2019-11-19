from django.shortcuts import render

from django.http import HttpResponse


def login(request):
    return HttpResponse("You want to login")


def uniqueid(request):
    return HttpResponse("You are generating uniqueID.")
