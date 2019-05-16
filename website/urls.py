
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from website.views import jogging, registration


urlpatterns = (
    url(r'^website/', jogging.index, name='website_home'),
    url(r'^information/$', jogging.information, name='information'),
    url(r'^rules/$', jogging.rules, name='rules'),
    url(r'^contact/$', jogging.contact, name='contact'),
    url(r'^preregistration/$', jogging.pre_registration, name='pre_registration'),
    url(r'^registration/$', jogging.registration, name='registration'),
    url(r'^registration/add/$', registration.add_registration, name='add_registration'),
    url(r'^sponsors/$', jogging.sponsors, name='sponsors'),
    url(r'^ranking_ultra/$', jogging.ranking_ultra, name='ranking_ultra'),
    url(r'^pictures/$', jogging.pictures, name='pictures'),
    url(r'^races/$', jogging.races, name='races'),


)
