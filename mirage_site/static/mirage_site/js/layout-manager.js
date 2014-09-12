// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Strict_mode
'use strict';

var LayoutManager = {
    init: function() {
        Events.subscribe('dataLoaded', this.render.bind(LayoutManager));
        Events.subscribe('contentChanged', this.updateSAM);
        Events.subscribe('contentChanged', this.updateResultsInfo);
        Events.subscribe('contentChanged', this.updateBreadcrumb);
    },

    // this is turning into something of a router
    // should be refactored [TS]
    render: function(results) {
        // if multiple pools should be rendered
        if (results.results.length > 1) {
            this.renderPools(results);
            Events.publish('contentChanged', results);
        }
        else {
            // if this is a vendor list page and the page has already been reloaded
            if (URLManager.getParameterByName('naics') === InputHandler.getNAICSCode()) {
                this.Pool.renderTable(results);
            }
            else {
                // if this is a vendor list page and we need to reload to get the template
                Events.publish('goToPoolPage', results);
            }
        }
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
        var dateObj = new Date(results['samLoad']);
        $("#sam_load").text("SAM data updated: " + (dateObj.getMonth() + 1) + '/' + dateObj.getDate() + '/' + dateObj.getFullYear().toString().substring(2));
    },

    updateResultsInfo: function(results) {
        $("#number_of_results span").text(results.total.toString() + " vendors in " + results.results.length + " pool(s) match your search");
        $("#your_search").text($("#naics-code option:selected").text());
        $("#your_filters").text(
            $("#setaside-filters input:checkbox:checked").map(function() {
                return $(this).parent().text();
            }).get().join(', ')
        );
        $("#your_search_criteria").show();
    },

};
