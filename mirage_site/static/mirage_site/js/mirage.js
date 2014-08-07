$( document ).ready( function() {
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
		}
	)
	$("#naics-code").select2({ placeholder: "Select NAICS code", width: "off"});
});
