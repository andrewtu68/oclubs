( function( $ ) {
	$( document )
		.ready( function() {
			$( "#loginModal input[name='hasaccount'][value='1']" )
				.click();
			$( "#loginModal input[name='hasaccount']" )
				.change( function() {
					switch ( $( "#loginModal input[name='hasaccount']:checked" )
						.val() ) {
						case '0':
							$( '#loginModal #loginform' )
								.hide();
							$( '#loginModal #registerform' )
								.show();
							break;
						default:
							$( '#loginModal #loginform' )
								.show();
							$( '#loginModal #registerform' )
								.hide();
							break;
					}
				} );

			$( ".clickable" )
				.click( function() {
					window.document.location = $( this )
						.data( "href" );
				} );

			$( "#updatecheck" )
				.click( function() {
					var checked = $( '#leader_radio input[type=radio]:checked' );
					if ( checked.size() > 0 ) {
						$( ".modal .modal-body" )
							.html( "<p>Your choice is " + checked.val() + ".</p>" );
						$( ".modal .modal-footer" )
							.html( "<button type='button' class='btn btn-default' data-dismiss='modal'>Reselect</button>" +
									'<input type="submit" class="btn btn-primary" form="leader_radio" name="change_leader" value="Confirm">' );
					} else {
						$( ".modal .modal-body" )
							.html( "<p>Please select one memeber as next club leader!</p>" );
						$( ".modal .modal-footer" )
							.html( "<button type='button' class='btn btn-default' data-dismiss='modal'>Close</button>" );
					}
				} );

			$( "#updatequit" )
				.click( function() {
					var selected = $( '.form-group select option:selected' );
					$( ".modal .modal-body" )
						.html( "<p>Your choice is " + selected.text() + ".</p>" );
				} );

			$( ".updatehm " )
				.click( function() {
					var date = $( "#date" ).val();
					var contents = $( "#contents" ).val();
					if ( date !== '' && contents !== '' ) {
						$( "#schedule tbody" )
							.append( "<tr><td>" + date + "</td><td>" + contents + "</td><td><button class='btn btn-primary' id='" + contents + "'>Delete</button></td></tr>");
						$( "#" + contents )
							.click( function() {$( this ).parents("tr").eq(0).remove();});
					}
				} );

			$( "#loginModal .modal-footer #login")
				.click( function() {
					if ( $( ".modal .modal-body div p").last().html() == "<p style='color:red'>Wrong student ID or password. Please input again.</p>" ){
						$( ".modal .modal-body div p").last().remove();
					}
					username = $( "#loginModal #username" ).val();
					password = $( "#loginModal #password" ).val();
					$.post( '/login' , { 'username': username, 'password': password } )
						.done( function(data) {
							if ( data.result == 'success' ) {
								location.reload();
							} else if ( data.result == 'loggedin') {
								$( ".modal .modal-body div").append( "<p style='color:#ffcc00'>Already logged in.</p>");
							} else if ( data.result == 'failure' ) {
								$( ".modal .modal-body div").append( "<p style='color:red'>Wrong student ID or password. Please input again.</p>");
							}
					} );
				} );
		} );
} )( jQuery );

function swing( x ) {
	x.className = 'swing animated';
}
