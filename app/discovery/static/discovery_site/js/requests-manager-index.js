
RequestsManager.initializers.index = function() {
    EventManager.subscribe('poolUpdated', this.loadMetadata.bind(RequestsManager));
};

RequestsManager.loadMetadata = function() {
    var url = "/api/metadata/";

    RequestsManager.getAPIRequest(url, {}, function(data) {
        EventManager.publish('dataLoaded', data);
    });
};
