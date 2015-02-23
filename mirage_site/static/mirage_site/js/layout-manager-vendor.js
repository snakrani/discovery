 // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Strict_mode
'use strict';

// for vendor pages
LayoutManager.vendorInit = function(original) {
    // binds events needed only in the vendor context on init and then
    // calls original init function
    Events.subscribe('contractDataLoaded', this.buildContractTable.bind(LayoutManager));

    original.bind(LayoutManager).call();
};

LayoutManager.originalInit = LayoutManager.init;

LayoutManager.init = function() {
    LayoutManager.vendorInit(LayoutManager.originalInit);
};

LayoutManager.render = function(results) {
    //update document title
    $(document).prop('title', results.name + " - " + URLManager.title);

    URLManager.updateVendorCSVURL(results);

    var currentDate = new Date();
    var mailto, t, indicatorsRow, formattedDate, dateObj;

    $('.vendor_title').html(results.name);
    if (results.sam_url) {
        $('#vendor_site_link').attr('href', results.sam_url);
    } else {
        $('.vendor_website').hide(); 
    }
    if (results.sam_exclusion == true) {
            $('.debarred_status').show();
    }
    $('.duns_number').html(results.duns ? results.duns : ' ');
    $('.cage_code').html(results.cage ? results.cage : ' ');
    $('.number_of_employees').html(results.number_of_employees ? this.numberWithCommas(results.number_of_employees) : 'N/A');
    $('.annual_revenue').html(results.annual_revenue ? '$' + this.numberWithCommas(results.annual_revenue) : 'N/A');

    //load SAM expiration date
    if (results['sam_expiration_date']) {
        dateObj = this.createDate(results['sam_expiration_date']);
        formattedDate = this.formatDate(dateObj);
    }
    else {
        formattedDate = 'unknown';
    }

    $(".vendor_sam_expiration_date").text(formattedDate);
    if (currentDate > dateObj) {
        $(".vendor_sam_expiration_notice").show();
    }

    //contact info
    $('.vendor_address1').html(results.sam_address ? results.sam_address : ' ');
    $('.vendor_address2').html(results.sam_citystate ? results.sam_citystate : ' ');
    $('.vendor_poc_name').html(results.pm_name ? results.pm_name : ' ');
    $('.vendor_poc_phone').html(results.pm_phone ? results.pm_phone : ' ');

    if (results.pm_email !== null) {
        mailto = $('<a href="mailto:' + results.pm_email + '">' + results.pm_email + '</a>');
        $('.vendor_poc_email').html(mailto);
    }

    //small business badge
    if (LayoutManager.showSbBadge(results['pools'])) {
        $('#sb_badge').show();
    }

    //socioeconomic indicators
    t = $('#socioeconomic_indicators');
    indicatorsRow = $('<tr></tr>');
    indicatorsRow.append(this.renderColumn(results, '8a', 'A6'));
    indicatorsRow.append(this.renderColumn(results, 'Hubz', 'XX'));
    indicatorsRow.append(this.renderColumn(results, 'sdvo', 'QF'));
    indicatorsRow.append(this.renderColumn(results, 'wo', 'A2'));
    indicatorsRow.append(this.renderColumn(results, 'vo', 'A5'));
    indicatorsRow.append(this.renderColumn(results, 'sdb', '27'));
    t.append(indicatorsRow);
    
    //update button value to have proper NAICS code
    $("#vendor_contract_history_title_container #naics_contracts_button").text("NAICS " + InputHandler.naicsCode);  
}; 

LayoutManager.renderColumn = function(v, prefix, setasideCode) {
    return $('<td class="' + prefix + '">' + this.vendorIndicator(v, prefix, setasideCode) + '</td>');
};

LayoutManager.setButtonAndCSV = function(listType){
    $("#vendor_contract_history_title_container .contracts_button_active").attr('class', 'contracts_button');
    $("#" + listType + "_contracts_button").attr('class', 'contracts_button_active');

    var a = $("a#csv_link");
    var csv_link = a.attr('href');

    if (csv_link.indexOf('naics-code') > -1) {
        //remove naics code if csv link has it, if not add it back in
        a.attr('href', csv_link.substring(0, csv_link.indexOf("?")));
    } else {
        a.attr('href', csv_link + "?naics-code=" + $("#vendor_contract_history_title_container").find("div").first().text().replace("NAICS", '').trim());
    }
};

