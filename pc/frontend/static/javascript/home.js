var options = [
    {
        name : "Productivity",
        index : 1
    },
    {
        name : "Gaming",
        index : 2
    },
    {
        name : "Basic",
        index : 3
    },
]

var clear = function(x) {
    for (var i=0; i<options.length; i++) {
        let op = options[i];
        if (op != x) {
            document.getElementById(op.name).style.display = 'none';
        }
    }
}

var select = function() {
    var x = document.getElementById("mySelect").options.selectedIndex; 
    
    if(x != 0) {
        var option = options[x];

        document.getElementById("choose").style.display = 'none';

        clear(x);

        document.getElementById(option.name).style.display = 'block';
        if(x == 3) {
            document.getElementById(option.name).style.display = 'block';
        }
    } else {
        clear(x);
        document.getElementById("choose").style.display = 'block';
    }

    console.log(x);
}
