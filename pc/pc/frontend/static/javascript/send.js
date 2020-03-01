var amountSelected = 0;

// from django documentation
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

function send(question, num1, choice) {
    var url = "/ajax/qa/";
    var params = "question="+question+"&awnser="+choice+"&group="+num1;
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

function select(num, num1) {
    document.getElementById("btn").className = "btn btn-primary";
    amountSelected++;
    send(num, num1, 'add');
    console.log("select");
    let q = document.getElementById("question-"+num.toString());
    q.setAttribute( "onClick", "remove("+num+", "+num1+");" );
    q.innerHTML = "X"
    q.className = "btn btn-danger";
}

function remove(num, num1) {
    amountSelected--;
    if (amountSelected <= 0) {
        document.getElementById("btn").className = "btn btn-primary disabled"
    }
    send(num, num1, 'remove');
    console.log("remove")
    let q = document.getElementById( "question-" + num.toString() );
    q.setAttribute( "onClick", "select("+num+", "+num1+");" );
    q.innerHTML = "Add"
    q.className = "btn btn-success";
}