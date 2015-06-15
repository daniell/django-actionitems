django-actionitems
==================
[![Build Status](https://travis-ci.org/birdsarah/django-actionitems.png?branch=master)](https://travis-ci.org/birdsarah/django-actionitems)

To use django-actionitems, add the actionitems directory to your project, and add <code>actionitems</code> to your INSTALLED_APPS in your project's settings.py

If you are using Django 1.7+, you will also want to add <code>MIGRATION_MODULES = { 'actionitems': 'actionitems.django_migrations' }</code> to your settings.py file.

specifying an origin
====================
django-actionitems can store a reference to sommething that creates the actionitem. For example, an action item may be the result of a Meeting, Event, or Decision. django-actionitems calls this the origin. If you wish to link your actionitem to an origin, you can supply the model in your project's settings.py in the form appname.Model e.g.

```python
 ACTIONITEMS_ORIGIN_MODEL = 'publicweb.Decision'
``` 
If ACTIONITEMS_ORIGIN_MODEL is set, then django-actionitems expects an origin to be provided when adding a new actionitem. The easiest way to do this is to override the get_origin method ActionItemCreateView in views.py.
The origin is the pk of the object. For example, if our origin is a "decision", we might set origin as follows: 
```python
from actionitems.views import ActionItemCreateView


class MyCustomActionItemCreateView(ActionItemCreateView):

    def get_origin(self, request, *args, **kwargs):
            origin = 'code for acquiring origin objects id' # e.g. origin = kwargs.get('decisionpk')
            return origin
``` 
get_origin() is called by the get_initial() method of ActionItemCreateVeiw, if you override get_initial() for this form, remember to supply an origin or manually call get_origin()

overriding success_urls
=======================
You will likely want to override the success urls using get_success_url() method in your views

migrating with south
====================
A south migration script is included to setup the basic table. However, if you wish to use an origin_model you will need to manually write a second migration script to add this column to your actionitems table.

To do this in a way that brought my second migration under version control, I did the following:

 1. <code>./manage.py schemamigration actionitems --auto</code>
 1. This generated 0002_auto__add_field_actionitem_origin.py, but it placed it in my actionitems directory that was not under version control
 1. I moved this migration script, to my main app's migrations directory (which is under version control)
 1. I added a [dependency](http://south.readthedocs.org/en/latest/dependencies.html):

```python

class Migration(SchemaMigration):

    depends_on = (
        ("actionitems", "0001_initial.py"),
    )

    def forwards(self, orm):
``` 
I then completed the migration, with <code>./manage.py migrate main</code>

running the tests
=================

The tests are not included as part of the actionitems app and so won't run when installed in your project and you use ./manage.py test. If you want to develop or extend the actionitems app you can run the tests with [tox](http://tox.readthedocs.org) by running <code>tox</code>. ([Instructions on installing tox](http://tox.readthedocs.org/en/latest/install.html)

You can pass [py.test arguments](http://pytest.org/latest/usage.html) by using <code>tox -- {your arguments}</code>. For example, to pass the py.test argument --pastebin=all use <code>tox -- --pastebin=all</code> or to pass -v --tb=short <code>tox -- -v --tb=short</code>

