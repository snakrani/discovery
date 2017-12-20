// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Strict_mode
'use strict';
 
RequestsManager.indexInit = function(original) {
    original.bind(RequestsManager).call();
    
    this.loadMetadata();
};
 
RequestsManager.originalInit = RequestsManager.init;
 
RequestsManager.init = function() {
    RequestsManager.indexInit(RequestsManager.originalInit);
};
 
RequestsManager.loadMetadata = function() {
    var url = "/api/metadata/";
    RequestsManager.getAPIRequest(url, {}, function(data) {
        var resultsObj = data; 
        Events.publish('metaDataLoaded', resultsObj);
    });
};
