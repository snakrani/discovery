var get_code = function () {
    code = $('#naics-code').val();
    if (code == 'Select an option') {
        code = 'all';
    }
    return code
};

var get_setasides = function(){
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
    if (get_code() != 'Select an option') {
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
    /* query api for search results based on current state of form elements */


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
        clear_content();
        load_content(data);
    });

    History.pushState(null, null, build_query_string());
    return false;
}

$("#naics-code").change(refresh_data);
$("#setaside-filters").change(refresh_data);
