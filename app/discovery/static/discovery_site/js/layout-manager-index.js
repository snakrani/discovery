
LayoutManager.initializers.index = function() {
    EventManager.subscribe('dataChanged', LayoutManager.route);
    EventManager.subscribe('dataChanged', LayoutManager.toggleFilters);
    EventManager.subscribe('dataChanged', LayoutManager.toggleZones);
    EventManager.subscribe('pageInitialized', LayoutManager.vehicleInfo);

    LayoutManager.hideZones();
};

LayoutManager.route = function(data) {
    var queryObject = DataManager.buildRequestQuery();

    if ('naics' in queryObject || 'vehicle' in queryObject || 'pool' in queryObject) {
        LayoutManager.loadPoolPage();
    }
};

LayoutManager.loadPoolPage = function() {
    var qs = DataManager.getQueryString();
    window.location.href = '/results' + qs;
};

LayoutManager.render = function(results) {
    if (! $.isEmptyObject(results)) {
        var dateStr = function(dateObj) {
            return ((dateObj.getMonth() + 1) + '/' + dateObj.getDate() + '/' + dateObj.getFullYear().toString().substring(2));
        };

        $("#data_source_date_sam").text(LayoutManager.convertDate(results['sam_load_date']));
        $("#data_source_date_fpds").text(LayoutManager.convertDate(results['fpds_load_date']));
    }
};

LayoutManager.vehicleInfo = function() {
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
};
