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
    q.style.backgroundImage = "url(https://meic.org/wp-content/uploads/2017/04/red-x.png)";
}

function remove(num) {
    send(num, 'remove');

    let q = document.getElementById("question-"+num.toString());
    q.onclick(remove(num.toString()));
    q.style.backgroundImage = "url(https://ih1.redbubble.net/image.33042761.6980/flat,800x800,070,f.jpg)";
}

