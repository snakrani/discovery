
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
        $('#vehicle-id').on('select2:select select2:unselecting', this.sendVehicleChange.bind(DataManager));
        $('#pool-id').on('select2:select select2:unselecting', this.sendPoolChange.bind(DataManager));
        $('#naics-code').on('select2:select select2:unselecting', this.sendCodeChange.bind(DataManager));
        $('#zone-id').on('select2:select select2:unselecting', this.sendZoneChange.bind(DataManager));
        $('#setaside-filters').change(this.sendFilterChange.bind(DataManager));
        $('#contract_pool_filters').change(this.sendPoolFilterContractsChange.bind(DataManager));

        $('#vendor_contract_history_title_container').on('click', 'div.contracts_button', this.sendContractsChange.bind(DataManager));
        $('#vendor_contract_history_title_container').on('keypress', 'div.contracts_button', this.sendContractsChange.bind(DataManager));

        $('#pool_table').on('click', 'th.sortable', this.sortVendors.bind(DataManager));
        $('#pool_table').on('keypress', 'th.sortable', this.sortVendors.bind(DataManager));

        $('#ch_table').on('click', 'th.sortable', this.sortContracts.bind(DataManager));
        $('#ch_table').on('keypress', 'th.sortable', this.sortContracts.bind(DataManager));

        // event subscriptions
        EventManager.subscribe('naicsChanged', this.update.bind(DataManager));
        EventManager.subscribe('vehicleChanged', this.update.bind(DataManager));
        EventManager.subscribe('poolChanged', this.update.bind(DataManager));
        EventManager.subscribe('zoneChanged', this.update.bind(DataManager));
        EventManager.subscribe('filtersChanged', this.update.bind(DataManager));
        EventManager.subscribe('vendorsChanged', this.update.bind(DataManager));
        EventManager.subscribe('contractsChanged', this.update.bind(DataManager));

        EventManager.subscribe('pageUpdated', this.bootstrap.bind(DataManager));
        EventManager.subscribe('pageInitialized', this.loadPools.bind(DataManager));

        if (LayoutManager.isHomePage() || LayoutManager.isPoolPage()) {
            EventManager.subscribe('poolUpdated', this.loadNaicsMap.bind(DataManager));

            EventManager.subscribe('naicsMapLoaded', this.populateVehicleDropDown.bind(DataManager));
            EventManager.subscribe('vehicleSelected', this.populatePoolDropDown.bind(DataManager));
            EventManager.subscribe('poolSelected', this.populateNaicsDropDown.bind(DataManager));
            EventManager.subscribe('naicsSelected', this.populateZoneDropDown.bind(DataManager));
            EventManager.subscribe('zoneSelected', this.sendDataChange.bind(DataManager));
        }
        else {
            EventManager.subscribe('poolUpdated', this.sendDataChange.bind(DataManager));
            EventManager.subscribe('dataChanged', this.initContractSort.bind(DataManager));
        }
    },

    bootstrap: function() {
        var vehicle = this.getParameterByName('vehicle');
        var pool = this.getParameterByName('pool');
        var naics = this.getParameterByName('naics-code');
        var zone = this.getParameterByName('zone');
        var setasides = this.getParameterByName('setasides');
        var type = this.getParameterByName('type');
        var page = this.getParameterByName('page');
        var count = this.getParameterByName('count');
        var ordering = this.getParameterByName('ordering');
        var data = {};

        if (vehicle) {
            this.vehicle = vehicle;
        }
        if (pool) {
            this.poolId = pool;
        }
        if (naics) {
            this.naicsCode = naics;
        }
        if (zone) {
            this.zoneId = zone;
        }
        if (setasides) {
            var setasides = setasides.split(',');
            var len = setasides.length - 1;

            for (var i = 0; i < len; i++) {
                $('input[value=' + setasides[i] + ']').attr('checked', 'checked');
            }
        }
        if (type) {
            this.listType = type;
        }
        else {
            this.listType = 'naics';
        }

        if (page) {
            this.page = page;
        }
        else {
            this.page = 1;
        }
        if (count) {
            this.pageCount = count;
        }
        else {
            this.pageCount = this.getDefaultPageCount();
        }
        if (ordering) {
            this.sortOrdering = ordering;
        }

        LayoutManager.route(data);
        LayoutManager.toggleZones();
        EventManager.publish('pageInitialized');
    },

    buildRequestQuery: function() {
        var vehicle = this.getVehicle();
        var pools = this.getVehiclePools();
        var pool = this.getPoolId();
        var naics = this.getNAICSCode();
        var zone = this.getZone();
        var setasides = this.getSetasides();
        var contractPools = this.getContractPools();
        var listType = this.getListType();
        var page = this.getPage();
        var pageCount = this.getPageCount();
        var sortOrdering = this.getSortOrdering();

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
        if (pageCount && pageCount != this.getPageCount()) {
            queryData['count'] = pageCount;
        }

        if (sortOrdering) {
            queryData['ordering'] = sortOrdering;
        }

        if (this.getParameterByName('test')) {
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

            this.sortOrdering = class_map[classes[0]];
            this.page = 1;

            if ($target.hasClass('arrow-down')) {
                $target.removeClass('arrow-down').addClass('arrow-up').attr("title", "Sorted ascending");
            } else if ($target.hasClass('arrow-sortable')) {
                this.sortOrdering = "-" + this.sortOrdering;
                $target.removeClass('arrow-sortable').addClass('arrow-down').attr("title", "Sorted descending");
            } else {
                this.sortOrdering = "-" + this.sortOrdering;
                $target.removeClass('arrow-up').addClass('arrow-down').attr("title", "Sorted descending");
            }

            //reset other ths that are sortable
            $target.siblings('.sortable').removeClass('arrow-down').removeClass('arrow-up').addClass('arrow-sortable').attr("title", "Select to sort");

            EventManager.publish('vendorsChanged');
        }
    },

    initContractSort: function() {
        var ordering = this.getSortOrdering();

        if (ordering) {
            var asc = (ordering[0] == '-' ? false : true);
            var field = this.getOrderingField(ordering.replace(/^-/, ''));
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

            this.sortOrdering = class_map[classes[0]];
            this.page = 1;

            if ($target.hasClass('arrow-down')) {
                $target.removeClass('arrow-down').addClass('arrow-up').attr("title", "Sorted ascending");
            } else if ($target.hasClass('arrow-sortable')) {
                this.sortOrdering = "-" + this.sortOrdering;
                $target.removeClass('arrow-sortable').addClass('arrow-down').attr("title", "Sorted descending");
            } else {
                this.sortOrdering = "-" + this.sortOrdering;
                $target.removeClass('arrow-up').addClass('arrow-down').attr("title", "Sorted descending");
            }

            //reset other ths that are sortable
            $target.siblings('.sortable').removeClass('arrow-down').removeClass('arrow-up').addClass('arrow-sortable').attr("title", "Select to sort");

            //prevent button flipping by selecting proper listType
            var $button = $("#vendor_contract_history_title_container").find('.contracts_button_active');
            if ($button.text() == "All Contracts") { this.listType = 'all'; }
            else { this.listType = 'naics'; }

            EventManager.publish('contractsChanged');
        }
    },

    sendContractsChange: function(e) {
        if ((e.type == "keypress" && e.charCode == 13) || e.type == "click") {
            this.listType = 'naics';

            if(e.target.textContent == "All Contracts" || e.target.innerText == "All Contracts"){
                this.listType = 'all';
            }

            //reset date header column classes
            var $date = $("div#ch_table th.h_date_signed");
            $date.removeClass('arrow-sortable').addClass('arrow-down').attr("title", "Sorted descending");
            $date.siblings('.sortable').removeClass('arrow-down').removeClass('arrow-up').addClass('arrow-sortable').attr("title", "Select to sort");

            EventManager.publish('contractsChanged');
        }
    },

    sendPoolFilterContractsChange: function() {
        this.listType = 'naics';

        var $button = $("#vendor_contract_history_title_container").find('.contracts_button_active');
        if ($button.text() == "All Contracts") {
            this.listType = 'all';
        }

        //reset date header column classes
        var $date = $("div#ch_table th.h_date_signed");
        $date.removeClass('arrow-sortable').addClass('arrow-down').attr("title", "Sorted descending");
        $date.siblings('.sortable').removeClass('arrow-down').removeClass('arrow-up').addClass('arrow-sortable').attr("title", "Select to sort");

        this.pool = this.getContractPools();

        EventManager.publish('contractsChanged');
    },

    sendVehicleChange: function() {
        this.vehicle = $('#vehicle-id').val();

        if (this.vehicle && this.vehicle == 'all') {
            this.vehicle = null;
        }
        EventManager.publish('vehicleChanged', this.vehicle);
    },

    sendPoolChange: function(e) {
        this.poolId = $('#pool-id').val();

        if (this.poolId && this.poolId == 'all') {
            this.poolId = null;
        }
        EventManager.publish('poolChanged', this.poolId);
    },

    sendCodeChange: function(e) {
        this.naicsCode = $('#naics-code').val();

        if (this.naicsCode && this.naicsCode == 'all') {
            this.naicsCode = null;
        }
        EventManager.publish('naicsChanged', this.naicsCode);
    },

    sendZoneChange: function(e) {
        this.zoneId = $('#zone-id').val();

        if (this.zoneId && this.zoneId == 'all') {
            this.zoneId = null;
        }
        EventManager.publish('zoneChanged', this.zoneId);
    },

    sendFilterChange: function() {
        EventManager.publish('filtersChanged');
    },

    sendDataChange: function() {
        EventManager.publish('dataChanged');
    },

    update: function() {
        History.pushState('', this.title, this.getURL());
        EventManager.publish('pageUpdated');
    },

    getURL: function(params) {
        return window.location.pathname + this.getQueryString(params);
    },

    getQueryString: function(params) {
        var queryObject = this.buildRequestQuery();
        var qs = '?';
        var k;

        if('naics' in queryObject) {
            queryObject['naics-code'] = queryObject.naics;
            delete queryObject.naics;
        }

        if (params !== undefined) {
            for (key in params) {
                queryObject[key] = params[key];
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
        return this.vehicle;
    },

    getVehicleMap: function() {
        return this.vehicleMap;
    },

    getPoolId: function() {
        return this.poolId;
    },

    getPool: function() {
        return this.pool;
    },

    getVehiclePools: function() {
        return this.vehiclePools;
    },

    getNAICSPools: function() {
        return this.naicsPools;
    },

    getNAICSCode: function() {
        return this.naicsCode;
    },

    getNaicsMap: function() {
        return this.naicsMap;
    },

    getZone: function() {
        return this.zoneId;
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
        return this.vendor;
    },

    getContractPools: function() {
        var pools = [];

        $("form#contract_pool_filters input:checked").each(function(index) {
            pools.push($(this).val());
        });

        return pools;
    },

    getListType: function() {
        return this.listType;
    },

    getPage: function() {
        return this.page;
    },

    getPageCount: function() {
        return this.pageCount;
    },

    getDefaultPageCount: function() {
        if (this.getParameterByName('test')) {
            return 5;
        }
        return 50;
    },

    getSortOrdering: function() {
        return this.sortOrdering;
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
        var vehicle = this.getVehicle();
        var naics = this.getNAICSCode();
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

            this.vehiclePools = vehiclePoolMap;
            this.naicsPools = naicsPoolMap;

            EventManager.publish('poolUpdated');
        });
    },

    loadNaicsMap: function() {
        var vehicle = this.getVehicle();
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

            this.naicsMap = naicsMap;
            EventManager.publish('naicsMapLoaded');
        });
    },

    populateVehicleDropDown: function() {
        var pools = this.getNaicsPools();
        var vehicle = this.getVehicle();
        var setasides = this.getSetasides();
        var vehicleMap = this.getVehicleMap();
        var vehicles = {};

        $('#vehicle-id').empty().select2({
            minimumResultsForSearch: -1,
            width: "170px"
        }).append($("<option></option>")
            .attr("value", 'all')
            .text("All vehicles"));

        Object.keys(pools).forEach(function (id) {
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
            this.vehicle = null;
            $("#vehicle-id").val('all');
        }

        if (this.getVehicle() != this.getParameterByName('vehicle')) {
            EventManager.publish('vehicleChanged');
        }
        else {
            EventManager.publish('vehicleSelected');
        }
    },

    populatePoolDropDown: function() {
        var pools = this.getVehiclePools();
        var pool = this.getPoolId();
        var setasides = this.getSetasides();
        var vehicleMap = this.getVehicleMap();
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
            this.pool = pools[pool];
            $("#pool-id").val(pool);
        }
        else {
            if (count == 1) {
                this.poolId = poolId;
                this.pool = pools[poolId];
                $("#pool-id").val(poolId);
            }
            else {
                this.poolId = null;
                this.pool = null;
                $("#pool-id").val('all');
            }
        }

        if (this.getPoolId() != this.getParameterByName('pool')) {
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
        var vehicle = this.getVehicle();
        var naicsMap = this.getNaicsMap();
        var pool = this.getPoolId();
        var naics = this.getNAICSCode();

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
                    this.naicsCode = null;
                    $("#naics-code").val('all');
                }

                if (this.getNAICSCode() != this.getParameterByName('naics-code')) {
                    EventManager.publish('naicsChanged');
                }
                else {
                    EventManager.publish('naicsSelected');
                }
            }
        );
    },

    populateZoneDropDown: function() {
        var zone = this.getZone();
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
                this.zoneId = null;
                $("#zone-id").val('all');
            }

            if (this.getZone() != this.getParameterByName('zone')) {
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
