from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView
from hitcount.views import HitCountDetailView
from .models import Post
from Gallery.models import Project
from Loghome_2020.views import initiate_context


class BlogView(ListView):
    model = Post
    context_object_name = 'blogs'
    paginate_by = 10

    def get_queryset(self):
        qs = super(BlogView, self).get_queryset().filter(category__title="Blog")
        return qs

    def get_context_data(self, **kwargs):
        context = super(BlogView, self).get_context_data(**kwargs)
        context = initiate_context(context)
        context['popular_posts'] = Post.objects.filter(category__slug='blog').order_by('-hit_count')[:5]
        context['projects'] = Project.objects.filter(status=4)[:5]
        context['about_me'] = Post.objects.get(slug='about-me')

        return context


class BlogDetailView(HitCountDetailView):
    model = Post
    context_object_name = 'post'
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        context = initiate_context(context)
        context['popular_posts'] = Post.objects.filter(category__slug='blog').order_by('-hit_count')
        context['projects'] = Project.objects.filter(status=4)[:5]
        context['about_me'] = Post.objects.get(slug='about-me')
        return context

