
RequestsManager.initializers.index = function() {
    this.loadMetadata();
};

RequestsManager.loadMetadata = function() {
    var url = "/api/metadata/";
    RequestsManager.getAPIRequest(url, {}, function(data) {
        var resultsObj = data;
        Events.publish('metaDataLoaded', resultsObj);
    });
};
