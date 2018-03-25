
RequestsManager.loadMetadata = function() {
    var url = "/api/metadata/";

    RequestsManager.getAPIRequest(url, {}, function(data) {
        EventManager.publish('dataLoaded', data);
    });
};

RequestsManager.load = function() {
    this.loadMetadata();
};
