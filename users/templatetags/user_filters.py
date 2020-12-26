from django import template


register = template.Library()


@register.filter 
def addclass(field, css):
        return field.as_widget(attrs={"class": css})


@register.filter(name='get_filter_values')
def get_filter_values(style):
    return style.getlist('filters')


@register.filter(name='get_filter_link')
def get_filter_link(request, tag):
    new_request = request.GET.copy()
    if tag.style in request.GET.getlist('filters'):
        filters = new_request.getlist('filters')
        filters.remove(tag.style)
        new_request.setlist('filters', filters)
    else:
        new_request.appendlist('filters', tag.style)
    return new_request.urlencode()
