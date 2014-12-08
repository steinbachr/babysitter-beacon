from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from web.models import *
import pdb


def slug_matches_login(wrapped):
    """
    decorator to verify that the slug in a given request matches the User who is logged in. That is, if user with slug
    bobby-slug tries to go to URL pam-slug, he should be denied.
    Note: login_required should be wrapping this decorator
    TODO: known bug = if a parent and sitter have the same slug, a logged in sitter can get to the parent's profile by just switching URL
    :param wrapped: the wrapped function to execute on success
    :return: the decorated function
    :raises: Http404 if trying to access someone elses account
    """
    def inner(request, slug=None, **kwargs):
        request_user = request.user

        if not request_user.slug == slug:
            raise Http404

        return wrapped(request, slug=slug, **kwargs)

    return inner