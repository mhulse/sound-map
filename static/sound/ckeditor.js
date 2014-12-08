(function($) {
	
	$(document).ready(function() {
		
		var config = {
			toolbar:
			[
				['Bold', 'Italic', '-', 'NumberedList', 'BulletedList', '-', 'Link', 'Unlink'],
				['UIColor']
			]
		};
		
		$( 'textarea.editor' ).ckeditor(config);
		
	});
	
})(django.jQuery);