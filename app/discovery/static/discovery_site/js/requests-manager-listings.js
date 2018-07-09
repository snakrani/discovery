
RequestsManager.sortClassMap = function() {
    return {
        'h_vendor_name': 'name',
        'h_vendor_location': 'sam_location_citystate',
        'h_naics_results': 'number_of_contracts',
    };
};

RequestsManager.load = function() {
    var url = "/api/vendors/";
    var pools = DataManager.getVehiclePools();
    var pool = DataManager.getPool();
    var poolIds = [];

    var requestVars = DataManager.buildRequestQuery();
    var ordering = DataManager.getSortOrdering();
    var queryData = {
        'page': DataManager.getPage(),
        'count': DataManager.getPageCount()
    };

    if (ordering) {
        queryData['ordering'] = ordering;
    }
    var filters = [];

    if ('naics' in requestVars) {
        queryData['contract_naics'] = requestVars['naics'];
    }
    if (! $.isEmptyObject(pools)) {
        if (pool) {
            filters.push('(pools__pool__id' + '=' + pool.id + ')');
        } else {
            Object.keys(pools).forEach(function (id) {
                poolIds.push(id);
            });
            filters.push('(pools__pool__id__in' + '=' + poolIds.join(',') + ')');
        }
    }

    if (LayoutManager.zoneActive() && 'zone' in requestVars) {
        filters.push('(pools__zones__id' + '=' + requestVars['zone'] + ')');
    }

    if ('setasides' in requestVars) {
        var setasides = requestVars['setasides'].split(',');
        for (var index = 0; index < setasides.length; index++) {
            filters.push('(pools__setasides__code' + '=' + setasides[index] + ')');
        }
    }
    queryData['filters'] = encodeURIComponent(filters.join('&'));

    LayoutManager.disableVehicles();
    LayoutManager.disablePools();
    LayoutManager.disableZones();
    LayoutManager.disableFilters();
    $('.table_wrapper').addClass('loading');

    this.getAPIRequest(url, queryData,
        function(response) {
            if (queryData['contract_naics'] == DataManager.getParameterByName('naics-code')) {
                EventManager.publish('dataLoaded', response);

                LayoutManager.enableVehicles();
                LayoutManager.enablePools();
                LayoutManager.enableZones();
                LayoutManager.enableFilters();
                $('.table_wrapper').removeClass('loading');
            }
        },
        function(req, status, error) {
            LayoutManager.enableVehicles();
            LayoutManager.enablePools();
            LayoutManager.enableZones();
            LayoutManager.enableFilters();
            $('.table_wrapper').removeClass('loading');
        }
    );
};
