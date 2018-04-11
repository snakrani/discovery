
RequestsManager.sortClassMap = function() {
    return {
        'h_vendor_name': 'name',
        'h_vendor_location': 'sam_location_citystate',
        'h_naics_results': 'number_of_contracts',
    };
};

RequestsManager.initializers.listings = function() {
    EventManager.subscribe('vendorsChanged', this.refreshVendors.bind(RequestsManager));
};

RequestsManager.loadVendors = function(data, callback) {
    var url = "/api/vendors/";

    var requestVars = this.buildRequestQuery();
    var queryData = $.extend(data, {'count': this.getPageCount()});
    var filters = [];

    if ('naics' in requestVars) {
        queryData['contract_naics'] = requestVars['naics'];
        filters.push('(pools__pool__naics__code' + '=' + requestVars['naics'] + ')');

        if ('vehicle' in requestVars) {
            filters.push('(pools__pool__vehicle__iexact' + '=' + requestVars['vehicle'] + ')');
        }
        if ('pool' in requestVars) {
            filters.push('(pools__pool__number' + '=' + requestVars['pool'] + ')');
        }

        if ('zone' in requestVars && requestVars['zone'] != 'all') {
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
        LayoutManager.disableNaics();
        LayoutManager.disableZone();
        LayoutManager.disableFilters();
        $('.table_wrapper').addClass('loading');

        RequestsManager.getAPIRequest(url, queryData,
            function(response) {
                callback(queryData, response);

                LayoutManager.enableVehicles();
                LayoutManager.enableNaics();
                LayoutManager.toggleZone();
                LayoutManager.enableFilters();
                $('.table_wrapper').removeClass('loading');
            },
            function(req, status, error) {
                LayoutManager.enableVehicles();
                LayoutManager.enableNaics();
                LayoutManager.toggleZone();
                LayoutManager.enableFilters();
                $('.table_wrapper').removeClass('loading');
            }
        );
    };
};

RequestsManager.load = function() {
    if (URLManager.isPoolPage()) {
        RequestsManager.loadVendors(RequestsManager.currentSortParams(), function(queryData, response) {
            EventManager.publish('dataLoaded', response);
        });
    }
};

RequestsManager.refreshVendors = function(data) {
    RequestsManager.loadVendors(data, function(queryData, response) {
        EventManager.publish('vendorDataLoaded', response, data['page'], queryData['count']);
    });
};
