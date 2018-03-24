
var InputHandler = {
    init: function() {
        this.populateNaicsDropDown();

        // event bindings
        $('#naics-code').change(this.sendCodeChange.bind(InputHandler));
        $('#setaside-filters').change(this.sendFilterChange);
        $('form#vehicle-select select').change(this.sendVehicleChange.bind(InputHandler));
        //should this be bound to the InputHandler? KBD
        $('#vendor_contract_history_title_container').on('click', 'div.contracts_button', this.sendContractsChange);
        $('#vendor_contract_history_title_container').on('keypress', 'div.contracts_button', this.sendContractsChange);

        $('#pool_table').on('click', 'th.sortable', this.sortVendors);
        $('#pool_table').on('keypress', 'th.sortable', this.sortVendors);

        $('#ch_table').on('click', 'th.sortable', this.sortContracts);
        $('#ch_table').on('keypress', 'th.sortable', this.sortContracts);

        // event subscriptions
        Events.subscribe('loadedWithQS', this.updateFields.bind(InputHandler));

        Events.subscribe('fieldsUpdated', this.loadPool.bind(InputHandler));
        Events.subscribe('naicsChanged', this.loadPool.bind(InputHandler));
        Events.subscribe('fieldsUpdated', this.loadVehiclePools.bind(InputHandler));
        Events.subscribe('vehicleChanged', this.loadVehiclePools.bind(InputHandler));
        Events.subscribe('poolDataLoaded', this.populateNaicsDropDown.bind(InputHandler));
    },

    updateFields: function(obj) {
        var setasides, i, len;

        if (obj['naics-code'] !== null) {
            $('#naics-code').val(obj['naics-code']).trigger('change');
            this.naicsCode = obj['naics-code'];
        }

        if (obj.setasides) {
            setasides = obj.setasides.split(',');
            len = setasides.length - 1;

            for (i = 0; i < len; i++) {
                $('input[value=' + setasides[i] + ']').attr('checked', 'checked');
            }
        }

        if(obj.vehicle){
            this.vehicle = obj['vehicle'];
            $('form#vehicle-select select').val(obj['vehicle']);
        }

        Events.publish('fieldsUpdated');
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

            Events.publish('vendorsChanged', data);
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

            Events.publish('contractsChanged', data);
        }
    },

    sendContractsChange: function(e) {
        if ((e.type == "keypress" && e.charCode == 13) || e.type == "click") {
            var listType = 'naics';
            if(e.target.textContent == "All Contracts" || e.target.innerText == "All Contracts"){
                this.naicsCode = 'all';
                listType = 'all';
            } else {
                this.naicsCode = $("#vendor_contract_history_title_container").find("div").first().text().replace("NAICS", '').trim();
            }

            //reset date header column classes
            var $date = $("div#ch_table th.h_date_signed");
            $date.removeClass('arrow-sortable').addClass('arrow-down').attr("title", "Sorted descending");
            $date.siblings('.sortable').removeClass('arrow-down').removeClass('arrow-up').addClass('arrow-sortable').attr("title", "Select to sort");

            Events.publish('contractsChanged', {'page': 1, 'naics': this.naicsCode, 'listType': listType});
            return false;
        }
    },

    sendVehicleChange: function() {
        this.vehicle = $('form#vehicle-select select').val(); //to get the default

        $("form#setaside-filters input:checked").prop('checked', false);
        Events.publish('vehicleChanged', {'vehicle': this.vehicle, 'vehicleOnly': true});
    },

    sendCodeChange: function(e) {
        this.naicsCode = $('#naics-code').val();
        Events.publish('naicsChanged');
    },

    sendFilterChange: function() {
        Events.publish('filtersChanged');
    },

    getVehicle: function() {
        return this.vehicle;
    },

    getNAICSCode: function() {
        return this.naicsCode;
    },

    getPool: function() {
        return this.pool;
    },

    getSetasides: function() {
        /* returns array of setaside ids that are checked */
        var setasides = [];
        $("form#setaside-filters input:checked").each(function(index) {
            setasides.push($(this).val());
        });

        return setasides;
    },

    loadPool: function() {
        var vehicle = this.getVehicle();
        var naics = this.getNAICSCode();
        var url = "/api/pools/";
        var queryData = {};

        if (vehicle !== null && naics !== null) {
            queryData['vehicle__iexact'] = vehicle;
            queryData['naics__code'] = naics;

            RequestsManager.getAPIRequest(url, queryData, function(data) {
                if (data['results'].length == 1) {
                    Events.publish('poolUpdated', data['results'][0]);
                }
            });
        }
    },

    loadVehiclePools: function() {
        var vehicle = this.getVehicle();
        var url = "/api/pools/";
        var queryData = {};

        if (vehicle !== null) {
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
                        naicsMap[naics].push(pool.number);
                    }
                }
            }
            Events.publish('poolDataLoaded', {"vehicle": vehicle, "naics": naicsMap});
        });
    },

    populateNaicsDropDown: function(data) {
        var vehicle = (data !== undefined ? data.vehicle : null);
        var naicsMap = (data !== undefined ? data.naics : {});
        var naics = URLManager.getParameterByName('naics-code');
        var naics_exists = false;
        var first_naics = null;

        $('#naics-code').select2({placeholder:'Select a NAICS code', width: '380px'});

        // can't seem to use cached jqobj, something goes wrong with select2
        this.populatePromise = RequestsManager.getAPIRequest(
            "/api/naics/",
            { ordering: "description" },
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

                if (naics_exists) {
                    $("#naics-code").select2({placeholder:'Select a NAICS code', width: '380px'}).val(naics).trigger('change');
                }
                else {
                    $("#naics-code").select2({placeholder:'Select a NAICS code', width: '380px'}).val(first_naics).trigger('change');
                }
            }
        );
    },

    /*
     * This function is asynchronous because getting the selected NAICS text
     * depends on having populated the dropdown via a JSON request. Usage:
     *
     * InputHandler.getSelectedNAICS(function(text) {
     *   // do something with text here
     * });
     */
    getSelectedNAICS: function(callback) {
        this.populatePromise.done(function() {
            var text = $("#naics-code option:selected").text();
            callback(text);
        });
    }
};
