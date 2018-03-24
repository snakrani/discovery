
var LayoutManager = {
    initializers: {},

    init: function() {
        Events.subscribe('dataLoaded', this.render.bind(LayoutManager));
        Events.subscribe('poolUpdated', this.updatePoolInfo);
        Events.subscribe('contentChanged', this.updateResultsInfo);
        Events.subscribe('vehicleChanged', this.enableNaics);

        for(var handler in this.initializers){
            this.initializers[handler].call(this);
        }
    },

    enableNaics: function() {
        $("div#search span.select_text").css('color', 'white');
        $("div#search select").attr("disabled", false);
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

        // Asynchronously get the selected NAICS text
        InputHandler.getSelectedNAICS(function(text) {
            $("#your_search").text(text);
        });

        $("#your_filters").text(
            $("#setaside-filters input:checkbox:checked").map(function() {
                return $(this).parent().text();
            }).get().join(', ')
        );

        $("#your_search_criteria").show();
    },

    updatePoolInfo: function(data) {
        $(".results_pool_name_number_pool").text("Pool " + data['number'] + ": ");
        $(".results_pool_name_number_description").text(data['name']);
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
        return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();}).replace('U.s.', 'U.S.');
    }
};

LayoutManager.disableFilters = function() {
    //disable socioeconomic indicators until a naics is selected
    $('#choose_filters').removeClass('filter_text').addClass('filter_text_disabled');
    $('.pure-checkbox').addClass('pure-checkbox-disabled');
    $('.se_filter').attr("disabled", true);
};

LayoutManager.enableFilters = function() {
    $('#choose_filters').removeClass('filter_text_disabled').addClass('filter_text');
    $('.pure-checkbox-disabled').removeClass('pure-checkbox-disabled');
    $('.se_filter').attr("disabled", false);
};

LayoutManager.formatDate = function(dateObj) {
  //returns (mm/dd/yyyy) string representation of a date object
  return (dateObj.getMonth() + 1) + '/' + dateObj.getDate() + '/' + dateObj.getFullYear().toString().substring(2);
};

LayoutManager.numberWithCommas = function(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
};
