import cgi
import string

from crits.indicators.handlers import does_indicator_relationship_exist

from django import template
register = template.Library()

# TODO: make this more generic if it winds up being used more
@register.filter
def is_in(var, obj):
    """
    If the contents of "var" is equivalent to the value in obj.name.

    :param var: The value to look for.
    :type var: str
    :param obj: The object to iterate over.
    :type obj: dict/class
    :returns: True, False
    """

    r = False
    for o in obj:
        if var == o.name:
            r = True
    return r

@register.filter
def user_source(var, obj):
    """
    If var is in obj.

    :param var: The value to look for.
    :type var: str
    :param obj: The object to search through.
    :type obj: str/list/tuple
    :returns: True, False
    """

    if var in obj:
        return True
    else:
        return False

@register.filter
def does_field_have_indicator(field, relationships):
    """
    Used in Django templates, this function checks if an indicator already
    exists by examining the list of relationships and comparing it against the
    values of the input field. This filter is generally used on fields with
    values that can create an indicator (e.g. objects, email fields)

    Args:
        field: The generic input field to check if an indicator already exists.
            This field is generally from custom dictionaries such as from
            Django templates.
        relationships: The list of relationships to cross reference the input
            field against.

    Returns:
        Returns true if the input field already has an indicator associated
        with its values. Returns false otherwise.
    """

    return_value = False

    # validate the input parameters
    if field and relationships:
        return_value = does_indicator_relationship_exist(field, relationships.get("Indicator"))

    return return_value

@register.filter
def type(value):
    """
    Get the type of value.

    :param value: What to get the type of.
    :type value: anything
    :returns: str
    """

    return type(value)

@register.filter
def nicify(value):
    """
    Make the string pretty.

    :param value: What to make pretty.
    :type value: str.
    :returns: str
    """

    return string.capwords(value.replace("_", " "))

@register.filter
def template_exists(template_name):
    """
    Check to see if this template exists and is known to Django.

    :param template_name: The name of the template.
    :type template_name: str
    :returns: True, False
    """

    try:
        template.loader.get_template(template_name)
        return True
    except template.TemplateDoesNotExist:
        return False

@register.filter
def to_line_table(value):
    """
    Convert a chunk of data into a line table.

    :param value: The data to convert (will be split by newline).
    :type value: str
    :returns: str
    """

    html = """
        <div class="line_table_container">
        <table class="line_table">
            <tbody>
    """
    lines = value.split('\n')
    l = 1
    for line in lines:
        lhtml = '<tr class="file_line" data-position="%d">' % l
        lhtml += '\n<td class="add_highlight ui-icon ui-icon-star"></td><td class="line_num">'
        lhtml += '<span class="line_number">%d</span></td>\n' % l
        lhtml += '<td class="line_pre"><pre>%s</pre></td>\n</tr>\n' % cgi.escape(line)
        html += lhtml
        l += 1
    html += '</tbody>\n</table>\n</div>\n'
    return html

@register.filter
def cgi_escape(value):
    """
    CGI Escape a string.

    :param value: The string to escape.
    :type value: str
    :returns: str
    """

    return cgi.escape(value)

@register.filter
def absVal(value):
    """
    return absolute value
    
    :param value: the int to get the absolute value of
    :type value: int
    :returns: int
    """
    return abs(value)
    