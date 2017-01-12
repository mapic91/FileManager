function deleteDir(path) {
    if(confirm("Dlelet Dir: " + path + "  ?")) {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            console.log("xmlhttprequest status: " + this.status + " readyState: " + this.readyState);
            if (this.readyState == 4 && this.status != 0) {
                if (this.status == 200) {
                    location.reload(true)
                }
                else {
                    document.getElementById('error_msg').innerText = 'Delete [' + path + "] failed!"
                }
            }
        };
        xhttp.open("GET", "?delete=1&dir=1&path=" + path, false);
        xhttp.send();
    }
}

function deleteFile(path) {
    if(confirm("Dlelet Dir: " + path + "  ?")) {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            console.log("xmlhttprequest status: " + this.status + " readyState: " + this.readyState);
            if (this.readyState == 4 && this.status != 0) {
                if (this.status == 200) {
                    location.reload(true)
                }
                else {
                    document.getElementById('error_msg').innerText = 'Delete [' + path + "] failed!"
                }
            }
        };
        xhttp.open("GET", "?delete=1&path=" + path, false);
        xhttp.send();
    }
}


function deleteAllContent(path) {
    if(confirm("Dlelet all content in dir: " + path + "  ?")) {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            console.log("xmlhttprequest status: " + this.status + " readyState: " + this.readyState);
            if (this.readyState == 4 && this.status != 0) {
                if (this.status == 200) {
                    location.reload(true)
                }
                else {
                    document.getElementById('error_msg').innerText = 'Delete [' + path + "] failed!"
                }
            }
        };
        xhttp.open("GET", "?deleteall=1&path=" + path, false);
        xhttp.send();
    }
}

function rename(path, oldname) {
    var newname = prompt("New name:", oldname);
    if(newname != null) {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            console.log("xmlhttprequest status: " + this.status + " readyState: " + this.readyState);
            if (this.readyState == 4 && this.status != 0) {
                if (this.status == 200) {
                    location.reload(true)
                }
                else {
                    document.getElementById('error_msg').innerText = 'Rename [' + oldname + "] failed!"
                }
            }
        };
        xhttp.open("GET", "?rename=1&path=" + path + "&oldname=" + oldname + "&newname=" + newname, false);
        xhttp.send();
    }
}