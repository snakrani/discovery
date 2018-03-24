// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Strict_mode
'use strict';

var RequestsManager = {
    initializers: {},

    init: function() {
        Events.subscribe('naicsChanged', this.load.bind(RequestsManager));
        Events.subscribe('vehicleChanged', this.load.bind(RequestsManager));
        Events.subscribe('filtersChanged', this.load.bind(RequestsManager));
        Events.subscribe('loadedWithQS', this.load.bind(RequestsManager));

        for(var handler in this.initializers){
            this.initializers[handler].call(this);
        }
    },

    getPageCount: function() {
        if (URLManager.getParameterByName('test')) {
            return 5;
        }
        return 100;
    },

    getAPIRequest: function(url, params, callback) {
        url = APIHOST + url;

        var responder = function(data) {
          console.log(" > results: %s %o -> %o", url, params, data);
          return callback(data);
        };

        console.log("URL: %s %o", url, params);
        return $.ajax({
              url: url,
              dataType: 'json',
              data: params
            })
            .done(responder)
            .fail(function(req, status, error) {
              if (!window.console) return;
              console.log('Failed to load: ', url);
              console.log(error);
            });
    },

    buildRequestQuery: function() {
        var setasides = InputHandler.getSetasides();
        var naicsCode = InputHandler.getNAICSCode() || URLManager.getParameterByName('naics-code');
        var vehicle = InputHandler.getVehicle();
        var queryData = {};
        var pool = this.getPool();

        if (typeof naicsCode !== 'undefined') {
            queryData['naics'] = naicsCode;
        }

        if (setasides.length > 0) {
            queryData["setasides"] = setasides.join(',');
        }
        if (pool !== null) {
            queryData['pool'] = pool[0];
            queryData['vehicle'] = pool[1];
        }
        if (vehicle !== null) {
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


    getPool: function() {
        var poolInfo = URLManager.getPoolInfo();

        if (poolInfo !== null){
            return [poolInfo['vehicle'] + '_' + poolInfo['pool_number'], poolInfo['vehicle']];
        }
        else {
            return null;
        }
    }

};
