// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Strict_mode
'use strict';
LayoutManager.indexInit = function(original) {
    Events.subscribe('metaDataLoaded', this.renderMetaData);
    Events.subscribe('loadedWithQS', this.enableNaics);
    original.bind(LayoutManager).call()
    this.disabledColor = '#999999';
    this.disableNaics();
    this.disableFilters();
};
 
LayoutManager.originalInit = LayoutManager.init;
 
LayoutManager.init = function() {
    LayoutManager.indexInit(LayoutManager.originalInit);
};

LayoutManager.renderMetaData = function(results) {

    if ($.isEmptyObject(results)) {
        //clear out content
    }
    else {
        var dateStr = function(dateObj) {
            return ((dateObj.getMonth() + 1) + '/' + dateObj.getDate() + '/' + dateObj.getFullYear().toString().substring(2));
        }
        //render data load dates
        $("#data_source_date_sam").text(LayoutManager.convertDate(results['sam_load_date']));
        $("#data_source_date_fpds").text(LayoutManager.convertDate(results['fpds_load_date']));
    }
};

LayoutManager.disableNaics = function() {
    $("div#search span.select_text").css('color', this.disabledColor);
    $("div#search select").attr("disabled", true);
};

LayoutManager.disableFilters = function() {
    //disable socioeconomic indicators until a naics is selected
    $('#choose_filters').css('color', this.disabledColor);
    $('.pure-checkbox').css('color', this.disabledColor);
    $('.se_filter').attr("disabled", true);
}

LayoutManager.convertDate = function(oldDate) {
    var dateArray = oldDate.split('-')
    return dateArray[1] + '/' + dateArray[2]+ '/' + dateArray[0]
}
