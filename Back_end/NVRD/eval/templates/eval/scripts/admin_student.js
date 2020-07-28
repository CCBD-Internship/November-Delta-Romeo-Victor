// function student_refresh_A() {
//     tbody = document.getElementById("student_body")
//     var xhttp = new XMLHttpRequest()
//     xhttp.onreadystatechange = function () {
//         if (this.readyState == XMLHttpRequest.DONE) {
//             if (this.status == 200) {
//                 let data = JSON.parse(this.responseText)
//                 var str = ''
//                 var svgstr = '<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-pencil" fill="currentColor" xmlns="http://www.w3.org/2000/svg">'
//                 svgstr += '<path fill-rule="evenodd" d="M11.293 1.293a1 1 0 0 1 1.414 0l2 2a1 1 0 0 1 0 1.414l-9 9a1 1 0 0 1-.39.242l-3 1a1 1 0 0 1-1.266-1.265l1-3a1 1 0 0 1 .242-.391l9-9zM12 2l2 2-9 9-3 1 1-3 9-9z"/>'
//                 svgstr += '<path fill-rule="evenodd" d="M12.146 6.354l-2.5-2.5.708-.708 2.5 2.5-.707.708zM3 10v.5a.5.5 0 0 0 .5.5H4v.5a.5.5 0 0 0 .5.5H5v.5a.5.5 0 0 0 .5.5H6v-1.5a.5.5 0 0 0-.5-.5H5v-.5a.5.5 0 0 0-.5-.5H3z"/>'
//                 svgstr += '</svg>'
//                 for (let i in data) {
//                     str += '<tr><td scope="row" style="text-align:right"><input name="student_boxes_A" class="form-check-input position-static" type="checkbox"></input></td>'
//                     for (let j in data[i]) {
//                         str += ("<td>" + data[i][j] + "</td>")
//                     }
//                     str += '<td scope="col"><button type="button" class="btn btn-dark active btn" data-toggle="modal" data-target="#modal_admin_student_put" onclick="admin_student_put_form(this)">' + svgstr + '</button></td></tr>'
//                 }
//                 document.getElementById("student_body_A").innerHTML = str
//                 checkerInit("student_boxes_main_A", "student_boxes_A")
//             }
//         }
//     }
//     refreshLoader(xhttp)
//     xhttp.open("GET", "/api/" + getCookie("username") + "/student/", true);
//     xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
//     xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
//     xhttp.send();
// }

function student_refresh_A() {
    document.getElementById("student_initial_A").setAttribute('style', 'display:none')
    tbody = document.getElementById("student_body")
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == XMLHttpRequest.DONE && this.status == 200) {
            let data = JSON.parse(this.responseText)
            var str = ''
            var svgstr = '<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-pencil" fill="currentColor" xmlns="http://www.w3.org/2000/svg">'
            svgstr += '<path fill-rule="evenodd" d="M11.293 1.293a1 1 0 0 1 1.414 0l2 2a1 1 0 0 1 0 1.414l-9 9a1 1 0 0 1-.39.242l-3 1a1 1 0 0 1-1.266-1.265l1-3a1 1 0 0 1 .242-.391l9-9zM12 2l2 2-9 9-3 1 1-3 9-9z"/>'
            svgstr += '<path fill-rule="evenodd" d="M12.146 6.354l-2.5-2.5.708-.708 2.5 2.5-.707.708zM3 10v.5a.5.5 0 0 0 .5.5H4v.5a.5.5 0 0 0 .5.5H5v.5a.5.5 0 0 0 .5.5H6v-1.5a.5.5 0 0 0-.5-.5H5v-.5a.5.5 0 0 0-.5-.5H3z"/>'
            svgstr += '</svg>'
            for (let i in data) {
                str += '<tr><td scope="row" style="text-align:right"><input name="student_boxes_A" class="form-check-input position-static" type="checkbox"></input></td>'
                for (let j in data[i]) {
                    str += ("<td>" + data[i][j] + "</td>")
                }
                str += '<td scope="col"><button type="button" class="btn btn-dark active btn" data-toggle="modal" data-target="#modal_admin_student_put" onclick="admin_student_put_form(this)">' + svgstr + '</button></td></tr>'
            }
            document.getElementById("student_body_A").innerHTML = str
            checkerInit("student_boxes_main_A", "student_boxes_A")
        }
    }
    refreshLoader(xhttp)
    var srn = document.getElementById("student_search_srn_A").value
    var name = document.getElementById("student_search_name_A").value
    var str = "/api/" + getCookie("username") + "/student/"
    var Team_year_code = document.getElementById("student_search_team_year_code_A").value
    var Team_id = document.getElementById("student_search_team_id_A").value
    var guide = document.getElementById("student_search_guide_A").value
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
    str += sstr
    xhttp.open("GET", str, true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.send();
}

