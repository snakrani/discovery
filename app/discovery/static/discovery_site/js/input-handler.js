
var InputHandler = {
    init: function() {
        // event bindings
        $('#vehicle-id').on('select2:select select2:unselecting', this.sendVehicleChange.bind(InputHandler));
        $('#pool-id').on('select2:select select2:unselecting', this.sendPoolChange.bind(InputHandler));
        $('#naics-code').change(this.sendCodeChange.bind(InputHandler));
        $('#zone-id').change(this.sendZoneChange.bind(InputHandler));
        $('#setaside-filters').change(this.sendFilterChange.bind(InputHandler));
        $('input#pool_filter').change(this.sendPoolFilterContractsChange.bind(InputHandler));
        $('input#pool_filter').change(this.sendVendorPoolFilterChange.bind(InputHandler));

        //should this be bound to the InputHandler? KBD
        $('#vendor_contract_history_title_container').on('click', 'div.contracts_button', this.sendContractsChange.bind(InputHandler));
        $('#vendor_contract_history_title_container').on('keypress', 'div.contracts_button', this.sendContractsChange.bind(InputHandler));

        $('#pool_table').on('click', 'th.sortable', this.sortVendors.bind(InputHandler));
        $('#pool_table').on('keypress', 'th.sortable', this.sortVendors.bind(InputHandler));

        $('#ch_table').on('click', 'th.sortable', this.sortContracts.bind(InputHandler));
        $('#ch_table').on('keypress', 'th.sortable', this.sortContracts.bind(InputHandler));

        // event subscriptions
        EventManager.subscribe('loadPage', this.updateFields.bind(InputHandler));

        if (URLManager.isHomePage() || URLManager.isPoolPage()) {
            EventManager.subscribe('loadPage', this.populateZoneDropDown.bind(InputHandler));

            EventManager.subscribe('fieldsUpdated', this.loadVehiclePools.bind(InputHandler));
            EventManager.subscribe('vehicleChanged', this.loadVehiclePools.bind(InputHandler));
            EventManager.subscribe('poolDataLoaded', this.populateNaicsDropDown.bind(InputHandler));

            EventManager.subscribe('vehicleChanged', this.loadPools.bind(InputHandler));
            EventManager.subscribe('naicsChanged', this.loadPools.bind(InputHandler));

            EventManager.subscribe('poolUpdated', this.populateVehicleDropDown.bind(InputHandler));

            EventManager.subscribe('poolUpdated', this.populatePoolDropDown.bind(InputHandler));
            EventManager.subscribe('poolChanged', this.populatePoolDropDown.bind(InputHandler));
        }
        else {
            EventManager.subscribe('loadPage', this.loadPools.bind(InputHandler));
        }
    },

    updateFields: function(obj) {
        var setasides, i, len;

        if(obj['vehicle']){
            this.vehicle = obj['vehicle'];
            $('form#vehicle-select select').val(obj['vehicle']);
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

        if (obj.setasides) {
            setasides = obj.setasides.split(',');
            len = setasides.length - 1;

            for (i = 0; i < len; i++) {
                $('input[value=' + setasides[i] + ']').attr('checked', 'checked');
            }
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

            EventManager.publish('vendorsChanged', data);
        }
    },

    sortContracts: function(e) {
        //if enter pressed or if click then sort
        if ((e.type == "keypress" && e.charCode == 13) || e.type == "click") {
            var $target = $(e.target);
            var data = {
                'naics': this.naicsCode,
                'listType': 'naics',
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
            if ($button.text() == "All Contracts") { data['listType'] = 'all'; }
            else { data['listType'] = 'naics'; }

            EventManager.publish('contractsChanged', data);
        }
    },

    sendContractsChange: function(e) {
        if ((e.type == "keypress" && e.charCode == 13) || e.type == "click") {
            var listType = 'naics';

            if(e.target.textContent == "All Contracts" || e.target.innerText == "All Contracts"){
                this.naicsCode = 'all';
                listType = 'all';
            } else {
                this.naicsCode = $("#vendor_contract_history_title_container").find("div").first().text().replace(/\D/g,'').trim();
            }

            //reset date header column classes
            var $date = $("div#ch_table th.h_date_signed");
            $date.removeClass('arrow-sortable').addClass('arrow-down').attr("title", "Sorted descending");
            $date.siblings('.sortable').removeClass('arrow-down').removeClass('arrow-up').addClass('arrow-sortable').attr("title", "Select to sort");

            EventManager.publish('contractsChanged', {'page': 1, 'naics': this.naicsCode, 'listType': listType});
            return false;
        }
    },

    sendPoolFilterContractsChange: function() {
        var listType = 'naics';

        var $button = $("#vendor_contract_history_title_container").find('.contracts_button_active');
        if ($button.text() == "All Contracts") {
            this.naicsCode = 'all';
            listType = 'all';
        }
        else {
            this.naicsCode = $("#vendor_contract_history_title_container").find("div").first().text().replace(/\D/g,'').trim();
        }

        //reset date header column classes
        var $date = $("div#ch_table th.h_date_signed");
        $date.removeClass('arrow-sortable').addClass('arrow-down').attr("title", "Sorted descending");
        $date.siblings('.sortable').removeClass('arrow-down').removeClass('arrow-up').addClass('arrow-sortable').attr("title", "Select to sort");

        EventManager.publish('contractsChanged', {'page': 1, 'naics': this.naicsCode, 'listType': listType});
        return false;
    },

    sendVehicleChange: function() {
        this.vehicle = $('form#vehicle-select select').val(); //to get the default

        $("form#setaside-filters input:checked").prop('checked', false);
        EventManager.publish('vehicleChanged', {'vehicle': this.vehicle, 'vehicleOnly': true});
    },

    sendPoolChange: function(e) {
        this.poolId = $('#pool-id').val();
        EventManager.publish('poolChanged', this.poolId);
    },

    sendCodeChange: function(e) {
        this.naicsCode = $('#naics-code').val();
        EventManager.publish('naicsChanged', this.naicsCode);
    },

    sendZoneChange: function(e) {
        this.zoneId = $('#zone-id').val();
        EventManager.publish('zoneChanged', this.zoneId);
    },

    sendFilterChange: function() {
        EventManager.publish('filtersChanged');
    },

    sendVendorPoolFilterChange: function() {
        EventManager.publish('vendorPoolFilterChanged');
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

    getZone: function() {
        return this.zoneId;
    },

    getSetasides: function() {
        /* returns array of setaside ids that are checked */
        var setasides = [];
        $("form#setaside-filters input:checked").each(function(index) {
            setasides.push($(this).val());
        });

        return setasides;
    },

    //getVendorPoolFilter: function() {
    //  return $('input#pool_filter').is(':checked');
    //},

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

                if (! vehicle || vehicle == 'all' || pool.vehicle == vehicle) {
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

        if (pool && pool != 'all' && pool in poolMap) {
            RequestsManager.pool = poolMap[pool];
        }
        else {
            RequestsManager.pool = null;
        }

        EventManager.publish('poolSelected', RequestsManager.pool);
    },

    loadVehiclePools: function() {
        var vehicle = this.getVehicle();
        var url = "/api/pools/";
        var queryData = {};

        if (vehicle && vehicle != 'all') {
            queryData['vehicle__iexact'] = vehicle;
        }

        RequestsManager.getAPIRequest(url, queryData, function(data) {
            var naicsMap = {};
            var pool;
            var naics;

            for (var poolIndex = 0; poolIndex < data.results.length; poolIndex++) {
                pool = data.results[poolIndex];

                if (vehicle !== null || pool.vehicle == vehicle.toUpperCase()) {
                    for (var naicsIndex = 0; naicsIndex < pool.naics.length; naicsIndex++) {
                        naics = pool.naics[naicsIndex].code;

                        if (!(naics in naicsMap)) {
                            naicsMap[naics] = [];
                        }
                        naicsMap[naics].push(pool.vehicle + "|" + pool.number);
                    }
                }
            }
            EventManager.publish('poolDataLoaded', {"vehicle": vehicle, "naics": naicsMap});
        });
    },

    populateVehicleDropDown: function() {
        var pools = RequestsManager.naicsPools;
        var vehicle = URLManager.getParameterByName('vehicle');
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
            $("#vehicle-id").val('all');
        }
    },

    populatePoolDropDown: function(updatedId) {
        var pools = RequestsManager.vehiclePools;
        var count = 0;
        var pool;

        if (updatedId) {
            pool = updatedId;
        }
        else {
            pool = URLManager.getParameterByName('pool');
        }

        $('#pool-id').empty().select2({
            'placeholder': 'Select a pool',
            minimumResultsForSearch: -1,
            width: "415px"
        }).append($("<option></option>")
            .attr("value", 'all')
            .text("All pools"));

        Object.keys(pools).forEach(function (id) {
            var pool = pools[id];

            $("#pool-id")
                .append($("<option></option>")
                .attr("value", id)
                .text(pool.name + " (" + pool.vehicle.split('_').join(' ') + ")"));

            count += 1;
        });

        if (pool && pool in pools) {
            $("#pool-id").val(pool);
        }
        else {
            $("#pool-id").val('all');
        }

        if (count > 1) {
            LayoutManager.showPools();
        }
        else {
            LayoutManager.hidePools();
        }

        this.updatePools();
    },

    populateNaicsDropDown: function(data) {
        var vehicle = (data !== undefined ? data.vehicle : null);
        var naicsMap = (data !== undefined ? data.naics : {});
        var naics = URLManager.getParameterByName('naics-code');
        var naics_exists = false;
        var first_naics = null;

        $('#naics-code').select2({placeholder:'Select a NAICS code', width: '600px'});

        // can't seem to use cached job, something goes wrong with select2
        this.populatePromise = RequestsManager.getAPIRequest(
            "/api/naics/",
            { ordering: "description", code__in: Object.keys(naicsMap).join(',') },
            function( data ) {
                $("#naics-code").empty().append($("<option></option>"));

                $.each(data.results, function(key, result) {
                    if ($.isEmptyObject(naicsMap) || (result.code in naicsMap)) {
                        if (!first_naics) {
                            first_naics = result.code;
                        }
                        if (naics == result.code) {
                            naics_exists = true;
                        }
                        $("#naics-code")
                            .append($("<option></option>")
                            .attr("value", result.code)
                            .text(result.description + " ( " + result.code + " ) "));
                    }
                });

                if (naics_exists || ! naics) {
                    $("#naics-code").val(naics).trigger('change');
                }
                else {
                    $("#naics-code").val(first_naics).trigger('change');
                }
            }
        );
    },

    populateZoneDropDown: function() {
        var zone = URLManager.getParameterByName('zone');
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
        });
    }
};
