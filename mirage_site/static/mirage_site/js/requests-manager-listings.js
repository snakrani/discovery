// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Strict_mode
'use strict';

// for pool and vendor lists pages
// anything under url /pool
RequestsManager.load = function() {
    var url = "/api/vendors/";
    var queryData = this.buildRequestQuery();

    $.getJSON(url, queryData, function(data) {
        var resultsObj = {}; 

        if (data.num_results !== 0) {
            resultsObj.vehicle = data['results'][0]['vehicle'].toLowerCase();
            resultsObj.poolNumber = data['results'][0]['number'];
            resultsObj.samLoad = data.sam_load;
            resultsObj.total = data.num_results;
            resultsObj.results = data.results;
            resultsObj.naics = queryData['naics'];
        }

        Events.publish('dataLoaded', resultsObj);
    });
};
