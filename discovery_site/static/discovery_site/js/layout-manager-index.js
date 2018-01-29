
LayoutManager.initializers.index = function() {
    Events.subscribe('metaDataLoaded', this.renderMetaData);
    Events.subscribe('loadedWithQS', this.enableNaics);

    this.disableNaics();
    this.disableFilters();

    this.vehicleInfo();
    this.samInfo();
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

LayoutManager.samInfo = function() {
    $("#data_source_dialog_sam").dialog({
        modal: true,
        position: {
          my: "center",
          at: "center"
        },
        resizable: false,
        autoOpen: false,
        draggable: false,
        closeText: "X",
        closeOnEscape: true,
        title: "SAM Details",
        width: 440,
        height: "auto"
    });
    $('.ui-dialog-titlebar-close').removeAttr('title');

    $("#data_source_more_info_sam").click(function () {
      $('#data_source_dialog_sam').dialog('open');
      $('#data_source_dialog_sam_wrapper').css({ "display": "block" });
    });
    $(document).mouseup(function(e) {
      var container = $("#data_source_dialog_sam");

      // if the target of the click isn't the container or a descendant of the container
      if (!container.is(e.target) && container.has(e.target).length === 0) {
        container.dialog('close');
        $('#data_source_dialog_sam_wrapper').css({ "display": "none" });
      }
    });
};
