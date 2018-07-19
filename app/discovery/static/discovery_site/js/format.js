
var Format = {

    createDate: function(date) {
        // in IE + Safari, if we pass the date the api sends right
        // into a date object, it outputs NaN
        // http://biostall.com/javascript-new-date-returning-nan-in-ie-or-invalid-date-in-safari
        var dateArray = date.split('-'),
            i,
            len = dateArray.length - 1;
        for (i = 0; i <= len; i++) {
            dateArray[i] = parseInt(dateArray[i], 10);
        }

        return new Date(dateArray[0], dateArray[1], dateArray[2]);
    },

    formatDate: function(dateObj) {
        //returns (mm/dd/yyyy) string representation of a date object
        return dateObj.getMonth() + '/' + dateObj.getDate() + '/' + dateObj.getFullYear().toString().substring(2);
    },

    convertDate: function(oldDate) {
        if (!oldDate) return 'Unknown';
        var dateArray = oldDate.split('-');
        return dateArray[1] + '/' + dateArray[2]+ '/' + dateArray[0];
    },

    numberWithCommas: function(x) {
        return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    },

    toTitleCase: function(str) {
        // from http://stackoverflow.com/questions/5097875/help-parsing-string-city-state-zip-with-javascript
        return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();}).replace('U.s.', 'U.S.');
    },

    cleanLocation: function(loc) {
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
                new_location = Format.toTitleCase(location_obj.city) + ', ' + location_obj.state;
            }
        }
        return new_location;
    }
};
