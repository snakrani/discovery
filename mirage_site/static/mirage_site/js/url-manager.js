// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Strict_mode
'use strict';

var URLManager = {
    init: function() {
        var naics = this.getParameterByName('naics');
        var setasides = this.getParameterByName('setasides');

        if (naics || setasides) {
            Events.publish('loadedWithQS', {'naics': naics, 'setasides': setasides});
        }

        Events.subscribe('contentChanged', this.update.bind(URLManager));
        Events.subscribe('goToPoolPage', this.loadPoolPage.bind(URLManager));
    },

    getQueryString: function() {
        var queryObject = ResultsManager.buildRequestQuery();
        var qs = '?';
        var k;

        for (k in queryObject) {
            qs += k + '=' + queryObject[k] + '&';
        }

        return qs;
    },

    getURL: function(results) {
        var qs = this.getQueryString();
        var vehicle = results.vehicle;
        var poolNumber = results.poolNumber;

        return '/pool/' + vehicle + '/' + poolNumber + '/' + qs;
    },

    update: function(results) {
        window.history.pushState(true, true, this.getURL(results));
    },

    loadPoolPage: function(results) {
        window.location.href = this.getURL(results);
    },

    getPoolInfo: function() {
        //extract pool information from document url
        var pathArray = window.location.href.split('/');
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
    }
};
