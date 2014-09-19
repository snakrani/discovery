// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Strict_mode
'use strict';

var RequestsManager = {
    init: function() {
        Events.subscribe('naicsChanged', this.load.bind(RequestsManager));
        Events.subscribe('filtersChanged', this.load.bind(RequestsManager));
        Events.subscribe('loadedWithQS', this.load.bind(RequestsManager));
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
