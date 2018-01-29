
RequestsManager.vendorsPageCount = 25;

RequestsManager.initializers.listings = function() {
    Events.subscribe('vendorsChanged', this.refreshVendors.bind(RequestsManager));
};

RequestsManager.loadVendors = function(data, callback) {
    var url = "/api/vendors/";
    var queryData = $.extend(data, this.buildRequestQuery(), {'count': RequestsManager.vendorsPageCount});

    if (queryData['naics'] !== "") {
        RequestsManager.getAPIRequest(url, queryData, function(response) {
            var resultsObj = {};

            resultsObj.poolNumber = response['pools'][0]['number'];
            resultsObj.poolName = response['pools'][0]['name'];
            resultsObj.lastUpdated = response['last_updated'];
            resultsObj.total = 0; //overwritten below if there are any

            if (response['num_results'] !== 0) {
                resultsObj.naics = queryData['naics'];
                resultsObj.vehicle = response['pools'][0]['vehicle'].toLowerCase();
                resultsObj.total = response['num_results'];
                resultsObj.count = response['page']['results'].length;
                resultsObj.results = response['page']['results'];
            }

            callback(queryData, response, resultsObj);
        });
    };
};

RequestsManager.load = function() {
    RequestsManager.loadVendors(LayoutManager.currentSortParams(), function(queryData, response, results) {
        Events.publish('dataLoaded', results);
    });
};

RequestsManager.refreshVendors = function(data) {
    if (data['sort'] && !data['direction']) {
        data['direction'] = 'desc';
    }

    RequestsManager.loadVendors(data, function(queryData, response, results) {
        Events.publish('vendorDataLoaded', results, data['page'], RequestsManager.vendorsPageCount);
    });
};
