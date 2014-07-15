from django import template
from loadprograms import dbcontext

register = template.Library()

@register.assignment_tag
def get_category():
    x = dbcontext.DBContext()
    results = x.executequery("Select id, name from Categories")
    print ' category_tags Categories =', results
    print 'outside category tags'
    x.close()
    return results 
