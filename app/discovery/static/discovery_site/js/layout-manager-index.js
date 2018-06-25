
LayoutManager.initializers.index = function() {
    EventManager.subscribe('naicsChanged', this.route.bind(LayoutManager));
    EventManager.subscribe('loadPage', this.vehicleInfo.bind(LayoutManager));

    this.hideZone();
    this.disableFilters();
};

LayoutManager.route = function(data) {
    var queryObject = RequestsManager.buildRequestQuery();

    if ('vehicle' in queryObject && 'naics' in queryObject) {
        this.loadPoolPage();
    }
};

LayoutManager.loadPoolPage = function() {
    var qs = URLManager.getQueryString();
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
