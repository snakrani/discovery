
DataManager.initializers.listings = function() {
    DataManager.initSearch();

    // External action subscriptions
    $('#pool_table').on('click', 'th.sortable', DataManager.sortVendors);
    $('#pool_table').on('keypress', 'th.sortable', DataManager.sortVendors);

    // Internal event subscriptions
    EventManager.subscribe('dataInitialized', DataManager.loadVendors);
    EventManager.subscribe('sortChanged', DataManager.update);
};

DataManager.getStatusCount = function() {
    return 4;
};

DataManager.loadVendors = function() {
    var url = "/api/vendors/";
    var vehiclePools = DataManager.getVehiclePools();
    var pools = DataManager.getPools();
    var poolIds = [];

    var requestVars = DataManager.buildRequestQuery();
    var ordering = DataManager.getSortOrdering();
    var queryData = {
        'page': DataManager.getPage(),
        'count': DataManager.getPageCount()
    };

    if (ordering) {
        queryData['ordering'] = ordering;
    }
    var filters = [];

    if ('naics' in requestVars) {
        queryData['contract_naics'] = requestVars['naics'];
    }
    if (! $.isEmptyObject(vehiclePools)) {
        if (pools.length > 0) {
            for (var index = 0; index < pools.length; index++) {
                poolIds.push(pools[index]);
            }
        } else {
            Object.keys(vehiclePools).forEach(function (id) {
                poolIds.push(id);
            });
        }
        filters.push('(pools__pool__id__in' + '=' + poolIds.join(',') + ')');
    }

    if (LayoutManager.zoneActive() && 'zones' in requestVars) {
        filters.push('(pools__zones__id__in' + '=' + requestVars['zones'] + ')');
    }

    if ('setasides' in requestVars) {
        var setasides = requestVars['setasides'].split(',');
        for (var index = 0; index < setasides.length; index++) {
            filters.push('(pools__setasides__code' + '=' + setasides[index] + ')');
        }
    }
    queryData['filters'] = encodeURIComponent(filters.join('&'));

    DataManager.getAPIRequest(url, queryData,
        function(response) {
            EventManager.publish('vendorDataLoaded', response);
        },
        function(req, status, error) {
            if (queryData['page'] > 1 && req.status == 404) {
                DataManager.setPage(1);
                DataManager.update();
            }
            else {
                $('.table_wrapper').addClass('loading');
                $('.table_wrapper').addClass('warning');
            }
        }
    );
};

DataManager.sortClassMap = function() {
    return {
        'h_vendor_name': 'name',
        'h_naics_results': 'number_of_contracts',
    };
};

DataManager.sortVendors = function(e) {
    if ((e.type == "keypress" && e.charCode == 13) || e.type == "click") {
        var $target = $(e.target);
        var class_map = DataManager.sortClassMap();
        var classes = $target.attr('class').split(' ');

        DataManager.setSortOrdering(class_map[classes[0]]);
        DataManager.setPage(1);

        if ($target.hasClass('arrow-down')) {
            $target.removeClass('arrow-down').addClass('arrow-up').attr("title", "Sorted ascending");
        } else if ($target.hasClass('arrow-sortable')) {
            DataManager.setSortOrdering("-" + DataManager.get('ordering'));
            $target.removeClass('arrow-sortable').addClass('arrow-down').attr("title", "Sorted descending");
        } else {
            DataManager.setSortOrdering("-" + DataManager.get('ordering'));
            $target.removeClass('arrow-up').addClass('arrow-down').attr("title", "Sorted descending");
        }

        $target.siblings('.sortable').removeClass('arrow-down').removeClass('arrow-up').addClass('arrow-sortable').attr("title", "Select to sort");

        EventManager.publish('sortChanged');
    }
};
