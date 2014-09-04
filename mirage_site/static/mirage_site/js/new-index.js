var InputHandler = {
    $codeField: $('#naics-code'),

    init: function() {
        // initialize special field lib
        this.$codeField.select2({placeholder:'Select a NAICS code', dropdownAutoWidth : true});

        // event bindings
        this.$codeField.change(this.sendCodeChange);
        $('#setaside-filters').change(this.sendFilterChange);
    },
    
    sendCodeChange: function(e) {
        Events.publish('naicsChanged', e.val);
    },

    sendFilterChange: function(e) {
        console.log(e);
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
    },

    buildRequestQS: function(naicsCode) {
        var setasides = InputHandler.getSetasides();
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

    load: function(naicsCode) {
        var url = "/api/vendors/";
        var queryData = this.buildRequestQS(naicsCode);        

        $.getJSON(url, queryData, function(data) {
            console.log(data);
        });
    },

    getPool: function() {
        return null;
    },

};

$(document).ready(function() {
    // http://thejacklawson.com/Mediator.js/
    window.Events = new Mediator() || {};

    InputHandler.init();
    ResultsManager.init();
});
