
DataManager.initSearch = function() {
    // External action subscriptions
    $('#vehicle-id').on('click select2:select select2:unselect', DataManager.sendVehicleChange);
    $('#pool-id').on('click select2:select select2:unselect', DataManager.sendPoolChange);
    $('#naics-code').on('click select2:select select2:unselect', DataManager.sendNaicsChange);
    $('#zone-id').on('click select2:select select2:unselect', DataManager.sendZoneChange);
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

DataManager.defaultNaicsWidth = function() {
    return '620px';
};

DataManager.setNaicsWidth = function(width) {
    DataManager.set('naics_width', width);
};

DataManager.getNaicsWidth = function() {
    return DataManager.get('naics_width', DataManager.defaultNaicsWidth());
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

DataManager.defaultVehicleWidth = function() {
    return '150px';
};

DataManager.setVehicleWidth = function(width) {
    DataManager.set('vehicle_width', width);
};

DataManager.getVehicleWidth = function() {
    return DataManager.get('vehicle_width', DataManager.defaultVehicleWidth());
};

DataManager.sendVehicleChange = function() {
    DataManager.setVehicle($('#vehicle-id').val());
    EventManager.publish('vehicleChanged');
};

DataManager.setPools = function(values) {
    if (typeof values == 'string') {
        values = [values];
    }
    DataManager.set('pools', values);
};

DataManager.getPools = function() {
    return DataManager.get('pools', []);
};

DataManager.defaultPoolWidth = function() {
    return '455px';
};

DataManager.compressedPoolWidth = function() {
    return '235px';
};

DataManager.setPoolWidth = function(width) {
    DataManager.set('pool_width', width);
};

DataManager.getPoolWidth = function() {
    return DataManager.get('pool_width', DataManager.defaultPoolWidth());
};

DataManager.getSortedPools = function(pools, defaultPools) {
    var vehicleMap = DataManager.getVehicleMap();
    var vehiclePools = DataManager.getVehiclePools();
    var vehiclePoolIds = Object.keys(vehiclePools);

    if (pools.length == 0 && defaultPools) {
        pools = defaultPools;
    }
    else {
        pools = pools.filter(function(id) { return vehiclePoolIds.indexOf(id) > -1; });
    }
    pools = pools.sort(function(a, b) {
        a = vehiclePools[a];
        b = vehiclePools[b];

        if (a.vehicle == b.vehicle) {
            if (vehicleMap[a.vehicle].pool_numeric) {
                return a.number - b.number;
            }
            else {
                return a.number > b.number ? 1 : -1;
            }
        }
        return a.vehicle > b.vehicle ? 1 : -1;
    });
    return pools;
};

DataManager.sendPoolChange = function(e) {
    DataManager.setPools($('#pool-id').val());
    EventManager.publish('poolChanged');
};

DataManager.setZones = function(values) {
    if (typeof values == 'string') {
        values = [values];
    }
    DataManager.set('zones', values);
};

DataManager.getZones = function() {
    return DataManager.get('zones', []);
};

DataManager.defaultZoneWidth = function() {
    return '205px';
};

DataManager.setZoneWidth = function(width) {
    DataManager.set('zone_width', width);
};

DataManager.getZoneWidth = function() {
    return DataManager.get('zone_width', DataManager.defaultZoneWidth());
};

DataManager.sendZoneChange = function(e) {
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
        $('#pool-id').attr('multiple', 'multiple');
    }
    else {
        DataManager.setVehicle(null);
        $("#vehicle-id").val('all');
        $('#pool-id').removeAttr('multiple');
    }

    if (DataManager.getVehicle() != DataManager.getParameterByName('vehicle')) {
        EventManager.publish('vehicleChanged');
    }
    else {
        EventManager.publish('vehicleSelected');
    }
};

DataManager.populatePoolDropDown = function() {
    var vehicle = DataManager.getVehicle();
    var vehiclePools = DataManager.getVehiclePools();
    var vehiclePoolIds = DataManager.getSortedPools(Object.keys(vehiclePools));
    var pools = DataManager.getSortedPools(DataManager.getPools());
    var count = 0;
    var poolId;

    if (vehicle) {
        $('#pool-id').empty();
    }
    else {
        $('#pool-id').empty()
            .append($("<option></option>")
            .attr("value", 'all')
            .text("All service categories"));
    }

    for (var index = 0; index < vehiclePoolIds.length; index++) {
        var id = vehiclePoolIds[index];
        var poolData = vehiclePools[id];
        var poolName = poolData.vehicle.split('_').join(' ') + ' ' + poolData.number + ' - ' + poolData.name;

        $("#pool-id")
            .append($("<option></option>")
            .attr("value", id)
            .text(poolName));

	    count += 1;
        poolId = id;
    }

    if (pools.length > 0) {
        if (vehicle) {
            DataManager.setPools(pools);
            $("#pool-id").val(pools);
        }
        else {
            DataManager.setPools([pools[0]]);
            $("#pool-id").val(pools[0]);
        }
    }
    else {
        if (count == 1) {
            DataManager.setPools([poolId]);

            if (vehicle) {
                $("#pool-id").val([poolId]);
            }
            else {
                $("#pool-id").val(poolId);
            }
        }
        else {
            DataManager.setPools([]);

            if (vehicle) {
                $("#pool-id").val([]);
            }
            else {
                $("#pool-id").val('all');
            }
        }
    }

    var currentSelection = DataManager.getPools().join(',');
    var paramSelection = DataManager.getParameterByName('pools');

    if (!paramSelection) {
        paramSelection = "";
    }

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

        if (currentSelection != paramSelection) {
            EventManager.publish('zoneChanged');
        }
        else {
            EventManager.publish('zoneSelected');
        }
    });
};

