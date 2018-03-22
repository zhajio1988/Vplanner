import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wplanner.settings')

import django
django.setup()

from planner.models import Category, Page

def populate():
    python_cat = add_cat('Python', 128, 64)

    add_page(cat=python_cat,
        title="Official Python Tutorial",
        url="http://docs.python.org/2/tutorial/")

    add_page(cat=python_cat,
        title="How to Think like a Computer Scientist",
        url="http://www.greenteapress.com/thinkpython/")

    add_page(cat=python_cat,
        title="Learn Python in 10 Minutes",
        url="http://www.korokithakis.net/tutorials/python/")

    django_cat = add_cat("Django", 64, 32)

    add_page(cat=django_cat,
        title="Official Django Tutorial",
        url="https://docs.djangoproject.com/en/1.5/intro/tutorial01/")

    add_page(cat=django_cat,
        title="Django Rocks",
        url="http://www.djangorocks.com/")

    add_page(cat=django_cat,
        title="How to Tango with Django",
        url="http://www.tangowithdjango.com/")

    frame_cat = add_cat("Other Frameworks", 32, 16)

    add_page(cat=frame_cat,
        title="Bottle",
        url="http://bottlepy.org/docs/dev/")

    add_page(cat=frame_cat,
        title="Flask",
        url="http://flask.pocoo.org")    

    perl_cat = add_cat("perl", 320, 160)

    add_page(cat=perl_cat,
        title="Perl",
        url="http://www.perl.org/")

    add_page(cat=perl_cat,
        title="PerlMonks",
        url="http://www.perlmonks.com/")

    sv_cat = add_cat("systemverilog", 150, 161)

    add_page(cat=sv_cat,
        title="sv",
        url="https://baike.baidu.com/item/SystemVerilog/2431946?fr=aladdin")

    add_page(cat=sv_cat,
        title="SvLib",
        url="http://www.perlmonks.com/")    

    # Print out what we have added to the user.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print ("- {0} - {1}".format(str(c), str(p)))

def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    p.save()
    return p

def add_cat(name, views=0, likes=0):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c

# Start execution here!
if __name__ == '__main__':
    print ("Starting Planner population script...")
    populate()
