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
    }
};

var ResultsManager = {
    init: function() {
        Events.subscribe('naicsChanged', this.load);
    },

    load: function(naicsCode) {
        console.log(naicsCode);
    }
};

$(document).ready(function() {
    // http://thejacklawson.com/Mediator.js/
    window.Events = new Mediator() || {};

    InputHandler.init();
    ResultsManager.init();
});
