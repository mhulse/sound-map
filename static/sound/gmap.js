/*
** 
** 2011 Micky Hulse <hulse.me>
** Inspired by: <http://djangosnippets.org/snippets/2106/>
** Sorry, not enough time to re-write this using jQuery. :(
** http://stackoverflow.com/questions/3913103/javascript-object-literal-pattern-with-multiple-instances
** 
*/

GmapObject = function() {
	
	var that = this;
	var id = undefined;
	var geocoder = new Object;
	var map = new Object;
	
	save = function(point) {
		
		var input = document.getElementById('id_' + that.id);
		input.value = point.lat().toFixed(6) + ',' + point.lng().toFixed(6);
		
	},
	
	addy = function() {
		
		var address = document.getElementById('address_' + that.id).value;
		
		that.geocoder.geocode({'address': address}, function(results, status) {
			if (status == google.maps.GeocoderStatus.OK) {
				that.map.setCenter(results[0].geometry.location);
				save(that.map.getCenter());
			} else {
				alert('Geocode was not successful for the following reason: ' + status);
			}
		});
		
	},

	init = function(id, lat, lng) {
		
		that.id = id;
		
		that.geocoder = new google.maps.Geocoder();
		
		var point = new google.maps.LatLng(lat, lng);
		
		var options = {
			zoom: 13,
			center: point,
			mapTypeId: google.maps.MapTypeId.HYBRID
		};
		
		that.map = new google.maps.Map(document.getElementById('map_' + that.id), options);
		
		google.maps.event.addListener(that.map, 'center_changed', function() {
			save(that.map.getCenter());
		});
		
	};
	
	// Public API:
	return {
		init: init,
		addy: addy
	};
	
};

(function($) {
	
	function add_addy() {
		
		var id_address1 = $('#id_address1').val();
		var id_address2 = $('#id_address2').val();
		var id_city = $('#id_city').val();
		var id_state = $('#id_state').val();
		var id_zip = $('#id_zip').val();
		var id_country = $('#id_country').val();
		
		id_address1 = (id_address1.length > 0) ? id_address1 + ', ' : '';
		id_address2 = (id_address2.length > 0) ? id_address2 + ', ' : '';
		id_city = (id_city.length > 0) ? id_city + ', ' : '';
		id_state = (id_state.length > 0) ? id_state + ', ' : '';
		id_zip = (id_zip.length > 0) ? id_zip + ', ' : '';
		
		$('#address_geolocation').val(id_address1 + id_address2 + id_city + id_state + id_zip + id_country);
		
	};
	
	$(document).ready(function() {
		
		// Do it on page load:
		add_addy();
		
		// Do it again as they type:
		$('#id_address1, #id_address2, #id_city, #id_state, #id_zip, #id_country').bind('keypress blur', function() {
			
			// Format: 5555 Fake Street, Somewhere, NY, 55555, United States
			add_addy();
			
		});
		
	});
	
})(django.jQuery);