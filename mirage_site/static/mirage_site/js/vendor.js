var get_duns = function() {
    //extract pool information from document url
    var parser = document.createElement('a');
    parser.href = document.URL;
    path_arr = parser.pathname.split('/');
    return path_arr[2]
}

var happy_date = function(date_obj) {
	//returns (mm/dd/yyyy) string representation of a date object
	return (date_obj.getMonth() + 1) + '/' + date_obj.getDate() + '/' + date_obj.getFullYear().toString().substring(2);
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

	//load SAM expiration date
    var current_date = new Date();
    var date_obj = new Date(results['sam_expiration_date']);
    $(".vendor_sam_expiration_date").text(happy_date(date_obj));
    if (current_date > date_obj) {
        $(".vendor_sam_expiration_notice").show();
    }

	//contact info
	$('.vendor_address1').html(results.sam_address);
	$('.vendor_address2').html(results.sam_citystate);
	$('.vendor_poc_name').html(results.cm_name);
	$('.vendor_poc_phone').html(results.cm_phone);
	mailto = $(document.createElement('a'));
	mailto.attr('href', 'mailto:' + results.cm_email);
	mailto.text(results.cm_email);
	$('.vendor_poc_email').html(mailto);

	//socioeconomic indicators
    t = $(document.getElementById('socioeconomic_indicators'));
    indicators_row = $(document.createElement('tr'));
	indicators_row.append(render_column(results, '8a', 'A6'));
	indicators_row.append(render_column(results, 'Hubz', 'XX'));
	indicators_row.append(render_column(results, 'sdvo', 'QF'));
	indicators_row.append(render_column(results, 'wo', 'A2'));
	indicators_row.append(render_column(results, 'vo', 'A5'));
	indicators_row.append(render_column(results, 'sdb', '27'));
	t.append(indicators_row);

	//breadcrumbs
	$('#vendor_breadcrumb').html(results.name);
    get_contracts();
}

var build_table = function(data){
    var table = $("div#ch_table table").clone();
    var results = data['results'];
    for (item in results) {
        var tr = $(document.createElement('tr'));
        var display_date = happy_date(new Date(results[item]['date_signed']));
        var td = tr.append($(document.createElement('td')).addClass('date_signed').text(display_date));
        var td = tr.append($(document.createElement('td')).addClass('piid').text(results[item]['piid']));
        var td = tr.append($(document.createElement('td')).addClass('agency').text(to_title_case(results[item]['agency_name'])));
        var td = tr.append($(document.createElement('td')).addClass('type').text(results[item]['pricing_type']));
        var td = tr.append($(document.createElement('td')).addClass('value').text(results[item]['obligated_amount']));
        var td = tr.append($(document.createElement('td')).addClass('email_poc').text(lower(results[item]['point_of_contact'])));
        var td = tr.append($(document.createElement('td')).addClass('status').text(results[item]['status']));
        //more goes here
    
        table.append(tr);
    };

    $("div#ch_table table").remove();
    $("div#ch_table").append(table);
};

var get_contracts = function(){
    var url = "/api/contracts/";
    var params = {
        'duns': get_duns(),
    };

    var naics = getParameterByName('naics-code');
    if (naics){ 
        params['naics'] = naics; 
        $("span.vendor_contract_history_naics").text(" NAICS " + naics + ":");
    } else {
       $("span.vendor_contract_history_naics").text(" All Contracts:"); 
    }

    $.getJSON(url, params, function(data){
       build_table(data); 
    });
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
	if (!getParameterByName("naics-code")) {
		//load data if naics-code isn't defined. if it is defined, it's loaded elsewhere
		refresh_data();
	}
})
