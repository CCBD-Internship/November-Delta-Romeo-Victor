var marks_store_A;

// function marks_view_refresh_A() {
//     document.getElementById("marks_view_initial_A").setAttribute('style','display:none')
//     var xhttp = new XMLHttpRequest()
//     xhttp.onreadystatechange = function () {
//         if (this.readyState == XMLHttpRequest.DONE && this.status == 200) {
//             let data = JSON.parse(this.responseText)
//             marks_store_A = data
//             var lst = ['srn', 'name', 'team_year_code', 'team_id', 'dept_id']
//             var str = ''
//             for (let i in data) {
//                 str += '<tr><td scope="row" style="text-align:right"><input name="marks_view_boxes_A" class="form-check-input position-static" type="checkbox"></input></td>'
//                 for (let j in lst) {
//                     str += ("<td>" + data[i][lst[j]] + "</td>")
//                 }
//                 str += ("<td>" + admin_marks_return_status(data[i]) + "</td>")
//                 str += '</tr>'
//             }
//             document.getElementById("marks_view_body_A").innerHTML = str
//             var tbody = document.getElementById("marks_view_body_A")
//             for (i = 0; i < tbody.children.length; i++) {
//                 tbody.children[i].addEventListener('click', marks_view_modal_A)
//             }
//             checkerInit("marks_view_boxes_main_A", "marks_view_boxes_A")
//         }
//     }
//     refreshLoader(xhttp)
//     xhttp.open("GET", "/api/" + getCookie("username") + "/marks-view/", true);
//     xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
//     xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
//     xhttp.send();
// }

function marks_view_search_A() {
    document.getElementById("marks_view_initial_A").setAttribute('style', 'display:none')
    var tbody
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == XMLHttpRequest.DONE && this.status == 200) {
            let data = JSON.parse(this.responseText)
            marks_store_A = data
            var lst = ['srn', 'name', 'team_year_code', 'team_id', 'dept_id']
            var str = ''
            for (let i in data) {
                str += '<tr><td scope="row" style="text-align:right"><input name="marks_view_boxes_A" class="form-check-input position-static" type="checkbox"></input></td>'
                for (let j in lst) {
                    str += ("<td>" + data[i][lst[j]] + "</td>")
                }
                str += ("<td>" + admin_marks_return_status(data[i]) + "</td>")
                str += '</tr>'
            }
            document.getElementById("marks_view_body_A").innerHTML = str
            tbody = document.getElementById("marks_view_body_A")
            for (i = 0; i < tbody.children.length; i++) {
                tbody.children[i].addEventListener('click', marks_view_modal_A)
            }
            checkerInit("marks_view_boxes_main_A", "marks_view_boxes_A")
        }
    }
    refreshLoader(xhttp)
    var srn = document.getElementById("marks_view_search_srn_A").value
    var name = document.getElementById("marks_view_search_name_A").value
    var Team_year_code = document.getElementById("marks_view_search_team_year_code_A").value
    var Team_id = document.getElementById("marks_view_search_team_id_A").value
    var str = "/api/" + getCookie("username") + "/marks-view/"
    var guide_weight = document.getElementById("guide_weight_search_team_id_A").value
    var guide = document.getElementById("guide_search_team_id_A").value
    var sstr = ''
    if (Team_year_code != "") {
        if (sstr == "")
            sstr += ("?team_year_code=" + Team_year_code)
        else
            sstr += ("&team_year_code=" + Team_year_code)
    }
    if (Team_id != "") {
        if (sstr == "")
            sstr += ("?team_id=" + Team_id)
        else
            sstr += ("&team_id=" + Team_id)
    }
    if (name != "") {
        if (sstr == "")
            sstr += ("?name=" + name)
        else
            sstr += ("&name=" + name)
    }
    if (srn != "") {
        if (sstr == "")
            sstr += ("?srn=" + srn)
        else
            sstr += ("&srn=" + srn)
    }
    if (guide != "") {
        if (sstr == "")
            sstr += ("?guide=" + guide)
        else
            sstr += ("&guide=" + guide)
    }
    if (guide_weight != "") {
        if (sstr == "")
            sstr += ("?guide_weight=" + guide_weight)
        else
            sstr += ("&guide_weight=" + guide_weight)
    } else {
        if (sstr == "")
            sstr += ("?guide_weight=" + 0)
        else
            sstr += ("&guide_weight=" + 0)
    }
    str += sstr
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
    if (e.target.getAttribute("name") != 'marks_view_boxes_A') {
        val = marks_view_elem_A(e.target.parentElement.children[1].innerHTML)
        document.getElementById("marks_modal_A_title").innerHTML = val["srn"]
        document.getElementById("marks_modal_A_subtitle").innerHTML = val["name"]
        for (var i = 1; i <= 5; i++) {
            var tbody = document.getElementById("marks_view_body_A_Review" + i.toString())
            var ctitle = document.getElementById("Card_A_Title_Review" + i.toString())
            var str = ''
            if (i in val["review"]) {
                ctitle.setAttribute('class', 'btn btn-link')
                for (let j = 0; j < val["review"][i].length; j++) {
                    str += '<tr>'
                    for (k in val["review"][i][j]) {
                        if (k == "is_evaluated") {
                            if (val["review"][i][j][k] == true) {
                                str += ("<td>" + '&#9989;' + "</td>")
                            }
                            else {
                                str += ("<td>" + '&#10060;' + "</td>")
                                ctitle.setAttribute('class', 'btn btn-link text-warning')
                            }
                        }
                        else {
                            str += ("<td>" + val["review"][i][j][k] + "</td>")
                        }
                    }
                    str += "</tr>"
                }
            }
            else {
                ctitle.setAttribute('class', 'btn btn-link text-danger')
            }
            tbody.innerHTML = str
        }
        var tot_body = document.getElementById("marks_view_body_A_Total")
        var rows = tot_body.children
        var c_c = 0;
        for (let i of val["review"]["total_individual"]) {
            rows[c_c].children[1].innerHTML = i["marks_scored"];
            rows[c_c].children[2].innerHTML = i["total_marks"];
            rows[c_c].children[3].innerHTML = i["percentage"].toFixed(2) + "%";
            c_c++
        }
        rows[c_c].children[1].innerHTML = '<b>' + val["review"]["total"]["marks_scored"] + '</b>';
        rows[c_c].children[2].innerHTML = '<b>' + val["review"]["total"]["total_marks"] + '</b>';
        rows[c_c].children[3].innerHTML = '<b>' + val["review"]["total"]["percentage"].toFixed(2) + "%" + '</b>';
        $('#modal_admin_marks_view').modal({
            show: true
        })
    }
}

