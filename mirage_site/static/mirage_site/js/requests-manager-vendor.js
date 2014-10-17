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
    
    $.getJSON(url, function(data){
        Events.publish('dataLoaded', data);
        Events.publish('vendorInfoLoaded', listType);
    });
};

RequestsManager.loadContracts = function(listType) {
    var listType = typeof listType !== 'undefined' ? listType : 'naics';
    var url = "/api/contracts/";
    var params = {
        'duns': URLManager.getDUNS()
    };

    naics = RequestsManager.stripSubCategories(URLManager.getParameterByName('naics-code'));
    
    if (naics && naics != 'all'){ 
        params['naics'] = naics;
    }

    if (listType == 'all') {
        params['naics'] = '';
    }

    $.getJSON(url, params, function(data){
        Events.publish('contractDataLoaded', data, listType);
    });

};

//no idea why, but if I integrate the updated_naics parameter into the above function it becomes an infinite loop -- KBD
RequestsManager.refreshContracts = function(updated_naics, listType) {
    var url = "/api/contracts/";
    var params = {
        'duns': URLManager.getDUNS()
    };
    
    if (updated_naics && updated_naics != 'all'){ 
        params['naics'] = naics; 
    }

    $.getJSON(url, params, function(data){
        Events.publish('contractDataLoaded', data, listType);
    });
};

RequestsManager.stripSubCategories = function(naics_code) {
    //if last character in naics code isn't a number, strip it out
    if (isNaN(naics_code.slice(-1))) {
        //strip it
        naics_code = naics_code.substring(0, naics_code.length - 1);
        console.log(naics_code);
    }
    return naics_code
}
