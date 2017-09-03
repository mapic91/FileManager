function utoa(str) {
    return btoa(encodeURIComponent(str))
}

function atou(base64str) {
    return decodeURIComponent(atob(base64str))
}

function openPath(path) {
    window.location.href = '?path=' + utoa(path);
    return false;
}

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
        xhttp.open("GET", "?delete=1&dir=1&path=" + utoa(path), false);
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
        xhttp.open("GET", "?delete=1&path=" + utoa(path), false);
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
        xhttp.open("GET", "?deleteall=1&path=" + utoa(path), false);
        xhttp.send();
    }
}

function deleteSelected() {
    var files = [].slice.apply(document.querySelectorAll("input[type=checkbox]"))
        .filter(function(c){ return (c.name == "floder" || c.name == "file") && c.checked; })
        .map(function(c) {return {type:c.name, value: c.value};});
    var jsonStr = JSON.stringify(files)
    if(files.length > 0 && confirm("Dlelet all selections?")) {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            console.log("xmlhttprequest status: " + this.status + " readyState: " + this.readyState);
            if (this.readyState == 4 && this.status != 0) {
                if (this.status == 200) {
                    location.reload(true);
                }
                else {
                    document.getElementById('error_msg').innerText = "Delete selections failed!";
                }
            }
        };
        xhttp.open("POST", "/deletselections", false);
        xhttp.setRequestHeader("Content-type", "application/json");
        xhttp.send(jsonStr);
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
        xhttp.open("GET", "?rename=1&path=" + utoa(path) + "&oldname=" + utoa(oldname) + "&newname=" + utoa(newname), false);
        xhttp.send();
    }
}