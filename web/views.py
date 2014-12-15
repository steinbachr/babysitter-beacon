from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from web.decorators import slug_matches_login
from web.forms import *
import pdb


def home(request):
    return render(request, 'index.html', {})


#####-----< Signup/Login >-----#####
def _authenticate_user(cls, signup_form_cls=None, request=None):
    """
    helper method for authenticating / logging a user into the session.
    :param cls: The type of user to login (one of a Parent or Sitter cls object)
    :param signup_form_cls: the signup form (one of ParentSignupForm or SitterSignupForm)
    :param request:
    :return: a 3-tuple of: the logged in user (or None if login failed), the bound (or unbound) login form, and the
    bound (or unbound) signup form
    """
    login_form = LoginForm(target=cls)
    signup_form = signup_form_cls()
    user = None

    if request.method == 'POST':
        was_login_request = request.POST.get('phone_number') is None
        email = password = None

        if was_login_request:
            login_form = LoginForm(data=request.POST, target=cls)
            is_valid = login_form.is_valid()
            if is_valid:
                email, password = login_form.cleaned_data.get('email'), login_form.cleaned_data.get('password')
        else:
            signup_form = signup_form_cls(request.POST)
            is_valid = signup_form.is_valid()
            if is_valid:
                email, password = signup_form.cleaned_data.get('email'), signup_form.cleaned_data.get('password')
                user = signup_form.save()
                user.set_password(user.password)
                user.save()

        if is_valid:
            user = authenticate(cls=cls, email=email, password=password)
            login(request, user)

    return user, login_form, signup_form

def parent_signup(request):
    user, login_form, signup_form = _authenticate_user(Parent, signup_form_cls=ParentSignupForm, request=request)
    if user:
        return redirect(reverse('web.views.parents_dashboard', args=(user.slug,)))

    return render(request, 'signup.html', {
        'type': 'Parents',
        'login_form': login_form,
        'signup_form': signup_form,
    })


def sitter_signup(request):
    user, login_form, signup_form = _authenticate_user(Sitter, signup_form_cls=SitterSignupForm, request=request)
    if user:
        return redirect(reverse('web.views.sitters_dashboard', args=(user.slug,)))

    return render(request, 'signup.html', {
        'type': 'Babysitters',
        'login_form': login_form,
        'signup_form': signup_form,
    })


def app_logout(request):
    logout(request)
    return redirect(reverse('web.views.home'))


#####-----< Dashboards >-----#####
@login_required()
@slug_matches_login
def parents_dashboard(request, slug=None):
    parent = Parent.objects.get(slug=slug)
    return render(request, 'parents/index.html', {
        'parent': parent,
        'stripe_publishable_key': settings.STRIPE_PUBLIC_KEY,
        'create_child_form': ChildForm(initial={'parent': parent.id}),
        'beacon_form': BeaconForm(initial={'created_by': parent.id}),
        'payment_form': PaymentForm(),
        'location_form': ParentLocationForm(instance=parent)
    })


@login_required()
@slug_matches_login
def sitters_dashboard(request, slug=None):
    sitter = Sitter.objects.get(slug=slug)
    return render(request, 'sitters/dashboard.html', {
        'sitter': sitter
    })