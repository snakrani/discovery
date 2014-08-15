var get_code = function () {
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

var clear_content = function(){
    $("#custom_page_content").find("div.column").remove();
};

var build_query_string = function() {
    /* build query string from search form and push to history stack */
    var qs = "?";
    if (get_code() != 'Select a NAICS code') {
        qs += "naics-code=" + get_code() + "&";
    } else {
        qs += "naics-code=all&";
    }
    if (get_setasides().length > 0) {
        qs += "setasides=" + get_setasides();
    }
    return qs;
}

var refresh_data = function(event) {
    /* query api for search results based on current state of form elements 
    and display results */
    var code = get_code();
    if (code == 'all') {
        $("#naics-code").select2().select2("val", "all");
    }

    var setasides = get_setasides();
    var url = "/api/vendors/"
    var query_data = {'group': 'pool'}

    if (code != 'null' && code != null) {
        query_data["naics"] = code;
    }
    if (setasides.length > 0) {
        query_data["setasides"] = setasides.join();
    }
    
    $.getJSON(url, query_data, function(data){
        /* when data loads clear content and rebuild results */
        clear_content();
        show_content(data);
    });

    //add current search status query string to url in address bar and push to history
    qs = build_query_string();
    History.pushState(null, null, qs);

    $('#naics-code').select2({dropdownAutoWidth : true});

    return false;
}

//refresh data on page if search criteria changes 
$("#naics-code").change(refresh_data);
$("#setaside-filters").change(refresh_data);
