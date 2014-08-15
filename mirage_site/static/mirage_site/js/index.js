var load_content = function(results) {
    var container = $("#custom_page_content");
    var data = results['results'];
    var total = results['num_results'];

    //load SAM update date
    var date_obj = new Date(results['sam_load']);
    $("#sam_load").text("SAM data updated: " + (date_obj.getMonth() + 1) + '/' + date_obj.getDate() + '/' + date_obj.getFullYear().toString().substring(2));

    //load title data
    $("#number_of_results span").text(total.toString() + " vendors in " + data.length.toString()  + " pool(s) match your search");

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
