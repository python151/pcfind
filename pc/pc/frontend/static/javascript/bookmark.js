function sendAjax(params, url) {
    var xhr = new XMLHttpRequest();
    var csrftoken = getCookie('csrftoken');
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    xhr.send(params);
    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            var response = xhr.responseText;
            console.log(response);
            if(response == "ok") {
                console.log(params);
            }
            else {
                alert("Unexpected Error. Please try again later.");
            }
        }
    }
}

var id;
function bookmark(id) {
    let url = "/ajax/bookmark/";
    let params = "lessonID="+id+"&action=save";
    sendAjax(params, url);
}