
LayoutManager.initializers.index = function() {
    EventManager.subscribe('dataChanged', this.route.bind(LayoutManager));
    EventManager.subscribe('dataChanged', this.toggleZones.bind(LayoutManager));
    EventManager.subscribe('loadPage', this.vehicleInfo.bind(LayoutManager));

    this.hideZones();
};

LayoutManager.route = function(data) {
    var queryObject = DataManager.buildRequestQuery();

    if ('naics' in queryObject || 'vehicle' in queryObject || 'pool' in queryObject) {
        this.loadPoolPage();
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

        $("#data_source_date_sam").text(this.convertDate(results['sam_load_date']));
        $("#data_source_date_fpds").text(this.convertDate(results['fpds_load_date']));
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
