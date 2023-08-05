
function valid(){
    var zahl_1 = parseInt(document.getElementById("zahl_1").value);
    var zahl_2 = parseInt(document.getElementById("zahl_2").value);
    if (isNaN(zahl_1) || isNaN(zahl_2)){
        return false;
    }else{
        return true;
    }
}



function rechne(){
    var operator = document.getElementById("operator").value;
    if (valid()){
        var zahl_1 = parseInt(document.getElementById("zahl_1").value);
        var zahl_2 = parseInt(document.getElementById("zahl_2").value);
        if(operator == "+"){
            var wert = zahl_1 + zahl_2;
        }else if (operator == "-"){
            var wert = zahl_1 - zahl_2;
        }else if (operator == "*"){
            var wert = zahl_1 * zahl_2;
        }else if (operator == "/"){
            var wert = zahl_1 / zahl_2;
        } else{
            var wert = "Der Operator: " + operator + " ist nicht gültig!";
        }
         
        document.getElementById("Ergebniss").innerHTML = "Ergebniss: " + wert;
    }else{
        document.getElementById("Ergebniss").innerHTML = "Es dürfen nur Zahlen Eingegeben werden!";
    }
}

