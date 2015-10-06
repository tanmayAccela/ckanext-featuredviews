=============
ckanext-featuredviews
=============

Display select resource views on dataset and organization pages.

By default, CKAN only shows Resource Views on the resource page, but has no
mechanism for showing users which resources have visualizations, and where the
good ones are.

This extension lets you mark Resource Views as featured so they show up right
on your dataset pages or even on the CKAN front page.

Usage
=============
Clone it. This package is not on PyPI yet: ::

    git clone https://github.com/deniszgonjanin/ckanext-featuredviews.git
    cd ckanext-featuredviews
    python setup.py develop
    

Add to the list of plugins: ::

    ckan.plugins = ... featuredviews


The database table for civicdata_featured views should be created automatically at startup.
So the following command is optional: ::

    paster --plugin=ckanext-featuredviews featured migrate -c production.ini
