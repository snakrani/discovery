
var RequestsManager = {
    initializers: {},
    vendor: null,
    naicsPools: {},
    vehiclePools: {},
    pool: null,

    init: function() {
        if (URLManager.isHomePage() || URLManager.isPoolPage()) {
            EventManager.subscribe('vehicleChanged', this.load.bind(RequestsManager));
            EventManager.subscribe('poolChanged', this.load.bind(RequestsManager));
            EventManager.subscribe('naicsChanged', this.load.bind(RequestsManager));
            EventManager.subscribe('zoneChanged', this.load.bind(RequestsManager));
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
        var vehicle = InputHandler.getVehicle();
        var pools = RequestsManager.vehiclePools;
        var pool = InputHandler.getPool();
        var naics = InputHandler.getNAICSCode() || URLManager.getParameterByName('naics-code');
        var zone = InputHandler.getZone() || URLManager.getParameterByName('zone');
        var setasides = InputHandler.getSetasides();
        var contractPools = InputHandler.getContractPools();
        var queryData = {};

        if (vehicle && vehicle != 'all') {
            queryData['vehicle'] = vehicle;
        }
        if (contractPools.length > 0) {
            queryData['pool'] = contractPools.join(',');
        }
        else if (pool && pool in pools) {
            queryData['pool'] = pool;
        }

        if (naics && naics != 'all') {
            queryData['naics'] = naics;
        }
        if (zone && zone != 'all') {
            queryData['zone'] = zone;
        }

        if (setasides.length > 0) {
            queryData["setasides"] = setasides.join(',');
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
