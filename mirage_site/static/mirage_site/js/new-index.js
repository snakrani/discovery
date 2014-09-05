'use strict;'

var InputHandler = {
    $codeField: $('#naics-code'),

    init: function() {
        // initialize special field lib
        this.$codeField.select2({placeholder:'Select a NAICS code', dropdownAutoWidth : true});

        // event bindings
        this.$codeField.change(this.sendCodeChange.bind(InputHandler));
        $('#setaside-filters').change(this.sendFilterChange);
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
            'group': 'pool',
            'naics': naicsCode
        };
        var pool = this.getPool();

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
        return null;
    }

};

var URLManager = {
    init: function() {
        Events.subscribe('contentChanged', this.update.bind(URLManager));
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

    update: function(results) {
        var qs = this.getQueryString();
        var vehicle = results.vehicle;
        var poolNumber = results.poolNumber;

        window.history.pushState(true, true, '/pool/' + vehicle + '/' + poolNumber + '/' + qs);
    }
};

var LayoutManager = {
    init: function() {
        Events.subscribe('dataLoaded', this.render.bind(LayoutManager));
        Events.subscribe('dataLoaded', this.updateSAM);
        Events.subscribe('dataLoaded', this.updateResultsInfo);
        Events.subscribe('dataLoaded', this.updateBreadcrumb);
    },

    render: function(results) {
        //load vendor and pool results.results
        for (var i in results.results) {
            var obj = results.results[i];
            var $poolLink, poolHeader; 
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

        $('#custom_page_content').append($div);
        }

        Events.publish('contentChanged', results);
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
    URLManager.init();
    LayoutManager.init();
});
