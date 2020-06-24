from django.forms import model_to_dict
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.views.generic import ListView, DetailView
from . import models
from .models import Project
from Loghome_2020.views import initiate_context


class GalleryView(DetailView):
    model = models.Project
    #
    # def get_queryset(self):
    #     qs = super(GalleryView, self).get_queryset()
    #     return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = initiate_context(context)
        context['images'] = models.HomeImage.objects.filter(project__slug=self.kwargs['slug'], status=4)
        context['gallery'] = Project.objects.all()
        context['specs'] = Project.objects.filter(slug=self.kwargs['slug']).values()[0]

        return context
