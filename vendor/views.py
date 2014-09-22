from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from vendor.models import Vendor, Pool, Naics, SetAside
import csv

def pool_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="search_results.csv"'
    writer = csv.writer(response)
    #write results
    vendors = Vendor.objects.all()
    setasides_all = SetAside.objects.all().order_by('far_order')
    filter_text = []
    #naics
    if 'naics-code' in request.GET:
        naics = request.GET['naics-code']
        naics_obj = Naics.objects.get(short_code=naics)
        vendors = vendors.filter(pools__naics=naics_obj)
        filter_text.append("NAICS code {0}".format(naics))
    #setasides
    if 'setasides' in request.GET:
        setasides = request.GET.getlist('setasides')[0].split(',')
        setaside_objs = SetAside.objects.filter(code__in=setasides)
        for sobj in setaside_objs:
            vendors = vendors.filter(setasides=sobj)

        filter_text.append("Set Aside filters: {0}".format(", ".join(setasides)))

    writer.writerow(("Search Results: {0} Vendors".format(len(vendors)),))
    writer.writerow(filter_text)

    writer.writerow(('',))
    header_row = ['Vendor', 'Location']
    header_row.extend([sa_obj.short_name for sa_obj in setasides_all])
    writer.writerow(header_row)

    for v in vendors: 
        setaside_list = []
        for sa in setasides_all:
            if sa in v.setasides.all():
                setaside_list.append('X')
            else:
                setaside_list.append('')

        v_row = [v.name, v.sam_citystate]
        v_row.extend(setaside_list)
        writer.writerow(v_row)

    return response




