
var RequestsManager = {
    initializers: {},

    init: function() {
        if (URLManager.isHomePage() || URLManager.isPoolPage()) {
            EventManager.subscribe('vehicleChanged', this.load.bind(RequestsManager));
            EventManager.subscribe('naicsChanged', this.load.bind(RequestsManager));
            EventManager.subscribe('filtersChanged', this.load.bind(RequestsManager));
        }
        else {
            EventManager.subscribe('loadPage', this.load.bind(RequestsManager));
        }

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
    },

    buildRequestQuery: function() {
        var setasides = InputHandler.getSetasides();
        var naicsCode = InputHandler.getNAICSCode() || URLManager.getParameterByName('naics-code');
        var vehicle = InputHandler.getVehicle();
        var pool = URLManager.getPool();
        var queryData = {};

        if (naicsCode && typeof naicsCode !== 'undefined') {
            queryData['naics'] = naicsCode;
        }

        if (setasides.length > 0) {
            queryData["setasides"] = setasides.join(',');
        }
        if (pool && typeof pool != undefined) {
            queryData['pool'] = pool[0];
            queryData['vehicle'] = pool[1];
        }
        if (vehicle && typeof vehicle != undefined) {
            queryData['vehicle'] = vehicle;
        }

        if (URLManager.getParameterByName('test')) {
            queryData['test'] = 'true';
        }
        return queryData;
    },

    currentSortParams: function() {
        var data = {};
        var class_map = RequestsManager.sortClassMap();

        $('th.arrow-down').exists(function() {
            data['ordering'] = "-" + class_map[this.attr('class').split(' ')[0]];
        });
        $('th.arrow-up').exists(function() {
            data['ordering'] = class_map[this.attr('class').split(' ')[0]];
        });
        return data;
    },

    getPageCount: function() {
        if (URLManager.getParameterByName('test')) {
            return 5;
        }
        return 100;
    }
};