LayoutManager.initSearch = function() {
    // Internal event subscriptions
    EventManager.subscribe('dataInitialized', LayoutManager.updateSearch);

    // Input element initialization
    if (LayoutManager.zoneActive()) {
        DataManager.setPoolWidth(DataManager.compressedPoolWidth());
    }

    LayoutManager.initNaics();
    LayoutManager.initVehicle();
    LayoutManager.initPool();
    LayoutManager.initZone();
};

LayoutManager.updateSearch = function() {
    // Element actions
    setTimeout(function(){
        LayoutManager.initNaics(true);
        LayoutManager.initVehicle(true);
        LayoutManager.initPool(true);
        LayoutManager.initZone(true);
    }, 50);
};

LayoutManager.enableSearch = function() {
    $('.table_wrapper').removeClass('loading');
    $('#pool_table').removeClass('init');

    LayoutManager.enableNaics();
    LayoutManager.enableVehicle();
    LayoutManager.enablePool();
    LayoutManager.enableZone();
    LayoutManager.toggleFilters();
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

LayoutManager.initNaics = function(update) {
    if (update) {
        $('#naics-code').select2('destroy');
    }
    $('#naics-code').select2({
        placeholder: 'Select NAICS code',
        minimumResultsForSearch: 1,
        dropdownAutoWidth: true,
        width: DataManager.getNaicsWidth()
    });
};

LayoutManager.enableNaics = function() {
    $("div#naics_select select").attr("disabled", false);
};

LayoutManager.disableNaics = function() {
    $("div#naics_select select").attr("disabled", true);
};

LayoutManager.initVehicle = function(update) {
    if (update) {
        $('#vehicle-id').select2('destroy');
    }
    $('#vehicle-id').select2({
        placeholder: 'Select vehicle',
        minimumResultsForSearch: -1,
        dropdownAutoWidth: true,
        width: DataManager.getVehicleWidth()
    });
};

LayoutManager.enableVehicle = function() {
    $("div#vehicle_select select").attr("disabled", false);
};

LayoutManager.disableVehicle = function() {
    $("div#vehicle_select select").attr("disabled", true);
};

LayoutManager.initPool = function(update) {
    var vehicle = DataManager.getVehicle();
    var options = {
        placeholder: 'Select service categories',
        minimumResultsForSearch: -1,
        dropdownAutoWidth: true,
        width: DataManager.getPoolWidth()
    };
    if (vehicle) {
        options['allowClear'] = true;
    }

    if (update) {
        $('#pool-id').select2('destroy');
    }
    $('#pool-id').select2(options);
};

LayoutManager.enablePool = function() {
    $("div#pool_select select").attr("disabled", false);
};

LayoutManager.disablePool = function() {
    $("div#pool_select select").attr("disabled", true);
};

LayoutManager.initZone = function(update) {
    if (update) {
        $('#zone-id').select2('destroy');
    }
    $('#zone-id').select2({
        placeholder: 'Select service zones',
        minimumResultsForSearch: -1,
        allowClear: true,
        dropdownAutoWidth: true,
        width: DataManager.getZoneWidth()
    });
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
    DataManager.setPoolWidth(DataManager.compressedPoolWidth());
    $("div#zone_select").show();
};

LayoutManager.disableZone = function() {
    $("div#zone_select select").attr("disabled", true);
};

LayoutManager.hideZone = function() {
    DataManager.setPoolWidth(DataManager.defaultPoolWidth());
    $("div#zone_select").hide();
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
