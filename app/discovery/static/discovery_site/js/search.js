
DataManager.initSearch = function() {
    // External action subscriptions
    $('#vehicle-id').on('click select2:select select2:unselecting', DataManager.sendVehicleChange);
    $('#pool-id').on('click select2:select select2:unselecting', DataManager.sendPoolChange);
    $('#naics-code').on('click select2:select select2:unselecting', DataManager.sendNaicsChange);
    $('#zone-id').on('click select2:select select2:unselecting', DataManager.sendZoneChange);
    $('#setaside-filters').change(DataManager.sendFilterChange);

    // Internal event subscriptions
    EventManager.subscribe('pageInitialized', DataManager.loadPools);
    EventManager.subscribe('poolUpdated', DataManager.loadNaicsMap);

    EventManager.subscribe('naicsMapLoaded', DataManager.populateVehicleDropDown);
    EventManager.subscribe('vehicleSelected', DataManager.populatePoolDropDown);
    EventManager.subscribe('poolSelected', DataManager.populateNaicsDropDown);
    EventManager.subscribe('naicsSelected', DataManager.populateZoneDropDown);
    EventManager.subscribe('zoneSelected', DataManager.sendDataInitialized);

    EventManager.subscribe('naicsChanged', DataManager.update);
    EventManager.subscribe('vehicleChanged', DataManager.update);
    EventManager.subscribe('poolChanged', DataManager.update);
    EventManager.subscribe('zoneChanged', DataManager.update);
    EventManager.subscribe('filtersChanged', DataManager.update);

    // Parameter initialization
    function splitParam(field, value) {
        if (value) {
            value = value.split(',');
        }
        return value;
    };

    DataManager.collect('naics');
    DataManager.collect('vehicle');
    DataManager.collect('pools', [], splitParam);
    DataManager.collect('zones', [], splitParam);

    DataManager.collect('setasides', [], function(field, value) {
        if (value) {
            value = value.split(',');
            var len = value.length - 1;

            for (var i = 0; i < len; i++) {
                $('input[value=' + value[i] + ']').attr('checked', 'checked');
            }
        }
        return value;
    });

    // Input element initialization
    $('#naics-code').select2({
        placeholder: 'Select a NAICS code',
        minimumResultsForSearch: 1,
        width: '600px'
    });
    $('#vehicle-id').select2({
        placeholder: 'Select a vehicle',
        minimumResultsForSearch: -1,
        width: '150px'
    });
    $('#pool-id').select2({
        placeholder: 'Select a service category',
        //minimumResultsForSearch: -1,
        allowClear: true,
        closeOnSelect: false,
        width: '220px'
    });
    $('#zone-id').select2({
        placeholder: 'Select a service zone',
        //minimumResultsForSearch: -1,
        allowClear: true,
        width: '200px'
    });
};

DataManager.requestParams = function(queryData) {
    var naics = DataManager.getNaics();
    var vehicle = DataManager.getVehicle();
    var pools = DataManager.getPools();
    var zones = DataManager.getZones();
    var setasides = DataManager.getSetasides();

    if (naics) {
        queryData['naics'] = naics;
    }
    if (vehicle) {
        queryData['vehicle'] = vehicle;
    }
    if (pools.length > 0) {
        queryData['pools'] = pools.join(',');
    }
    if (zones.length > 0) {
        queryData['zones'] = zones.join(',');
    }
    if (setasides.length > 0) {
        queryData['setasides'] = setasides.join(',');
    }
    console.log("Query data: %o", queryData);
    return queryData;
};

DataManager.setNaics = function(value) {
    DataManager.set('naics', value);
};

DataManager.getNaics = function() {
    return DataManager.get('naics', null);
};

DataManager.setNaicsPools = function(value) {
    DataManager.set('naics_pools', value);
};

DataManager.getNaicsPools = function() {
    return DataManager.get('naics_pools', {});
};

