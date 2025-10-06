from django import template
from django.utils.safestring import mark_safe


register = template.Library()


@register.filter
def star_rating(value):
    full_star = 0
    half_star = 0
    empty_star = 0
    for i in range(1, 6):
        if (i - 0.5) == value:
            half_star += 1
        elif i < value:
            full_star += 1
        else:
            empty_star += 1
    rating = []
    for star in range(full_star):
        rating.append("<i class='bi bi-star-fill'></i>")
    for star in range(half_star):
        rating.append("<i class='bi bi-star-half'></i>")
    for star in range(empty_star):
        rating.append("<i class='bi bi-star'></i>")
 
    return mark_safe("".join(rating))

