var update = function(id) {
    $.ajax({
        url : "/api/favorite",
        type : "POST",
        contentType: 'application/json',
        data: JSON.stringify({
            club_id: id
        }),
        crossdomain: true,
        success: function(thing) {
            if(thing) {
                console.log("HERE");
                span = document.getElementById("fav_"+id);
                span_val = parseInt(span.innerHTML);
                console.log(span_val);
                span.innerHTML = span_val + 1;
            };
        }
    });
};
