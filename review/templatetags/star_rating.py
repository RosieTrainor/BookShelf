from django import template
from django.utils.safestring import mark_safe
from django.conf import settings
from functools import lru_cache
import os


register = template.Library()


@lru_cache(maxsize=3)
def load_svg(file_url):
    """
    Load the content of an SVG file from the static directory.
    """
    try:
        file_path = os.path.join(settings.BASE_DIR, "static", file_url)
        with open(file_path, "r", encoding="utf-8") as svg_file:
            return svg_file.read()
    except FileNotFoundError:
        return None


@register.filter
def star_rating(value):
    """
    Generate the star rating HTML or return the rating value as fallback.
    """
    full_star_url = "icons/star-fill.svg"
    half_star_url = "icons/star-half.svg"
    empty_star_url = "icons/star.svg"

    full_star_svg = load_svg(full_star_url)
    half_star_svg = load_svg(half_star_url)
    empty_star_svg = load_svg(empty_star_url)

    if not full_star_svg or not half_star_svg or not empty_star_svg:
        return f"Rating: {value}"

    full_star = 0
    half_star = 0
    empty_star = 0
    for i in range(1, 6):
        if (i - 0.5) == value:
            half_star += 1
        elif i <= value:
            full_star += 1
        else:
            empty_star += 1
    rating = []
    for star in range(full_star):
        rating.append(full_star_svg)
    for star in range(half_star):
        rating.append(half_star_svg)
    for star in range(empty_star):
        rating.append(empty_star_svg)

    return mark_safe("".join(rating))
