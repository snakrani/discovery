
LayoutManager.initializers.vendor = function() {
    Events.subscribe('vendorPoolLoaded', this.renderVendor.bind(LayoutManager));
    Events.subscribe('contractDataLoaded', this.renderTable.bind(LayoutManager));
};

LayoutManager.render = function(results) {
    this.renderVendor(results, null);
};

LayoutManager.renderVendor = function(results, pool) {
    var membership = null;

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
    $('.duns_number').html(results.duns);
    $('.cage_code').html(results.cage);
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
    $('.vendor_address2').html(results.sam_location ? results.sam_location.city + ', ' + results.sam_location.state + ' ' + results.sam_location.zipcode : ' ');

    if (pool) {
        for (var i = 0; i < results.pools.length; i++) {
            if (results.pools[i].pool.id == pool.id) {
                membership = results.pools[i];
            }
        }

        if (membership.pms.length > 0) {
            $('.vendor_poc_name').html(membership.pms[0].name);
            $('.vendor_poc_phone').html(membership.pms[0].phone.length ? membership.pms[0].phone.join(',') : ' ');

            var mailto = [];
            for (var i = 0; i < membership.pms[0].email.length; i++) {
                email = membership.pms[0].email[i];
                mailto.push('<a href="mailto:' + email + '">' + email + '</a>');
            }
            $('.vendor_poc_email').html(mailto.join(','));
        }
    }
    else {
        membership = results;
    }

    //small business badge
    if (LayoutManager.showSbBadge(results['pools'])) {
        $('#sb_badge').show();
    }

    //socioeconomic indicators
    t = $('#socioeconomic_indicators');
    t.find("tr:gt(0)").remove();

    indicatorsRow = $('<tr></tr>');
    indicatorsRow.append(this.renderColumn(membership, '8a', 'A6'));
    indicatorsRow.append(this.renderColumn(membership, 'Hubz', 'XX'));
    indicatorsRow.append(this.renderColumn(membership, 'sdvo', 'QF'));
    indicatorsRow.append(this.renderColumn(membership, 'wo', 'A2'));
    indicatorsRow.append(this.renderColumn(membership, 'vo', 'A5'));
    indicatorsRow.append(this.renderColumn(membership, 'sdb', '27'));
    t.append(indicatorsRow);

    if (pool) {
        $("#naics_contracts_button").show();
        $("#naics_contracts_button").text("NAICS " + InputHandler.naicsCode);
        $("#all_contracts_button").show();
        $(".vendor_contract_history_text").html("Showing this vendor's complete contract history for: ");
    }
    else {
        $("#naics_contracts_button").hide();
        $("#all_contracts_button").hide();
        $(".vendor_contract_history_text").html("Showing this vendor's indexed contract history");

        this.renderButtonAndCSV('all');
    }
};

LayoutManager.showSbBadge = function(pools) {
    for (var i = 0; i < pools.length; i++) {
        if (pools[i].pool.id.indexOf("_SB") != -1) {
            return true;
        }
    }
    return false;
};

LayoutManager.renderColumn = function(v, prefix, setasideCode) {
    return $('<td class="' + prefix + '">' + this.vendorIndicator(v, prefix, setasideCode) + '</td>');
};

LayoutManager.renderTable = function(results, listType, pageNumber, itemsPerPage) {
    var $table = $('#vendor_contracts');
    var len = results['results'].length;

    this.renderButtonAndCSV(listType);

    $table.find('tr').not(':first').remove();

    //show or hide 'no matching contracts' indicator
    if (results['count'] == 0) {
        $('#no_matching_contracts').show();
    } else {
        $('#no_matching_contracts').hide();
    }

    for (var i = 0; i < len; i++) {
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

    if (listType == 'all') {
        a.attr('href', csv_link.substring(0, csv_link.indexOf("?")));
    } else {
        a.attr('href', csv_link + URLManager.getQueryString());
    }
};

LayoutManager.renderRow = function(contract, i) {
    var $contractRow = $('<tr class="table_row_data"></tr>');

    var displayDate = (contract['date_signed'] ? this.formatDate(this.createDate(contract['date_signed'])) : ' ');
    var piid = (contract['piid'] ? contract['piid'] : ' ');
    var agencyName = (contract['agency_name'] ? contract['agency_name'] : ' ');
    var pricingType = (contract['pricing_type'] ? contract['pricing_type'].name : ' ');
    var location = (contract['place_of_performance_location'] ? contract['place_of_performance_location'] : ' ');
    var obligatedAmount = (contract['obligated_amount'] ? this.numberWithCommas(contract['obligated_amount']) : ' ');
    var status = (contract['status'] ? contract['status'].name : ' ');
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
    if (results['count'] > 0) {
        if (pageNumber == undefined) {
            var pageNumber = 1;
        }

        var startnum = (pageNumber - 1) * itemsPerPage + 1;
        var endnum = Math.min((pageNumber * itemsPerPage), results['count']);

        $("#contracts_current").text(startnum + " - " + endnum);
        $("#contracts_total").text(LayoutManager.numberWithCommas(results['count']));

        $(function() {
            $("#pagination_container").pagination({
                items: results['count'],
                itemsOnPage: itemsPerPage,
                cssStyle: 'light-theme',
                currentPage: pageNumber,
                onPageClick: function(pageNumber, e) {
                    var contract_data = RequestsManager.currentSortParams();

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
        if (results['results'].length < results['count']) {
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

LayoutManager.vendorIndicator = function(membership, prefix, setaside_code) {
    //returns X if vendor and socioeconomic indicator match
    if (membership['setasides'].length > 0) {
        for (var i = 0; i < membership['setasides'].length; i++) {
            if (membership['setasides'][i]['code'] == setaside_code) {
                return '<img alt="X" src="' + static_image_path  + 'green_dot.png" class="green_dot">';
            }
        }
    }
    return '';
};
