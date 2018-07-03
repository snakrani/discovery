
LayoutManager.initializers.vendor = function() {
    EventManager.subscribe('contractsLoaded', this.renderTable.bind(LayoutManager));
};

LayoutManager.render = function(data) {
    this.renderVendor(data);
};

LayoutManager.renderVendor = function(data) {
    var vendor = RequestsManager.vendor;
    var pools = {};

    if (! $.isEmptyObject(RequestsManager.vehiclePools)) {
        for (var i = 0; i < vendor.pools.length; i++) {
            if (vendor.pools[i].pool.id in RequestsManager.vehiclePools) {
                pools[vendor.pools[i].pool.id] = {
                    "vendor": vendor.pools[i],
                    "pool": RequestsManager.vehiclePools[vendor.pools[i].pool.id]
                };
            }
        }
    }

    $(document).prop('title', vendor.name + " - " + URLManager.title);

    URLManager.updateVendorCSVURL(vendor);

    var currentDate = new Date();
    var mailto, t, indicatorsRow, formattedDate, dateObj;

    $('.vendor_title').html(vendor.name);
    if (vendor.sam_url) {
        $('#vendor_site_link').attr('href', vendor.sam_url);
    } else {
        $('.vendor_website').hide();
    }
    if (vendor.sam_exclusion == true) {
        $('.debarred_status').show();
    }
    $('.duns_number').html(vendor.duns);
    $('.cage_code').html(vendor.cage);
    $('.number_of_employees').html(vendor.number_of_employees ? this.numberWithCommas(vendor.number_of_employees) : 'N/A');
    $('.annual_revenue').html(vendor.annual_revenue ? '$' + this.numberWithCommas(vendor.annual_revenue) : 'N/A');

    //load SAM expiration date
    if (vendor['sam_expiration_date']) {
        dateObj = this.createDate(vendor['sam_expiration_date']);
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
    $('.vendor_address1').html(vendor.sam_location ? vendor.sam_location.address : ' ');
    $('.vendor_address2').html(vendor.sam_location ? vendor.sam_location.city + ', ' + vendor.sam_location.state + ' ' + vendor.sam_location.zipcode : ' ');

    if (! $.isEmptyObject(pools)) {
        this.renderContacts(vendor, pools);
    }

    //small business badge
    if (LayoutManager.showSbBadge(vendor['pools'])) {
        $('#sb_badge').show();
    }

    //socioeconomic indicators
    t = $('#socioeconomic_indicators');
    t.find("tr:gt(0)").remove();

    indicatorsRow = $('<tr></tr>');
    indicatorsRow.append(this.renderColumn(vendor, '8a', 'A6'));
    indicatorsRow.append(this.renderColumn(vendor, 'Hubz', 'XX'));
    indicatorsRow.append(this.renderColumn(vendor, 'sdvo', 'QF'));
    indicatorsRow.append(this.renderColumn(vendor, 'wo', 'A2'));
    indicatorsRow.append(this.renderColumn(vendor, 'vo', 'A5'));
    indicatorsRow.append(this.renderColumn(vendor, 'sdb', '27'));
    t.append(indicatorsRow);

    if (InputHandler.getNAICSCode()) {
        $("#naics_contracts_button").show();
        $("#naics_contracts_button").text("NAICS " + URLManager.stripSubCategories(InputHandler.getNAICSCode()));
        $("#all_contracts_button").show();
        $(".vendor_contract_history_text").html("Showing vendor's indexed 5 year contract history for PSCs related to: ");
    }
    else {
        $("#naics_contracts_button").hide();
        $("#all_contracts_button").hide();
        $(".vendor_contract_history_text").html("Showing vendor's indexed 5 year contract history");

        this.renderButtonAndCSV('all');
    }

    EventManager.publish('vendorRendered', {});
};

LayoutManager.renderContacts = function(vendor, pools) {
    var $table = $('#contact_details');
    var poolIds = URLManager.getParameterByName('pool');

    if (poolIds) {
        poolIds = poolIds.split(',').filter(Boolean);
    }

    $table.find("tr:gt(0)").remove();

    for (var poolId in pools) {
        var data = pools[poolId];
        var checked = "";

        if (poolIds && poolIds.includes(data.pool.id)) {
            checked = "checked";
        }

        var $contractRow = $('<tr class="contact_filter"></tr>');

        $contractRow.append('<td class="filter"><input type="checkbox" class="contract_pool_filter" name="' + data.pool.id + '" value="' + data.pool.id + '" ' + checked + ' /></td>');
        $contractRow.append('<td class="pool">' + data.pool.vehicle.split('_').join(' ') + ': ' + data.pool.name + '</td>');
        $contractRow.append('<td class="contact">' + data.vendor.cms[0].name + '</td>');
        $contractRow.append('<td class="phones">' + data.vendor.cms[0].phone.join('<br/>') + '</td>');
        $contractRow.append('<td class="emails">' + data.vendor.cms[0].email.join('<br/>') + '</td>');

        $table.append($contractRow);
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

LayoutManager.renderTable = function(results, pageNumber, itemsPerPage) {
    var listType = InputHandler.getListType();
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

    EventManager.publish('contentChanged', results);
};

LayoutManager.renderButtonAndCSV = function(data) {
    var listType = InputHandler.getListType();

    $("#vendor_contract_history_title_container .contracts_button_active").attr('class', 'contracts_button');
    $("#" + listType + "_contracts_button").attr('class', 'contracts_button_active');

    var a = $("a#csv_link");
    var csv_link = a.attr('href');

    csv_link = csv_link.substring(0, csv_link.indexOf("?"));

    if (listType == 'all') {
        a.attr('href', csv_link);
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
    var pointOfContact = (contract['point_of_contact'] ? contract['point_of_contact'].name : ' ');
    var location = (contract['place_of_performance_location'] ? contract['place_of_performance_location'] : ' ');
    var obligatedAmount = (contract['obligated_amount'] ? this.numberWithCommas(contract['obligated_amount']) : ' ');
    var status = (contract['status'] ? contract['status'].name : ' ');
    var psc = (contract['PSC'] ? contract['PSC'] : ' ');
    var naics = (contract['NAICS'] ? contract['NAICS'] : ' ');

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
    $contractRow.append('<td class="poc">' + pointOfContact + '</td>');
    $contractRow.append('<td class="value">' + obligatedAmount+ '</td>');
    $contractRow.append('<td class="status">' + status + '</td>');
    $contractRow.append('<td class="codes"><i>NAICS</i><br/><b>' + naics + '</b><br/><i>PSC</i><br/><b>' + psc + '</b></td>');

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

                    EventManager.publish("contractsChanged", contract_data);
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

LayoutManager.updateResultsInfo = function(results) {
    var totalResults, totalPools, resultsStr;
    if (results['count'] == 0) {
        totalResults = 0;
        totalPools = 0;
    }
    else {
        totalResults = results['count'].toString();
        totalPools = results['results'].length;
    }
    resultsStr = totalResults + " contracts match your search";

    URLManager.updateResultCSVURL(results);

    $("#number_of_results span").text(resultsStr);
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
