// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Strict_mode
'use strict';
 
RequestsManager.indexInit = function(original) {
    original.bind(RequestsManager).call();
    
    this.load();
 
};
 
RequestsManager.originalInit = RequestsManager.init;
 
RequestsManager.init = function() {
    RequestsManager.indexInit(RequestsManager.originalInit);
};
 
RequestsManager.load = function() {
    var url = "/api/metadata/";
 
    $.getJSON(url, function(data) {
        var resultsObj = data; 
        Events.publish('dataLoaded', resultsObj);
    });
};