function getCheckedBoxes_A(chkboxName) {
    var checkboxes = document.getElementsByName(chkboxName);
    var checkboxesChecked = [];
    for (var i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked) {
            checkboxesChecked.push(checkboxes[i]);
        }
    }
    return checkboxesChecked.length > 0 ? checkboxesChecked : null;
}

function student_delete_A() {
    tbody = document.getElementById("student_body")
    var checkedBoxes = getCheckedBoxes_A("student_boxes_A");
    if (checkedBoxes.length > 0) {
        a = []
        for (i = 0; i < checkedBoxes.length; i++) { a.push(checkedBoxes[i].parentElement.parentElement.firstElementChild.nextElementSibling.innerHTML) }
        var modal = $("#A_Student_DeleteconfirmModal");
        modal.modal("show");
        $("#A_Student_DeleteconfirmMessage").empty().append("Do you want to delete " + a.length + " students");
        $('#A_Student_DeleteconfirmOk')
            .on('click', function (e) {
                e.preventDefault();
                send_delete_A(a);
                $('#A_Student_DeleteconfirmModal').modal('hide');
            });
        $("#A_Student_DeleteconfirmCancel").on('click', function (e) {
            e.preventDefault();
            $('#A_Student_DeleteconfirmModal').modal('hide');
        });
    }
}

function send_delete_A(students) {
    var JSON_array = []
    for (let i = 0; i < students.length; ++i)
        JSON_array.push({ "srn": students[i] })
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == XMLHttpRequest.DONE && this.status == 202) {
            student_refresh_A()
        }
    }
    refreshLoader(xhttp)
    xhttp.open("DELETE", "/api/" + getCookie("username") + "/student/", true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("Content-type", "application/json;charset=UTF-8");
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.send(JSON.stringify(JSON_array));

}

