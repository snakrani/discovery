
DataManager.initializers.vendor = function() {
    // External action subscriptions
    $('#naics-code').on('click select2:select select2:unselecting', DataManager.sendNaicsChange);
    $('#contract_filters').change(DataManager.sendMembershipFilterChange);

    $('#ch_table').on('click', 'th.sortable', DataManager.sortContracts);
    $('#ch_table').on('keypress', 'th.sortable', DataManager.sortContracts);

    // Internal event subscriptions
    EventManager.subscribe('pageInitialized', DataManager.loadVendor);
    EventManager.subscribe('vendorLoaded', DataManager.loadPools);
    EventManager.subscribe('poolsUpdated', DataManager.populateNaicsDropDown);
    EventManager.subscribe('naicsSelected', DataManager.populateMembershipFilters);
    EventManager.subscribe('membershipSelected', DataManager.sendDataInitialized);
    EventManager.subscribe('dataInitialized', DataManager.loadContracts);

    EventManager.subscribe('naicsChanged', DataManager.update);
    EventManager.subscribe('membershipChanged', DataManager.update);
    EventManager.subscribe('sortChanged', DataManager.update);

    // Parameter initialization
    DataManager.set('duns', window.location.pathname.split('/')[2]);
    DataManager.collect('naics');

    DataManager.collect('memberships', null, function(field, value) {
        if (value) {
            value = value.split(',');
        }
        return value;
    });
};

DataManager.getStatusCount = function() {
    return 4;
};

DataManager.requestParams = function(queryData) {
    var naics = DataManager.getNaics();
    var memberships = DataManager.getMemberships();

    if (naics) {
        queryData['naics'] = naics;
    }
    if (memberships.length > 0) {
        queryData['memberships'] = memberships.join(',');
    }
    return queryData;
};

DataManager.setDuns = function(value) {
    DataManager.set('duns', value);
};

DataManager.getDuns = function() {
    return DataManager.get('duns', {});
};

DataManager.setVendor = function(value) {
    DataManager.set('vendor', value);
};

DataManager.getVendor = function() {
    return DataManager.get('vendor', {});
};

DataManager.getVendorMemberships = function() {
    return DataManager.getVendor().pools;
};

DataManager.getMembershipMap = function() {
    var vendorMemberships = DataManager.getVendorMemberships();
    var vehicleMap = DataManager.getVehicleMap();
    var poolMap = DataManager.getPoolMap();
    var membershipMap = {};

    for (var index = 0; index < vendorMemberships.length; index++) {
        var membership = vendorMemberships[index];

        if (!(membership.piid in membershipMap)) {
            membershipMap[membership.piid] = {
                'vehicleIds': [],
                'vehicles': [],
                'pools': [],
                'poolIds': [],
                'zones': [],
                'contacts': [],
                'phones': [],
                'emails': [],
                'setasides': [],
                'reference': membership
            };
        }

        var vehicle = poolMap[membership.pool.id].vehicle;
        var vehicleName = vehicleMap[vehicle].title;
        if (!$.inArray(vehicle, membershipMap[membership.piid]['vehicleIds'])) {
            membershipMap[membership.piid]['vehicleIds'].push(vehicle);
            membershipMap[membership.piid]['vehicles'].push(vehicleName);
        }

        var pool = membership.pool.id;
        var poolNumber = poolMap[pool].number;
        if (!$.inArray(pool, membershipMap[membership.piid]['poolIds'])) {
            membershipMap[membership.piid]['poolIds'].push(pool);
            membershipMap[membership.piid]['pools'].push(poolNumber);
        }
        for (var zindex = 0; zindex < membership.zones.length; zindex++) {
            var zoneId = membership.zones[zindex].id;
            if (!$.inArray(zoneId, membershipMap[membership.piid]['zones'])) {
                membershipMap[membership.piid]['zones'].push(zoneId);
            }
        }

        var contactName = membership.cms[0].name;
        if (!$.inArray(contactName, membershipMap[membership.piid]['contacts'])) {
            membershipMap[membership.piid]['contacts'].push(contactName);
        }
        var phoneNumber = membership.cms[0].phone.join('<br/>');
        if (!$.inArray(phoneNumber, membershipMap[membership.piid]['phones'])) {
            membershipMap[membership.piid]['phones'].push(phoneNumber);
        }
        var emailAddress = membership.cms[0].email.join('<br/>');
        if (!$.inArray(emailAddress, membershipMap[membership.piid]['emails'])) {
            membershipMap[membership.piid]['emails'].push(emailAddress);
        }
        for (var sindex = 0; sindex < membership.setasides.length; sindex++) {
            var setasideCode = membership.setasides[sindex].code;
            if (!$.inArray(setasideCode, membershipMap[membership.piid]['setasides'])) {
                membershipMap[membership.piid]['setasides'].push(setasideCode);
            }
        }
    }
    return membershipMap;
};

