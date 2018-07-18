
var DataManager = {
    initializers: {},
    preprocessors: {},
    fields: {},

    title: 'Discovery',

    vehicleMap: {
        "OASIS_SB": {
            "title": "OASIS Small Business",
            "sb": true
        },
        "OASIS": {
            "title": "OASIS Unrestricted",
            "sb": false
        },
        "HCATS_SB": {
            "title": "HCATS Small Business",
            "sb": true
        },
        "HCATS": {
            "title": "HCATS Unrestricted",
            "sb": false
        },
        "BMO_SB": {
            "title": "BMO Small Business",
            "sb": true
        },
        "BMO": {
            "title": "BMO Unrestricted",
            "sb": false
        },
        "PSS": {
            "title": "Professional Services",
            "sb": true
        }
    },

    init: function() {
        DataManager.collect('page', 1);
        DataManager.collect('count');
        DataManager.collect('ordering');

        EventManager.subscribe('pageUpdated', DataManager.bootstrap);

        for (var handler in DataManager.initializers){
            DataManager.initializers[handler].call(this);
        }
    },

    update: function() {
        History.pushState('', DataManager.title, DataManager.getURL());
        EventManager.publish('pageUpdated');
    },

    bootstrap: function() {
        DataManager.runningStatus();

        // Preprocessing
        for (var handler in DataManager.preprocessors){
            DataManager.preprocessors[handler].call(this);
        }
        LayoutManager.execPreprocessors();

        // Routing / Broadcast
        LayoutManager.route();
        EventManager.publish('pageInitialized');
    },

    sendDataInitialized: function() {
        EventManager.publish('dataInitialized');
    },

    buildRequestQuery: function() {
        var page = DataManager.getPage();
        var pageCount = DataManager.getPageCount();
        var sortOrdering = DataManager.getSortOrdering();
        var queryData = {};

        if (page && page > 1) {
            queryData['page'] = page;
        }
        if (pageCount && pageCount != DataManager.getPageCount()) {
            queryData['count'] = pageCount;
        }

        if (sortOrdering) {
            queryData['ordering'] = sortOrdering;
        }

        if (DataManager.getParameterByName('test')) {
            queryData['test'] = 'true';
        }

        return DataManager.requestParams(queryData);
    },

    requestParams: function(queryData) {
        return queryData;
    },

    get: function(field, defaultValue) {
        if (! defaultValue) {
            defaultValue = null;
        }

        if (! (field in DataManager.fields)) {
            return defaultValue;
        }
        return DataManager.fields[field];
    },

    collect: function(field, defaultValue, preprocessor) {
        if (! defaultValue) {
            defaultValue = null;
        }

        var value = DataManager.getParameterByName(field);

        if (preprocessor && typeof preprocessor == 'function') {
            value = preprocessor.call(field, value);
        }

        if (value) {
            DataManager.fields[field] = value;
        }
    },

    set: function(field, value) {
        if (value && (typeof value != 'string' || value != 'all')) {
            DataManager.fields[field] = value;
        }
        else {
            DataManager.fields[field] = null;
        }
    },

    runningStatus: function() {
        console.log("<<<Running>>>");
        $('#site_status').text('running');
    },

    completeStatus: function() {
        console.log("<<<<Complete>>>>");
        $('#site_status').text('complete');
    },

    getVehicleMap: function() {
        return DataManager.vehicleMap;
    },

    setPage: function(value) {
        DataManager.set('page', value);
    },

    getPage: function() {
        return DataManager.get('page', 1);
    },

    setPageCount: function(count) {
        DataManager.set('count', value);
    },

    getPageCount: function() {
        var defaultCount = 50;

        if (DataManager.getParameterByName('test')) {
            defaultCount = 5;
        }
        return DataManager.get('count', defaultCount);
    },

    setSortOrdering: function(value) {
        DataManager.set('ordering', value);
    },

    getSortOrdering: function() {
        return DataManager.get('ordering', null);
    },

    getOrderingField: function(param) {
        var classMap = DataManager.sortClassMap();

        for (var field in classMap) {
            if (classMap[field] == param) {
                return field;
            }
        }
        return null;
    },

    getParameterByName: function(name) {
        name = name.replace(/[*+?^$.\[\]{}()|\\\/]/g, "\\$&"); // escape RegEx meta chars
        var match = location.search.match(new RegExp("[?&]"+name+"=([^&]+)(&|$)"));
        return match && decodeURIComponent(match[1].replace(/\+/g, " "));
    },

    getURL: function(params) {
        return window.location.pathname + DataManager.getQueryString(params);
    },

    getQueryString: function(params) {
        var queryObject = DataManager.buildRequestQuery();
        var qs = '?';
        var k;

        if (params !== undefined) {
            for (key in params) {
                if (params[key] !== null) {
                    queryObject[key] = params[key];
                }
                else {
                    delete queryObject[key];
                }
            }
        }

        for (k in queryObject) {
            if (queryObject[k]) {
                qs += k + '=' + queryObject[k] + '&';
            }
        }

        return qs;
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
