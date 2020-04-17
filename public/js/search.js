function searchURL(filepath, target){
    console.log("serchURL is called");
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            console.log("HTTP 200 OK");
            var myObj = JSON.parse(this.responseText);
            var len = myObj["nodes"].length;
            var flag = 0;
            var url;

            for(var i = 0; i < len; i++){
                url = myObj["nodes"][i]["id"];
                console.log(i);
                console.log(target.value);
                console.log(url);
                if (url == target.value){
                    flag = 1;
                    break;
                }
            }

            if (flag == 1){
                document.getElementById("search_result").innerHTML = target.value + " is found in the URL map";
            }
            else{
                document.getElementById("search_result").innerHTML = target.value + " is not found in the URL map";
            }
        }
        else{
            document.getElementById("search_result").innerHTML = "Error occurred during the innternal process";
        }
    };
    xmlhttp.open("GET", filepath, true);
    xmlhttp.send();
}