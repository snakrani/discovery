ResultsManager.vendorInit = function(original) {
    Events.subscribe('vendorInfoLoaded', this.loadContracts.bind(ResultsManager));

    return function() {
        original();
    }
};

ResultsManager.init = function() {
    ResultsManager.vendorInit(ResultsManager.init);
};

ResultsManager.load = function() {
    /* get vendor info from api */

    var url = "/api/vendor/" + URLManager.getDUNS() + "/";
    
    $.getJSON(url, function(data){
        Events.publish('dataLoaded', data);
    });
};

ResultsManager.loadContracts = function() {
    var url = "/api/contracts/";
    var params = {
        'duns': URLManager.getDUNS(),
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
