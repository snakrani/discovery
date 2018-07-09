
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
    EventManager.subscribe('vendorRendered', RequestsManager.loadContracts);
};

RequestsManager.load = function(callback) {
    var duns = DataManager.getDUNS();
    var url = "/api/vendors/" + duns + "/";

    RequestsManager.getAPIRequest(url, {}, function(vendor) {
        DataManager.vendor = vendor;
        EventManager.publish('dataLoaded', vendor);
    });
};

RequestsManager.loadContracts = function() {
    var url = "/api/contracts";
    var piids = RequestsManager.getPIIDs();
    var naics = DataManager.getNaicsCode();
    var ordering = DataManager.getSortOrdering();
    var queryData = {
        'vendor__duns': DataManager.getDUNS(),
        'page': DataManager.getPage(),
        'count': DataManager.getPageCount()
    };

    if (ordering) {
        queryData['ordering'] = ordering;
    }

    if (DataManager.getListType() == 'naics' && naics) {
        queryData['psc_naics'] = naics;
    }

    if (piids.length > 0) {
        queryData['base_piid__in'] = piids.join(',');
    }

    $('.table_wrapper').addClass('loading');

    RequestsManager.getAPIRequest(url, queryData,
        function(response) {
            EventManager.publish('contractsLoaded', response);
            $('.table_wrapper').removeClass('loading');
        },
        function(req, status, error) {
            if (queryData['page'] > 1 && req.status == 404) {
                DataManager.page = 1;
                DataManager.update();
            }
            else {
                $('.table_wrapper').removeClass('loading');
            }
        }
    );
};

RequestsManager.getPIIDs = function() {
  var vendor = DataManager.getVendor();
  var vehiclePools = DataManager.getVehiclePools();
  var pools = DataManager.getContractPools();
  var piids = [];

  if (vendor && pools.length > 0) {
      for (var pindex = 0; pindex < pools.length; pindex++) {
          var pool = vehiclePools[pools[pindex]];

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
