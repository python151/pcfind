window.onload = function() {
    const myInput = document.getElementById('inputPassword');
    myInput.onpaste = function(e) {
        e.preventDefault();
    }
}