function send(question, choice) {
    var url = "/ajax/qa/";
    var params = "question="+question+"&awnser="+choice;
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send(params);
    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            var response = xhr.responseText;
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

    let q = document.getElementById("question-"+num.toString());
    q.onclick(remove(num.toString()));
    q.value = "Del"
    q.style.className = "btn btn-danger";
}

function remove(num) {
    send(num, 'remove');

    let q = document.getElementById("question-"+num.toString());
    q.onclick(remove(num.toString()));
    q.value = "Add"
    q.className = "btn btn-success";
}

