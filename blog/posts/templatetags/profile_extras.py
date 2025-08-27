from django import template
from posts.models import Profile

register = template.Library()

@register.filter
def get_profile(user):
    if not getattr(user, "is_authenticated", False):
        return None
    prof = getattr(user, "profile", None)
    if prof:
        return prof
    profile, _ = Profile.objects.get_or_create(user=user)
    return profile