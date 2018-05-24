
RequestsManager.vendor = null;
RequestsManager.pool = null;

RequestsManager.sortClassMap = function() {
    return {
        'h_date_signed': 'date_signed',
        'h_piid': 'piid',
        'h_agency': 'agency_name',
        'h_type': 'pricing_type__name',
        'h_poc': 'point_of_contact',
        'h_value': 'obligated_amount',
        'h_status': 'status__name',
    };
};

RequestsManager.initializers.vendor = function() {
    EventManager.subscribe('poolUpdated', this.refreshVendor.bind(RequestsManager));

    EventManager.subscribe('vendorInfoLoaded', this.refreshContracts.bind(RequestsManager));
    EventManager.subscribe('contractsChanged', this.refreshContracts.bind(RequestsManager));
};

RequestsManager.loadVendor = function(callback) {
    var duns = URLManager.getDUNS();
    var url = "/api/vendors/" + duns + "/";

    RequestsManager.getAPIRequest(url, {}, function(response){
        callback(duns, response);
    });
};

RequestsManager.loadContracts = function(data, callback) {
    var duns = URLManager.getDUNS();
    var url = "/api/contracts";
    var queryData = $.extend(data, {'vendor__duns': duns, 'count': this.getPageCount()});
    var piids = RequestsManager.getPIIDs();

    queryData['psc_naics'] = queryData['naics'];
    delete queryData['naics'];

    if (queryData['psc_naics'] == 'all') {
        delete queryData['psc_naics'];
    }

    if (piids.length > 0) {
        queryData['base_piid__in'] = piids.join(',');
    }

    $('.table_wrapper').addClass('loading');

    RequestsManager.getAPIRequest(url, queryData,
        function(response) {
            callback(queryData, response);
            $('.table_wrapper').removeClass('loading');
        },
        function(req, status, error) {
            $('.table_wrapper').removeClass('loading');
        }
    );
};

RequestsManager.load = function() {
    var listType = 'naics';

    if (URLManager.getParameterByName('showall')) {
        listType = 'all';
    }

    RequestsManager.loadVendor(function(duns, vendor) {
        RequestsManager.vendor = vendor;
        EventManager.publish('dataLoaded', vendor);
        EventManager.publish('vendorInfoLoaded', {'listType': listType});
    });
};

RequestsManager.refreshVendor = function(pool) {
    var listType = 'naics';

    if (URLManager.getParameterByName('showall')) {
        listType = 'all';
    }

    RequestsManager.pool = pool;
    RequestsManager.loadVendor(function(duns, vendor) {
        RequestsManager.vendor = vendor;
        EventManager.publish('vendorPoolLoaded', vendor, pool);
        EventManager.publish('vendorInfoLoaded', {'listType': listType});
    });
};

RequestsManager.refreshContracts = function(data) {
    data['listType'] = typeof data['listType'] !== 'undefined' ? data['listType'] : 'naics';

    if (data['naics']) {
        if (data['naics'] != 'all') {
          data['naics'] = URLManager.stripSubCategories(data['naics']);
        }
    }
    else {
        naics = URLManager.stripSubCategories(URLManager.getParameterByName('naics-code'));

        if (naics && naics != 'all'){
            data['naics'] = naics;
        }

        if (data['listType'] == 'all') {
            data['naics'] = '';
        }
    }

    if (!data['page']) {
        data['page'] = 1;
    }

    RequestsManager.loadContracts(data, function(queryData, response) {
        EventManager.publish('contractDataLoaded', response, data['listType'], data['page'], queryData['count']);
    });
};

RequestsManager.getPIIDs = function() {
  var vendor = RequestsManager.vendor;
  var pool = RequestsManager.pool;
  var piids = [];
  var vehicle = null;

  if (vendor && pool && InputHandler.getVendorPoolFilter()) {
    vehicle = pool.id.split("_")[0];

    for (var index = 0; index < vendor.pools.length; index++) {
      vendor_pool = vendor.pools[index];
      vendor_pool_vehicle = vendor_pool.pool.id.split("_")[0];

      if (vehicle == vendor_pool_vehicle) {
        piids.push(vendor_pool.piid);
      }
    }
  }

  return piids;
};
