
var RequestsManager = {
    initializers: {},

    init: function() {
        EventManager.subscribe('dataChanged', this.load.bind(RequestsManager));

        for(var handler in this.initializers){
            this.initializers[handler].call(this);
        }
    },

    load: function() {
    },

    getAPIRequest: function(url, params, success_callback, error_callback) {
        url = APIHOST + url;

        return CacheService.get({
              url: url,
              data: params,
              dataType: 'json'
            })
            .done(function(data) {
                // Just in case...
                success_callback(data);
            })
            .fail(function(req, status, error) {
              if (error_callback) {
                error_callback(req, status, error);
              }
              if (!window.console) return;
              console.log('Failed to load: ', url);
              console.log(error);
            });
    }
};
