
var DataManager = {

    title: 'Discovery',

    vehicleMap: {
        "OASIS_SB": {"title": "OASIS Small Business", "sb": true},
        "OASIS": {"title": "OASIS Unrestricted", "sb": false},
        "HCATS_SB": {"title": "HCATS Small Business", "sb": true},
        "HCATS": {"title": "HCATS Unrestricted", "sb": false},
        "BMO_SB": {"title": "BMO Small Business", "sb": true},
        "BMO": {"title": "BMO Unrestricted", "sb": false},
        "PSS": {"title": "Professional Services", "sb": true}
    },
    vehiclePools: {},
    naicsPools: {},

    init: function() {
        // event bindings
        $('#vehicle-id').on('select2:select select2:unselecting', DataManager.sendVehicleChange);
        $('#pool-id').on('select2:select select2:unselecting', DataManager.sendPoolChange);
        $('#naics-code').on('select2:select select2:unselecting', DataManager.sendCodeChange);
        $('#zone-id').on('select2:select select2:unselecting', DataManager.sendZoneChange);
        $('#setaside-filters').change(DataManager.sendFilterChange);
        $('#contract_pool_filters').change(DataManager.sendPoolFilterContractsChange);

        $('#vendor_contract_history_title_container').on('click', 'div.contracts_button', DataManager.sendContractsChange);
        $('#vendor_contract_history_title_container').on('keypress', 'div.contracts_button', DataManager.sendContractsChange);

        $('#pool_table').on('click', 'th.sortable', DataManager.sortVendors);
        $('#pool_table').on('keypress', 'th.sortable', DataManager.sortVendors);

        $('#ch_table').on('click', 'th.sortable', DataManager.sortContracts);
        $('#ch_table').on('keypress', 'th.sortable', DataManager.sortContracts);

        // event subscriptions
        EventManager.subscribe('naicsChanged', DataManager.update);
        EventManager.subscribe('vehicleChanged', DataManager.update);
        EventManager.subscribe('poolChanged', DataManager.update);
        EventManager.subscribe('zoneChanged', DataManager.update);
        EventManager.subscribe('filtersChanged', DataManager.update);
        EventManager.subscribe('vendorsChanged', DataManager.update);
        EventManager.subscribe('contractsChanged', DataManager.update);

        EventManager.subscribe('pageUpdated', DataManager.bootstrap);
        EventManager.subscribe('pageInitialized', DataManager.loadPools);

        if (LayoutManager.isHomePage() || LayoutManager.isPoolPage()) {
            EventManager.subscribe('poolUpdated', DataManager.loadNaicsMap);

            EventManager.subscribe('naicsMapLoaded', DataManager.populateVehicleDropDown);
            EventManager.subscribe('vehicleSelected', DataManager.populatePoolDropDown);
            EventManager.subscribe('poolSelected', DataManager.populateNaicsDropDown);
            EventManager.subscribe('naicsSelected', DataManager.populateZoneDropDown);
            EventManager.subscribe('zoneSelected', DataManager.sendDataChange);
        }
        else {
            EventManager.subscribe('poolUpdated', DataManager.sendDataChange);
            EventManager.subscribe('dataChanged', DataManager.initContractSort);
        }
    },

    bootstrap: function() {
        var vehicle = DataManager.getParameterByName('vehicle');
        var pool = DataManager.getParameterByName('pool');
        var naics = DataManager.getParameterByName('naics-code');
        var zone = DataManager.getParameterByName('zone');
        var setasides = DataManager.getParameterByName('setasides');
        var type = DataManager.getParameterByName('type');
        var page = DataManager.getParameterByName('page');
        var count = DataManager.getParameterByName('count');
        var ordering = DataManager.getParameterByName('ordering');
        var data = {};

        if (vehicle) {
            DataManager.vehicle = vehicle;
        }
        if (pool) {
            DataManager.poolId = pool;
        }
        if (naics) {
            DataManager.naicsCode = naics;
        }
        if (zone) {
            DataManager.zoneId = zone;
        }
        if (setasides) {
            var setasides = setasides.split(',');
            var len = setasides.length - 1;

            for (var i = 0; i < len; i++) {
                $('input[value=' + setasides[i] + ']').attr('checked', 'checked');
            }
        }
        if (type) {
            DataManager.listType = type;
        }
        else {
            DataManager.listType = 'naics';
        }

        if (page) {
            DataManager.page = page;
        }
        else {
            DataManager.page = 1;
        }
        if (count) {
            DataManager.pageCount = count;
        }
        else {
            DataManager.pageCount = DataManager.getDefaultPageCount();
        }
        if (ordering) {
            DataManager.sortOrdering = ordering;
        }

        LayoutManager.route(data);
        LayoutManager.toggleZones();
        EventManager.publish('pageInitialized');
    },

    buildRequestQuery: function() {
        var vehicle = DataManager.getVehicle();
        var pools = DataManager.getVehiclePools();
        var pool = DataManager.getPoolId();
        var naics = DataManager.getNaicsCode();
        var zone = DataManager.getZone();
        var setasides = DataManager.getSetasides();
        var contractPools = DataManager.getContractPools();
        var listType = DataManager.getListType();
        var page = DataManager.getPage();
        var pageCount = DataManager.getPageCount();
        var sortOrdering = DataManager.getSortOrdering();

        var queryData = {};

        if (vehicle && vehicle != 'all') {
            queryData['vehicle'] = vehicle;
        }

        if (LayoutManager.isVendorPage()) {
            if (contractPools.length > 0) {
                queryData['pool'] = contractPools.join(',');
            }
        }
        else if (pool && pool in pools) {
            queryData['pool'] = pool;
        }

        if (naics && naics != 'all') {
            queryData['naics'] = naics;
        }
        if (zone && zone != 'all') {
            queryData['zone'] = zone;
        }

        if (setasides.length > 0) {
            queryData["setasides"] = setasides.join(',');
        }

        if (listType && listType != 'naics') {
            queryData['type'] = listType;
        }

        if (page && page > 1) {
            queryData['page'] = page;
        }
        if (pageCount && pageCount != DataManager.getPageCount()) {
            queryData['count'] = pageCount;
        }

        if (sortOrdering) {
            queryData['ordering'] = sortOrdering;
        }

        if (DataManager.getParameterByName('test')) {
            queryData['test'] = 'true';
        }
        return queryData;
    },

    sortVendors: function(e) {
        //if enter pressed or if click then sort
        if ((e.type == "keypress" && e.charCode == 13) || e.type == "click") {
            var $target = $(e.target);
            var class_map = RequestsManager.sortClassMap();
            var classes = $target.attr('class').split(' ');

            DataManager.sortOrdering = class_map[classes[0]];
            DataManager.page = 1;

            if ($target.hasClass('arrow-down')) {
                $target.removeClass('arrow-down').addClass('arrow-up').attr("title", "Sorted ascending");
            } else if ($target.hasClass('arrow-sortable')) {
                DataManager.sortOrdering = "-" + DataManager.sortOrdering;
                $target.removeClass('arrow-sortable').addClass('arrow-down').attr("title", "Sorted descending");
            } else {
                DataManager.sortOrdering = "-" + DataManager.sortOrdering;
                $target.removeClass('arrow-up').addClass('arrow-down').attr("title", "Sorted descending");
            }

            //reset other ths that are sortable
            $target.siblings('.sortable').removeClass('arrow-down').removeClass('arrow-up').addClass('arrow-sortable').attr("title", "Select to sort");

            EventManager.publish('vendorsChanged');
        }
    },

    initContractSort: function() {
        var ordering = DataManager.getSortOrdering();

        if (ordering) {
            var asc = (ordering[0] == '-' ? false : true);
            var field = DataManager.getOrderingField(ordering.replace(/^-/, ''));
            var $target = $('th.' + field);

            $target.siblings('.sortable').removeClass('arrow-down').removeClass('arrow-up').addClass('arrow-sortable').attr("title", "Select to sort");

            if (asc) {
                $target.removeClass('arrow-sortable').removeClass('arrow-down').addClass('arrow-up').attr("title", "Sorted ascending");
            } else {
                $target.removeClass('arrow-sortable').removeClass('arrow-up').addClass('arrow-down').attr("title", "Sorted descending");
            }
        }
    },

    sortContracts: function(e) {
        //if enter pressed or if click then sort
        if ((e.type == "keypress" && e.charCode == 13) || e.type == "click") {
            var $target = $(e.target);
            var class_map = RequestsManager.sortClassMap();
            var classes = $target.attr('class').split(' ');

            DataManager.sortOrdering = class_map[classes[0]];
            DataManager.page = 1;

            if ($target.hasClass('arrow-down')) {
                $target.removeClass('arrow-down').addClass('arrow-up').attr("title", "Sorted ascending");
            } else if ($target.hasClass('arrow-sortable')) {
                DataManager.sortOrdering = "-" + DataManager.sortOrdering;
                $target.removeClass('arrow-sortable').addClass('arrow-down').attr("title", "Sorted descending");
            } else {
                DataManager.sortOrdering = "-" + DataManager.sortOrdering;
                $target.removeClass('arrow-up').addClass('arrow-down').attr("title", "Sorted descending");
            }

            //reset other ths that are sortable
            $target.siblings('.sortable').removeClass('arrow-down').removeClass('arrow-up').addClass('arrow-sortable').attr("title", "Select to sort");

            //prevent button flipping by selecting proper listType
            var $button = $("#vendor_contract_history_title_container").find('.contracts_button_active');
            if ($button.text() == "All Contracts") { DataManager.listType = 'all'; }
            else { DataManager.listType = 'naics'; }

            EventManager.publish('contractsChanged');
        }
    },

    sendContractsChange: function(e) {
        if ((e.type == "keypress" && e.charCode == 13) || e.type == "click") {
            DataManager.listType = 'naics';

            if(e.target.textContent == "All Contracts" || e.target.innerText == "All Contracts"){
                DataManager.listType = 'all';
            }

            //reset date header column classes
            var $date = $("div#ch_table th.h_date_signed");
            $date.removeClass('arrow-sortable').addClass('arrow-down').attr("title", "Sorted descending");
            $date.siblings('.sortable').removeClass('arrow-down').removeClass('arrow-up').addClass('arrow-sortable').attr("title", "Select to sort");

            EventManager.publish('contractsChanged');
        }
    },

    sendPoolFilterContractsChange: function() {
        DataManager.listType = 'naics';

        var $button = $("#vendor_contract_history_title_container").find('.contracts_button_active');
        if ($button.text() == "All Contracts") {
            DataManager.listType = 'all';
        }

        //reset date header column classes
        var $date = $("div#ch_table th.h_date_signed");
        $date.removeClass('arrow-sortable').addClass('arrow-down').attr("title", "Sorted descending");
        $date.siblings('.sortable').removeClass('arrow-down').removeClass('arrow-up').addClass('arrow-sortable').attr("title", "Select to sort");

        DataManager.pool = DataManager.getContractPools();

        EventManager.publish('contractsChanged');
    },

    sendVehicleChange: function() {
        DataManager.vehicle = $('#vehicle-id').val();

        if (DataManager.vehicle && DataManager.vehicle == 'all') {
            DataManager.vehicle = null;
        }
        EventManager.publish('vehicleChanged', DataManager.vehicle);
    },

    sendPoolChange: function(e) {
        DataManager.poolId = $('#pool-id').val();

        if (DataManager.poolId && DataManager.poolId == 'all') {
            DataManager.poolId = null;
        }
        EventManager.publish('poolChanged', DataManager.poolId);
    },

    sendCodeChange: function(e) {
        DataManager.naicsCode = $('#naics-code').val();

        if (DataManager.naicsCode && DataManager.naicsCode == 'all') {
            DataManager.naicsCode = null;
        }
        EventManager.publish('naicsChanged', DataManager.naicsCode);
    },

    sendZoneChange: function(e) {
        DataManager.zoneId = $('#zone-id').val();

        if (DataManager.zoneId && DataManager.zoneId == 'all') {
            DataManager.zoneId = null;
        }
        EventManager.publish('zoneChanged', DataManager.zoneId);
    },

    sendFilterChange: function() {
        EventManager.publish('filtersChanged');
    },

    sendDataChange: function() {
        EventManager.publish('dataChanged');
    },

    update: function() {
        History.pushState('', DataManager.title, DataManager.getURL());
        EventManager.publish('pageUpdated');
    },

    getURL: function(params) {
        return window.location.pathname + DataManager.getQueryString(params);
    },

    getQueryString: function(params) {
        var queryObject = DataManager.buildRequestQuery();
        var qs = '?';
        var k;

        if('naics' in queryObject) {
            queryObject['naics-code'] = queryObject.naics;
            delete queryObject.naics;
        }

        if (params !== undefined) {
            for (key in params) {
                if (params[key] !== null) {
                    queryObject[key] = params[key];
                }
                else {
                    delete queryObject[key];
                }
            }
        }

        for (k in queryObject) {
            if (queryObject[k]) {
                qs += k + '=' + queryObject[k] + '&';
            }
        }

        return qs;
    },

    getVehicle: function() {
        return DataManager.vehicle;
    },

    getVehicleMap: function() {
        return DataManager.vehicleMap;
    },

    getPoolId: function() {
        return DataManager.poolId;
    },

    getPool: function() {
        return DataManager.pool;
    },

    getVehiclePools: function() {
        return DataManager.vehiclePools;
    },

    getNaicsPools: function() {
        return DataManager.naicsPools;
    },

    getNaicsCode: function() {
        return DataManager.naicsCode;
    },

    getNaicsMap: function() {
        return DataManager.naicsMap;
    },

    getZone: function() {
        return DataManager.zoneId;
    },

    getSetasides: function() {
        var setasides = [];

        $("form#setaside-filters input:checked").each(function(index) {
            setasides.push($(this).val());
        });

        return setasides;
    },

    getDUNS: function() {
        var pathArray = window.location.pathname.split('/');
        pathArray = pathArray.removeEmpties();

        for (var i = 0; i < pathArray.length; i++) {
            if (!isNaN(pathArray[i])) {
                return pathArray[i];
            }
        }
        return false;
    },

    getVendor: function() {
        return DataManager.vendor;
    },

    getContractPools: function() {
        var pools = [];

        $("form#contract_pool_filters input:checked").each(function(index) {
            pools.push($(this).val());
        });

        return pools;
    },

    getListType: function() {
        return DataManager.listType;
    },

    getPage: function() {
        return DataManager.page;
    },

    getPageCount: function() {
        return DataManager.pageCount;
    },

    getDefaultPageCount: function() {
        if (DataManager.getParameterByName('test')) {
            return 5;
        }
        return 50;
    },

    getSortOrdering: function() {
        return DataManager.sortOrdering;
    },

    getOrderingField: function(param) {
        var classMap = RequestsManager.sortClassMap();

        for (var field in classMap) {
            if (classMap[field] == param) {
                return field;
            }
        }
        return null;
    },

    loadPools: function() {
        var vehicle = DataManager.getVehicle();
        var naics = DataManager.getNaicsCode();
        var url = "/api/pools/";
        var queryData = {};

        if (naics) {
            queryData['naics__code'] = naics;
        }

        RequestsManager.getAPIRequest(url, queryData, function(data) {
            var pools = data['results'];
            var vehiclePoolMap = {};
            var naicsPoolMap = {};

            for (var index = 0; index < pools.length; index++) {
                var pool = pools[index];

                if (! vehicle || vehicle == pool.vehicle) {
                    vehiclePoolMap[pool.id] = pool;
                }
                naicsPoolMap[pool.id] = pool;
            }

            DataManager.vehiclePools = vehiclePoolMap;
            DataManager.naicsPools = naicsPoolMap;

            EventManager.publish('poolUpdated');
        });
    },

    loadNaicsMap: function() {
        var vehicle = DataManager.getVehicle();
        var url = "/api/pools/";
        var queryData = {};

        if (vehicle) {
            queryData['vehicle__iexact'] = vehicle;
        }

        RequestsManager.getAPIRequest(url, queryData, function(data) {
            var naicsMap = {};
            var pool;
            var naics;

            for (var poolIndex = 0; poolIndex < data.results.length; poolIndex++) {
                pool = data.results[poolIndex];

                if (! vehicle || pool.vehicle == vehicle.toUpperCase()) {
                    for (var naicsIndex = 0; naicsIndex < pool.naics.length; naicsIndex++) {
                        naics = pool.naics[naicsIndex].code;

                        if (!(naics in naicsMap)) {
                            naicsMap[naics] = [];
                        }
                        naicsMap[naics].push(pool.id);
                    }
                }
            }

            DataManager.naicsMap = naicsMap;
            EventManager.publish('naicsMapLoaded');
        });
    },

    populateVehicleDropDown: function() {
        var pools = DataManager.getNaicsPools();
        var vehicle = DataManager.getVehicle();
        var setasides = DataManager.getSetasides();
        var vehicleMap = DataManager.getVehicleMap();
        var vehicles = {};

        $('#vehicle-id').empty().select2({
            minimumResultsForSearch: -1,
            width: "170px"
        }).append($("<option></option>")
            .attr("value", 'all')
            .text("All vehicles"));

        Object.keys(pools).forEach(function(id) {
            var pool = pools[id];

            if (!(pool.vehicle in vehicles) && (setasides.length == 0 || vehicleMap[pool.vehicle]["sb"])) {
                $("#vehicle-id")
                    .append($("<option></option>")
                    .attr("value", pool.vehicle)
                    .text(vehicleMap[pool.vehicle]["title"]));

                vehicles[pool.vehicle] = true;
            }
        });

        if (vehicle && vehicle in vehicles) {
            $("#vehicle-id").val(vehicle);
        }
        else {
            DataManager.vehicle = null;
            $("#vehicle-id").val('all');
        }

        if (DataManager.getVehicle() != DataManager.getParameterByName('vehicle')) {
            EventManager.publish('vehicleChanged');
        }
        else {
            EventManager.publish('vehicleSelected');
        }
    },

    populatePoolDropDown: function() {
        var pools = DataManager.getVehiclePools();
        var pool = DataManager.getPoolId();
        var setasides = DataManager.getSetasides();
        var vehicleMap = DataManager.getVehicleMap();
        var count = 0;
        var poolId;

        $('#pool-id').empty().select2({
            minimumResultsForSearch: -1,
            width: "415px"
        }).append($("<option></option>")
            .attr("value", 'all')
            .text("All pools"));

        Object.keys(pools).forEach(function (id) {
            var poolData = pools[id];

            if (setasides.length == 0 || vehicleMap[poolData.vehicle]["sb"]) {
                $("#pool-id")
                    .append($("<option></option>")
                    .attr("value", id)
                    .text(poolData.name + " (" + poolData.vehicle.split('_').join(' ') + ")"));

                count += 1;
                poolId = id;
            }
        });

        if (pool && pool in pools) {
            DataManager.pool = pools[pool];
            $("#pool-id").val(pool);
        }
        else {
            if (count == 1) {
                DataManager.poolId = poolId;
                DataManager.pool = pools[poolId];
                $("#pool-id").val(poolId);
            }
            else {
                DataManager.poolId = null;
                DataManager.pool = null;
                $("#pool-id").val('all');
            }
        }

        if (DataManager.getPoolId() != DataManager.getParameterByName('pool')) {
            EventManager.publish('poolChanged');
        }
        else {
            if (count > 1) {
                LayoutManager.showPools();
            }
            else {
                LayoutManager.hidePools();
            }
            EventManager.publish('poolSelected');
        }
    },

    populateNaicsDropDown: function(data) {
        var vehicle = DataManager.getVehicle();
        var naicsMap = DataManager.getNaicsMap();
        var pool = DataManager.getPoolId();
        var naics = DataManager.getNaicsCode();

        $('#naics-code').select2({
            minimumResultsForSearch: -1,
            width: '600px'
        });

        RequestsManager.getAPIRequest(
            "/api/naics/",
            { ordering: "code", code__in: Object.keys(naicsMap).join(',') },
            function( data ) {
                $("#naics-code").empty()
                    .append($("<option></option>")
                        .attr("value", 'all')
                        .text("All NAICS codes"));

                $.each(data.results, function(key, result) {
                    if (result.code in naicsMap && (! pool || naicsMap[result.code].includes(pool))) {
                        $("#naics-code")
                            .append($("<option></option>")
                            .attr("value", result.code)
                            .text(result.code + ' - ' + result.description));
                    }
                });

                if (naics) {
                    $("#naics-code").val(naics);
                }
                else {
                    DataManager.naicsCode = null;
                    $("#naics-code").val('all');
                }

                if (DataManager.getNaicsCode() != DataManager.getParameterByName('naics-code')) {
                    EventManager.publish('naicsChanged');
                }
                else {
                    EventManager.publish('naicsSelected');
                }
            }
        );
    },

    populateZoneDropDown: function() {
        var zone = DataManager.getZone();
        var url = "/api/zones/";
        var queryData = {};

        $('#zone-id').select2({placeholder:'Filter by zone', width: '415px'});

        RequestsManager.getAPIRequest(url, queryData, function(data) {
            $("#zone-id").empty()
                .append($("<option></option>")
                    .attr("value", 'all')
                    .text("All zones"));

            $.each(data.results, function(id, result) {
                $("#zone-id")
                    .append($("<option></option>")
                    .attr("value", result.id)
                    .text("Zone " + result.id + " (" + result.state.join(', ') + ")"));
            });

            if (zone) {
                $("#zone-id").val(zone);
            }
            else {
                DataManager.zoneId = null;
                $("#zone-id").val('all');
            }

            if (DataManager.getZone() != DataManager.getParameterByName('zone')) {
                EventManager.publish('zoneChanged');
            }
            else {
                EventManager.publish('zoneSelected');
            }
        });
    },

    getParameterByName: function(name) {
        name = name.replace(/[*+?^$.\[\]{}()|\\\/]/g, "\\$&"); // escape RegEx meta chars
        var match = location.search.match(new RegExp("[?&]"+name+"=([^&]+)(&|$)"));
        return match && decodeURIComponent(match[1].replace(/\+/g, " "));
    }
};
