
LayoutManager.initializers.listings = function() {
    LayoutManager.initSearch();

    // Internal event subscriptions
    EventManager.subscribe('dataInitialized', LayoutManager.renderSort);
    EventManager.subscribe('vendorDataLoaded', LayoutManager.renderVendors);
    EventManager.subscribe('pageChanged', DataManager.update);
};

LayoutManager.preprocessors.index = function() {
    LayoutManager.hideZone();
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
};

LayoutManager.renderVendors = function(data) {
    $(document).prop('title', "Results - " + DataManager.title);

    LayoutManager.renderPoolInfo();
    LayoutManager.renderResultsInfo(data);
    LayoutManager.renderVendorList(data);

    DataManager.completeStatus();
};

LayoutManager.renderPoolInfo = function() {
    var vehiclePools = DataManager.getVehiclePools();
    var pool = DataManager.getPool();
    var poolNames = [];
    var pools;

    if (pool) {
        pools = [pool];
    }
    else {
        pools = Object.keys(vehiclePools).sort();
    }

    if (pools.length > 0) {
        for (var index = 0; index < pools.length; index++) {
            var poolData = vehiclePools[pools[index]];

            if (pools.length > 1) {
                var url = DataManager.getURL({'vehicle': poolData.vehicle, 'pool': poolData.id});
                poolNames.push('<div class="pool"><div class="spacer"/><a id="link_' + poolData.id + '" class="pool_filter_link" href="' + url + '"><span class="vehicle">' + poolData.vehicle.split('_').join(' ') + " pool " + poolData.number + ':</span><span class="title">' + poolData.name + '</span></a></div>');
            }
            else {
                poolNames.push('<div class="pool"><div class="spacer"/><span class="vehicle">' + poolData.vehicle.split('_').join(' ') + " " + poolData.number + ':</span><span class="title">' + poolData.name + '</span></div>');
            }
        }
        $(".results_pool_names").html(poolNames.join(''));
    }
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
        'vehicle': null,
        'pool': null,
        'zone': null,
        'setasides': null,
        'ordering': null,
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

    // Vendor location
    var locationStr = (vendor.sam_location_citystate ? Format.cleanLocation(vendor.sam_location_citystate) : ' ');
    $vendorRow.append($('<td class="vendor_location">' + locationStr + '</td>'));

    // Contract count
    $vendorRow.append($('<td class="naics_results">' + vendor.number_of_contracts + '</td>'));

    // Vehicle memberships
    var vendorPools = DataManager.vendorPools(vendor);
    var renderedPools = [];

    for (var index = 0; index < vendorPools.length; index++) {
        var vehicleId = vendorPools[index];
        renderedPools.push('<a href="/results/' + qs + '&vehicle=' + vehicleId + '" class="link_style">' + DataManager.getVehicleMap()[vehicleId].title + '</a>');
    }
    $vendorRow.append($('<td class="vendor_pools">' + renderedPools.join(', ') + '</td>'));

    // Setasides
    if (vendor.setasides.length > 0) {
        $vendorRow.append(LayoutManager.renderSetaside(vendor, '8a', 'A6'));
        $vendorRow.append(LayoutManager.renderSetaside(vendor, 'Hubz', 'XX'));
        $vendorRow.append(LayoutManager.renderSetaside(vendor, 'sdvo', 'QF'));
        $vendorRow.append(LayoutManager.renderSetaside(vendor, 'wo', 'A2'));
        $vendorRow.append(LayoutManager.renderSetaside(vendor, 'vo', 'A5'));
        $vendorRow.append(LayoutManager.renderSetaside(vendor, 'sdb', '27'));
    }
    else {
        $vendorRow.append($('<td colspan="6" class="unrestricted"></td>'));
    }
    return $vendorRow;
};

LayoutManager.renderSetaside = function(vendor, prefix, setaside) {
    var $col = $('<td class="' + prefix + '"></td>');

    for (var index = 0; index < vendor.setasides.length; index++) {
        if (vendor.setasides[index]['code'] == setaside) {
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

