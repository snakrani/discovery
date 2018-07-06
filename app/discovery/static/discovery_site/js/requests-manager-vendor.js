
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
    EventManager.subscribe('vendorRendered', this.refreshContracts.bind(RequestsManager));
};

RequestsManager.loadVendor = function(callback) {
    var duns = URLManager.getDUNS();
    var url = "/api/vendors/" + duns + "/";

    RequestsManager.getAPIRequest(url, {}, function(vendor) {
        RequestsManager.vendor = vendor;
        callback(duns, vendor);
    });
};

RequestsManager.loadContracts = function(callback) {
    var url = "/api/contracts";
    var piids = RequestsManager.getPIIDs();
    var naics = InputHandler.getNAICSCode();
    var ordering = InputHandler.getSortOrdering();
    var queryData = {
        'vendor__duns': URLManager.getDUNS(),
        'page': InputHandler.getPage(),
        'count': InputHandler.getPageCount()
    };

    if (ordering) {
        queryData['ordering'] = ordering;
    }

    if (InputHandler.getListType() == 'naics' && naics) {
        queryData['psc_naics'] = naics;
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
            if (queryData['page'] > 1 && req.status == 404) {
                InputHandler.page = 1;
                URLManager.update();
            }
            else {
                $('.table_wrapper').removeClass('loading');
            }
        }
    );
};

RequestsManager.load = function() {
    RequestsManager.loadVendor(function(duns, vendor) {
        EventManager.publish('dataLoaded', vendor);
    });
};

RequestsManager.refreshContracts = function() {
    RequestsManager.loadContracts(function(queryData, response) {
        EventManager.publish('contractsLoaded', response);
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
