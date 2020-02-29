var width = 0;
var inter;
var i = 0;

var listOfWords = [
    "Amazon", "Ebay", "Newegg", "Dell", "Walmart", "Target", "Microsoft", "Apple", "Asus", "Lenovo"
]

function randInt(min, max) { // min and max included 
    return Math.floor(Math.random() * (max - min + 1) + min);
  }

function artificialAnimate() {
    let bar = document.getElementById("hidden");
    bar.style.display = "block";
    bar.style.height = "100%";
    bar.style.width = "100%";
    bar.style.background = "rgba(0, 0, 0, .5)";
    inter = setInterval(updateBar, randInt(10, 50));
}

function updateBar() {
    console.log(width);

    if (width % 11 == 0) {
        document.getElementById("currentText").innerHTML = listOfWords[i++];
    }
    document.getElementById("b1").style.width = String(width++)+"%";
    if (width == 100) {
        clearInterval(inter);
        window.location = "/get-pc"
        width = 0;
        i = 0;
    }
}