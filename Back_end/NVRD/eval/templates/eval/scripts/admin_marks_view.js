var marks_store_A;

function marks_view_refresh_A() {
    var tbody
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            let data = JSON.parse(this.responseText)
            marks_store_A = data
            var lst = ['srn', 'name', 'team_year_code', 'team_id', 'dept_id']
            var str = ''
            for (let i in data) {
                str += '<tr><td scope="row" style="text-align:right"><input name="marks_view_boxes_A" class="form-check-input position-static" type="checkbox"></input></td>'
                for (let j in lst) {
                    str += ("<td>" + data[i][lst[j]] + "</td>")
                }
                str += '</tr>'
            }
            document.getElementById("marks_view_body_A").innerHTML = str
            tbody = document.getElementById("marks_view_body_A")
            for (i = 0; i < tbody.children.length; i++) {
                tbody.children[i].addEventListener('click', marks_view_modal_A)
            }
            checkerInit("marks_view_boxes_main_A","marks_view_boxes_A")
        }
    }
    refreshLoader(xhttp)
    xhttp.open("GET", "/api/" + getCookie("username") + "/marks-view/", true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.send();
}

function marks_view_search_A() {
    var tbody
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            let data = JSON.parse(this.responseText)
            marks_store_A = data
            var lst = ['srn', 'name', 'team_year_code', 'team_id', 'dept_id']
            var str = ''
            for (let i in data) {
                str += '<tr><td scope="row" style="text-align:right"><input name="marks_view_boxes_A" class="form-check-input position-static" type="checkbox"></input></td>'
                for (let j in lst) {
                    str += ("<td>" + data[i][lst[j]] + "</td>")
                }
                str += '</tr>'
            }
            document.getElementById("marks_view_body_A").innerHTML = str
            tbody = document.getElementById("marks_view_body_A")
            for (i = 0; i < tbody.children.length; i++) {
                tbody.children[i].addEventListener('click', marks_view_modal_A)
            }
            checkerInit("marks_view_boxes_main_A","marks_view_boxes_A")
        }
    }
    refreshLoader(xhttp)
    var srn = document.getElementById("marks_view_search_srn_A").value
    var name = document.getElementById("marks_view_search_name_A").value
    var str = "/api/" + getCookie("username") + "/marks-view/"
    if (name != "" || srn != "") {
        str += '?'
        if (name != "") {
            str += ("name=" + name)
        }
        if (srn != "") {
            if (name != "") {
                str += '&'
            }
            str += ("srn=" + srn)
        }
    }
    xhttp.open("GET", str, true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.send();
}

function marks_view_elem_A(x) {
    for (var i = 0; i < marks_store_A.length; i++) {
        if (x == marks_store_A[i]["srn"]) {
            return marks_store_A[i]
        }
    }
}
var val;
function marks_view_modal_A(e) {
    val = marks_view_elem_A(e.target.parentElement.children[1].innerHTML)
    document.getElementById("marks_modal_A_title").innerHTML = val["srn"]
    document.getElementById("marks_modal_A_subtitle").innerHTML = val["name"]
    for (var i = 1; i <= 5; i++) {
        var tbody = document.getElementById("marks_view_body_A_Review" + i.toString())
        var ctitle = document.getElementById("Card_A_Title_Review" + i.toString())
        var str = ''
        if (i in val["review"]) {
            ctitle.setAttribute('class', 'btn btn-link')
            // document.getElementById("Card_A_Review" + i.toString()).setAttribute("style", "display:inline")
            for (let j = 0; j < val["review"][i].length; j++) {
                str += '<tr>'
                for (k in val["review"][i][j]) {
                    str += ("<td>" + val["review"][i][j][k] + "</td>")
                }
                str += "</tr>"
            }
        }
        else {
            ctitle.setAttribute('class', 'btn btn-link text-danger')
            // document.getElementById("Card_A_Review" + i.toString()).setAttribute("style", "display:none")
        }
        tbody.innerHTML = str
    }
    $('#modal_admin_marks_view').modal({
        show: true
    })
}

admin_refresh = marks_view_refresh_A