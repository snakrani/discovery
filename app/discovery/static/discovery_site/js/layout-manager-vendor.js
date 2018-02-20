
LayoutManager.initializers.vendor = function() {
    Events.subscribe('contractDataLoaded', this.renderTable.bind(LayoutManager));
};

LayoutManager.sortClassMap = function() {
    return {
        'h_date_signed': 'date_signed',
        'h_piid': 'piid',
        'h_agency': 'agency_name',
        'h_type': 'pricing_type',
        'h_location': 'place_of_performance,location',
        'h_value': 'obligated_amount',
        'h_status': 'status',
    };
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
    $('.vendor_address1').html(results.sam_location ? results.sam_location.address : ' ');
    $('.vendor_address2').html(results.sam_location ? results.sam_location.citystate : ' ');

    if (results.pms.length > 0) {
      $('.vendor_poc_name').html(results.pms[0].name);
      $('.vendor_poc_phone').html(results.pms[0].phones.length ? results.pms[0].phones.join(',') : ' ');

      var mailto = [];
      for (var i = 0; i < results.pms[0].emails.length; i++) {
        email = results.pms[0].emails[i];
        mailto.push('<a href="mailto:' + email + '">' + email + '</a>');
      }
      $('.vendor_poc_email').html(mailto.join(','));
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

LayoutManager.showSbBadge = function(pools) {
    //return true if pool number is same in more than one pool
    for (var i=0; i<pools.length; i++) {
        for (var j=i+1; j<pools.length; j++) {
            if (pools[i].number == pools[j].number) {
                return true;
            }
        }
    }
    return false;
};

LayoutManager.renderColumn = function(v, prefix, setasideCode) {
    return $('<td class="' + prefix + '">' + this.vendorIndicator(v, prefix, setasideCode) + '</td>');
};

LayoutManager.renderTable = function(results, listType, pageNumber, itemsPerPage) {
    var $table = $('#vendor_contracts');
    var len = results['count'] - 1;

    this.renderButtonAndCSV(listType);

    $table.find('tr').not(':first').remove();

    //show or hide 'no matching contracts' indicator
    if (results['total'] == 0) {
        $('#no_matching_contracts').show();
    } else {
        $('#no_matching_contracts').hide();
    }

    for (var i = 0; i <= len; i++) {
        $table.append(this.renderRow(results['results'][i], i));
    }

    $("#ch_table").show();

    LayoutManager.renderPager(listType, results, pageNumber, itemsPerPage);
};

LayoutManager.renderButtonAndCSV = function(listType){
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

LayoutManager.renderRow = function(contract, i) {
    var $contractRow = $('<tr class="table_row_data"></tr>');

    var displayDate = (contract['date_signed'] ? this.formatDate(this.createDate(contract['date_signed'])) : ' ');
    var piid = (contract['piid'] ? contract['piid'] : ' ');
    var agencyName = (contract['agency_name'] ? contract['agency_name'] : ' ');
    var pricingType = (contract['pricing_type'] ? contract['pricing_type'] : ' ');
    var location = (contract['place_of_performance'] ? contract['place_of_performance']['location'] : ' ');
    var obligatedAmount = (contract['obligated_amount'] ? this.numberWithCommas(contract['obligated_amount']) : ' ');
    var status = (contract['status'] ? contract['status'] : ' ');
    var naics = (contract['NAICS'] ? contract['NAICS'] : ' ');
    var pointOfContact;

    if (typeof contract['point_of_contact'] === 'string') {
        pointOfContact = contract['point_of_contact'].toLowerCase();
    }
    else {
        pointOfContact = (contract['point_of_contact'] ? contract['point_of_contract'] : ' ');
    }

    $contractRow.append('<td class="date_signed">' + displayDate + '</td>');
    $contractRow.append('<td class="piid" scope="row">' + piid + '</td>');
    $contractRow.append('<td class="agency">' + this.toTitleCase(agencyName) + '</td>');
    $contractRow.append('<td class="type">' + pricingType + '</td>');
    $contractRow.append('<td class="location">' + location + '</td>');
    $contractRow.append('<td class="value">' + obligatedAmount+ '</td>');
    $contractRow.append('<td class="status">' + status + '</td>');
    $contractRow.append('<td class="naics">' + naics + '</td>');

    return $contractRow;
};

LayoutManager.renderPager = function(listType, results, pageNumber, itemsPerPage) {
    if (results['total'] > 0) {
        if (pageNumber == undefined) {
            var pageNumber = 1;
        }

        var startnum = (pageNumber - 1) * itemsPerPage + 1;
        var endnum = Math.min((pageNumber * itemsPerPage), results['total']);

        $("#contracts_current").text(startnum + " - " + endnum);
        $("#contracts_total").text(LayoutManager.numberWithCommas(results['total']));

        $(function() {
            $("#pagination_container").pagination({
                items: results['total'],
                itemsOnPage: itemsPerPage,
                cssStyle: 'light-theme',
                currentPage: pageNumber,
                onPageClick: function(pageNumber, e) {
                    var contract_data = LayoutManager.currentSortParams();

                    contract_data['duns'] = results['duns'];

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
        if (results['count'] < results['total']) {
            $('#pagination_container').show();
        } else {
            $('#pagination_container').hide();
        }
        $("#viewing_contracts").show();

    } else {
        $('#pagination_container').hide();
        $("#viewing_contracts").hide();
    }
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
