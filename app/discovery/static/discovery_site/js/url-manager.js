
var URLManager = {
    title: 'Discovery',

    init: function() {
        EventManager.subscribe('vehicleChanged', this.update.bind(URLManager));
        EventManager.subscribe('poolSelected', this.update.bind(URLManager));
        EventManager.subscribe('naicsChanged', this.update.bind(URLManager));
        EventManager.subscribe('zoneChanged', this.update.bind(URLManager));
        EventManager.subscribe('contentChanged', this.update.bind(URLManager));
        EventManager.subscribe('contractsChanged', this.update.bind(URLManager));

        this.initFromQS();
    },

    initFromQS: function() {
        var vehicle = this.getParameterByName('vehicle');
        var pool = this.getParameterByName('pool');
        var naics = this.getParameterByName('naics-code');
        var zone = this.getParameterByName('zone');
        var setasides = this.getParameterByName('setasides');
        var data = {};

        if (vehicle) {
            data['vehicle'] = vehicle;
        }
        if (pool) {
            data['pool'] = pool;
        }
        if (naics) {
            data['naics-code'] = naics;
        }
        if (zone) {
            data['zone'] = zone;
        }
        if (setasides) {
            data['setasides'] = setasides;
        }

        LayoutManager.route(data);
        EventManager.publish('loadPage', data);
    },

    update: function() {
        History.pushState('', this.title, this.getURL());
        EventManager.publish('pageUpdated');
    },

    getQueryString: function(params) {
        var queryObject = RequestsManager.buildRequestQuery();
        var qs = '?';
        var k;

        if('naics' in queryObject) {
            queryObject['naics-code'] = queryObject.naics;
            delete queryObject.naics;
        }

        if (params !== undefined) {
            for (key in params) {
                queryObject[key] = params[key];
            }
        }

        for (k in queryObject) {
            if (queryObject[k]) {
                qs += k + '=' + queryObject[k] + '&';
            }
        }

        return qs;
    },

    getParameterByName: function(name) {
        name = name.replace(/[*+?^$.\[\]{}()|\\\/]/g, "\\$&"); // escape RegEx meta chars
        var match = location.search.match(new RegExp("[?&]"+name+"=([^&]+)(&|$)"));
        return match && decodeURIComponent(match[1].replace(/\+/g, " "));
    },

    getURL: function(params) {
        return window.location.pathname + this.getQueryString(params);
    },

    updateResultCSVURL: function(results) {
        var qs = this.getQueryString();
        //generate csv link (sloppy)
        $("#csv_link").attr("href", "/results/csv/" + qs );
    },

    updateVendorCSVURL: function() {
        var url = document.location.href;
        var pathArray = url.split('/');

        if (url.indexOf("/?") == -1) {
            pathArray.pop();
        }
        pathArray.splice(5, 0, "csv");

        $("#csv_link").attr("href", pathArray.join('/'));
    },

    getDUNS: function() {
        var pathArray = window.location.pathname.split('/');
        pathArray = pathArray.removeEmpties();

        for (var i = 0; i < pathArray.length; i++) {
            if (!isNaN(pathArray[i])) {
                return pathArray[i];
            }
        }
        return false;
    },

    stripSubCategories: function(naics_code) {
        //if last character in naics code isn't a number, strip it out
        if (isNaN(naics_code.slice(-1))) {
            //strip it
            naics_code = naics_code.substring(0, naics_code.length - 1);
        }
        return naics_code;
    },

    isHomePage: function() {
        var pathArray =  window.location.pathname.split('/').join('').split('');

        if (pathArray.length == 0) {
            return true;
        }
        else {
            return false;
        }
    },

    isPoolPage: function() {
        var pathArray =  window.location.pathname.split('/');

        if ($.inArray('results', pathArray) !== -1) {
            return true;
        }
        else {
            return false;
        }
    },

    isVendorPage: function() {
        var pathArray =  window.location.pathname.split('/').join('').split('');

        if ($.inArray('vendor', pathArray) !== -1) {
            return true;
        }
        else {
            return false;
        }
    }
};
