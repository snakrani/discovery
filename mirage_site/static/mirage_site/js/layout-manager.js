// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Strict_mode
'use strict';

var LayoutManager = {
    init: function() {
        Events.subscribe('dataLoaded', this.render.bind(LayoutManager));
        Events.subscribe('contentChanged', this.updateSAM.bind(LayoutManager));
        Events.subscribe('contentChanged', this.updateResultsInfo);
    },

    updateSAM: function(results) {
        if ($.isEmptyObject(results) === false) {
            var dateObj = this.createDate(results['samLoad']);
            $("#sam_load").text("SAM data updated: " + (dateObj.getMonth()) + '/' + dateObj.getDate() + '/' + dateObj.getFullYear().toString().substring(2));
        }
    },

    updateResultsInfo: function(results) {
        var totalResults, totalPools, resultsStr;
        if (results['total'] == 0) {
            totalResults = 0;
            totalPools = 0;
        }
        else {
            totalResults = results.total.toString();
            totalPools = results.results.length;
        }

        if (totalPools === 1) {
            resultsStr = totalResults + " vendors match your search";
        } 
        else {
            resultsStr =  totalResults + " vendors in " + totalPools + " pool(s) match your search";
        }

        console.log(results);
        $(".results_pool_name_number_pool").text("Pool " + results.poolNumber + ": ");
        $(".results_pool_name_number_description").text(results.poolName);
        URLManager.updateResultCSVURL(results);

        $("#number_of_results span").text(resultsStr);
        $("#your_search").text($("#naics-code option:selected").text());
        $("#your_filters").text(
            $("#setaside-filters input:checkbox:checked").map(function() {
                return $(this).parent().text();
            }).get().join(', ')
        );

        $("#your_search_criteria").show();
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

    toTitleCase: function(str) {
        // from http://stackoverflow.com/questions/5097875/help-parsing-string-city-state-zip-with-javascript
        return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
    }
};
