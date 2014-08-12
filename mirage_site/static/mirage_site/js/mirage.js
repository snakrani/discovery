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
			refresh_data();
		}
	)
	$("#naics-code").select2({ placeholder: "Select NAICS code", width: "off" });

	//bind History
	History.Adapter.bind(window, 'statechange', null);
});

function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}
