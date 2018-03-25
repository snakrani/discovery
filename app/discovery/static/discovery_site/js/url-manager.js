
var URLManager = {
    title: 'Discovery',

    init: function() {
        EventManager.subscribe('vehicleChanged', this.update.bind(URLManager));
        EventManager.subscribe('naicsChanged', this.update.bind(URLManager));
        EventManager.subscribe('contentChanged', this.update.bind(URLManager));

        this.initFromQS();
    },

    initFromQS: function() {
        var vehicle = this.getParameterByName('vehicle');
        var naics = this.getParameterByName('naics-code');
        var setasides = this.getParameterByName('setasides');
        var data = {};

        if (vehicle) {
            data['vehicle'] = vehicle;
        }
        if (naics) {
            data['naics-code'] = naics;
        }
        if (setasides) {
            data['setasides'] = setasides;
        }

        LayoutManager.route(data);
        EventManager.publish('loadPage', data);
    },

    update: function(results) {
        History.pushState('', this.title, this.getURL());
    },

    getQueryString: function() {
        var queryObject = RequestsManager.buildRequestQuery();
        var qs = '?';
        var k;

        // these aren't needed for query string, included for requestquery.
        delete queryObject.group;
        delete queryObject.pool;

        if('naics' in queryObject) {
            queryObject['naics-code'] = queryObject.naics;
            delete queryObject.naics;
        }

        for (k in queryObject) {
            if (queryObject[k]) {
                qs += k + '=' + queryObject[k] + '&';
            }
        }
        return qs;
    },

    getParameterByName: function(name) {
        // http://stackoverflow.com/questions/901115/how-can-i-get-query-string-values-in-javascript
        name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
        var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
            results = regex.exec(location.search);
        return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
    },

    getURL: function() {
        return window.location.pathname + this.getQueryString();
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

    getPoolInfo: function() {
        var pathArray = window.location.href.split('/').removeEmpties();
        var poolStart = $.inArray('pool', pathArray);

        if (poolStart !== -1) {
            return {'vehicle': pathArray[poolStart + 1], 'pool_number': pathArray[poolStart + 2]};
        }
        else {
            return null;
        }
    },

    getPool: function() {
        var poolInfo = this.getPoolInfo();

        if (poolInfo !== null){
            return [poolInfo['vehicle'] + '_' + poolInfo['pool_number'], poolInfo['vehicle']];
        }
        else {
            return null;
        }
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
