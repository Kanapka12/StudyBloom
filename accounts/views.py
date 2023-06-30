import os
import random
from random import choice
from uuid import uuid4
from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.core.cache import cache
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, FormView, TemplateView, ListView, DetailView
from django.views.generic.edit import FormMixin, ModelFormMixin, UpdateView
from django.utils.translation import gettext_lazy as _
from .forms import AppearanceChangeForm, EmailChangeConfirmationForm, EmailChangeRequestForm, UsernameChangeForm, SignUpForm
from .models import CustomUser, EmailChangeRequest
from django.contrib import messages


class SignUpView(SuccessMessageMixin, CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
    success_message = 'User registered successfully'


# DEFAULT_PROFILE_IMAGES_PATH = 'accounts/default_profile_images'
# class UserDetailView(LoginRequiredMixin, UpdateView):
#     form_class = AppearanceChangeForm
#     template_name = 'registration/account_detail.html'
#     success_url = reverse_lazy('account_detail')
#     default_images = None
#
#     def get_default_profile_images(self):
#         if self.default_images is None:
#             image_folder = DEFAULT_PROFILE_IMAGES_PATH
#             self.default_images = default_storage.listdir(image_folder)[1]
#         return self.default_images
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['default_images'] = self.get_default_profile_images()
#         context['default_images_path'] = DEFAULT_PROFILE_IMAGES_PATH
#         return context
#
#         # dzieki temu wie zeby wyswietlac tylko dane usera, pomija id w urls i model w widoku
#     def get_object(self, queryset=None):
#         return self.request.user
#
#     def form_valid(self, form):
#         self.object = form.save(commit=False)
#         if 'random_image' in self.request.POST:
#             self.object.profile_image = f'{DEFAULT_PROFILE_IMAGES_PATH}/{choice(self.get_default_profile_images())}'
#         elif 'default_image' in form.cleaned_data and form.cleaned_data["default_image"]:
#             self.object.profile_image = f'{DEFAULT_PROFILE_IMAGES_PATH}/{form.cleaned_data["default_image"]}'
#         self.object.save()
#         return super().form_valid(form)
#
#     def post(self, request, *args, **kwargs):
#         if 'selected_image' in request.POST:
#             image_name = request.POST['selected_image']
#             if image_name == "random_image_chest.png":
#                 image_name = random.choice(self.get_default_profile_images())
#             request.user.profile_image = f'{DEFAULT_PROFILE_IMAGES_PATH}/{image_name}'
#             request.user.save()
#             return HttpResponseRedirect(self.success_url)
#         return super().post(request, *args, **kwargs)


class DefaultAvatarsMixin:
    default_avatars_path = 'accounts/default_avatars'

    @property
    def get_default_avatars(self):
        return default_storage.listdir(self.default_avatars_path)[1]

    @property
    def get_random_default_avatar(self):
        return random.choice(self.get_default_avatars)


class UserDetailView(LoginRequiredMixin, SuccessMessageMixin, DefaultAvatarsMixin, UpdateView):
    form_class = AppearanceChangeForm
    template_name = 'registration/account_detail.html'
    success_url = reverse_lazy('account_detail')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['default_avatars'] = self.get_default_avatars
        context['default_avatars_path'] = self.default_avatars_path
        return context

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        if form.cleaned_data['avatar_choice']:
            form.instance.avatar = os.path.join(self.default_avatars_path, form.cleaned_data['avatar_choice'])
        elif form.cleaned_data['avatar_draw']:
            form.instance.avatar = os.path.join(self.default_avatars_path, self.get_random_default_avatar)
        return super().form_valid(form)




class UsernameChangeView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = UsernameChangeForm
    template_name = 'registration/username_change.html'
    success_url = reverse_lazy('account_detail')
    success_message = "Username updated successfully"

    def get_object(self, queryset=None):
        return self.request.user


class EmailChangeView(LoginRequiredMixin, FormView):
    template_name = 'registration/email_change.html'
    form_class = EmailChangeRequestForm
    success_url = reverse_lazy('email_change_confirm')

    def form_valid(self, form):
        email_change_request = form.save(commit=False)
        email_change_request.user = self.request.user
        email_change_request.save()

        send_mail(
            _('Email change request'),
            _('Your email change confirmation code is: {}').format(email_change_request.confirmation_code),
            'noreply@example.com',
            [self.request.user.email],
            fail_silently=False,
        )

        return super().form_valid(form)


class EmailChangeConfirmView(LoginRequiredMixin, FormView):
    template_name = 'registration/email_confirmation.html'
    form_class = EmailChangeConfirmationForm
    success_url = reverse_lazy('account_detail')
    success_message = "Email updated successfully"

    def form_valid(self, form):
        confirmation_code = form.cleaned_data['confirmation_code']
        password = form.cleaned_data['password']

        if not self.request.user.check_password(password):
            messages.error(self.request, _("The password is incorrect."))
            return self.form_invalid(form)

        try:
            email_change_request = EmailChangeRequest.objects.get(confirmation_code=confirmation_code, user=self.request.user, is_confirmed=False)
        except EmailChangeRequest.DoesNotExist:
            messages.error(self.request, _("Invalid confirmation code."))
            return self.form_invalid(form)

        self.request.user.email = email_change_request.new_email
        self.request.user.save()
        email_change_request.is_confirmed = True
        email_change_request.save()

        update_session_auth_hash(self.request, self.request.user)

        return super().form_valid(form)
