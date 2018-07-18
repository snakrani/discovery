
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
    DataManager.collect('naics');
    DataManager.collect('vehicle');
    DataManager.collect('pool');
    DataManager.collect('zone');

    DataManager.collect('setasides', null, function(field, value) {
        if (value) {
            value = value.split(',');
            var len = value.length - 1;

            for (var i = 0; i < len; i++) {
                $('input[value=' + value[i] + ']').attr('checked', 'checked');
            }
        }
        return value;
    });
};

DataManager.requestParams = function(queryData) {
    var naics = DataManager.getNaics();
    var vehicle = DataManager.getVehicle();
    var pool = DataManager.getPool();
    var zone = DataManager.getZone();
    var setasides = DataManager.getSetasides();

    if (naics) {
        queryData['naics'] = naics;
    }
    if (vehicle) {
        queryData['vehicle'] = vehicle;
    }
    if (pool && pool in DataManager.getVehiclePools()) {
        queryData['pool'] = pool;
    }
    if (zone) {
        queryData['zone'] = zone;
    }
    if (setasides.length > 0) {
        queryData['setasides'] = setasides.join(',');
    }
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

DataManager.setPool = function(value) {
    DataManager.set('pool', value);
};

DataManager.getPool = function() {
    return DataManager.get('pool', null);
};

DataManager.setPoolData = function(value) {
    DataManager.set('pool_data', value);
};

DataManager.getPoolData = function() {
    return DataManager.get('pool_data', null);
};

DataManager.sendPoolChange = function(e) {
    DataManager.setPool($('#pool-id').val());
    EventManager.publish('poolChanged');
};

DataManager.setZone = function(value) {
    DataManager.set('zone', value);
};

DataManager.getZone = function() {
    return DataManager.get('zone', null);
};

DataManager.sendZoneChange = function(e) {
    DataManager.setZone($('#zone-id').val());
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
    var vehicle = DataManager.getVehicle();
    var naics = DataManager.getNaics();
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

            if (! vehicle || vehicle == pool.vehicle) {
                vehiclePoolMap[pool.id] = pool;
            }
            naicsPoolMap[pool.id] = pool;
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
    var pool = DataManager.getPool();

    $('#naics-code').select2({
        minimumResultsForSearch: -1,
        width: '600px'
    });

    DataManager.getAPIRequest(
        "/api/naics/",
        {ordering: "code", code__in: Object.keys(naicsMap).join(','), count: 2000},
        function(data) {
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
    var vehicleMap = DataManager.getVehicleMap();
    var pools = DataManager.getVehiclePools();
    var pool = DataManager.getPool();
    var poolMap = {};
    var setasides = DataManager.getSetasides();
    var count = 0;
    var poolId;

    $('#pool-id').empty().select2({
        minimumResultsForSearch: -1,
        width: "415px"
    }).append($("<option></option>")
        .attr("value", 'all')
        .text("All pools"));

    for (var id in pools) {
        var poolData = pools[id];
        var poolName = poolData.vehicle.split('_').join(' ') + ' - ' + poolData.name;

        if (setasides.length == 0 || vehicleMap[poolData.vehicle]["sb"]) {
            poolMap[poolName] = id;
            count += 1;
            poolId = id;
        }
    }
    Object.keys(poolMap).sort().forEach(function(name) {
        $("#pool-id")
            .append($("<option></option>")
            .attr("value", poolMap[name])
            .text(name));
    });

    if (pool && pool in pools) {
        DataManager.setPoolData(pools[pool]);
        $("#pool-id").val(pool);
    }
    else {
        if (count == 1) {
            DataManager.setPool(poolId);
            DataManager.setPoolData(pools[pool]);
            $("#pool-id").val(poolId);
        }
        else {
            DataManager.setPool(null);
            DataManager.setPoolData(null);
            $("#pool-id").val('all');
        }
    }

    if (DataManager.getPool() != DataManager.getParameterByName('pool')) {
        EventManager.publish('poolChanged');
    }
    else {
        EventManager.publish('poolSelected');
    }
};

DataManager.populateZoneDropDown = function() {
    var zone = DataManager.getZone();
    var url = "/api/zones/";
    var queryData = {count: 1000};

    $('#zone-id').select2({placeholder:'Filter by zone', width: '415px'});

    DataManager.getAPIRequest(url, queryData, function(data) {
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
            DataManager.setZone(null);
            $("#zone-id").val('all');
        }

        if (DataManager.getZone() != DataManager.getParameterByName('zone')) {
            EventManager.publish('zoneChanged');
        }
        else {
            EventManager.publish('zoneSelected');
        }
    });
};

LayoutManager.initSearch = function() {
    EventManager.subscribe('dataChanged', LayoutManager.toggleFilters);
    EventManager.subscribe('pageInitialized', LayoutManager.toggleZone);
    EventManager.subscribe('dataChanged', LayoutManager.toggleZone);
    LayoutManager.hideZone();
};

LayoutManager.enableSearch = function() {
    LayoutManager.enableNaics();
    LayoutManager.enableVehicle();
    LayoutManager.enablePool();
    LayoutManager.toggleZone();
    LayoutManager.toggleFilters();
};

LayoutManager.disableSearch = function() {
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

LayoutManager.showPool = function() {
    if ($("div#zone_select").is(":visible")) {
        $("#pool-id").select2({width: '200px'});
        $("#zone-id").select2({width: '200px'});
    }
    else {
        $("#pool-id").select2({width: '415px'});
    }
    $("div#pool_select").show();
};

LayoutManager.disablePool = function() {
    $("div#pool_select select").attr("disabled", true);
};

LayoutManager.hidePool = function() {
    $("div#pool_select").hide();

    if ($("div#zone_select").is(":visible")) {
        $("#zone-id").select2({width: '415px'});
    }
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
    if ($("div#pool_select").is(":visible")) {
        $("#zone-id").select2({width: '200px'});
        $("#pool-id").select2({width: '200px'});
    }
    else {
        $("#zone-id").select2({width: '415px'});
    }
    $("div#zone_select").show();
};

LayoutManager.disableZone = function() {
    $("div#zone_select select").attr("disabled", true);
};

LayoutManager.hideZone = function() {
    $("div#zone_select").hide();

    if ($("div#pool_select").is(":visible")) {
        $("#pool-id").select2({width: '415px'});
    }
};

LayoutManager.toggleZone = function() {
    if (LayoutManager.zoneActive()) {
        LayoutManager.enableZone();
        LayoutManager.showZone();
    }
    else {
        LayoutManager.hideZone();
        LayoutManager.disableZone();
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
