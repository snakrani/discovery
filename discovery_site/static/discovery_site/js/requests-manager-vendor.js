
RequestsManager.contractsPageCount = 100;

RequestsManager.initializers.vendor = function() {
    Events.subscribe('vendorInfoLoaded', this.refreshContracts.bind(RequestsManager));
    Events.subscribe('contractsChanged', this.refreshContracts.bind(RequestsManager));
};

RequestsManager.loadVendor = function(callback) {
    var duns = URLManager.getDUNS();
    var url = "/api/vendor/" + duns + "/";

    RequestsManager.getAPIRequest(url, {}, function(response){
        callback(duns, response);
    });
};

RequestsManager.loadContracts = function(data, callback) {
    var duns = URLManager.getDUNS();
    var url = "/api/contracts";
    var queryData = $.extend(data, {'duns': duns, 'count': RequestsManager.contractsPageCount});

    RequestsManager.getAPIRequest(url, queryData, function(response){
        var resultsObj = {};

        resultsObj.lastUpdated = response['last_updated'];
        resultsObj.total = 0; //overwritten below if there are any

        if (response['num_results'] !== 0) {
            resultsObj.duns = queryData['duns'];
            resultsObj.total = response['num_results'];
            resultsObj.count = response['page']['results'].length;
            resultsObj.results = response['page']['results'];
        }

        callback(queryData, response, resultsObj);
    });
};

RequestsManager.load = function() {
    var listType = 'naics';

    if (URLManager.getParameterByName('showall')) {
        listType = 'all';
    }

    RequestsManager.loadVendor(function(duns, results) {
        Events.publish('dataLoaded', results);
        Events.publish('vendorInfoLoaded', {'listType': listType});
    });
};

RequestsManager.refreshContracts = function(data) {
    data['listType'] = typeof data['listType'] !== 'undefined' ? data['listType'] : 'naics';

    if (data['naics']) {
        if (data['naics'] != 'all') {
          data['naics'] = RequestsManager.stripSubCategories(data['naics']);
        }
    }
    else {
        naics = RequestsManager.stripSubCategories(URLManager.getParameterByName('naics-code'));

        if (naics && naics != 'all'){
            data['naics'] = naics;
        }

        if (data['listType'] == 'all') {
            data['naics'] = '';
        }
    }

    if (data['sort'] && !data['direction']) {
        data['direction'] = 'desc';
    }

    if (!data['page']) {
        data['page'] = 1;
    }

    RequestsManager.loadContracts(data, function(queryData, response, results) {
        Events.publish('contractDataLoaded', results, data['listType'], data['page'], RequestsManager.contractsPageCount);
    });
};

RequestsManager.stripSubCategories = function(naics_code) {
    //if last character in naics code isn't a number, strip it out
    if (isNaN(naics_code.slice(-1))) {
        //strip it
        naics_code = naics_code.substring(0, naics_code.length - 1);
    }
    return naics_code;
};
