
LayoutManager.initializers.vendor = function() {

    // Internal event subscriptions
    EventManager.subscribe('dataInitialized', LayoutManager.renderVendor);
    EventManager.subscribe('dataInitialized', LayoutManager.renderContractSort);
    EventManager.subscribe('contractsLoaded', LayoutManager.renderContracts);

    EventManager.subscribe('pageChanged', DataManager.update);
};

LayoutManager.renderVendor = function() {
    var vendor = DataManager.getVendor();

    $(document).prop('title', vendor.name + " - " + DataManager.title);

    LayoutManager.renderBasicVendorInfo(vendor);
    LayoutManager.renderSamExpiration(vendor);
    LayoutManager.renderWebsite(vendor);
    LayoutManager.renderAddress(vendor);
    LayoutManager.renderBadges(vendor.pools);
    LayoutManager.renderResultInfo(vendor);
    DataManager.completeStatus();
};

LayoutManager.renderBasicVendorInfo = function(vendor) {
    $('.vendor_title').html(vendor.name);

    if (vendor.sam_exclusion == true) {
        $('.debarred_status').show();
    }
    $('.duns_number').html(vendor.duns);
    $('.cage_code').html(vendor.cage);
    $('.number_of_employees').html(vendor.number_of_employees ? Format.numberWithCommas(vendor.number_of_employees) : 'N/A');
    $('.annual_revenue').html(vendor.annual_revenue ? '$' + Format.numberWithCommas(vendor.annual_revenue) : 'N/A');
};

LayoutManager.renderSamExpiration = function(vendor) {
    var currentDate = new Date();
    var formattedDate, dateObj;

    if (vendor.sam_expiration_date) {
        dateObj = Format.createDate(vendor.sam_expiration_date);
        formattedDate = Format.formatDate(dateObj);
    }
    else {
        formattedDate = 'unknown';
    }

    $(".vendor_sam_expiration_date").text(formattedDate);

    if (currentDate > dateObj) {
        $(".vendor_sam_expiration_notice").show();
    }
};

LayoutManager.renderWebsite = function(vendor) {
    if (vendor.sam_url) {
        $('#vendor_site_link').attr('href', vendor.sam_url);
    } else {
        $('.vendor_website').hide();
    }
};

LayoutManager.renderAddress = function(vendor) {
    $('.vendor_address1').html(vendor.sam_location ? vendor.sam_location.address : ' ');
    $('.vendor_address2').html(vendor.sam_location ? vendor.sam_location.city + ', ' + vendor.sam_location.state + ' ' + vendor.sam_location.zipcode : ' ');
};

LayoutManager.renderBadges = function(memberships) {
    var vehicleMap = DataManager.getVehicleMap();
    var poolMap = DataManager.getPoolMap();
    var smallBusiness = false;

    for (var index = 0; index < memberships.length; index++) {
        var pool = poolMap[memberships[index].pool.id];

        if (vehicleMap[pool.vehicle].sb) {
            smallBusiness = true;
        }
    }
    if (smallBusiness) {
        $('#sb_badge').show();
    }
};

LayoutManager.renderResultInfo = function(vendor) {
    var duns = DataManager.getDuns();
    var vehicleMap = DataManager.getVehicleMap();
    var poolMap = DataManager.getPoolMap();
    var naics = DataManager.getNaics();
    var memberships = DataManager.getMemberships();

    var resultMessage = "Showing vendor's indexed 5 year contract history";
    var filterMessages = [];
    var vehicles = [];

    for (var index = 0; index < vendor.pools.length; index++) {
        var vendorMembership = vendor.pools[index];

        if (memberships.length > 0 && memberships.includes(vendorMembership.piid)) {
            vehicles.push(vehicleMap[poolMap[vendorMembership.pool.id].vehicle].title);
        }
    }
    if (vehicles.length > 0) {
        filterMessages.push(vehicles.join(', '));
    }

    if (naics) {
        filterMessages.push('NAICS ' + naics);
    }

    if (filterMessages.length > 0) {
        resultMessage += ' for ' + filterMessages.join(' and ');
    }
    $(".vendor_contract_history_text").html(resultMessage);

    // CSV results link
    $("#csv_link").attr("href", "/vendor/" + duns + "/csv/" + DataManager.getQueryString());
};

