function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function send(question, choice) {
    var url = "/ajax/qa/";
    var params = "question="+question+"&awnser="+choice;
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
                console.log("error");
            }
        }
    }
}

function select(num) {
    send(num, 'add');
    console.log("select");
    let q = document.getElementById("question-"+num.toString());
    q.setAttribute( "onClick", "remove("+num+");" );
    q.innerHTML = "X"
    q.className = "btn btn-danger";
}

function remove(num) {
    send(num, 'remove');
    console.log("remove")
    let q = document.getElementById("question-"+num.toString());
    q.setAttribute( "onClick", "select("+num+");" );
    q.innerHTML = "Add"
    q.className = "btn btn-success";
}