function admin_student_put() {
    var jsonarray = {}
    var modal = document.getElementById("admin_student_details_put").firstElementChild
    while (modal) {
        if (modal.placeholder)
            jsonarray[modal.placeholder] = (modal.value == "null") ? null : (modal.value == "" ? null : modal.value)
        modal = modal.nextElementSibling
    }
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == XMLHttpRequest.DONE) {
            if (this.status == 202) {
                var svg_tick = '<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-check-circle-fill" fill="green" xmlns="http://www.w3.org/2000/svg">'
                svg_tick += '<path fill-rule="evenodd" d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>'
                svg_tick += '</svg>'
                document.getElementById('student_put_svg_A').innerHTML = svg_tick
                var str = this.responseText
                d = JSON.parse(str)
                str = "<b>" + d["detail"] + "</b>"
                if (d["assumption"])
                    for (let i = 0; i < d["assumption"].length; ++i) {
                        str += "<br>" + d["assumption"][i]["detail"] + "<br>"
                    }
                document.getElementById('student_put_toast_admin_header').innerHTML = 'SUCCESS'
                document.getElementById('student_put_toast_admin_body').innerHTML = str
                $('#student_put_toast_admin').toast('show');
                student_refresh_A()
            }
            else {
                var svg_cross = '<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-x-circle-fill" fill="red" xmlns="http://www.w3.org/2000/svg">'
                svg_cross += '<path fill-rule="evenodd" d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-4.146-3.146a.5.5 0 0 0-.708-.708L8 7.293 4.854 4.146a.5.5 0 1 0-.708.708L7.293 8l-3.147 3.146a.5.5 0 0 0 .708.708L8 8.707l3.146 3.147a.5.5 0 0 0 .708-.708L8.707 8l3.147-3.146z"/>'
                svg_cross += '</svg>'
                document.getElementById('student_put_svg_A').innerHTML = svg_cross
                var str = JSON.stringify(JSON.parse(this.responseText), null, 4);
                d = JSON.parse(str)
                str = ''
                for (let i = 0; i < d.length; ++i) {
                    if (typeof (d[i]["detail"]) == "string")
                        str += "<br>" + d[i]["detail"] + "<br>"
                    else {
                        let k = Object.keys(d[i]["detail"])
                        for (let j = 0; j < k.length; ++j)
                            str += "<br>" + k[j] + ":" + d[i]["detail"][k[j]] + "<br>"
                    }
                }
                document.getElementById('student_put_toast_admin_header').innerHTML = 'FAILURE'
                document.getElementById('student_put_toast_admin_body').innerHTML = str
                $('#student_put_toast_admin').toast('show');
            }
        }
    }
    refreshLoader(xhttp)
    xhttp.open("PUT", "/api/" + getCookie("username") + "/student/", true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("Content-type", "application/json;charset=UTF-8");
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.send(JSON.stringify([jsonarray]));
}

function admin_student_put_form(arg) {
    var head = arg.parentNode.parentNode.children
    var modal = document.getElementById("admin_student_details_put").children
    document.getElementById("response_admin_student_put").innerHTML = ""
    modal[1].value = head[1].innerHTML
    modal[3].value = head[2].innerHTML
    modal[5].value = head[3].innerHTML
    modal[7].value = head[4].innerHTML
    modal[11].value = head[5].innerHTML
    modal[13].value = head[6].innerHTML
    modal[9].value = head[7].innerHTML
}

function insert_dept_options_A(ele_id) {
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == XMLHttpRequest.DONE && this.status == 200) {
            let data = JSON.parse(this.responseText)
            deptSelect = document.getElementById(ele_id);
            let str = ""
            str += `<option selected="selected" disabled="disabled" class="form-control">Department</option>`
            for (let i = 0; i < data.length; i++) {
                str += `<option value="${data[i]['dept']}">${data[i]['dept']}</option>`
            }
            document.getElementById(ele_id).innerHTML = ""
            document.getElementById(ele_id).innerHTML += str
        }
    }
    xhttp.open("GET", "/api/" + getCookie("username") + "/department", true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("Content-type", "application/json;charset=UTF-8");
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.send()
}

