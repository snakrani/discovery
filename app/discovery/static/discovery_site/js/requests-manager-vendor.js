
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
    EventManager.subscribe('dataLoaded', this.refreshContracts.bind(RequestsManager));
    EventManager.subscribe('contractsSorted', this.refreshContracts.bind(RequestsManager));
};

RequestsManager.loadVendor = function(callback) {
    var duns = URLManager.getDUNS();
    var url = "/api/vendors/" + duns + "/";

    RequestsManager.getAPIRequest(url, {}, function(vendor){
        RequestsManager.vendor = vendor;
        callback(duns, vendor);
    });
};

RequestsManager.loadContracts = function(data, callback) {
    var duns = URLManager.getDUNS();
    var url = "/api/contracts";
    var queryData = $.extend(data, {'vendor__duns': duns, 'count': this.getPageCount()});
    var piids = RequestsManager.getPIIDs();

    if (InputHandler.getListType() == 'naics' && 'naics' in queryData) {
        queryData['psc_naics'] = queryData['naics'];

        if (queryData['psc_naics'] == 'all') {
            delete queryData['psc_naics'];
        }
    }
    delete queryData['naics'];

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
    RequestsManager.loadVendor(function(duns, vendor) {
        EventManager.publish('dataLoaded', {});
    });
};

RequestsManager.refreshContracts = function(data) {
    data['naics'] = InputHandler.getNAICSCode();

    if (!data['page']) {
        data['page'] = 1;
    }

    RequestsManager.loadContracts(data, function(queryData, response) {
        EventManager.publish('contractsLoaded', response, data['page'], queryData['count']);
    });
};

RequestsManager.getPIIDs = function() {
  var vendor = RequestsManager.vendor;
  var pools = InputHandler.getContractPools();
  var piids = [];

  if (vendor && pools.length > 0) {
      for (var pindex = 0; pindex < pools.length; pindex++) {
          var pool = RequestsManager.vehiclePools[pools[pindex]];

          for (var vindex = 0; vindex < vendor.pools.length; vindex++) {
              var vendor_pool = vendor.pools[vindex];

              if (pool.id == vendor_pool.pool.id) {
                  piids.push(vendor_pool.piid);
              }
          }
      }
  }
  return piids;
};
