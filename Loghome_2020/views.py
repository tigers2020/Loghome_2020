from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.views.generic import ListView, TemplateView, FormView
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from Gallery.models import Project
from Post.models import Post
from .forms import ContactForm


def initiate_context(context):
    context['gallery'] = Project.objects.all()
    context['no_image'] = settings.NO_IMAGE_URL
    context['who_we_are'] = Post.objects.get(slug='who-we-are')
    context['blogs'] = Post.objects.order_by('-hit_count').filter(category__slug='blog')[:5]

    return context


class MainIndex(generic.TemplateView):
    template_name = 'base/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = initiate_context(context)
        return context


#
class AboutUsView(generic.ListView):
    model = Post
    template_name = 'about_us.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context = initiate_context(context)
        context['about_us'] = Post.objects.get(slug='about-us')
        context['faqs'] = Post.objects.filter(category__slug='faq')
        context['timeline'] = ""
        return context


class ContactView(generic.FormView):
    template_name = 'Contact/contact.html'
    form_class = ContactForm
    success_url = '/contact/success'

    def form_valid(self, form):
        if self.send_mail(form.cleaned_data):
            self.success = "You have successfully submitted. We will contact you in short time."

        return super(ContactView, self).form_valid(form)

    def send_mail(self, valid_data):
        first_name = valid_data.get('first_name')

        last_name = valid_data.get('last_name')
        from_email = valid_data.get('email')
        subject = valid_data.get('subject')
        feedback = settings.FEED_BACK[int(valid_data.get('topic'))][1]
        message = valid_data['message']

        title = '[%s]%s - from: %s %s ' % (feedback, subject, first_name, last_name)
        body_message = message

        if send_mail(title, body_message, from_email, recipient_list=[settings.DEFAULT_FROM_EMAIL],
                     html_message=body_message):
            return True
            # return "You have successfully submitted. We will contact you in short time."
        else:
            return False
            # return "Sorry your mail didn't go though our system. try it later"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = initiate_context(context)

        return context



class SuccessView(generic.TemplateView):
    template_name = 'Contact/success.html'

    def get_context_data(self, **kwargs):
        context = super(SuccessView, self).get_context_data(**kwargs)
        context = initiate_context(context)
        return context
