var starting;
function shrink(starting, AmountOfAllowedChars) {
  /* var starting: int */
  var ret = "";
  var flag = false;

  starting = starting.split('')

  for(i = 0; i<=AmountOfAllowedChars; i++) {
    ret = ret + starting[i];
    if (i == AmountOfAllowedChars) {
      flag = true;
    }
  }

  if (flag) {
    ret = ret + "...";
  }

  return ret;
}

function onPageFunc() {
  var allowedChars = 30;
  var i = 1;
  while (i <= savedComputers) {
    let old = document.getElementById(i);
    old.innerHTML = shrink(old.innerText, allowedChars);
    i++;
  }
}

function hideAdvanced() {
  console.log("advanced being hidden");
  var advanced = document.getElementsByClassName("advanced");
  for (i=0; i<advanced.length; i++) {
    let current = advanced[i];
    current.style.display = "none";
  }
  document.getElementById("btn").setAttribute("onClick", "showAdvanced()");
  document.getElementById("btn").innerText = "Advanced";
}

function showAdvanced() {
  console.log("advanced being shown");
  var advanced = document.getElementsByClassName("advanced");
  for (i=0; i<advanced.length; i++) {
    let current = advanced[i];
    current.style.display = "initial";
    console.log(i)
  }
  document.getElementById("btn").setAttribute("onClick", "hideAdvanced()");
  document.getElementById("btn").innerText = "Advanced";
}
