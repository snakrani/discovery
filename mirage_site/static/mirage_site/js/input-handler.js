// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Strict_mode
'use strict';

var InputHandler = {
    init: function() {
        this.populateDropDown();

        // event bindings
        $('#naics-code').change(this.sendCodeChange.bind(InputHandler));
        $('#setaside-filters').change(this.sendFilterChange);

        Events.subscribe('loadedWithQS', this.updateFields.bind(InputHandler));
    },

    updateFields: function(obj) {
        if (obj['naics-code'] !== null) {
            $('#naics-code').select2('val', obj['naics-code']);
            this.naicsCode = obj['naics-code'];
        }

        if (obj.setasides) {
            // break out setasides and loop
            $('input[value=' + obj.setasides + ']').attr('checked', 'checked');
        }
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
    },

    populateDropDown: function() {
        // can't seem to use cached jqobj, something goes wrong with select2
        $('#naics-code')
             .append($("<option></option>")
             .attr("value", "all")
             .text("All NAICS codes")); 
        $.getJSON(
            "/api/naics/",
            { format: "json" },
            function( data ) {
                $.each(data.results, function(key, result) {   
                    $("#naics-code")
                         .append($("<option></option>")
                         .attr("value", result.short_code)
                         .text(result.short_code + " - " + result.description)); 
                });
                if (URLManager.getParameterByName("naics-code")) {
                    $("#naics-code").select2().select2("val", URLManager.getParameterByName("naics-code"));
                }
                //load data if search criteria is defined in querystring
                if (URLManager.getParameterByName("naics-code") || URLManager.getParameterByName("setasides")) {
                    Events.publish('loadData');
                }
            }
        );
        //$('#naics-code').select2({placeholder:'Select a NAICS code', dropdownAutoWidth : true});
        $('#naics-code').select2({placeholder: 'Select a NAICS code', width: '400px' });
    }
};
