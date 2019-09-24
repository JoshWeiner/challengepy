//Changes heading back to default when mouse is no loger over the list item
var changeBack = function() {
  var h = document.getElementById("h");
  h.innerHTML = "Hello World!";
}

var tag_num = 0;
var tag_list = [];

//Removes item from list
var remove = function(e) {
    //console.log(e);
    //console.log(e.target);
    var toRemove = e.target;
    var tag = e.value;
    tag_list.pop(tag);
    tag_num -= 1;
    toRemove.parentNode.removeChild(toRemove);
};


/*
2. Add new list items to the current list
*/
var addToList = function(e) {
    var list = document.getElementById("taglist");
    var listItem = document.createElement("button");
    var tag = document.getElementById("tagselect")
    listItem.type = "button";
    listItem.className = "btn btn-primary";
    listItem.style = "margin: 1em;";
    if(!tag_list.includes(tag.value)) {
        listItem.innerHTML=tag.value;
        listItem.addEventListener('click', remove);
        listItem.addEventListener('mouseover',
          function (e) {
            setHeading(this.innerHTML);
          });
        listItem.addEventListener('mouseout', changeBack);
        list.appendChild(listItem);
        tag_num += 1;
        tag_list.push(tag.value)
    }
};

var upload = function() {
    var club_name = document.getElementById("name").value;
    var description = document.getElementById("desc").value;
    console.log(tag_list);
    $.ajax({
        url : "/api/clubs",
        type : "POST",
        contentType: 'application/json',
        data: JSON.stringify({
            name: club_name,
            description: description,
            tags: tag_list,
        }),
        crossdomain: true,
        success: function(response) {
            if (response.redirect) {
                window.location.href = response.redirect;
            };
        }
    });
};

var button = document.getElementById("b");
button.addEventListener('click', addToList);

var submit = document.getElementById("submit");
submit.addEventListener('click', upload);
