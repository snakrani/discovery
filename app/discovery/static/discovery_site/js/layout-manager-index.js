
LayoutManager.initializers.index = function() {
    Events.subscribe('metaDataLoaded', this.renderMetaData);
    Events.subscribe('loadedWithQS', this.enableNaics);

    this.disableNaics();
    this.disableFilters();

    this.vehicleInfo();
};

LayoutManager.renderMetaData = function(results) {

    if ($.isEmptyObject(results)) {
        //clear out content
    }
    else {
        var dateStr = function(dateObj) {
            return ((dateObj.getMonth() + 1) + '/' + dateObj.getDate() + '/' + dateObj.getFullYear().toString().substring(2));
        };
        //render data load dates
        $("#data_source_date_sam").text(LayoutManager.convertDate(results['sam_load_date']));
        $("#data_source_date_fpds").text(LayoutManager.convertDate(results['fpds_load_date']));
    }
};

LayoutManager.disableNaics = function() {
    $("div#search span.select_text").css('color', this.disabledColor);
    $("div#search select").attr("disabled", true);
};

LayoutManager.convertDate = function(oldDate) {
    if (!oldDate) return 'Unknown';
    var dateArray = oldDate.split('-');
    return dateArray[1] + '/' + dateArray[2]+ '/' + dateArray[0];
};

LayoutManager.vehicleInfo = function() {
    $('#discovery_vehicles').collapsible({
        accordion: false,
        accordionUpSpeed: 100,
        accordionDownSpeed: 100,
        collapseSpeed: 100,
        contentOpen: 0,
        arrowRclass: 'arrow-r',
        arrowDclass: 'arrow-d',
        animate: true
    });
};
