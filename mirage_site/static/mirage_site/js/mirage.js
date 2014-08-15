$( document ).ready( function() {
	//populate NAICS dropdown
    $("#naics-code")
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
			})
			if (getParameterByName("naics-code")) {
				$("#naics-code").select2().select2("val", getParameterByName("naics-code"));
			}
			//load data if search criteria is defined in querystring
			if (getParameterByName("naics-code") || getParameterByName("setasides")) {
				refresh_data();
			}
		}
	)

	//bind History
	History.Adapter.bind(window, 'statechange', null);

	//set naics dropdown width
	$('#naics-code').select2({dropdownAutoWidth : true});

});

//from http://stackoverflow.com/questions/901115/how-can-i-get-query-string-values-in-javascript
function getParameterByName(name) {
	//return querystring value of given parameter
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}
