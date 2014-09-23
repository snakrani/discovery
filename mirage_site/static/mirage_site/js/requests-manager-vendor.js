RequestsManager.vendorInit = function(original) {
    Events.subscribe('vendorInfoLoaded', this.loadContracts.bind(RequestsManager));

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
    });
};

RequestsManager.loadContracts = function() {
    var url = "/api/contracts/";
    var params = {
        'duns': URLManager.getDUNS()
    };

    var naics = URLManager.getParameterByName('naics-code');
    if (naics && naics != 'all'){ 
        params['naics'] = naics; 
        $("span.vendor_contract_history_naics").text(" NAICS " + naics + ":");
    } else {
       $("span.vendor_contract_history_naics").text(" All Contracts:"); 
    }

    $.getJSON(url, params, function(data){
        Events.publish('contractDataLoaded', data);
    });

};
