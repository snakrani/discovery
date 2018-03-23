
RequestsManager.vendorsPageCount = 25;

RequestsManager.sortClassMap = function() {
    return {
        'h_vendor_name': 'name',
        'h_vendor_location': 'sam_location_citystate',
        'h_naics_results': 'number_of_contracts',
    };
};

RequestsManager.initializers.listings = function() {
    Events.subscribe('vendorsChanged', this.refreshVendors.bind(RequestsManager));
};

RequestsManager.loadVendors = function(data, callback) {
    var url = "/api/vendors/";

    var requestVars = this.buildRequestQuery();
    var queryData = $.extend(data, {'count': RequestsManager.vendorsPageCount});
    var filters = [];

    if (requestVars['naics'] !== "") {
        filters.push('(pools__pool__naics__code' + '=' + requestVars['naics'] + ')');

        if ('vehicle' in requestVars) {
            filters.push('(pools__pool__vehicle__iexact' + '=' + requestVars['vehicle'] + ')');
        }
        if ('pool' in requestVars) {
            filters.push('(pools__pool__number' + '=' + requestVars['pool'] + ')');
        }

        if ('setasides' in requestVars) {
            var setasides = requestVars['setasides'].split(',');
            for (var index = 0; index < setasides.length; index++) {
                filters.push('(pools__setasides__code' + '=' + setasides[index] + ')');
            }
        }
        queryData['filters'] = encodeURIComponent(filters.join('&'));

        RequestsManager.getAPIRequest(url, queryData, function(response) {
            callback(queryData, response);
        });
    };
};

RequestsManager.load = function() {
    RequestsManager.loadVendors(RequestsManager.currentSortParams(), function(queryData, response) {
        Events.publish('dataLoaded', response);
    });
};

RequestsManager.refreshVendors = function(data) {
    RequestsManager.loadVendors(data, function(queryData, response) {
        Events.publish('vendorDataLoaded', response, data['page'], RequestsManager.vendorsPageCount);
    });
};
