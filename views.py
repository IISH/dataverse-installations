import simplejson as json
from collections import OrderedDict

from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.clickjacking import xframe_options_exempt

from dv_apps.installations.models import Installation, Institution
from dv_apps.utils.metrics_cache_time import get_metrics_cache_time

from dv_apps.metrics.stats_count_util import get_total_published_counts

@cache_page(get_metrics_cache_time())
def view_map(request):
    """Show Dataverse map with affiliated Institutions"""

    # Retrieve the installations
    install_list = Installation.objects.filter(is_active=True)
    arr = []

    # For each Installation, add the affiliated Institutions
    for i  in install_list:
        lists = Institution.objects.filter(host__name=i.name)
        arr.append(lists)

    d = dict(
        install_list = install_list,
        arr = arr,
        installation_count=install_list.count()
    )

    d.update(get_total_published_counts())

    return render(request, 'installations/map2.html', d)


@cache_page(get_metrics_cache_time())
def view_installations_json_pretty(request):

    return view_installations_json(request, True)

@cache_page(get_metrics_cache_time())
def view_installations_json(request, pretty=False):

    l = Installation.objects.all()

    dv_list = [dv.to_json() for dv in l]

    installations_dict =  object_pairs_hook=OrderedDict(installations=dv_list)

    print 'pretty', pretty
    if pretty:
        content = '<html><pre>%s</pre></html>' %\
                  json.dumps(installations_dict,
                             indent=4)
        return HttpResponse(content)
    else:
        content = json.dumps(installations_dict)
        return HttpResponse(content,
                            content_type="application/json")




@xframe_options_exempt
@cache_page(get_metrics_cache_time())
def view_homepage_counts_dataverse_org(request):

    d = get_total_published_counts()
    d['installation_count'] = Installation.objects.filter(is_active=True).count()

    return render(request, 'installations/homepage_counts.html', d)


@xframe_options_exempt
@cache_page(get_metrics_cache_time())
def view_map_dataverse_org(request):
    """
    Return map visualization page
    If iframe parameter not present, then redirect to dataverse.org homepage
    """
    if not request.GET.get('iframe', None):
        return HttpResponseRedirect('http://dataverse.org')

    return view_map(request)
