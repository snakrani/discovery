
DataManager.initializers.index = function() {
    DataManager.initSearch();

    // Internal event subscriptions
    EventManager.subscribe('pageInitialized', DataManager.loadMetadata);
};

DataManager.loadMetadata = function() {
    var url = "/api/metadata/";

    DataManager.getAPIRequest(url, {}, function(data) {
        EventManager.publish('metadataLoaded', data);
    });
};
