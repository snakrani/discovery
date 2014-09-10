// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Strict_mode
'use strict';

var ResultsManager = {
    init: function() {
        Events.subscribe('naicsChanged', this.load.bind(ResultsManager));
        Events.subscribe('filtersChanged', this.load.bind(ResultsManager));
        Events.subscribe('loadedWithQS', this.load.bind(ResultsManager));
    },

    buildRequestQuery: function() {
        var setasides = InputHandler.getSetasides();
        var naicsCode = InputHandler.getNAICSCode() || URLManager.getParameterByName('naics');
        var queryData = {'group':'pool'};
        var pool = this.getPool();

        if (typeof naicsCode !== 'undefined') {
            queryData['naics'] = naicsCode;
        }

        if (setasides.length > 0) {
            queryData["setasides"] = setasides.join();
        }
        if (pool !== null) {
            queryData['pool'] = pool;
        }

        return queryData;
    },

    load: function() {
        var url = "/api/vendors/";
        var queryData = this.buildRequestQuery();

        $.getJSON(url, queryData, function(data) {
            var resultsObj = {}; 
            console.log(data);
            resultsObj.vehicle = data['results'][0]['vehicle'].toLowerCase();
            resultsObj.poolNumber = data['results'][0]['number'];
            resultsObj.samLoad = data.sam_load;
            resultsObj.total = data.num_results;
            resultsObj.results = data.results;
            resultsObj.naics = queryData['naics'];

            Events.publish('dataLoaded', resultsObj);
        });
    },

    getPool: function() {
        var poolInfo = URLManager.getPoolInfo();

        if (poolInfo !== null){
            if (poolInfo['vehicle'] == 'oasissb'){
                return poolInfo['pool_number'] + '_' + 'SB';
            }
            else {
                return poolInfo['pool_number']
            }
        }
        else {
            return null 
        }
    }

};
