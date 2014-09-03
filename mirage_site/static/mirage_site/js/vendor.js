var get_duns = function() {
    //extract pool information from document url
    var parser = document.createElement('a');
    parser.href = document.URL;
    path_arr = parser.pathname.split('/');
    return path_arr[2]
}

var render_column = function(v, prefix, setaside_code) {
    //returns properly formatted column for vendor/socioeconomic indicator

    var vendor_indicator = function(v, prefix, setaside_code) {
        //returns X if vendor and socioeconomic indicator match
        if (v['setasides'].length > 0) {
            for (var i=0; i<v['setasides'].length; i++) {
                if (v['setasides'][i]['code'] == setaside_code) {
                    return 'X';
                }
            }
        } else {
            return '';
        }
    }

    col = $(document.createElement('td'));
    col.attr('class', prefix);
    col.text(vendor_indicator(v, prefix, setaside_code));
    return col
}

var show_content = function(results) {

	//vendor info
	$('.vendor_title').html(results.name);
	if (results.sam_exclusion == true) {
			$('.debarred_status').show();
	}
	$('.duns_number').html(results.duns);
	$('.cage_code').html(results.cage);
	$('.number_of_employees').html(results.number_of_employees ? results.number_of_employees : 'N/A');
	$('.annual_revenue').html(results.annual_revenue ? '$' + results.annual_revenue : 'N/A');

	//contact info
	$('.vendor_address1').html(results.sam_address);
	$('.vendor_address2').html(results.sam_citystate);

	//socioeconomic indicators
    t = $(document.getElementById('socioeconomic_indicators'));
    indicators_row = $(document.createElement('tr'));
	indicators_row.append(render_column(results, 'vo', 'A5'));
	indicators_row.append(render_column(results, 'sdb', '27'));
	indicators_row.append(render_column(results, 'sdvo', 'QF'));
	indicators_row.append(render_column(results, 'wo', 'A2'));
	indicators_row.append(render_column(results, '8a', 'A6'));
	indicators_row.append(render_column(results, 'Hubz', 'XX'));
	t.append(indicators_row);

	//breadcrumbs
	$('#vendor_breadcrumb').html(results.name);
}

var refresh_data = function(event) {
    /* get vendor info from api */

    var url = "/api/vendor/" + get_duns() + "/";
    
    $.getJSON(url, function(data){
        /* when data loads clear content and rebuild results */
        show_content(data);
    });

    return false;
}

$(document).ready(function() {
    refresh_data();
})