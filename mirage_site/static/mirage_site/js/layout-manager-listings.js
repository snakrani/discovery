// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Strict_mode
'use strict';

// for pool page and single pool list
// anything with a url under /pool
LayoutManager.render = function(results) {
    // this is turning into something of a router
    // should be refactored [TS]

    // if multiple pools should be rendered
    if ($.isEmptyObject(results)) {
        //clear out content
        $('#pool_vendors').find('tr').not(':first').remove();
        Events.publish('contentChanged', results);       
    }
    else if (results.results.length > 1) {
        this.renderPools(results);
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
};

LayoutManager.renderPools = function(results) {
    var $container = $('#custom_page_content');
    //clear out content
    $container.find('.column').remove();

    for (var i in results.results) {
        if (results.results.hasOwnProperty(i)) {
            var obj = results.results[i];
            var $poolLink, $poolHeader; 
            var $div = $('<div class="column post-header"></div>');
            var qs = URLManager.getQueryString();

            $poolLink = $('<a class="pool_link" href="/pool/' + obj['vehicle'].toLowerCase() + '/' + obj['number'] + '/' + qs + '">Pool ' + obj['number'] + '</a>');
            $poolLink.text();
           
            $poolHeader = $('<h2 class="pool_title"></h2>');
            $poolHeader.append($poolLink);
            $div.append($poolHeader);
            
            $div.append('<p class="post-meta number_of_vendors_in_pool">' + obj['vendors'].length.toString() + ' vendors</p>');

            for (var v in obj['vendors']){
                if (obj['vendors'].hasOwnProperty(v)) {
                    $div.append('<p class="vendor_names">' + obj['vendors'][v]['name'] + '</p>');
                }
            }

            $container.append($div);
        }
    }
};

LayoutManager.renderTable = function(results) {
    var $t = $('#pool_vendors');
    var i, len = results.results[0].vendors.length - 1;

    $t.find('tr').not(':first').remove();

    for (i = 0; i <= len; i++) {
        $t.append(this.renderRow(results.results[0].vendors[i]));
    }

    $('#pool_table').show();
    Events.publish('contentChanged', results);
};

LayoutManager.renderRow = function(v) {
    var location_col;
    var qs = URLManager.getQueryString();
    var $vendorRow = $('<tr></tr>');
    var locationStr = (v.sam_citystate ? this.cleanLocation(v.sam_citystate) : ' ');
    var name_col = $('<td class="vendor_name"></td>');
    var name_a = $('<a href="/vendor/' + v.duns + '/' + qs + '" class="link_style">' + v.name + '</a>');
    name_col.append(name_a);
    $vendorRow.append(name_col);

    location_col = $('<td class="vendor_location">' + locationStr + '</td>');
    $vendorRow.append(location_col);

    //add socio-economic columns
    $vendorRow.append(this.renderColumn(v, '8a', 'A6'));
    $vendorRow.append(this.renderColumn(v, 'Hubz', 'XX'));
    $vendorRow.append(this.renderColumn(v, 'sdvo', 'QF'));
    $vendorRow.append(this.renderColumn(v, 'wo', 'A2'));
    $vendorRow.append(this.renderColumn(v, 'vo', 'A5'));
    $vendorRow.append(this.renderColumn(v, 'sdb', '27'));

    return $vendorRow;
};

LayoutManager.renderColumn = function(v, prefix, setasideCode) {
    var $col = $('<td class="' + prefix + '"></td>');
    if (this.findIndicatorMatch(v, prefix, setasideCode)) {
        $col.text('X');
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
