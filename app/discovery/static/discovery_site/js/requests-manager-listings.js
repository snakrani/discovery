
RequestsManager.sortClassMap = function() {
    return {
        'h_vendor_name': 'name',
        'h_vendor_location': 'sam_location_citystate',
        'h_naics_results': 'number_of_contracts',
    };
};

RequestsManager.initializers.listings = function() {
    EventManager.subscribe('poolUpdated', this.load.bind(RequestsManager));
    EventManager.subscribe('poolSelected', this.load.bind(RequestsManager));
    EventManager.subscribe('vendorsChanged', this.refreshVendors.bind(RequestsManager));
};

RequestsManager.loadVendorData = function(data, callback) {
    var url = "/api/vendors/";
    var pools = RequestsManager.vehiclePools;
    var poolIds = [];

    var requestVars = this.buildRequestQuery();
    var queryData = $.extend(data, {'count': this.getPageCount()});
    var filters = [];

    if (! $.isEmptyObject(pools) && 'naics' in requestVars) {
        queryData['contract_naics'] = requestVars['naics'];

        if (RequestsManager.pool) {
            filters.push('(pools__pool__id' + '=' + RequestsManager.pool.id + ')');
        } else {
            Object.keys(pools).forEach(function (id) {
                poolIds.push(id);
            });
            filters.push('(pools__pool__id__in' + '=' + poolIds.join(',') + ')');
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

        RequestsManager.getAPIRequest(url, queryData,
            function(response) {
                if (queryData['contract_naics'] == URLManager.getParameterByName('naics-code')) {
                    callback(queryData, response);

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
};

RequestsManager.load = function() {
    if (URLManager.isPoolPage()) {
        RequestsManager.loadVendorData(RequestsManager.currentSortParams(), function(queryData, response) {
            EventManager.publish('dataLoaded', response);
        });
    }
};

RequestsManager.refreshVendors = function(data) {
    RequestsManager.loadVendorData(data, function(queryData, response) {
        EventManager.publish('vendorDataLoaded', response, data['page'], queryData['count']);
    });
};
