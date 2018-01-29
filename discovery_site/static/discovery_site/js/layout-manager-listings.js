
LayoutManager.initializers.listings = function() {
    Events.subscribe('vendorDataLoaded', this.renderTable.bind(LayoutManager));
};

LayoutManager.sortClassMap = function() {
    return {
        'h_vendor_name': 'name',
        'h_vendor_location': 'sam_citystate',
        'h_naics_results': 'num_contracts',
    };
};

LayoutManager.render = function(results) {
    // this is turning into something of a router
    // should be refactored [TS]

    if (this.getQSByName(document.location, 'vehicle') == "oasis") {
        //disable filters for 'oasis unrestricted' results
        this.disableFilters();
    } else {
        this.enableFilters();
    }

    if ($.isEmptyObject(results)) {
        //clear out content
        $('#pool_vendors').find('tr').not(':first').remove();
        Events.publish('contentChanged', results);
    }
    else {
        // if this is a vendor list page and the page has already been reloaded
        if (URLManager.getParameterByName('naics-code') === InputHandler.getNAICSCode()) {
            Events.publish('vendorDataLoaded', results, 1, RequestsManager.vendorsPageCount);
        }
        else {
            // if this is a vendor list page and we need to reload to get the template
            Events.publish('goToPoolPage', results);
        }
    }
    //update document title
    $(document).prop('title', "Results - " + URLManager.title);
};

LayoutManager.renderTable = function(results, pageNumber, itemsPerPage) {
    var $table = $('#pool_vendors');
    var qs = URLManager.getQueryString();
    var len = results['count'] - 1;

    $table.find('tr').not(':first').remove();

    //show or hide 'no matching vendors' indicator
    if (results['total'] == 0) {
        $('#no_matching_vendors').show();
    } else {
        $('#no_matching_vendors').hide();
    }

    for (var i = 0; i <= len; i++) {
        $table.append(this.renderRow(results['results'][i], qs, i));
    }

    $('#pool_table').show();

    LayoutManager.renderPager(results, pageNumber, itemsPerPage);

    Events.publish('contentChanged', results);
};

LayoutManager.renderRow = function(vendor, qs, i) {
    var location_col, num_contracts_col;
    var $vendorRow = $('<tr></tr>');
    var locationStr = (vendor.sam_citystate ? this.cleanLocation(vendor.sam_citystate) : ' ');
    var name_col = $('<td class="vendor_name" scope="row"></td>');
    var name_a = $('<a href="/vendor/' + vendor.duns + '/' + qs + '" class="link_style">' + vendor.name + '</a>');
    var vehicle = this.getQSByName(qs, 'vehicle');

    name_col.append(name_a);
    $vendorRow.append(name_col);

    location_col = $('<td class="vendor_location">' + locationStr + '</td>');
    $vendorRow.append(location_col);

    num_contracts_col = $('<td class="naics_results">' + vendor.num_contracts + '</td>');
    $vendorRow.append(num_contracts_col);

    //add socio-economic columns
    if (vehicle == 'oasis') {
        if (i==0) {
            //if first row of content, create cell for "SB Only"
            var unrestricted_setasides = $('<td colspan="6" rowspan="100" class="unrestricted">Not Applicable </br>(OASIS SB Only)</td>');
            $vendorRow.append(unrestricted_setasides);
        }
    } else {
        //render socioeconomic indicators
        $vendorRow.append(this.renderColumn(vendor, '8a', 'A6'));
        $vendorRow.append(this.renderColumn(vendor, 'Hubz', 'XX'));
        $vendorRow.append(this.renderColumn(vendor, 'sdvo', 'QF'));
        $vendorRow.append(this.renderColumn(vendor, 'wo', 'A2'));
        $vendorRow.append(this.renderColumn(vendor, 'vo', 'A5'));
        $vendorRow.append(this.renderColumn(vendor, 'sdb', '27'));
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
    if (results['total'] > 0) {
        if (pageNumber == undefined) {
            var pageNumber = 1;
        }

        var startnum = (pageNumber - 1) * itemsPerPage + 1;
        var endnum = Math.min((pageNumber * itemsPerPage), results['total']);

        $("#vendors_current").text(startnum + " - " + endnum);
        $("#vendors_total").text(LayoutManager.numberWithCommas(results['total']));

        $(function() {
            $("#pagination_container").pagination({
                items: results['total'],
                itemsOnPage: itemsPerPage,
                cssStyle: 'light-theme',
                currentPage: pageNumber,
                onPageClick: function(pageNumber, e) {
                    var vendor_data = LayoutManager.currentSortParams();

                    vendor_data['page'] = pageNumber;

                    Events.publish("vendorsChanged", vendor_data);
                }
            });
        });
        if (results['count'] < results['total']) {
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
        new_location = this.toTitleCase(location_obj.city) + ', ' + location_obj.state;
    }
    return new_location;
};
