RequestsManager.vendorInit = function(original) {
    Events.subscribe('vendorInfoLoaded', this.loadContracts.bind(RequestsManager));
    Events.subscribe('contractsRefreshed', this.refreshContracts.bind(RequestsManager));
    original.bind(RequestsManager).call();
};

RequestsManager.originalInit = RequestsManager.init;

RequestsManager.init = function() {
    RequestsManager.vendorInit(RequestsManager.originalInit);
};

RequestsManager.load = function() {
    /* get vendor info from api */
 
    var url = "/api/vendor/" + URLManager.getDUNS() + "/";
    
    $.getJSON(url, function(data){
        Events.publish('dataLoaded', data);
        Events.publish('vendorInfoLoaded');
    });
};

RequestsManager.loadContracts = function() {
    var url = "/api/contracts/";
    var params = {
        'duns': URLManager.getDUNS()
    };

    
    naics = URLManager.getParameterByName('naics-code');
    
    if (naics && naics != 'all'){ 
        params['naics'] = naics; 
    }

    $.getJSON(url, params, function(data){
        Events.publish('contractDataLoaded', data);
    });

};

//no idea why, but if I integrate the updated_naics parameter into the above function it becomes an infinite loop -- KBD
RequestsManager.refreshContracts = function(updated_naics) {
    var url = "/api/contracts/";
    var params = {
        'duns': URLManager.getDUNS()
    };
    
    if (updated_naics && updated_naics != 'all'){ 
        params['naics'] = naics; 
    }

    $.getJSON(url, params, function(data){
        Events.publish('contractDataLoaded', data);
    });
};
