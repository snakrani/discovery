var get_code_from_dropdown = function () {
    /* returns naics-code from selected option in dropdown or 'all'
    if option is not selected */
    code = $('#naics-code').val();
    if (code == 'Select a NAICS code') {
        code = 'all';
    }
    return code
};

var get_setasides = function(){
    /* returns array of setaside ids that are checked */
    var setasides = [];
    $("form#setaside-filters input:checked").each( function(index) {
        setasides.push($(this).val());
    });

    return setasides;
}

var get_pool = function() {

    if (typeof(get_pool_info) != "undefined"){
        pool_data = get_pool_info();
        if (pool_data['vehicle'] == 'oasissb'){
            return pool_data['pool_number'] + '_' + 'SB';
        } else {
            return pool_data['pool_number']
        }
    } else {
        return null 
    }
}

var clear_content = function(){
    $("#custom_page_content").find("div.column").remove();
};

var build_query_string = function() {
    /* build query string from search form and push to history stack */
    var qs = "?";
    qs += "naics-code=" + get_code_from_dropdown() + "&";
    if (get_setasides().length > 0) {
        qs += "setasides=" + get_setasides() + "&";
    }
    
    return qs;
}

var to_title_case = function(str) {
    return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
}

var lower = function(str) {
    if (str) {
        return str.toLowerCase();
    } else {
        return str
    }
}

function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

//refresh data on page if search criteria changes 
$("#naics-code").change(refresh_data);
$("#setaside-filters").change(refresh_data);
