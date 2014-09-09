// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Strict_mode
'use strict';

var InputHandler = {
    $codeField: $('#naics-code'),

    init: function() {
        this.populateDropDown();

        // initialize special field lib
        this.$codeField.select2({placeholder:'Select a NAICS code', dropdownAutoWidth : true});

        // event bindings
        this.$codeField.change(this.sendCodeChange.bind(InputHandler));
        $('#setaside-filters').change(this.sendFilterChange);

        Events.subscribe('loadedWithData', this.updateFields.bind(InputHandler));
    },

    updateFields: function(obj) {
        if (obj.naics !== null) {
            this.$codeField.select2('val', obj.naics);
        }

        if (obj.setasides) {
            // break out setasides and loop
            $('input[value=' + obj.setasides + ']').attr('checked', 'checked');
        }
    },
    
    sendCodeChange: function(e) {
        this.naicsCode = e.val;
        Events.publish('naicsChanged');
    },

    sendFilterChange: function(e) {
        Events.publish('filtersChanged');
    },

    getNAICSCode: function() {
        return this.naicsCode;
    },

    getSetasides: function() {
        /* returns array of setaside ids that are checked */
        var setasides = [];
        $("form#setaside-filters input:checked").each( function(index) {
            setasides.push($(this).val());
        });

        return setasides;
    },

    populateDropDown: function() {
        this.$codeField
             .append($("<option></option>")
             .attr("value", "all")
             .text("All NAICS codes")); 
        $.getJSON(
            "/api/naics/",
            { format: "json" },
            function( data ) {
                $.each(data.results, function(key, result) {   
                    $("#naics-code")
                         .append($("<option></option>")
                         .attr("value", result.short_code)
                         .text(result.short_code + " - " + result.description)); 
                });
                if (URLManager.getParameterByName("naics-code")) {
                    $("#naics-code").select2().select2("val", getParameterByName("naics-code"));
                }
                //load data if search criteria is defined in querystring
                if (URLManager.getParameterByName("naics-code") || URLManager.getParameterByName("setasides")) {
                    Events.publish('loadData');
                }
            }
        );
    }
};

var ResultsManager = {
    init: function() {
        Events.subscribe('naicsChanged', this.load.bind(ResultsManager));
        Events.subscribe('filtersChanged', this.load.bind(ResultsManager));
    },

    buildRequestQuery: function() {
        var setasides = InputHandler.getSetasides();
        var naicsCode = InputHandler.getNAICSCode();
        var queryData = {
            'group': 'pool'
        };
        var pool = this.getPool();

        if (typeof naicsCode !== 'undefined') {
            queryData['naics-code'] = naicsCode;
        }

        if (setasides.length > 0) {
            queryData["setasides"] = setasides.join();
        }
        if (pool !== null) {
            queryData['pool'] = pool;
        }

        return queryData;
    },

    load: function() {
        var url = "/api/vendors/";
        var queryData = this.buildRequestQuery();

        $.getJSON(url, queryData, function(data) {
            var resultsObj = {}; 
            console.log(data);
            resultsObj.vehicle = data['results'][0]['vehicle'].toLowerCase();
            resultsObj.poolNumber = data['results'][0]['number'];
            resultsObj.samLoad = data.sam_load;
            resultsObj.total = data.num_results;
            resultsObj.results = data.results;

            Events.publish('dataLoaded', resultsObj);
        });
    },

    getPool: function() {
        var poolInfo = URLManager.getPoolInfo();

        if (poolInfo !== null){
            if (poolInfo['vehicle'] == 'oasissb'){
                return poolInfo['pool_number'] + '_' + 'SB';
            }
            else {
                return poolInfo['pool_number']
            }
        }
        else {
            return null 
        }
    }

};

var URLManager = {
    init: function() {
        var naics = this.getParameterByName('naics-code');
        var setasides = this.getParameterByName('setasides');

        if (naics || setasides) {
            Events.publish('loadedWithData', {'naics': naics, 'setasides': setasides});
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
            Events.publish('goToPoolPage', results);
        }
    },

    renderTable: function(results) {
        var t = $('#pool_vendors');
        var i, len = results.results.length - 1;

        for (i = 0; i <= len; i++) {
            t.append(this.renderRow(results.results[0].vendors[i]));
        }
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

$(document).ready(function() {
    // http://thejacklawson.com/Mediator.js/
    window.Events = new Mediator() || {};

    InputHandler.init();
    ResultsManager.init();
    LayoutManager.init();
    URLManager.init();
});