DataManager.getMembershipName = function(membershipInfo) {
    var membershipName = '';

    membershipInfo.pools.sort(function(a, b) {
        return Number(a) - Number(b);
    });
    membershipInfo.zones.sort(function(a, b) {
        return Number(a) - Number(b);
    });

    // Vehicle - Pool - Zone
    membershipName = '<div class="membership_vehicles">' + membershipInfo.vehicles.join(', ') + '</div>'
        + '<div class="membership_pools"><span class="admin_label">Service category:</span> ' + membershipInfo.pools.join(', ') + '</div>';
    if (membershipInfo.zones.length > 0) {
        membershipName += '<div class="membership_zones"><span class="admin_label">Zone:</span> ' + membershipInfo.zones.join(', ') + '</div>';
    }
    return membershipName;
};

DataManager.getMemberships = function() {
    var memberships = [];

    $("form#contract_filters input:checked").each(function(index) {
        memberships.push($(this).val());
    });
    return memberships;
};

DataManager.setNaics = function(value) {
    DataManager.set('naics', value);
};

DataManager.getNaics = function() {
    return DataManager.get('naics', null);
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

DataManager.setPoolMap = function(value) {
    DataManager.set('pool_map', value);
};

DataManager.getPoolMap = function() {
    return DataManager.get('pool_map', {});
};

DataManager.sendMembershipFilterChange = function() {
    EventManager.publish('membershipChanged');
};

DataManager.loadPools = function() {
    var url = "/api/pools/";
    var queryData = {count: 1000};
    var memberships = DataManager.getVendorMemberships();
    var vendorPools = {};

    for (var index = 0; index < memberships.length; index++) {
        vendorPools[memberships[index].pool.id] = true;
    }

    DataManager.getAPIRequest(url, queryData, function(data) {
        var pools = data['results'];
        var poolMap = {};
        var naicsMap = {};

        for (var index = 0; index < pools.length; index++) {
            var pool = pools[index];

            if (pool.id in vendorPools) {
                for (var naicsIndex = 0; naicsIndex < pool.naics.length; naicsIndex++) {
                    naics = pool.naics[naicsIndex].code;

                    if (!(naics in naicsMap)) {
                        naicsMap[naics] = [];
                    }
                    naicsMap[naics].push(pool.id);
                }
                poolMap[pool.id] = pool;
            }
        }

        DataManager.setPoolMap(poolMap);
        DataManager.setNaicsMap(naicsMap);
        EventManager.publish('poolsUpdated');
    });
};

DataManager.loadVendor = function(callback) {
    var url = "/api/vendors/" + DataManager.getDuns() + "/";

    DataManager.getAPIRequest(url, {}, function(vendor) {
        DataManager.setVendor(vendor);
        EventManager.publish('vendorLoaded', vendor);
    });
};

DataManager.loadContracts = function() {
    var url = "/api/contracts";
    var piids = DataManager.getMemberships();
    var naics = DataManager.getNaics();
    var ordering = DataManager.getSortOrdering();
    var queryData = {
        'vendor__duns': DataManager.getDuns(),
        'page': DataManager.getPage(),
        'count': DataManager.getPageCount()
    };

    if (ordering) {
        queryData['ordering'] = ordering;
    }

    if (naics) {
        queryData['psc_naics'] = naics;
    }

    if (piids.length > 0) {
        queryData['base_piid__in'] = piids.join(',');
    }

    $('.table_wrapper').addClass('loading');
    $('#ch_table').addClass('init');

    DataManager.getAPIRequest(url, queryData,
        function(response) {
            EventManager.publish('contractsLoaded', response);
            $('.table_wrapper').removeClass('loading');
            $('#ch_table').removeClass('init');
        },
        function(req, status, error) {
            if (queryData['page'] > 1 && req.status == 404) {
                DataManager.setPage(1);
                DataManager.update();
            }
            else {
                $('.table_wrapper').removeClass('loading');
                $('.table_wrapper').addClass('warning');
            }
        }
    );
};

DataManager.populateNaicsDropDown = function(data) {
    var naicsMap = DataManager.getNaicsMap();
    var naics = DataManager.getNaics();

    $('#naics-code').select2({
        minimumResultsForSearch: -1,
        width: '400px'
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
                $("#naics-code")
                    .append($("<option></option>")
                    .attr("value", result.code)
                    .text(result.code + ' - ' + result.description));
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

DataManager.populateMembershipFilters = function() {
    var $table = $('#vendor_contract_filter_table');
    var vendor = DataManager.getVendor();
    var membershipMap = DataManager.getMembershipMap();
    var vehicleMap = DataManager.getVehicleMap();
    var naicsMap = DataManager.getNaicsMap();
    var naics = DataManager.getNaics();
    var selectedMemberships = DataManager.getParameterByName('memberships');
    var piids = Object.keys(membershipMap);

    if (selectedMemberships) {
        selectedMemberships = selectedMemberships.split(',').filter(Boolean);
    }
    else {
        selectedMemberships = [];
    }

    $table.find("tr:gt(0)").remove();

    piids.sort(function(a, b) {
        var aVehicles = membershipMap[a].vehicles.join(' ');
        var bVehicles = membershipMap[b].vehicles.join(' ');

        if (aVehicles == bVehicles) {
            var aPools = membershipMap[a].pools.join(' ');
            var bPools = membershipMap[b].pools.join(' ');

            if (aPools == bPools) {
                var aZones = membershipMap[a].zones.join(' ');
                var bZones = membershipMap[b].zones.join(' ');

                if (aZones == bZones) {
                    return 0;
                }
                else {
                    return aZones > bZones ? 1 : -1;
                }
            }
            else {
                return aPools > bPools ? 1 : -1;
            }
        }
        return aVehicles > bVehicles ? 1 : -1;
    });

    for (var index = 0; index < piids.length; index++) {
        var piid = piids[index];
        var membership = membershipMap[piid];
        var membershipName = DataManager.getMembershipName(membership);
        var pools = membership.poolIds;
        var checked = '';

        if (naics) {
            pools = pools.filter(value => -1 !== naicsMap[naics].indexOf(value));
        }

        if (! naics || pools.length > 0) {
            var $membershipRow = $('<tr class="membership_filter"></tr>');

            if (selectedMemberships && $.inArray(piid, selectedMemberships)) {
                checked = "checked";
            }

            membershipName = '<div class="membership_info">' + membershipName + '</div>';
            if (membership.reference.capability_statement && membership.reference.capability_statement.length > 0) {
                var capabilityStatementLink = '<div class="capability_statement_link"><a href="' + membership.reference.capability_statement + '">Capability Statement (PDF)</a></div>';
                membershipName = membershipName + capabilityStatementLink;
            }

            $membershipRow.append('<td class="filter"><input type="checkbox" class="contract_pool_filter" id="' + piid + '" name="' + piid + '" value="' + piid + '" ' + checked + ' /></td>');
            $membershipRow.append('<td class="contract">' + membershipName + '</td>');
            $membershipRow.append('<td class="contact">' + membership.contacts.join('<br/>') + '</td>');
            $membershipRow.append('<td class="phone">' + membership.phones.join('<br/>') + '</td>');
            $membershipRow.append('<td class="email">' + membership.emails.join('<br/>') + '</td>');

            if (membership.vehicleIds.length == 1 && vehicleMap[membership.vehicleIds[0]].sb) {
                var exp_8a_date = '';

                $membershipRow.append(DataManager.setasideColumn(membership.setasides, 'sb', 'SB'));
                $membershipRow.append(DataManager.setasideColumn(membership.setasides, 'sdb', '27'));
                $membershipRow.append(DataManager.setasideColumn(membership.setasides, '8a', 'A6'));

                if (membership.reference.expiration_8a_date) {
                    exp_8a_date = Format.formatDate(Format.createDate(membership.reference.expiration_8a_date));
                }
                $membershipRow.append('<td class="setaside_info">' + exp_8a_date + '</td>');

                $membershipRow.append(DataManager.setasideColumn(membership.setasides, 'Hubz', 'XX'));
                $membershipRow.append(DataManager.setasideColumn(membership.setasides, 'wo', 'A2'));
                $membershipRow.append(DataManager.setasideColumn(membership.setasides, 'vo', 'A5'));
                $membershipRow.append(DataManager.setasideColumn(membership.setasides, 'sdvo', 'QF'));
                $membershipRow.append(DataManager.setasideColumn(membership.setasides, 'VIP', 'VIP'));
            }
            else {
                $membershipRow.append($('<td colspan="9" class="unrestricted"></td>'));
            }

            $table.append($membershipRow);
        }
    }

    if (DataManager.getMemberships().toString() != selectedMemberships.toString()) {
        EventManager.publish('membershipChanged');
    }
    else {
        EventManager.publish('membershipSelected');
    }
};

DataManager.setasideColumn = function(setasides, prefix, setaside) {
    var $col = $('<td class="' + prefix + '"></td>');

    for (var index = 0; index < setasides.length; index++) {
        if (setasides[index] == setaside) {
            $col.html('<img src="'+ static_image_path + 'green_dot.png" class="green_dot">');
            break;
        }
    }
    return $col;
};

DataManager.sortClassMap = function() {
    return {
        'h_date_signed': 'date_signed',
        'h_piid': 'piid',
        'h_agency': 'agency_name',
        'h_type': 'pricing_type__name',
        'h_poc': 'point_of_contact',
        'h_value': 'obligated_amount',
        'h_status': 'status__name',
    };
};

DataManager.sortContracts = function(e) {
    //if enter pressed or if click then sort
    if ((e.type == "keypress" && e.charCode == 13) || e.type == "click") {
        var $target = $(e.target);
        var class_map = DataManager.sortClassMap();
        var classes = $target.attr('class').split(' ');

        DataManager.setSortOrdering(class_map[classes[0]]);
        DataManager.setPage(1);

        if ($target.hasClass('arrow-down')) {
            $target.removeClass('arrow-down').addClass('arrow-up').attr("title", "Sorted ascending");
        } else if ($target.hasClass('arrow-sortable')) {
            DataManager.setSortOrdering("-" + DataManager.getSortOrdering());
            $target.removeClass('arrow-sortable').addClass('arrow-down').attr("title", "Sorted descending");
        } else {
            DataManager.setSortOrdering("-" + DataManager.getSortOrdering());
            $target.removeClass('arrow-up').addClass('arrow-down').attr("title", "Sorted descending");
        }

        //reset other ths that are sortable
        $target.siblings('.sortable').removeClass('arrow-down').removeClass('arrow-up').addClass('arrow-sortable').attr("title", "Select to sort");

        EventManager.publish('sortChanged');
    }
};
