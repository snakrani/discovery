// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Strict_mode
'use strict';

var LayoutManager = {
    init: function() {
        Events.subscribe('dataLoaded', this.render.bind(LayoutManager));
        Events.subscribe('contentChanged', this.updateSAM);
        Events.subscribe('contentChanged', this.updateResultsInfo);
        Events.subscribe('contentChanged', this.updateBreadcrumb);
    },

    render: function(results) {
        if (results.results.length > 1) {
            this.renderPools(results);
            Events.publish('contentChanged', results);
        }
        else {
            if (URLManager.getParameterByName('naics') === InputHandler.getNAICSCode()) {
                this.renderTable(results);
            }
            else {
                Events.publish('goToPoolPage', results);
            }
        }
    },

    renderTable: function(results) {
        var t = $('#pool_vendors');
        var i, len = results.results[0].vendors.length - 1;

        for (i = 0; i <= len; i++) {
            t.append(this.renderRow(results.results[0].vendors[i]));
        }

        $('#pool_table').show();
        Events.publish('contentChanged', results);
    },

    renderRow: function(v) {
        var location_col;
        var $vendorRow = $('<tr></tr>');

        var name_col = $('<td class="vendor_name"></td>');
        var name_a = $('<a href="/vendor/' + v.duns + '/" class="link_style">' + v.name + '</a>');
        name_col.append(name_a);
        $vendorRow.append(name_col);

        location_col = $('<td class="vendor_location">' + v.sam_citystate + '</td>');
        $vendorRow.append(location_col);

        //add socio-economic columns
        $vendorRow.append(this.renderColumn(v, 'vo', 'A5'));
        $vendorRow.append(this.renderColumn(v, 'sdb', '27'));
        $vendorRow.append(this.renderColumn(v, 'sdvo', 'QF'));
        $vendorRow.append(this.renderColumn(v, 'wo', 'A2'));

        return $vendorRow;
    },

    renderColumn: function(v, prefix, setasideCode) {
        var $col = $('<td class="' + prefix + '"></td>');
        if (this.findIndicatorMatch(v, prefix, setasideCode)) {
            $col.text('X');
        }

        return $col;
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

    findIndicatorMatch: function(v, prefix, setasideCode) {
        var i, len = v['setasides'].length - 1;

        if (v['setasides'].length > 0) {
            for (var i=0; i <= len; i++) {
                if (v['setasides'][i]['code'] == setasideCode) {
                    return true;
                }
            }
        }

        return false;
    },

    updateBreadcrumb: function(results) {
        //remove old seach results breadcrumb
        $('#sr').remove();

        //create new breadcrumb for search results
        $('#crumbs').append('<li id="sr"><a href="#">Search Results</a></li>');
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
    }
};