DataManager.setNaicsMap = function(value) {
    DataManager.set('naics_map', value);
};

DataManager.getNaicsMap = function() {
    return DataManager.get('naics_map', {});
};

DataManager.sendNaicsChange = function(e) {
    DataManager.setNaics($('#naics-code').val());
    EventManager.publish('naicsChanged');
};

DataManager.setVehicle = function(value) {
    DataManager.set('vehicle', value);
};

DataManager.getVehicle = function() {
    return DataManager.get('vehicle', null);
};

DataManager.setVehiclePools = function(value) {
    DataManager.set('vehicle_pools', value);
};

DataManager.getVehiclePools = function() {
    return DataManager.get('vehicle_pools', {});
};

DataManager.sendVehicleChange = function() {
    DataManager.setVehicle($('#vehicle-id').val());
    EventManager.publish('vehicleChanged');
};

DataManager.setPools = function(values) {
    DataManager.set('pools', values);
};

DataManager.getPools = function() {
    return DataManager.get('pools', []);
};

DataManager.setPoolData = function(values) {
    DataManager.set('pool_data', values);
};

DataManager.getPoolData = function() {
    return DataManager.get('pool_data', []);
};

DataManager.sendPoolChange = function(e) {
    console.log("Pool value: %o", $('#pool-id').val());
    DataManager.setPools($('#pool-id').val());
    EventManager.publish('poolChanged');
};

DataManager.setZones = function(values) {
    DataManager.set('zones', values);
};

DataManager.getZones = function() {
    return DataManager.get('zones', []);
};

DataManager.sendZoneChange = function(e) {
    console.log("Zone value: %o", $('#zone-id').val());
    DataManager.setZones($('#zone-id').val());
    EventManager.publish('zoneChanged');
};

DataManager.getSetasides = function() {
    var setasides = [];

    $("form#setaside-filters input:checked").each(function(index) {
        setasides.push($(this).val());
    });
    return setasides;
};

DataManager.sendFilterChange = function() {
    EventManager.publish('filtersChanged');
};

DataManager.vendorPools = function(vendor) {
    var pools = {};

    if ('pools' in vendor) {
        for (var index = 0; index < vendor.pools.length; index++) {
            var poolId = vendor.pools[index].pool.id;

            var poolComponents = poolId.split("_");
            poolComponents.pop();

            var vehicleId = poolComponents.join("_");

            pools[vehicleId] = true;
        }
    }
    return Object.keys(pools);
};

DataManager.loadPools = function() {
    var vehicleMap = DataManager.getVehicleMap();
    var vehicle = DataManager.getVehicle();
    var naics = DataManager.getNaics();
    var setasides = DataManager.getSetasides();
    var url = "/api/pools/";
    var queryData = {count: 1000, ordering: 'vehicle'};

    if (naics) {
        queryData['naics__code'] = naics;
    }

    DataManager.getAPIRequest(url, queryData, function(data) {
        var pools = data['results'];
        var vehiclePoolMap = {};
        var naicsPoolMap = {};

        for (var index = 0; index < pools.length; index++) {
            var pool = pools[index];

            if (setasides.length == 0 || vehicleMap[pool.vehicle]["sb"]) {
                if (! vehicle || vehicle == pool.vehicle) {
                    vehiclePoolMap[pool.id] = pool;
                }
                naicsPoolMap[pool.id] = pool;
            }
        }

        DataManager.setVehiclePools(vehiclePoolMap);
        DataManager.setNaicsPools(naicsPoolMap);
        EventManager.publish('poolUpdated');
    });
};

DataManager.loadNaicsMap = function() {
    var vehicle = DataManager.getVehicle();
    var url = "/api/pools/";
    var queryData = {count: 1000};

    if (vehicle) {
        queryData['vehicle__iexact'] = vehicle;
    }

    DataManager.getAPIRequest(url, queryData, function(data) {
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
        DataManager.setNaicsMap(naicsMap);
        EventManager.publish('naicsMapLoaded');
    });
};

