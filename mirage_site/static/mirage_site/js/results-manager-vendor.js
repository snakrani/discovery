ResultsManager.load = function() {
    /* get vendor info from api */

    var url = "/api/vendor/" + URLManager.getDUNS() + "/";
    
    $.getJSON(url, function(data){
debugger;
        Events.publish('dataLoaded', data);
    });
};
