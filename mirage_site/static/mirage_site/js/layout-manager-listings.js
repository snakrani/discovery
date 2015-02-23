// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Strict_mode
'use strict';

// for pool page and single pool list
// anything with a url under /pool
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
            this.renderTable(results);
        }
        else {
            // if this is a vendor list page and we need to reload to get the template
            Events.publish('goToPoolPage', results);
        }
    }
    //update document title
    $(document).prop('title', "Results - " + URLManager.title);

};

LayoutManager.renderTable = function(results) {
    var $t = $('#pool_vendors');
    var qs = URLManager.getQueryString();
    var i, len = results['total'] - 1;
    $t.find('tr').not(':first').remove();

    for (i = 0; i <= len; i++) {
        $t.append(this.renderRow(results.results[i], qs, i));
    }

    $('#pool_table').show();
    Events.publish('contentChanged', results);
};

LayoutManager.getQSByName = function(qs, name) {
        // http://stackoverflow.com/questions/901115/how-can-i-get-query-string-values-in-javascript
        name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
        var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
            results = regex.exec(qs);
        return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
};

LayoutManager.renderRow = function(v, qs, i) {
    var location_col, num_contracts_col;
    var $vendorRow = $('<tr></tr>');
    var locationStr = (v.sam_citystate ? this.cleanLocation(v.sam_citystate) : ' ');
    var name_col = $('<td class="vendor_name" scope="row"></td>');
    var name_a = $('<a href="/vendor/' + v.duns + '/' + qs + '" class="link_style">' + v.name + '</a>');
    name_col.append(name_a);
    $vendorRow.append(name_col);

    location_col = $('<td class="vendor_location">' + locationStr + '</td>');
    $vendorRow.append(location_col);

    num_contracts_col = $('<td class="naics_results">' + v.contracts_in_naics + '</td>');
    $vendorRow.append(num_contracts_col);

    var vehicle = this.getQSByName(qs, 'vehicle')
    //add socio-economic columns
    if (vehicle == 'oasis') {
        if (i==0) {
            //if first row of content, create cell for "SB Only"
            var unrestricted_setasides = $('<td colspan="6" rowspan="100" class="unrestricted">Not Applicable </br>(OASIS SB Only)</td>');
            $vendorRow.append(unrestricted_setasides)
        }
    } else {
        //render socioeconomic indicators
        $vendorRow.append(this.renderColumn(v, '8a', 'A6'));
        $vendorRow.append(this.renderColumn(v, 'Hubz', 'XX'));
        $vendorRow.append(this.renderColumn(v, 'sdvo', 'QF'));
        $vendorRow.append(this.renderColumn(v, 'wo', 'A2'));
        $vendorRow.append(this.renderColumn(v, 'vo', 'A5'));
        $vendorRow.append(this.renderColumn(v, 'sdb', '27'));
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
        new_location = this.toTitleCase(location_obj.city) + ', ' + location_obj.state
    }
    return new_location
};