LayoutManager.renderContractSort = function() {
    var ordering = DataManager.getSortOrdering();

    if (ordering) {
        var asc = (ordering[0] == '-' ? false : true);
        var field = DataManager.getOrderingField(ordering.replace(/^-/, ''));
        var $target = $('th.' + field);

        $target.siblings('.sortable').removeClass('arrow-down').removeClass('arrow-up').addClass('arrow-sortable').attr("title", "Select to sort");

        if (asc) {
            $target.removeClass('arrow-sortable').removeClass('arrow-down').addClass('arrow-up').attr("title", "Sorted ascending");
        } else {
            $target.removeClass('arrow-sortable').removeClass('arrow-up').addClass('arrow-down').attr("title", "Sorted descending");
        }
    }
    DataManager.completeStatus();
};

LayoutManager.renderContracts = function(data) {
    var $table = $('#vendor_contracts');

    $table.find('tr').not(':first').remove();

    if (data['count'] == 0) {
        $('#no_matching_contracts').show();
    }
    else {
        $('#no_matching_contracts').hide();

        for (var index = 0; index < data['results'].length; index++) {
            $table.append(LayoutManager.renderContract(data['results'][index]));
        }
    }

    $("#ch_table").show();

    LayoutManager.renderPager(data);
    DataManager.completeStatus();
};

LayoutManager.renderContract = function(contract) {
    var $contractRow = $('<tr class="table_row_data"></tr>');

    var displayDate = (contract['date_signed'] ? Format.formatDate(Format.createDate(contract['date_signed'])) : ' ');
    var piid = (contract['piid'] ? contract['piid'] : ' ');
    var agencyName = (contract['agency_name'] ? contract['agency_name'] : ' ');
    var pricingType = (contract['pricing_type'] ? contract['pricing_type'].name : ' ');
    var pointOfContact = (contract['point_of_contact'] ? contract['point_of_contact'].name : ' ');
    var location = (contract['place_of_performance_location'] ? contract['place_of_performance_location'] : ' ');
    var obligatedAmount = (contract['obligated_amount'] ? Format.numberWithCommas(contract['obligated_amount']) : ' ');
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
    $contractRow.append('<td class="agency">' + Format.toTitleCase(agencyName) + '</td>');
    $contractRow.append('<td class="type">' + pricingType + '</td>');
    $contractRow.append('<td class="poc">' + pointOfContact + '</td>');
    $contractRow.append('<td class="value">' + obligatedAmount+ '</td>');
    $contractRow.append('<td class="status">' + status + '</td>');
    $contractRow.append('<td class="codes"><i>NAICS</i><br/><b>' + naics + '</b><br/><i>PSC</i><br/><b>' + psc + '</b></td>');

    return $contractRow;
};

LayoutManager.renderPager = function(data) {
    var page = DataManager.getPage();
    var pageCount = DataManager.getPageCount();

    if (data['count'] > 0) {
        var startnum = (page - 1) * pageCount + 1;
        var endnum = Math.min((page * pageCount), data['count']);

        $("#contracts_current").text(startnum + " - " + endnum);
        $("#contracts_total").text(Format.numberWithCommas(data['count']));

        $(function() {
            $("#pagination_container").pagination({
                items: data['count'],
                itemsOnPage: pageCount,
                cssStyle: 'light-theme',
                currentPage: page,
                selectOnClick: false,
                onPageClick: function(pageNumber, e) {
                    DataManager.setPage(pageNumber);
                    EventManager.publish("pageChanged");
                }
            });
        });
        if (data['results'].length < data['count']) {
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
