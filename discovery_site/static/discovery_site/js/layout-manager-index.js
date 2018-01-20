// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Strict_mode
'use strict';
LayoutManager.indexInit = function(original) {
    Events.subscribe('metaDataLoaded', this.renderMetaData);
    Events.subscribe('loadedWithQS', this.enableNaics);
    original.bind(LayoutManager).call()

    this.disableNaics();
    this.disableFilters();

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

    $("#data_source_dialog_sam").dialog({
        modal: false,
        position: {
          my: "left top",
          at: "left top",
          of: "#data_source_fpds",
          collision: "none"
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
    });
    $(document).mouseup(function(e) {
      var container = $("#data_source_dialog_sam");

      // if the target of the click isn't the container or a descendant of the container
      if (!container.is(e.target) && container.has(e.target).length === 0) {
        container.dialog('close');
      }
    });
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

LayoutManager.convertDate = function(oldDate) {
    if (!oldDate) return 'Unknown'
    var dateArray = oldDate.split('-')
    return dateArray[1] + '/' + dateArray[2]+ '/' + dateArray[0]
}
