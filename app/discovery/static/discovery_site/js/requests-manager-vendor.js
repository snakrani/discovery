
RequestsManager.sortClassMap = function() {
    return {
        'h_date_signed': 'date_signed',
        'h_piid': 'piid',
        'h_agency': 'agency_name',
        'h_type': 'pricing_type__name',
        'h_location': 'place_of_performance_location',
        'h_value': 'obligated_amount',
        'h_status': 'status__name',
    };
};

RequestsManager.initializers.vendor = function() {
    Events.subscribe('poolUpdated', this.refreshVendor.bind(RequestsManager));

    Events.subscribe('vendorInfoLoaded', this.refreshContracts.bind(RequestsManager));
    Events.subscribe('contractsChanged', this.refreshContracts.bind(RequestsManager));
};

RequestsManager.loadVendor = function(callback) {
    var duns = URLManager.getDUNS();
    var url = "/api/vendors/" + duns + "/";

    RequestsManager.getAPIRequest(url, {}, function(response){
        callback(duns, response);
    });
};

RequestsManager.loadContracts = function(data, callback) {
    var duns = URLManager.getDUNS();
    var url = "/api/contracts";
    var queryData = $.extend(data, {'vendor__duns': duns, 'count': this.getPageCount()});

    queryData['NAICS'] = queryData['naics'];
    delete queryData['naics'];

    if (queryData['NAICS'] == 'all') {
        delete queryData['NAICS'];
    }
    RequestsManager.getAPIRequest(url, queryData, function(response){
        callback(queryData, response);
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

RequestsManager.refreshVendor = function(pool) {
    RequestsManager.loadVendor(function(duns, results) {
        Events.publish('vendorPoolLoaded', results, pool);
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

    if (!data['page']) {
        data['page'] = 1;
    }

    RequestsManager.loadContracts(data, function(queryData, response) {
        Events.publish('contractDataLoaded', response, data['listType'], data['page'], queryData['count']);
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
