
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
    var setasideFilters = [];

    if (requestVars['naics'] !== "") {
        queryData['pools__naics__code'] = requestVars['naics'];

        if ('vehicle' in requestVars) {
            queryData['pools__vehicle__iexact'] = requestVars['vehicle'];
        }
        if ('pool' in requestVars) {
            queryData['pools__number'] = requestVars['pool'];
        }

        if ('setasides' in requestVars) {
            var setasides = requestVars['setasides'].split(',');
            for (var index = 0; index < setasides.length; index++) {
                setasideFilters.push('(' + 'setasides__code' + '=' + setasides[index] + ')');
            }
            queryData['filters'] = encodeURIComponent(setasideFilters.join('&'));
        }

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
