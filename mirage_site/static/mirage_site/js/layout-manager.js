// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Strict_mode
'use strict';

var LayoutManager = {
    init: function() {
        Events.subscribe('dataLoaded', this.render.bind(LayoutManager));
        Events.subscribe('contentChanged', this.updateSAM.bind(LayoutManager));
        Events.subscribe('contentChanged', this.updateResultsInfo);
        Events.subscribe('contentChanged', this.updateBreadcrumb);
    },

    renderPools: function(results) {
        var $container = $('#custom_page_content');
        //clear out content
        $container.find('.column').remove();

        for (var i in results.results) {
            var obj = results.results[i];
            var $poolLink, $poolHeader; 
            var $div = $('<div class="column post-header"></div>');
            var qs = URLManager.getQueryString();

            $poolLink = $('<a class="pool_link" href="/pool/' + obj['vehicle'].toLowerCase() + '/' + obj['number'] + '/' + qs + '">Pool' + obj['number'] + '</a>');
            $poolLink.text();
           
            $poolHeader = $('<h2 class="pool_title"></h2>');
            $poolHeader.append($poolLink);
            $div.append($poolHeader);
            
            $div.append('<p class="post-meta number_of_vendors_in_pool">' + obj['vendors'].length.toString() + ' vendors</p>');

            for (var v in obj['vendors']){
                $div.append('<p class="vendor_names">' + obj['vendors'][v]['name'] + '</p>');
            }

            $container.append($div);
        }
    },

    updateBreadcrumb: function(results) {
        //remove old seach results breadcrumb
        $('#sr').remove();

        // pool pages load with breadcrumbs
        if ($('#crumbs').children().length <= 1) {
            //create new breadcrumb for search results
            $('#crumbs').append('<li id="sr"><a href="#">Search Results</a></li>');
        }
    },

    updateSAM: function(results) {
        if ($.isEmptyObject(results) === false) {
            var dateObj = this.createDate(results['samLoad']);
            $("#sam_load").text("SAM data updated: " + (dateObj.getMonth()) + '/' + dateObj.getDate() + '/' + dateObj.getFullYear().toString().substring(2));
        }
    },

    updateResultsInfo: function(results) {
        var totalResults, totalPools;
        if ($.isEmptyObject(results)) {
            totalResults = 0;
            totalPools = 0;
        }
        else {
            totalResults = results.total.toString();
            totalPools = results.results.length;
        }

        $("#number_of_results span").text( totalResults + " vendors in " + totalPools + " pool(s) match your search");
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
