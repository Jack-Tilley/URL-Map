function showTime(filepath){
    console.log("showTime is called")
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var myObj = JSON.parse(this.responseText);
            document.getElementById("time").innerHTML = myObj.exectime + " seconds";
        }
        else{
            document.getElementById("time").innerHTML = "Error occurred during the innternal process"
        }
    };
    xmlhttp.open("GET", filepath, true);
    xmlhttp.send();
}