LayoutManager.buildContractTable = function(data, listType, pageNumber) {
    var headers = $("div#ch_table table tr").first().clone();
    var table = $("<table></table>");
    var results = data['results'];
    var contract, tr, displayDate, pointOfContact, piid, agencyName, pricingType, obligatedAmount, status, naics;

    this.setButtonAndCSV(listType);

    //append headers from existing html
    table.append(headers);
    
    //show or hide 'no matching contracts' indicator
    if (results.length == 0) {
        $('#no_matching_contracts').show();
    } else {
        $('#no_matching_contracts').hide();
    }

    for (contract in results) {
        if (results.hasOwnProperty(contract)) {
            tr = $('<tr></tr>');
            displayDate = (results[contract]['date_signed'] ? this.formatDate(this.createDate(results[contract]['date_signed'])) : ' ');
            piid = (results[contract]['piid'] ? results[contract]['piid'] : ' ');
            agencyName = (results[contract]['agency_name'] ? results[contract]['agency_name'] : ' ');
            pricingType = (results[contract]['pricing_type'] ? results[contract]['pricing_type'] : ' ');
            obligatedAmount = (results[contract]['obligated_amount'] ? this.numberWithCommas(results[contract]['obligated_amount']) : ' ');
            status = (results[contract]['status'] ? results[contract]['status'] : ' ');
            naics = (results[contract]['NAICS'] ? results[contract]['NAICS'] : ' ')

            if (typeof results[contract]['point_of_contact'] === 'string') {
                pointOfContact = results[contract]['point_of_contact'].toLowerCase();
            }
            else {
                pointOfContact = (results[contract]['point_of_contact'] ? results[contract]['point_of_contract'] : ' ');
            }

            tr.append('<td class="date_signed">' + displayDate + '</td>');
            tr.append('<td class="piid" scope="row">' + piid + '</td>');
            tr.append('<td class="agency">' + this.toTitleCase(agencyName) + '</td>');
            tr.append('<td class="type">' + pricingType + '</td>');
            tr.append('<td class="value">' + obligatedAmount+ '</td>');
            tr.append('<td class="email_poc">' + pointOfContact + '</td>');
            tr.append('<td class="status">' + status + '</td>');
            tr.append('<td class="naics">' + naics + '</td>');
            //more goes here
        
            table.append(tr);
        }
    }

    $("div#ch_table table").remove();
    $("div#ch_table").append(table);


    //pagination
    if (data['num_results'] > 0) {

        if (pageNumber == undefined) {
            var pageNumber = 1;
        }
        var itemsPerPage = 100;
        var startnum = (pageNumber - 1) * itemsPerPage + 1;
        var endnum = Math.min((pageNumber * itemsPerPage), data['num_results']);
        $("#contracts_current").text(startnum + " - " + endnum);
        $("#contracts_total").text(LayoutManager.numberWithCommas(data['num_results']));

        $(function() {
            $("#pagination_container").pagination({
                items: data['num_results'],
                itemsOnPage: itemsPerPage,
                cssStyle: 'light-theme',
                currentPage: pageNumber,
                onPageClick: function(pageNumber, e) {
                    var contract_data = {}
                    if (listType == 'all') {
                        contract_data['naics'] == 'all';
                    } else {
                        contract_data['naics'] = naics;
                    }
                    contract_data['page'] = pageNumber;
                    contract_data['listType'] = listType;
                    Events.publish("contractsChanged", contract_data);
                }
            });
        });
        $('#pagination_container').show();
        $("#viewing_contracts").show();

    } else {
        $('#pagination_container').hide();
        $("#viewing_contracts").hide();
    }


};

LayoutManager.formatDate = function(dateObj) {
	//returns (mm/dd/yyyy) string representation of a date object
	return (dateObj.getMonth() + 1) + '/' + dateObj.getDate() + '/' + dateObj.getFullYear().toString().substring(2);
};

LayoutManager.vendorIndicator = function(v, prefix, setaside_code) {
    //returns X if vendor and socioeconomic indicator match
    if (v['setasides'].length > 0) {
        for (var i=0; i<v['setasides'].length; i++) {
            if (v['setasides'][i]['code'] == setaside_code) {
                return '<img alt="X" src="' + static_image_path  + 'green_dot.png" class="green_dot">';
            }
        }
    }

    return '';
};

LayoutManager.numberWithCommas = function(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
};

LayoutManager.showSbBadge = function(pools) {
    //return true if pool number is same in more than one pool
    for (var i=0; i<pools.length; i++) {
        for (var j=i+1; j<pools.length; j++) {
            if (pools[i].number == pools[j].number) {
                return true
            }
        }
    }
    return false
}
