var update = function(id) {
    $.ajax({
        url : "/api/favorite",
        type : "POST",
        contentType: 'application/json',
        data: JSON.stringify({
            club_id: id
        }),
        crossdomain: true,
        success: function(response) {
            if (response.redirect) {
                window.location.href = response.redirect;
            };
        }
    });
};