function student_post_Admin() {
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == XMLHttpRequest.DONE) {
            if (this.status == 201) {
                let data = JSON.parse(this.responseText)
                var svg_tick = '<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-check-circle-fill" fill="green" xmlns="http://www.w3.org/2000/svg">'
                svg_tick += '<path fill-rule="evenodd" d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>'
                svg_tick += '</svg>'
                document.getElementById('student_post_svg_A').innerHTML = svg_tick
                var str = JSON.stringify(JSON.parse(this.responseText), null, 4);
                d = JSON.parse(str)
                str = "<b>" + d["detail"] + "</b>"
                if (d["assumption"])
                    for (let i = 0; i < d["assumption"].length; ++i) {
                        str += "<br>" + d["assumption"][i]["detail"] + "<br>"
                    }
                document.getElementById('student_post_toast_admin_header').innerHTML = 'SUCCESS'
                document.getElementById('student_post_toast_admin_body').innerHTML = str
                $('#student_post_toast_admin').toast('show');
                x = document.forms["stupost_A"].firstElementChild
                while (x) {
                    x.value = null
                    x = x.nextElementSibling
                }
                insert_dept_options_A('dept-stu_post_A')
                student_refresh_A()
            }
            else {
                var svg_cross = '<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-x-circle-fill" fill="red" xmlns="http://www.w3.org/2000/svg">'
                svg_cross += '<path fill-rule="evenodd" d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-4.146-3.146a.5.5 0 0 0-.708-.708L8 7.293 4.854 4.146a.5.5 0 1 0-.708.708L7.293 8l-3.147 3.146a.5.5 0 0 0 .708.708L8 8.707l3.146 3.147a.5.5 0 0 0 .708-.708L8.707 8l3.147-3.146z"/>'
                svg_cross += '</svg>'
                document.getElementById('student_post_svg_A').innerHTML = svg_cross
                var str = JSON.stringify(JSON.parse(this.responseText), null, 4);
                d = JSON.parse(str)
                str = ''
                for (let i = 0; i < d.length; ++i) {
                    if (typeof (d[i]["detail"]) == "string")
                        str += "<br>" + d[i]["detail"] + "<br>"
                    else {
                        let k = Object.keys(d[i]["detail"])
                        for (let j = 0; j < k.length; ++j)
                            str += "<br>" + k[j] + ":" + d[i]["detail"][k[j]] + "<br>"
                    }
                }
                document.getElementById('student_post_toast_admin_header').innerHTML = 'FAILURE'
                document.getElementById('student_post_toast_admin_body').innerHTML = str
                $('#student_post_toast_admin').toast('show');
            }
        }
    }
    var jsonarray = {}
    let arr = document.forms["stupost_A"].firstElementChild
    while (arr) {
        if (arr.type != "checkbox" && arr.value)
            jsonarray[(arr.id).slice(0, arr.id.indexOf("-"))] = (arr.value == "null") ? null : (arr.value == "" ? null : arr.value)
        else if (arr.type == "checkbox")
            jsonarray[(arr.id).slice(0, arr.id.indexOf("-"))] = arr.checked
        arr = arr.nextElementSibling
    }
    refreshLoader(xhttp)
    xhttp.open("POST", "/api/" + getCookie("username") + "/student/", true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("Content-type", "application/json;charset=UTF-8");
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.send(JSON.stringify([jsonarray]));
}

function pass_button_launch_A() {
    var checkedBoxes = getCheckedBoxes_A("student_boxes_A")
    if (checkedBoxes.length > 0) {
        $('#pass-modal').modal('show')
    }
}

function student_password_gen(type) {
    var checkedBoxes = getCheckedBoxes_A("student_boxes_A")
    let obj = { "srns": [], "password": document.getElementById("student_pwgen_pass_A").value, "type":type }
    document.getElementById("student_pwgen_pass_A").value = ''
    for (let i = 0; i < checkedBoxes.length; i++) {
        obj["srns"].push(checkedBoxes[i].parentElement.parentElement.firstElementChild.nextElementSibling.innerHTML)
    }
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (type=='json' && xhttp.readyState == XMLHttpRequest.DONE && xhttp.status == 200) {
            let mainstr = ["SRN", "Name", "E-Mail","Password"].join(",")+',\n'
            let res = JSON.parse(this.responseText)
            for (let i=0;i<Object.keys(res).length;i++) {
                mainstr+=Object.keys(res)[i]+','+res[Object.keys(res)[i]]["name"]+','+res[Object.keys(res)[i]]["email"]+','+res[Object.keys(res)[i]]["password"]+',\n'
            }
            download_pwgen("student_passwords.csv", mainstr);
            $('#pass-modal').modal('hide')
        }
    }
    refreshLoader(xhttp)
    xhttp.open("POST", "/api/" + getCookie("username") + "/password-generate/", true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("Content-type", "application/json;charset=UTF-8");
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.send(JSON.stringify(obj))
}

function download_pwgen(filename, text) {
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/csv;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', filename);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}

admin_refresh = function () {
    var a = 10
}