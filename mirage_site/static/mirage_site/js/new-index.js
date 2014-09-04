var InputHandler = {
    $codeField: $('#naics-code'),

    init: function() {
        // initialize special field lib
        this.$codeField.select2({placeholder:'Select a NAICS code', dropdownAutoWidth : true});

        // event bindings
        this.$codeField.change(this.sendCodeChange.bind(InputHandler));
        $('#setaside-filters').change(this.sendFilterChange);
    },
    
    sendCodeChange: function(e) {
        this.naicsCode = e.val;
        Events.publish('naicsChanged');
    },

    sendFilterChange: function(e) {
        Events.publish('filtersChanged');
    },

    getNAICSCode: function() {
        return this.naicsCode;
    },

    getSetasides: function() {
        /* returns array of setaside ids that are checked */
        var setasides = [];
        $("form#setaside-filters input:checked").each( function(index) {
            setasides.push($(this).val());
        });

        return setasides;
    }
};

var ResultsManager = {
    init: function() {
        Events.subscribe('naicsChanged', this.load.bind(ResultsManager));
        Events.subscribe('filtersChanged', this.load.bind(ResultsManager));
    },

    buildRequestQuery: function() {
        var setasides = InputHandler.getSetasides();
        var naicsCode = InputHandler.getNAICSCode();
        var queryData = {
            'group': 'pool',
            'naics': naicsCode
        };
        var pool = this.getPool();

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
            console.log(data);
            ResultsManager.vehicle = data['results'][0]['vehicle'].toLowerCase();
            ResultsManager.poolNumber = data['results'][0]['number'];
            Events.publish('dataLoaded');
        });
    },

    getPool: function() {
        return null;
    },

    getVehicle: function() {
        return this.vehicle;
    },

    getPoolNumber: function() {
        return this.poolNumber;
    }

};

var URLManager = {
    init: function() {
        Events.subscribe('contentChanged', this.update.bind(URLManager));
    },

    getQueryString: function() {
        var queryObject = ResultsManager.buildRequestQuery();
        var qs = '?';
        var k;

        for (k in queryObject) {
            qs += k + '=' + queryObject[k] + '&';
        }

        return qs;
    },

    update: function() {
        var qs = this.getQueryString();
        var vehicle = ResultsManager.getVehicle();
        var poolNumber = ResultsManager.getPoolNumber();

        window.location.href = '/pool/' + vehicle + '/' + poolNumber + '/' + qs;
    }
};

var LayoutManager = {
    init: function() {
        Events.subscribe('dataLoaded', this.render.bind(LayoutManager));
    },

    render: function() {
        Events.publish('contentChanged');
    }
};

$(document).ready(function() {
    // http://thejacklawson.com/Mediator.js/
    window.Events = new Mediator() || {};

    InputHandler.init();
    ResultsManager.init();
    URLManager.init();
    LayoutManager.init();
});
