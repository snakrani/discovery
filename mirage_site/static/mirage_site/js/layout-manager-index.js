// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Strict_mode
'use strict';
LayoutManager.indexInit = function(original) {
    Events.subscribe('metaDataLoaded', this.renderMetaData);
    original.bind(LayoutManager).call();
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
        var samObj = new Date(results['sam_load_date']);
        var fpdsObj = new Date(results['fpds_load_date']);
        $("#data_source_date_sam").text(dateStr(samObj));
        $("#data_source_date_fpds").text(dateStr(fpdsObj));
    }
};

LayoutManager.disableFilters = function() {
    //disable socioeconomic indicators until a naics is selected
    var disabledColor = '#999999';
    $('#choose_filters').css('color', disabledColor);
    $('.pure-checkbox').css('color', disabledColor);
    $('.se_filter').attr("disabled", true);
}