DataManager.populateNaicsDropDown = function(data) {
    var naicsMap = DataManager.getNaicsMap();
    var naics = DataManager.getNaics();
    var vehicle = DataManager.getVehicle();
    var pools = DataManager.getPools();

    DataManager.getAPIRequest(
        "/api/naics/",
        {ordering: "code", code__in: Object.keys(naicsMap).join(','), count: 2000},
        function(data) {
            $("#naics-code").empty()
                .append($("<option></option>")
                    .attr("value", 'all')
                    .text("All NAICS codes"));

            $.each(data.results, function(key, result) {
                var included = false;

                if (pools.length > 0) {
                    for (var index = 0; index < pools.length; index++) {
                        if ($.inArray(pools[index], naicsMap[result.code]) !== -1) {
                            included = true;
                            break;
                        }
                    }
                }
                else {
                    included = true;
                }

                if (included) {
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
                DataManager.setNaics(null);
                $("#naics-code").val('all');
            }

            if (DataManager.getNaics() != DataManager.getParameterByName('naics')) {
                EventManager.publish('naicsChanged');
            }
            else {
                EventManager.publish('naicsSelected');
            }
        }
    );
};

DataManager.populateVehicleDropDown = function() {
    var pools = DataManager.getNaicsPools();
    var vehicleMap = DataManager.getVehicleMap();
    var vehicle = DataManager.getVehicle();
    var setasides = DataManager.getSetasides();
    var vehicles = {};

    $('#vehicle-id').empty()
        .append($("<option></option>")
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
        DataManager.setVehicle(null);
        $("#vehicle-id").val('all');
    }

    if (DataManager.getVehicle() != DataManager.getParameterByName('vehicle')) {
        EventManager.publish('vehicleChanged');
    }
    else {
        EventManager.publish('vehicleSelected');
    }
};

DataManager.populatePoolDropDown = function() {
    var vehiclePools = DataManager.getVehiclePools();
    var pools = DataManager.getPools();
    var poolMatches = pools.filter(function(id) { return Object.keys(vehiclePools).indexOf(id) > -1; });
    var count = 0;
    var poolId;

    console.log("Pools: %o", pools);
    console.log("Pool matches: %o", poolMatches);

    $('#pool-id').empty();

    for (var id in vehiclePools) {
        var poolData = vehiclePools[id];
        var poolName = poolData.vehicle.split('_').join(' ') + ' - ' + poolData.name;

        $("#pool-id")
            .append($("<option></option>")
            .attr("value", id)
            .text(poolName));

	    count += 1;
        poolId = id;
    }

    if (poolMatches.length > 0) {
        var poolData = [];

        for (var index = 0; index < poolMatches.length; index++) {
            poolData.push(vehiclePools[poolMatches[index]]);
        }

        DataManager.setPoolData(poolData);
        $("#pool-id").val(poolMatches);
    }
    else {
        if (count == 1) {
            DataManager.setPools([poolId]);
            DataManager.setPoolData([pools[pool]]);
            $("#pool-id").val([poolId]);
        }
        else {
            DataManager.setPools([]);
            DataManager.setPoolData([]);
            $("#pool-id").val([]);
        }
    }

    var currentSelection = DataManager.getPools().join(',');
    var paramSelection = DataManager.getParameterByName('pools');

    if (!paramSelection) {
        paramSelection = "";
    }

    console.log("Pool parameters: %o", paramSelection);
    console.log("Current pool selection: %o", currentSelection);

    if (currentSelection != paramSelection) {
        EventManager.publish('poolChanged');
    }
    else {
        EventManager.publish('poolSelected');
    }
};

DataManager.populateZoneDropDown = function() {
    var zones = DataManager.getZones();
    var url = "/api/zones/";
    var queryData = {count: 1000};

    DataManager.getAPIRequest(url, queryData, function(data) {
        $("#zone-id").empty();

        $.each(data.results, function(id, result) {
            $("#zone-id")
                .append($("<option></option>")
                .attr("value", result.id)
                .text("Zone " + result.id + " (" + result.state.join(', ') + ")"));
        });

        if (zones.length > 0) {
            $("#zone-id").val(zones);
        }
        else {
            DataManager.setZones([]);
            $("#zone-id").val([]);
        }

        var currentSelection = DataManager.getZones().join(',');
        var paramSelection = DataManager.getParameterByName('zones');

        if (!paramSelection) {
            paramSelection = "";
        }

        console.log("Zone parameters: %o", paramSelection);
        console.log("Current zone selection: %o", currentSelection);

        if (currentSelection != paramSelection) {
            EventManager.publish('zoneChanged');
        }
        else {
            EventManager.publish('zoneSelected');
        }
    });
};

LayoutManager.initSearch = function() {
    EventManager.subscribe('vehicleSelected', LayoutManager.toggleZone);
};

LayoutManager.enableSearch = function() {
    $('.table_wrapper').removeClass('loading');
    $('#pool_table').removeClass('init');

    LayoutManager.enableNaics();
    LayoutManager.enableVehicle();
    LayoutManager.enablePool();
    LayoutManager.enableZone();
    LayoutManager.enableFilters();
};

LayoutManager.disableSearch = function() {
    $('.table_wrapper').addClass('loading');
    $('#pool_table').addClass('init');

    LayoutManager.disableNaics();
    LayoutManager.disableVehicle();
    LayoutManager.disablePool();
    LayoutManager.disableZone();
    LayoutManager.disableFilters();
};

LayoutManager.enableNaics = function() {
    $("div#naics_select select").attr("disabled", false);
};

LayoutManager.disableNaics = function() {
    $("div#naics_select select").attr("disabled", true);
};

LayoutManager.enableVehicle = function() {
    $("div#vehicle_select select").attr("disabled", false);
};

LayoutManager.disableVehicle = function() {
    $("div#vehicle_select select").attr("disabled", true);
};

LayoutManager.enablePool = function() {
    $("div#pool_select select").attr("disabled", false);
};

LayoutManager.disablePool = function() {
    $("div#pool_select select").attr("disabled", true);
};

LayoutManager.zoneActive = function() {
    var vehicle = DataManager.getVehicle();

    if (vehicle && vehicle.match(/^BMO/i)) {
        return true;
    }
    else {
        return false;
    }
};

LayoutManager.enableZone = function() {
    if (LayoutManager.zoneActive()) {
        $("div#zone_select select").attr("disabled", false);
    }
};

LayoutManager.showZone = function() {
    $("#pool-id").select2({width: '220px'});
    $("div#zone_select").show();
};

LayoutManager.disableZone = function() {
    $("div#zone_select select").attr("disabled", true);
};

LayoutManager.hideZone = function() {
    $("div#zone_select").hide();
    $("#pool-id").select2({width: '435px'});
};

LayoutManager.toggleZone = function() {
    if (LayoutManager.zoneActive()) {
        LayoutManager.showZone();
    }
    else {
        LayoutManager.hideZone();
    }
};

LayoutManager.enableFilters = function() {
    $('#choose_filters').removeClass('filter_text_disabled').addClass('filter_text');
    $('.pure-checkbox-disabled').removeClass('pure-checkbox-disabled');
    $('.se_filter').attr("disabled", false);
};

LayoutManager.disableFilters = function() {
    $('#choose_filters').removeClass('filter_text').addClass('filter_text_disabled');
    $('.pure-checkbox').addClass('pure-checkbox-disabled');
    $('.se_filter').attr("disabled", true);
};

LayoutManager.toggleFilters = function() {
    if (! DataManager.getVehicle() || DataManager.getVehicleMap()[DataManager.getVehicle()]["sb"]) {
        LayoutManager.enableFilters();
    }
    else {
        LayoutManager.disableFilters();
    }
};
