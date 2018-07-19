
LayoutManager.initializers.index = function() {
    LayoutManager.initSearch();

    // Internal event subscriptions
    EventManager.subscribe('pageInitialized', LayoutManager.styleVehicleInfo);
    EventManager.subscribe('metadataLoaded', LayoutManager.renderMetadata);
};

LayoutManager.preprocessors.index = function() {
    LayoutManager.hideZone();
};

LayoutManager.route = function() {
    var queryObject = DataManager.buildRequestQuery();

    if ('naics' in queryObject || 'vehicle' in queryObject || 'pool' in queryObject || 'setasides' in queryObject) {
        var qs = DataManager.getQueryString();
        window.location.href = '/results' + qs;
    }
};

LayoutManager.styleVehicleInfo = function() {
    $('#discovery_vehicles').collapsible({
        accordion: false,
        accordionUpSpeed: 100,
        accordionDownSpeed: 100,
        collapseSpeed: 100,
        contentOpen: null,
        arrowRclass: 'arrow-r',
        arrowDclass: 'arrow-d',
        animate: true
    });
    DataManager.completeStatus();
};

LayoutManager.renderMetadata = function(data) {
    if (! $.isEmptyObject(data)) {
        $("#data_source_date_sam").text(Format.convertDate(data['sam_load_date']));
        $("#data_source_date_fpds").text(Format.convertDate(data['fpds_load_date']));
    }
    DataManager.completeStatus();
};
