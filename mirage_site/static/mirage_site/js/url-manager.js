// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Strict_mode
//
'use strict';

var URLManager = {
    init: function() {
        var naics = this.getParameterByName('naics-code');
        var setasides = this.getParameterByName('setasides');
        var vendor = URLManager.isVendorPage();

        // this + LayoutManager.render() are acting as a kind of router. should probably be rethought. [TS]
        if (naics || setasides || vendor) {
            Events.publish('loadedWithQS', {'naics-code': naics, 'setasides': setasides});
        }

        Events.subscribe('contentChanged', this.update.bind(URLManager));
        Events.subscribe('goToPoolPage', this.loadPoolPage.bind(URLManager));
    },

    getQueryString: function() {
        var queryObject = RequestsManager.buildRequestQuery();
        var qs = '?';
        var k;

        // these aren't needed for query string, included for requestquery.
        delete queryObject.group;
        delete queryObject.pool;

        // the API wants "naics", the query string should have "naics-code"
        queryObject['naics-code'] = queryObject.naics;
        delete queryObject.naics;

        for (k in queryObject) {
            qs += k + '=' + queryObject[k] + '&';
        }

        return qs;
    },

    getURL: function(results) {
        var qs = this.getQueryString();
        var vehicle, poolNumber, pathArray, numPools, empty;

        if ($.isEmptyObject(results)) {
            pathArray = window.location.href.split('/').removeEmpties();
            if (pathArray.length > 3) {
                vehicle = pathArray[3];
                poolNumber = pathArray[4];
            }
            else {
                empty = true;
            }
        }
        else {
            vehicle = results.vehicle;
            if (typeof results.poolNumber !== 'undefined') {
                poolNumber = results.poolNumber;
            }

            if (typeof results.numPools !== 'undefined') {
                numPools = results.numPools;
            }
        }

        if (numPools || empty) {
            return qs;
        }
        else {
            return '/pool/' + vehicle + '/' + poolNumber + '/' + qs;
        }
    },

    update: function(results) {
        window.history.pushState(true, true, this.getURL(results));
    },

    loadPoolPage: function(results) {
        window.location.href = this.getURL(results);
    },

    getPoolInfo: function() {
        //extract pool information from document url
        var pathArray = window.location.href.split('/').removeEmpties();
        var poolStart = $.inArray('pool', pathArray);

        if (poolStart !== -1) {
            return {'vehicle': pathArray[poolStart + 1], 'pool_number': pathArray[poolStart + 2]};
        }
        else {
            return null;
        }
    },

    getParameterByName: function(name) {
        // http://stackoverflow.com/questions/901115/how-can-i-get-query-string-values-in-javascript
        name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
        var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
            results = regex.exec(location.search);
        return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
    },

    getDUNS: function() {
        //extract pool information from document url
        var pathArray = window.location.href.split('/');
        pathArray = pathArray.removeEmpties();
        var i = pathArray.length - 1;

        while (i--) {
            if (parseInt(pathArray[i], 10) !== NaN) {
                return pathArray[i];
            }
        }

        return false;
    },

    isVendorPage: function() {
        var pathArray =  window.location.href.split('/');

        if ($.inArray('vendor', pathArray) !== -1) {
            return true;
        }
        else {
            return false;
        }
    } 
};
