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

