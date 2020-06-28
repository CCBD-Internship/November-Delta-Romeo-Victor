function loadJS() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            admin_JS = document.getElementById("admin_JS")
            admin_JS.innerHTML=""
            elem = document.createElement('script')
            elem.innerHTML = this.responseText;
            admin_JS.appendChild(elem)
        }
    };
    xhttp.open("GET", "admin_studentJS/", true);
    xhttp.send();
}
function loadDoc() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("admin_HTML").innerHTML = this.responseText;
        }
    };
    xhttp.open("GET", "admin_studentHTML/", true);
    xhttp.send();
}
var Tree = { "Admin": [], "Coordinator": [], "Evaluator": [] }
var evalview = { 1: { student: [], team: [] }, 2: { student: [], team: [] }, 3: { student: [], team: [] }, 4: { student: [], team: [] }, 5: { student: [], team: [] }, "team": [], "student": [], "faculty-panel": [] }
var coordview = { "department": [], "faculty-panel": [], "team-faculty-review": [] }
var adminview = { "department": [], "faculty": [], "panel": [], "faculty-panel": [], "team": [], "student": [], "marks-view": [] }
var User;
var Admin_BC = []
var Coordinator_BC = []
var Evaluator_BC = []
var currenttab;
function returnCurrentHTML() {
    var lst = NaN
    if (currenttab == "Admin")
        lst = document.getElementById("admin_HTML")
    else if (currenttab == "Coordinator")
        lst = document.getElementById("coordinator_HTML")
    else if (currenttab == "Evaluator")
        lst = document.getElementById("evaluator_HTML")
    return lst;
}
function returnCurrentJS() {
    var lst = NaN
    if (currenttab == "Admin")
        lst = document.getElementById("admin_JS")
    else if (currenttab == "Coordinator")
        lst = document.getElementById("coordinator_JS")
    else if (currenttab == "Evaluator")
        lst = document.getElementById("evaluator_JS")
    return lst;
}
function returnCurrentTab() {
    var lst = NaN
    if (currenttab == "Admin")
        lst = Admin_BC
    else if (currenttab == "Coordinator")
        lst = Coordinator_BC
    else if (currenttab == "Evaluator")
        lst = Evaluator_BC
    return lst;
}
window.addEventListener('hashchange', function (e) {
    if (window.location.hash != "") {
        spl = window.location.hash.split("#")[1].split('/')
        spl.pop()
        currenttab = spl[0]
        var lst = returnCurrentTab()
        var len = lst.length
        for (let i = 0; i < len; i++) {
            lst.pop()
        }
        for (let i = 0; i < spl.length; i++) {
            lst.push(spl[i])
        }
        crumbMaker()
    }
});
function setTree() {
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == XMLHttpRequest.DONE && this.status == 200) {
            let data = JSON.parse(this.responseText)
            User = data["user"]
            if (data["user"]["is_admin"] == true) {
                Tree.Admin = adminview
            }
            for (let i = 0; i < data["panels"].length; i++) {
                if (Tree.Evaluator.includes(data["panels"][i]["panel_year_code"] + '-' + data["panels"][i]["panel_id"]) == false) {
                    var st = data["panels"][i]["panel_year_code"] + '-' + data["panels"][i]["panel_id"]
                    Tree.Evaluator[st] = evalview
                }
                if (data["panels"][i]["is_coordinator"] == true && Tree.Coordinator.includes(["panels"][i]["panel_year_code"] + '-' + data["panels"][i]["panel_id"]) == false) {
                    var st = data["panels"][i]["panel_year_code"] + '-' + data["panels"][i]["panel_id"]
                    Tree.Coordinator[st] = coordview
                }
            }
            Admin_BC.push("Admin")
            Coordinator_BC.push("Coordinator")
            Evaluator_BC.push("Evaluator")
            navbarGenerate()
        }
    }
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTkzMjc4NzU0LCJqdGkiOiJjZjNiZTM1YjkwNmU0ZTMwYWU3YTU3MTU2Njg2NGYyMCIsInVzZXJfaWQiOjJ9.sYCPuIoDnKhtAL4TXqiAmeHR3aAdOhtUK7m2UWGl1lo"
    xhttp.open("GET", "/api/kvs1/aboutme/", true);
    xhttp.setRequestHeader("Authorization", "Bearer " + token);
    xhttp.send()
}
function crumbMaker() {
    lst = returnCurrentTab()
    NVRDbreadcrumb = document.getElementById(id = "NVRDbreadcrumb")
    len = NVRDbreadcrumb.children.length
    for (let i = 0; i < len; i++) {
        NVRDbreadcrumb.removeChild(NVRDbreadcrumb.children[0])
    }
    for (let i = 0; i < lst.length; i++) {
        elem = document.createElement("li")
        elem.innerHTML = lst[i]
        if (i + 1 == lst.length) {
            elem.setAttribute('aria-current', 'page')
            elem.setAttribute('class', 'breadcrumb-item active')
        }
        else {
            elem.setAttribute('class', 'breadcrumb-item')
        }
        elem.addEventListener('click', crumbPopper)
        NVRDbreadcrumb.appendChild(elem)
    }
    NVRDbreadcrumb = document.getElementById(id = "NVRDbreadcrumb")
    //elem = document.createElement("li")
    //elem.setAttribute('class', 'breadcrumb-item')
    //elem.addEventListener('click', crumbPopper)
    //NVRDbreadcrumb.appendChild(elem)
    listMaker()
    urlstr = ""
    for (let i = 0; i < lst.length; i++) {
        urlstr += (lst[i] + '/')
    }
    window.location.hash = urlstr;
}
function crumbPopper(e) {
    lst = returnCurrentTab()
    ind = lst.indexOf(e.target.innerHTML)
    len = lst.length
    for (let i = ind + 1; i < len; i++)
        lst.pop()
    crumbMaker()
}
function crumbPusher(e) {
    lst = returnCurrentTab()
    lst.push(e.target.innerHTML)
    crumbMaker()
}
function listMaker() {
    lst = returnCurrentTab()
    obj = Tree;
    for (let i = 0; i < lst.length; i++) {
        obj = obj[lst[i]]
    }
    if (Object.keys(obj).length>0) {
        NVRDlist = document.getElementById("NVRDlist")
        len = NVRDlist.children.length
        for (let i = 0; i < len; i++) {
            NVRDlist.removeChild(NVRDlist.children[0])
        }

        for (let i = 0; i < Object.keys(obj).length; i++) {
            elem = document.createElement("button")
            elem.setAttribute('class', 'list-group-item list-group-item-action');
            elem.addEventListener('click', crumbPusher)
            elem.innerHTML = Object.keys(obj)[i]
            NVRDlist.appendChild(elem)
        }
    }
}
function onClickNavbar(e) {
    NVRDnavbar = document.getElementById('NVRDnavbar').children;
    for (let i = 0; i < NVRDnavbar.length; i++) {
        if (e.target.innerHTML == NVRDnavbar[i].innerHTML) {
            NVRDnavbar[i].setAttribute('class', 'nav-item nav-link active')
            currenttab = NVRDnavbar[i].innerHTML
        }
        else {
            NVRDnavbar[i].setAttribute('class', 'nav-item nav-link')
        }
    }
    crumbMaker()
}
function navbarGenerate() {
    loadJS()
    loadDoc()
    NVRDnavbar = document.getElementById("NVRDnavbar")
    if (Object.keys(Tree.Admin).length > 0) {
        elem = document.createElement('a')
        elem.innerHTML = "Admin"
        elem.addEventListener('click', onClickNavbar)
        elem.setAttribute('class', 'nav-item nav-link')
        NVRDnavbar.appendChild(elem)
    }
    if (Object.keys(Tree.Coordinator).length > 0) {
        elem = document.createElement('a')
        elem.addEventListener('click', onClickNavbar)
        elem.setAttribute('class', 'nav-item nav-link')
        elem.innerHTML = "Coordinator"
        NVRDnavbar.appendChild(elem)
    }
    if (Object.keys(Tree.Evaluator).length > 0) {
        elem = document.createElement('a')
        elem.addEventListener('click', onClickNavbar)
        elem.setAttribute('class', 'nav-item nav-link')
        elem.innerHTML = "Evaluator"
        NVRDnavbar.appendChild(elem)
    }
}