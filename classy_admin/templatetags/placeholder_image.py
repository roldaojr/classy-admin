from base64 import b64encode

from django import template

register = template.Library()


@register.simple_tag
def placeholder_image_url(text, size=200, fg="#ffffffff", bg="#000000ff"):
    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40" width="40" height="40">
  <rect width="{size}" height="{size}" fill="{bg}"></rect>
  <text x="50%" y="55%" dominant-baseline="middle" text-anchor="middle" font-family="sans-serif"
  font-size="16pt" fill="{fg}">{text}</text>
</svg>"""  # NOQA
    base64str = b64encode(svg.encode()).decode()
    return f"data:image/svg+xml;base64,{base64str}"  # NOQA


@register.filter
def placeholder_user_photo(text):
    return placeholder_image_url(str(text)[0].upper(), bg="#4CAF50", fg="#ffffff")
