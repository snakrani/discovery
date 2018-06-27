
LayoutManager.initializers.listings = function() {
    EventManager.subscribe('vendorDataLoaded', this.renderTable.bind(LayoutManager));
};

LayoutManager.render = function(results) {
    if ($.isEmptyObject(results)) {
        $('#pool_vendors').find('tr').not(':first').remove();
        EventManager.publish('contentChanged', results);
    }
    else {
        this.renderTable(results, 1, RequestsManager.getPageCount());
    }

    $(document).prop('title', "Results - " + URLManager.title);

    $('#pool_vendors th span').tooltip();
};

LayoutManager.renderTable = function(results, pageNumber, itemsPerPage) {
    var $table = $('#pool_vendors');
    var qs = URLManager.getQueryString();
    var len = results['results'].length;

    $table.find('tr').not(':first').remove();

    //show or hide 'no matching vendors' indicator
    if (results['count'] == 0) {
        $('#no_matching_vendors').show();
    } else {
        $('#no_matching_vendors').hide();
    }

    for (var i = 0; i < len; i++) {
        $table.append(this.renderRow(results['results'][i], qs, i));
    }

    $('#pool_table').show();

    LayoutManager.renderPager(results, pageNumber, itemsPerPage);

    EventManager.publish('contentChanged', results);
};

LayoutManager.renderRow = function(vendor, qs, i) {
    var location_col, num_contracts_col;
    var $vendorRow = $('<tr class="table_row_data"></tr>');

    var locationStr = (vendor.sam_location_citystate ? this.cleanLocation(vendor.sam_location_citystate) : ' ');
    var name_col = $('<td class="vendor_name" scope="row"></td>');
    var name_a = $('<a href="/vendor/' + vendor.duns + '/' + qs + '" class="link_style">' + vendor.name + '</a>');
    var vehicle = this.getQSByName(qs, 'vehicle');

    name_col.append(name_a);
    $vendorRow.append(name_col);

    location_col = $('<td class="vendor_location">' + locationStr + '</td>');
    $vendorRow.append(location_col);

    num_contracts_col = $('<td class="naics_results">' + vendor.number_of_contracts + '</td>');
    $vendorRow.append(num_contracts_col);

    //add socio-economic columns
    if (vendor.setasides.length > 0) {
        $vendorRow.append(this.renderColumn(vendor, '8a', 'A6'));
        $vendorRow.append(this.renderColumn(vendor, 'Hubz', 'XX'));
        $vendorRow.append(this.renderColumn(vendor, 'sdvo', 'QF'));
        $vendorRow.append(this.renderColumn(vendor, 'wo', 'A2'));
        $vendorRow.append(this.renderColumn(vendor, 'vo', 'A5'));
        $vendorRow.append(this.renderColumn(vendor, 'sdb', '27'));
    }
    else {
        $vendorRow.append($('<td colspan="6" class="unrestricted"></td>'));
    }

    return $vendorRow;
};

LayoutManager.renderColumn = function(v, prefix, setasideCode) {
    var $col = $('<td class="' + prefix + '"></td>');
    if (this.findIndicatorMatch(v, prefix, setasideCode)) {
        $col.html('<img src="'+ static_image_path + 'green_dot.png" class="green_dot">');
    }
    return $col;
};

LayoutManager.renderPager = function(results, pageNumber, itemsPerPage) {
    var resultCount = results['results'].length;

    if (results['count'] > 0) {
        if (pageNumber == undefined) {
            var pageNumber = 1;
        }

        var startnum = (pageNumber - 1) * itemsPerPage + 1;
        var endnum = Math.min((pageNumber * itemsPerPage), results['count']);

        $("#vendors_current").text(startnum + " - " + endnum);
        $("#vendors_total").text(LayoutManager.numberWithCommas(results['count']));

        $(function() {
            $("#pagination_container").pagination({
                items: results['count'],
                itemsOnPage: itemsPerPage,
                cssStyle: 'light-theme',
                currentPage: pageNumber,
                onPageClick: function(pageNumber, e) {
                    var vendor_data = RequestsManager.currentSortParams();

                    vendor_data['page'] = pageNumber;

                    EventManager.publish("vendorsChanged", vendor_data);
                }
            });
        });
        if (resultCount < results['count']) {
            $('#pagination_container').show();
        } else {
            $('#pagination_container').hide();
        }
        $("#viewing_vendors").show();

    } else {
        $('#pagination_container').hide();
        $("#viewing_vendors").hide();
    }
};

LayoutManager.getQSByName = function(qs, name) {
        // http://stackoverflow.com/questions/901115/how-can-i-get-query-string-values-in-javascript
        name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
        var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
            results = regex.exec(qs);
        return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
};

LayoutManager.findIndicatorMatch = function(v, prefix, setasideCode) {
    var i, len = v['setasides'].length - 1;

    if (v['setasides'].length > 0) {
        for (var i=0; i <= len; i++) {
            if (v['setasides'][i]['code'] == setasideCode) {
                return true;
            }
        }
    }
    return false;
};

LayoutManager.cleanLocation = function(loc) {
    var location_obj = {};
    var new_location = loc;

    if (loc) {
        loc = loc.trim();
        var comma = loc.indexOf(',');
        location_obj.city = loc.slice(0, comma);
        var after = loc.substring(comma + 2);
        var space = after.lastIndexOf(' ');
        location_obj.state = after.slice(0, space).toUpperCase();

        if (location_obj.city.match(/^\s*$/) || location_obj.state.match(/^\s*$/)) {
            new_location = '';
        }
        else {
            new_location = this.toTitleCase(location_obj.city) + ', ' + location_obj.state;
        }
    }
    return new_location;
};
