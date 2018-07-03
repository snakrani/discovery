
var InputHandler = {
    init: function() {
        // event bindings
        $('#vehicle-id').on('select2:select select2:unselecting', this.sendVehicleChange.bind(InputHandler));
        $('#pool-id').on('select2:select select2:unselecting', this.sendPoolChange.bind(InputHandler));
        $('#naics-code').on('select2:select select2:unselecting', this.sendCodeChange.bind(InputHandler));
        $('#zone-id').on('select2:select select2:unselecting', this.sendZoneChange.bind(InputHandler));
        $('#setaside-filters').change(this.sendFilterChange.bind(InputHandler));
        $('#contract_pool_filters').change(this.sendPoolFilterContractsChange.bind(InputHandler));

        $('#vendor_contract_history_title_container').on('click', 'div.contracts_button', this.sendContractsChange.bind(InputHandler));
        $('#vendor_contract_history_title_container').on('keypress', 'div.contracts_button', this.sendContractsChange.bind(InputHandler));

        $('#pool_table').on('click', 'th.sortable', this.sortVendors.bind(InputHandler));
        $('#pool_table').on('keypress', 'th.sortable', this.sortVendors.bind(InputHandler));

        $('#ch_table').on('click', 'th.sortable', this.sortContracts.bind(InputHandler));
        $('#ch_table').on('keypress', 'th.sortable', this.sortContracts.bind(InputHandler));

        // event subscriptions
        EventManager.subscribe('loadPage', this.updateFields.bind(InputHandler));
        EventManager.subscribe('fieldsUpdated', this.loadPools.bind(InputHandler));

        if (URLManager.isHomePage() || URLManager.isPoolPage()) {
            EventManager.subscribe('poolUpdated', this.loadNaicsMap.bind(InputHandler));

            EventManager.subscribe('naicsMapLoaded', this.populateVehicleDropDown.bind(InputHandler));
            EventManager.subscribe('vehicleSelected', this.populatePoolDropDown.bind(InputHandler));
            EventManager.subscribe('poolSelected', this.populateNaicsDropDown.bind(InputHandler));
            EventManager.subscribe('naicsSelected', this.populateZoneDropDown.bind(InputHandler));
            EventManager.subscribe('zoneSelected', this.sendDataChange.bind(InputHandler));
        }
        else {
            EventManager.subscribe('poolUpdated', this.sendDataChange.bind(InputHandler));
        }
    },

    updateFields: function(obj) {
        var setasides, i, len;

        if(obj['vehicle']){
            this.vehicle = obj['vehicle'];
        }

        if (obj['pool']) {
            this.poolId = obj['pool'];
        }

        if (obj['naics-code']) {
            this.naicsCode = obj['naics-code'];
        }

        if (obj['zone']) {
            this.zoneId = obj['zone'];
        }

        if (obj['setasides']) {
            setasides = obj['setasides'].split(',');
            len = setasides.length - 1;

            for (i = 0; i < len; i++) {
                $('input[value=' + setasides[i] + ']').attr('checked', 'checked');
            }
        }

        if (obj['type']) {
            this.listType = obj['type'];
        }
        else {
            this.listType = 'naics';
        }

        LayoutManager.toggleZones();
        EventManager.publish('fieldsUpdated');
    },

    sortVendors: function(e) {
        //if enter pressed or if click then sort
        if ((e.type == "keypress" && e.charCode == 13) || e.type == "click") {
            var $target = $(e.target);
            var data = {};
            var class_map = RequestsManager.sortClassMap();

            var classes = $target.attr('class').split(' ');
            data['ordering'] = class_map[classes[0]];
            data['page'] = 1;

            if ($target.hasClass('arrow-down')) {
                $target.removeClass('arrow-down').addClass('arrow-up').attr("title", "Sorted ascending");
            } else if ($target.hasClass('arrow-sortable')) {
                data['ordering'] = "-" + data['ordering'];
                $target.removeClass('arrow-sortable').addClass('arrow-down').attr("title", "Sorted descending");
            } else {
                data['ordering'] = "-" + data['ordering'];
                $target.removeClass('arrow-up').addClass('arrow-down').attr("title", "Sorted descending");
            }

            //reset other ths that are sortable
            $target.siblings('.sortable').removeClass('arrow-down').removeClass('arrow-up').addClass('arrow-sortable').attr("title", "Select to sort");

            EventManager.publish('vendorsSorted', data);
        }
    },

    sortContracts: function(e) {
        //if enter pressed or if click then sort
        if ((e.type == "keypress" && e.charCode == 13) || e.type == "click") {
            var $target = $(e.target);
            var data = {
                'naics': this.getNAICSCode()
            };
            var class_map = RequestsManager.sortClassMap();
            var classes = $target.attr('class').split(' ');

            data['ordering'] = class_map[classes[0]];
            data['page'] = 1;

            if ($target.hasClass('arrow-down')) {
                $target.removeClass('arrow-down').addClass('arrow-up').attr("title", "Sorted ascending");
            } else if ($target.hasClass('arrow-sortable')) {
                data['ordering'] = "-" + data['ordering'];
                $target.removeClass('arrow-sortable').addClass('arrow-down').attr("title", "Sorted descending");
            } else {
                data['ordering'] = "-" + data['ordering'];
                $target.removeClass('arrow-up').addClass('arrow-down').attr("title", "Sorted descending");
            }

            //reset other ths that are sortable
            $target.siblings('.sortable').removeClass('arrow-down').removeClass('arrow-up').addClass('arrow-sortable').attr("title", "Select to sort");

            //prevent button flipping by selecting proper listType
            var $button = $("#vendor_contract_history_title_container").find('.contracts_button_active');
            if ($button.text() == "All Contracts") { this.listType = 'all'; }
            else { this.listType = 'naics'; }

            EventManager.publish('contractsSorted', data);
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

            EventManager.publish('contractsChanged', {});
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

        RequestsManager.pool = this.getContractPools();

        //EventManager.publish('contractsChanged', {});
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

    getVehicle: function() {
        return this.vehicle;
    },

    getPool: function() {
        return this.poolId;
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

            RequestsManager.vehiclePools = vehiclePoolMap;
            RequestsManager.naicsPools = naicsPoolMap;

            EventManager.publish('poolUpdated');
        });
    },

    updatePools: function() {
        var pool = this.getPool();
        var poolMap = RequestsManager.vehiclePools;

        if (pool && pool in poolMap) {
            RequestsManager.pool = poolMap[pool];
        }
        else {
            RequestsManager.pool = null;
        }

        EventManager.publish('poolSelected', RequestsManager.pool);
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

            InputHandler.naicsMap = naicsMap;
            EventManager.publish('naicsMapLoaded');
        });
    },

    populateVehicleDropDown: function() {
        var pools = RequestsManager.naicsPools;
        var vehicle = this.getVehicle();
        var vehicleMap = {
            "OASIS_SB": "OASIS Small Business",
            "OASIS": "OASIS Unrestricted",
            "HCATS_SB": "HCATS Small Business",
            "HCATS": "HCATS Unrestricted",
            "BMO_SB": "BMO Small Business",
            "BMO": "BMO Unrestricted",
            "PSS": "Professional Services"
        };

        $('#vehicle-id').empty().select2({
            'placeholder': 'Select a vehicle',
            minimumResultsForSearch: -1,
            width: "170px"
        }).append($("<option></option>")
            .attr("value", 'all')
            .text("All vehicles"));

        Object.keys(pools).forEach(function (id) {
            var pool = pools[id];

            if (pool.vehicle in vehicleMap) {
                $("#vehicle-id")
                    .append($("<option></option>")
                    .attr("value", pool.vehicle)
                    .text(vehicleMap[pool.vehicle]));

                delete vehicleMap[pool.vehicle];
            }
        });

        if (vehicle) {
            $("#vehicle-id").val(vehicle);
        }
        else {
            this.vehicle = null;
            $("#vehicle-id").val('all');
        }

        if (this.getVehicle() != URLManager.getParameterByName('vehicle')) {
            EventManager.publish('vehicleChanged');
        }
        else {
            EventManager.publish('vehicleSelected');
        }
    },

    populatePoolDropDown: function() {
        var pools = RequestsManager.vehiclePools;
        var pool = this.getPool();
        var count = 0;
        var poolId;

        $('#pool-id').empty().select2({
            'placeholder': 'Select a pool',
            minimumResultsForSearch: -1,
            width: "415px"
        }).append($("<option></option>")
            .attr("value", 'all')
            .text("All pools"));

        Object.keys(pools).forEach(function (id) {
            var poolData = pools[id];

            $("#pool-id")
                .append($("<option></option>")
                .attr("value", id)
                .text(poolData.name + " (" + poolData.vehicle.split('_').join(' ') + ")"));

            count += 1;
            poolId = id;
        });

        if (pool && pool in pools) {
            RequestsManager.pool = pools[pool];
            $("#pool-id").val(pool);
        }
        else {
            if (count == 1) {
                this.poolId = poolId;
                RequestsManager.pool = pools[poolId];
                $("#pool-id").val(poolId);
            }
            else {
                this.poolId = null;
                RequestsManager.pool = null;
                $("#pool-id").val('all');
            }
        }

        if (this.getPool() != URLManager.getParameterByName('pool')) {
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
        var pool = this.getPool();
        var naics = this.getNAICSCode();
        var naics_exists = false;
        var first_naics = null;

        $('#naics-code').select2({placeholder:'Select a NAICS code', width: '600px'});

        RequestsManager.getAPIRequest(
            "/api/naics/",
            { ordering: "code", code__in: Object.keys(naicsMap).join(',') },
            function( data ) {
                $("#naics-code").empty().append($("<option></option>"));

                $.each(data.results, function(key, result) {
                    if (result.code in naicsMap && (! pool || naicsMap[result.code].includes(pool))) {
                        if (!first_naics) {
                            first_naics = result.code;
                        }
                        if (naics == result.code) {
                            naics_exists = true;
                        }
                        $("#naics-code")
                            .append($("<option></option>")
                            .attr("value", result.code)
                            .text(result.code + ' - ' + result.description));
                    }
                });

                if (naics_exists || ! naics) {
                    $("#naics-code").val(naics);
                }
                else {
                    this.naicsCode = first_naics;
                    $("#naics-code").val(first_naics);
                }
            }
        );
        if (this.getNAICSCode() != URLManager.getParameterByName('naics-code')) {
            EventManager.publish('naicsChanged');
        }
        else {
            EventManager.publish('naicsSelected');
        }
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
        });
        if (this.getZone() != URLManager.getParameterByName('zone')) {
            EventManager.publish('zoneChanged');
        }
        else {
            EventManager.publish('zoneSelected');
        }
    }
};
