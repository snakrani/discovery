// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Strict_mode
'use strict';

// for pool and vendor lists pages
// anything under url /pool
RequestsManager.load = function() {
    var url = "/api/vendors/";
    var queryData = this.buildRequestQuery();
   
    if (queryData['naics'] !== "") {

        RequestsManager.getAPIRequest(url, queryData, function(data) {
            var resultsObj = {}; 

            resultsObj.poolNumber = data['pool'][0]['number'];
            resultsObj.poolName = data['pool'][0]['name'];
            resultsObj.samLoad = data.sam_load;
            resultsObj.total = 0; //overwritten below if there are any

            if (data.num_results !== 0) {
                resultsObj.vehicle = data['pool'][0]['vehicle'].toLowerCase();
                resultsObj.numPools = data.results.length;
                resultsObj.total = data.num_results;
                resultsObj.results = data.results;
                resultsObj['naics-code'] = queryData['naics-code'];
            }         
            Events.publish('dataLoaded', resultsObj);
        });
    };
};
