$('#textEntry').keydown(function(e) {
            console.log("hai!");
        	var searchTerm = $('#textEntry').val();
        	var searchCategory = $('#sel1').val();
            if (e.which == 13 && name.length > 0) { //catch Enter key
            	//POST request to API to create a new visitor entry in the database
                $.ajax({
				  method: "POST",
				  url: "./api/photoupload",
				  contentType: "application/json",
				  data: JSON.stringify({query:searchTerm, category:searchCategory })
				})
                .done(function(data) {
                    if (data) {
                        $('#response').html(data);
                    } else {
                        $('#response').html("whoops");
                    }
                });
            }
        });

