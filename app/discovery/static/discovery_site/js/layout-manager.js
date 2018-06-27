
var LayoutManager = {
    initializers: {},

    init: function() {
        if (URLManager.isHomePage() || URLManager.isPoolPage()) {
            EventManager.subscribe('vehicleChanged', this.toggleZones.bind(LayoutManager));
            EventManager.subscribe('poolUpdated', this.updatePoolInfo.bind(LayoutManager));
            EventManager.subscribe('poolSelected', this.updatePoolInfo.bind(LayoutManager));
            EventManager.subscribe('contentChanged', this.updateResultsInfo.bind(LayoutManager));
        }
        EventManager.subscribe('dataLoaded', this.render.bind(LayoutManager));

        for(var handler in this.initializers){
            this.initializers[handler].call(this);
        }
    },

    route: function(data) {
    },

    render: function(results) {
    },

    enableVehicles: function() {
        $("div#vehicle_select select").attr("disabled", false);
    },

    disableVehicles: function() {
        $("div#vehicle_select select").attr("disabled", true);
    },

    enablePools: function() {
        $("div#pool_select select").attr("disabled", false);
    },

    showPools: function() {
        $("div#pool_select").show();
    },

    disablePools: function() {
        $("div#pool_select select").attr("disabled", true);
    },

    hidePools: function() {
        $("div#pool_select").hide();
    },

    zoneActive: function() {
        var vehicle = InputHandler.getVehicle();

        if (vehicle && vehicle.match(/^BMO/i)) {
            return true;
        }
        else {
            return false;
        }
    },

    enableZones: function() {
        if (this.zoneActive()) {
            $("div#zone_select select").attr("disabled", false);
        }
    },

    showZones: function() {
        $("div#zone_select").show();
    },

    disableZones: function() {
        $("div#zone_select select").attr("disabled", true);
    },

    hideZones: function() {
        $("div#zone_select").hide();
    },

    toggleZones: function() {
        if (this.zoneActive()) {
            this.enableZones();
            this.showZones();
        }
        else {
            this.hideZones();
            this.disableZones();
        }
    },

    enableFilters: function() {
        $('#choose_filters').removeClass('filter_text_disabled').addClass('filter_text');
        $('.pure-checkbox-disabled').removeClass('pure-checkbox-disabled');
        $('.se_filter').attr("disabled", false);
    },

    disableFilters: function() {
        $('#choose_filters').removeClass('filter_text').addClass('filter_text_disabled');
        $('.pure-checkbox').addClass('pure-checkbox-disabled');
        $('.se_filter').attr("disabled", true);
    },

    updateResultsInfo: function(results) {
        var totalResults, totalPools, resultsStr;
        if (results['count'] == 0) {
            totalResults = 0;
            totalPools = 0;
        }
        else {
            totalResults = results['count'].toString();
            totalPools = results['results'].length;
        }
        resultsStr = totalResults + " vendors match your search";

        URLManager.updateResultCSVURL(results);

        $("#number_of_results span").text(resultsStr);
    },

    updatePoolInfo: function() {
        var poolNames = [];
        var pools;

        if (RequestsManager.pool) {
            pools = [RequestsManager.pool.id];
        }
        else {
            pools = Object.keys(RequestsManager.vehiclePools).sort();
        }

        if (pools.length > 0) {
            for (var index = 0; index < pools.length; index++) {
                var pool = RequestsManager.vehiclePools[pools[index]];

                if (pools.length > 1) {
                    var url = URLManager.getURL({'vehicle': pool.vehicle, 'pool': pool.id});
                    poolNames.push('<div class="pool"><div class="spacer"/><a class="pool_filter_link" href="' + url + '"><span class="vehicle">' + pool.vehicle.split('_').join(' ') + " pool " + pool.number + ':</span><span class="title">' + pool.name + '</span></a></div>');
                }
                else {
                    poolNames.push('<div class="pool"><div class="spacer"/><span class="vehicle">' + pool.vehicle.split('_').join(' ') + " pool " + pool.number + ':</span><span class="title">' + pool.name + '</span></div>');
                }
            }
            $(".results_pool_names").html(poolNames.join(''));
        }
    },

    createDate: function(date) {
        // in IE + Safari, if we pass the date the api sends right
        // into a date object, it outputs NaN
        // http://biostall.com/javascript-new-date-returning-nan-in-ie-or-invalid-date-in-safari
        var dateArray = date.split('-'),
            i,
            len = dateArray.length - 1;
        for (i = 0; i <= len; i++) {
            dateArray[i] = parseInt(dateArray[i], 10);
        }

        return new Date(dateArray[0], dateArray[1], dateArray[2]);
    },

    formatDate: function(dateObj) {
        //returns (mm/dd/yyyy) string representation of a date object
        return dateObj.getMonth() + '/' + dateObj.getDate() + '/' + dateObj.getFullYear().toString().substring(2);
    },

    convertDate: function(oldDate) {
        if (!oldDate) return 'Unknown';
        var dateArray = oldDate.split('-');
        return dateArray[1] + '/' + dateArray[2]+ '/' + dateArray[0];
    },

    numberWithCommas: function(x) {
        return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    },

    toTitleCase: function(str) {
        // from http://stackoverflow.com/questions/5097875/help-parsing-string-city-state-zip-with-javascript
        return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();}).replace('U.s.', 'U.S.');
    }
};
