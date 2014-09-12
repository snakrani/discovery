// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Strict_mode
'use strict';

// for pool page
LayoutManager.Pool = {
    renderTable: function(results) {
        var t = $('#pool_vendors');
        var i, len = results.results[0].vendors.length - 1;

        for (i = 0; i <= len; i++) {
            t.append(this.renderRow(results.results[0].vendors[i]));
        }

        $('#pool_table').show();
        Events.publish('contentChanged', results);
    },

    renderRow: function(v) {
        var location_col;
        var $vendorRow = $('<tr></tr>');

        var name_col = $('<td class="vendor_name"></td>');
        var name_a = $('<a href="/vendor/' + v.duns + '/" class="link_style">' + v.name + '</a>');
        name_col.append(name_a);
        $vendorRow.append(name_col);

        location_col = $('<td class="vendor_location">' + this.cleanLocation(v.sam_citystate) + '</td>');
        $vendorRow.append(location_col);

        //add socio-economic columns
        $vendorRow.append(this.renderColumn(v, 'vo', 'A5'));
        $vendorRow.append(this.renderColumn(v, 'sdb', '27'));
        $vendorRow.append(this.renderColumn(v, 'sdvo', 'QF'));
        $vendorRow.append(this.renderColumn(v, 'wo', 'A2'));

        return $vendorRow;
    },

    renderColumn: function(v, prefix, setasideCode) {
        var $col = $('<td class="' + prefix + '"></td>');
        if (this.findIndicatorMatch(v, prefix, setasideCode)) {
            $col.text('X');
        }

        return $col;
    },

    findIndicatorMatch: function(v, prefix, setasideCode) {
        var i, len = v['setasides'].length - 1;

        if (v['setasides'].length > 0) {
            for (var i=0; i <= len; i++) {
                if (v['setasides'][i]['code'] == setasideCode) {
                    return true;
                }
            }
        }

        return false;
    },

    cleanLocation: function(location) {
        var location_obj = {};
        var new_location = location;

        if (location) {
            location = location.trim();
            var comma = location.indexOf(',');
            location_obj.city = location.slice(0, comma);
            var after = location.substring(comma + 2);
            var space = after.lastIndexOf(' ');
            location_obj.state = after.slice(0, space).toUpperCase();
            new_location = this.toTitleCase(location_obj.city) + ', ' + location_obj.state
        }
        return new_location
    }, 

    toTitleCase: function(str) {
        // from http://stackoverflow.com/questions/5097875/help-parsing-string-city-state-zip-with-javascript
        return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
    }

};