function admin_marks_return_status(val) {
    var str = ''
    for (var i = 1; i <= 5; i++) {
        if (i in val["review"]) {
            var bool = true
            for (j = 0; j < val["review"][i].length; j++) {
                if (val["review"][i][j]["is_evaluated"] == false) {
                    bool = false
                }
            }
            str += (bool ? '&#9989;' : '❕')
        }
        else {
            str += '&#10060;'
        }
    }
    return str
}

function download(filename, text) {
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/csv;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', filename);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}
function getCheckedBoxes_A_marksview(chkboxName) {
    var checkboxes = document.getElementsByName(chkboxName);
    var checkboxesChecked = [];
    for (var i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked) {
            checkboxesChecked.push(checkboxes[i].parentElement.nextElementSibling.textContent);
        }
    }
    return checkboxesChecked.length > 0 ? checkboxesChecked : null;
}
function Admin_print() {
    var students = getCheckedBoxes_A_marksview("marks_view_boxes_A")
    var mainstr = "SRN,Name,Review 1(40),Review 2(40),Review 3(35),Review 4(40),Review 5(40),Total(195),Percentage,\n"
    if (students && students.length) {
        for (let i of marks_store_A) {
            if (students.indexOf(i["srn"]) != -1) {
                var str = i["srn"] + ',' + i["name"] + ','
                for (j of i["review"]["total_individual"]) {
                    str += (j["marks_scored"] + ',')
                }
                str += (i["review"]["total"]["marks_scored"] + ',' + i["review"]["total"]["percentage"].toFixed(2) + ',' + '\n')
                mainstr += str
            }
        }
        download("results.csv", mainstr);
    }
}

admin_refresh = function () {
    var a = 10
}