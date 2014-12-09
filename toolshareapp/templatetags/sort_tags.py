from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def sort_url(context, field, value):
    #makes a copy so I don't alter the data
    request = context['request']
    args = request.GET.copy()
    #if it has been sorted already, sort it the other way
    if field == 'order_by' and field in args.keys():
        if args[field].startswith('-') and args[field].lstrip('-') == value:
            args[field] = value
        else:
            args[field] = '-' + value
    else:
        args[field] = value

    return args.urlencode()