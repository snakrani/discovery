
LayoutManager.initializers.listings = function() {
    LayoutManager.initSearch();

    // Internal event subscriptions
    EventManager.subscribe('dataInitialized', LayoutManager.renderPoolInfo);
    EventManager.subscribe('dataInitialized', LayoutManager.renderSort);
    EventManager.subscribe('vendorDataLoaded', LayoutManager.renderVendors);
    EventManager.subscribe('pageChanged', DataManager.update);
};

LayoutManager.preprocessors.index = function() {
    LayoutManager.disableSearch();
    LayoutManager.updateSearch();
    LayoutManager.toggleZone();
};

LayoutManager.renderPoolInfo = function() {
    var vehicleMap = DataManager.getVehicleMap();
    var vehiclePools = DataManager.getVehiclePools();
    var pools = DataManager.getSortedPools(DataManager.getPools(), Object.keys(vehiclePools));
    var poolNames = [];

    for (var index = 0; index < pools.length; index++) {
        var poolData = vehiclePools[pools[index]];
        var vehicleInfo = vehicleMap[poolData.vehicle];
        var poolName;

        if (vehicleInfo.display_number) {
            poolName = '<span class="vehicle">' + poolData.vehicle.split('_').join(' ') + " " + poolData.number + ':</span><span class="title">' + poolData.name + '</span>';
        }
        else {
            poolName = '<span class="vehicle">' + poolData.vehicle.split('_').join(' ') + ':</span><span class="title">' + poolData.name + '</span>';
        }

        if (pools.length > 1) {
            var url = DataManager.getURL({'vehicle': poolData.vehicle, 'pools': poolData.id});
            poolNames.push('<div class="pool"><div class="spacer"/><a id="link_' + poolData.id + '" class="pool_filter_link" href="' + url + '">' + poolName + '</a></div>');
        }
        else {
            poolNames.push('<div class="pool"><div class="spacer"/>' + poolName + '</div>');
        }
    }
    $(".results_pool_names").html(poolNames.join(''));

    DataManager.completeStatus();
};

LayoutManager.renderSort = function() {
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
    DataManager.completeStatus();
};

LayoutManager.renderVendors = function(data) {
    $(document).prop('title', "Results - " + DataManager.title);

    LayoutManager.renderResultsInfo(data);
    LayoutManager.renderVendorList(data);

    LayoutManager.enableSearch();
    DataManager.completeStatus();
};

LayoutManager.renderResultsInfo = function(data) {
    // CSV results link
    $("#csv_link").attr("href", "/results/csv/" + DataManager.getQueryString());

    // Result count
    $("#number_of_results span").text(data['count'] + " vendors match your search");
};

LayoutManager.renderVendorList = function(data) {
    var $table = $('#pool_vendors');
    var qs = DataManager.getQueryString({
        'page': null
    });

    $('#pool_vendors th span').tooltip();
    $table.find('tr').not(':first').remove();

    if (data['count'] == 0) {
        $('#no_matching_vendors').show();
    }
    else {
        $('#no_matching_vendors').hide();

        for (var index = 0; index < data['results'].length; index++) {
            $table.append(LayoutManager.renderVendor(data['results'][index], qs));
        }
    }
    LayoutManager.renderPager(data);
};

LayoutManager.renderVendor = function(vendor, qs) {
    var $vendorRow = $('<tr class="table_row_data"></tr>');

    // Vendor name
    var nameCol = $('<td class="vendor_name" scope="row"></td>');
    nameCol.append($('<a href="/vendor/' + vendor.duns + '/' + qs + '" class="link_style">' + vendor.name + '</a>'));
    $vendorRow.append(nameCol);

    // Contract count
    $vendorRow.append($('<td class="naics_results">' + vendor.number_of_contracts + '</td>'));

    // Vehicle memberships
    var vehicleMap = DataManager.getVehicleMap();
    var vendorPools = DataManager.vendorPools(vendor);
    var renderedPools = [];

    for (var index = 0; index < vendorPools.length; index++) {
        var vehicleId = vendorPools[index];
        renderedPools.push(vehicleMap[vehicleId].title);
    }
    $vendorRow.append($('<td class="vendor_pools">' + renderedPools.join(', ') + '</td>'));

    // Setasides
    var setasides = DataManager.vendorSetasides(vendor);

    if (setasides.length > 0) {
        $vendorRow.append(LayoutManager.renderSetaside(setasides, 'sb', 'SB'));
        $vendorRow.append(LayoutManager.renderSetaside(setasides, 'sdb', '27'));
        $vendorRow.append(LayoutManager.renderSetaside(setasides, '8a', 'A6'));
        $vendorRow.append(LayoutManager.renderSetaside(setasides, 'Hubz', 'XX'));
        $vendorRow.append(LayoutManager.renderSetaside(setasides, 'wo', 'A2'));
        $vendorRow.append(LayoutManager.renderSetaside(setasides, 'vo', 'A5'));
        $vendorRow.append(LayoutManager.renderSetaside(setasides, 'sdvo', 'QF'));
        $vendorRow.append(LayoutManager.renderSetaside(setasides, 'vip', 'VIP'));
    }
    else {
        $vendorRow.append($('<td colspan="8" class="unrestricted"></td>'));
    }
    return $vendorRow;
};

LayoutManager.renderSetaside = function(setasides, prefix, setaside) {
    var $col = $('<td class="' + prefix + '"></td>');

    for (var index = 0; index < setasides.length; index++) {
        if (setasides[index] == setaside) {
            $col.html('<img src="'+ static_image_path + 'green_dot.png" class="green_dot">');
            break;
        }
    }
    return $col;
};

LayoutManager.renderPager = function(data) {
    var page = DataManager.getPage();
    var count = DataManager.getPageCount();

    if (data['count'] > 0) {
        var startnum = (page - 1) * count + 1;
        var endnum = Math.min((page * count), data['count']);

        $("#vendors_current").text(startnum + " - " + endnum);
        $("#vendors_total").text(Format.numberWithCommas(data['count']));

        $(function() {
            $("#pagination_container").pagination({
                items: data['count'],
                itemsOnPage: count,
                cssStyle: 'light-theme',
                currentPage: page,
                onPageClick: function(pageNumber, e) {
                    DataManager.setPage(pageNumber);
                    EventManager.publish('pageChanged');
                }
            });
        });
        if (data['results'].length < data['count']) {
            $('#pagination_container').show();
        } else {
            $('#pagination_container').hide();
        }
        $("#viewing_vendors").show();

    } else {
        $('#pagination_container').hide();
        $('#viewing_vendors').hide();
    }
};

