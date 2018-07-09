
RequestsManager.initializers.index = function() {
    EventManager.subscribe('pageInitialized', RequestsManager.loadMetadata);
};

RequestsManager.loadMetadata = function() {
    var url = "/api/metadata/";

    RequestsManager.getAPIRequest(url, {}, function(data) {
        EventManager.publish('dataLoaded', data);
    });
};
