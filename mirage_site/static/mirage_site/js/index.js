var show_content = function(results) {
    var container = $("#custom_page_content");
    var data = results['results'];
    var total = results['num_results'];

    //add current search status query string to url in address bar and push to history
    qs = build_query_string();
    History.pushState(null, null, qs);

    //$('#naics-code').select2({placeholder:'Select a NAICS code', dropdownAutoWidth : true});
    $("#naics-code").select2({placeholder: 'Select a NAICS code1', width: '400px' });

    //load SAM update date
    var date_obj = new Date(results['sam_load']);
    $("#sam_load").text("SAM data updated: " + (date_obj.getMonth() + 1) + '/' + date_obj.getDate() + '/' + date_obj.getFullYear().toString().substring(2));

    //show search information
    $("#number_of_results span").text(total.toString() + " vendors in " + data.length.toString()  + " pool(s) match your search");
    $("#your_search").text($("#naics-code option:selected").text());
    $("#your_filters").text(
        $("#setaside-filters input:checkbox:checked").map(function() {
            return $(this).parent().text();
        }).get().join(', ')
    );
    $("#your_search_criteria").show();

    //load vendor and pool data
    for (var e in data) {
        var obj = data[e];
        
        var div = $(document.createElement('div'));
        div.addClass("column post-header");

        pool_link = $(document.createElement('a'));
        pool_link.attr('href', '/pool/' + obj['vehicle'].toLowerCase() + '/' + obj['number'] + '/');
        pool_link.attr('class', 'pool_link');
        pool_link.text("Pool " + obj['number']);
        
        pool_header = $(document.createElement('h2'));
        pool_header.addClass("pool_title");
        pool_header.append(pool_link);
        div.append(pool_header);
        
        div.append( $(document.createElement('p')).addClass("post-meta number_of_vendors_in_pool").text(obj['vendors'].length.toString() + ' vendors'));

        for (var v in obj['vendors']){
            div.append( $(document.createElement('p')).addClass("vendor_names").text(obj['vendors'][v]['name']) );
        }
        container.append(div);
    }

    //add current search status query string to links to pools
    qs = build_query_string();
    $(".pool_link").each(function() {
        var parser = document.createElement('a');
        parser.href = this.href;
        parser.search = qs;
        $(this).attr('href', parser);  
    });

    //remove old seach results breadcrumb
    $('#sr').remove();

    //create new breadcrumb for search results
    new_crumb = $(document.createElement('li'));
    new_crumb.attr('id', 'sr');
    crumb_anchor = $(document.createElement('a'));
    crumb_anchor.attr('href', '#');
    crumb_anchor.text('Search Results');
    new_crumb.append(crumb_anchor);
    $('#crumbs').append(new_crumb);
}

var refresh_data = function(event) {
    /* query api for search results based on current state of form elements 
    and display results */

    code = get_code_from_dropdown();
    var setasides = get_setasides();
    var url = "/api/vendors/";
    var query_data = {'group': 'pool'}

    if (code != 'null' && code != null) {
        query_data["naics"] = code;
    }
    if (setasides.length > 0) {
        query_data["setasides"] = setasides.join();
    }
    if (get_pool() != null) {
        query_data['pool'] = get_pool();
    }
    
    $.getJSON(url, query_data, function(data){
        /* when data loads clear content and rebuild results */
        if (data['results'].length == 1) {
            obj = data['results'][0];
            qs = build_query_string();
            window.location.href = '/pool/' + obj['vehicle'].toLowerCase() + '/' + obj['number'] + '/' + qs;
        } else {
            clear_content();
            show_content(data);
        }

    });

    return false;
}

$(document).ready(function() {
    //load results when page loads
    var code = get_code_from_dropdown();
    if (code == 'all') {
        $("#naics-code").select2().select2("val", "all");
    }
})
