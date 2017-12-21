RequestsManager.vendorInit = function(original) {
    Events.subscribe('vendorInfoLoaded', this.loadContracts.bind(RequestsManager));
    Events.subscribe('contractsChanged', this.refreshContracts.bind(RequestsManager));
    original.bind(RequestsManager).call();
};

RequestsManager.originalInit = RequestsManager.init;

RequestsManager.init = function() {
    RequestsManager.vendorInit(RequestsManager.originalInit);
};

RequestsManager.load = function() {
    /* get vendor info from api */
 
    var url = "/api/vendor/" + URLManager.getDUNS() + "/";

    var listType = 'naics';
    if (URLManager.getParameterByName('showall')) {
        listType = 'all';
    }
    
    RequestsManager.getAPIRequest(url, {}, function(data){
        Events.publish('dataLoaded', data);
        Events.publish('vendorInfoLoaded', listType);
    });
};

RequestsManager.loadContracts = function(listType) {
    var listType = typeof listType !== 'undefined' ? listType : 'naics';
    var url = "/api/contracts/";
    var params = {
        'duns': URLManager.getDUNS(),
        'page': 1, 
    };

    naics = RequestsManager.stripSubCategories(URLManager.getParameterByName('naics-code'));
    
    if (naics && naics != 'all'){ 
        params['naics'] = naics;
    }

    if (listType == 'all') {
        params['naics'] = '';
    }

    RequestsManager.getAPIRequest(url, params, function(data){
        Events.publish('contractDataLoaded', data, listType, data['page']);
    });

};

//no idea why, but if I integrate the updated_naics parameter into the above function it becomes an infinite loop -- KBD
RequestsManager.refreshContracts = function(data) {
    var url = "/api/contracts/";

    var params = {
        'duns': URLManager.getDUNS(),
        'page': data['page'], 
    };
    
    if (data['naics'] && data['naics'] != 'all'){ 
        params['naics'] = RequestsManager.stripSubCategories(data['naics']); 
    }

    if (data['direction']) { params['direction'] = data['direction'] }
    if (data['sort']) { 
        params['sort'] = data['sort'] 
        if (!data['direction']) {
            params['direction'] = 'desc'
        }
    }

    RequestsManager.getAPIRequest(url, params, function(resp_data){
        Events.publish('contractDataLoaded', resp_data, data['listType'], data['page']);
    });
};

RequestsManager.stripSubCategories = function(naics_code) {
    //if last character in naics code isn't a number, strip it out
    if (isNaN(naics_code.slice(-1))) {
        //strip it
        naics_code = naics_code.substring(0, naics_code.length - 1);
    }
    return naics_code
}
