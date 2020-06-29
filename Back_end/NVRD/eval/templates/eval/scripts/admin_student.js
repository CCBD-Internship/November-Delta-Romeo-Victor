function student_refresh_A() {
    tbody = document.getElementById("student_body")
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            let data = JSON.parse(this.responseText)
            var str = ''
            var svgstr='<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-pencil" fill="currentColor" xmlns="http://www.w3.org/2000/svg">'
            svgstr+='<path fill-rule="evenodd" d="M11.293 1.293a1 1 0 0 1 1.414 0l2 2a1 1 0 0 1 0 1.414l-9 9a1 1 0 0 1-.39.242l-3 1a1 1 0 0 1-1.266-1.265l1-3a1 1 0 0 1 .242-.391l9-9zM12 2l2 2-9 9-3 1 1-3 9-9z"/>'
            svgstr+='<path fill-rule="evenodd" d="M12.146 6.354l-2.5-2.5.708-.708 2.5 2.5-.707.708zM3 10v.5a.5.5 0 0 0 .5.5H4v.5a.5.5 0 0 0 .5.5H5v.5a.5.5 0 0 0 .5.5H6v-1.5a.5.5 0 0 0-.5-.5H5v-.5a.5.5 0 0 0-.5-.5H3z"/>'
            svgstr+='</svg>'
            for (let i in data) {
                str += '<tr><td scope="row" style="text-align:right"><input name="student_boxes_A" class="form-check-input position-static" type="checkbox"></input></td>'
                for (let j in data[i]) {
                    str += ("<td>" + data[i][j] + "</td>")
                }
                str += '<td scope="col"><button type="button" class="btn btn-dark active btn" data-toggle="modal" data-target="#modal_admin_student_put" onclick="admin_student_put_form(this)">'+svgstr+'</button></td></tr>'
            }
            document.getElementById("student_body_A").innerHTML = str
        }
    }
    refreshLoader(xhttp)
    xhttp.open("GET", "/api/" + getCookie("username") + "/student/", true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.send();
}

function student_search_A() {
    tbody = document.getElementById("student_body")
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            let data = JSON.parse(this.responseText)
            var str = ''
            for (let i in data) {
                str += '<tr><td scope="row" style="text-align:right"><input name="boxes" class="form-check-input position-static" type="checkbox"></input></td>'
                for (let j in data[i]) {
                    str += ("<td>" + data[i][j] + "</td>")
                }
                str += '<td scope="col"><button type="button" class="btn btn-info btn" data-toggle="modal" data-target="#modal_admin_student_put" onclick="admin_student_put_form(this)">Edit</button></td></tr>'
            }
            document.getElementById("student_body_A").innerHTML = str
        }
    }
    refreshLoader(xhttp)
    var srn = document.getElementById("student_search_srn_A").value
    var name = document.getElementById("student_search_name_A").value
    var str = "/api/" + getCookie("username") + "/student/"
    if (name != "" || srn != "") {
        str += '?'
        if (name != "") {
            str += ("name=" + name)
        }
        if (srn != "") {
            str += ("srn=" + srn)
        }
    }
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

function setCheckedBoxes_A(e) {
    var checkboxes = document.getElementsByName("student_boxes_A");
    if (e.target.checked) {
        for (var i = 0; i < checkboxes.length; i++) {
            checkboxes[i].checked = true
        }
    }
    else {
        for (var i = 0; i < checkboxes.length; i++) {
            checkboxes[i].checked = false
        }
    }
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
                console.log(a);
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
        if (this.readyState == 4 && this.status == 202) {
            student_refresh_A()
        }
        else {
            console.log(JSON_array)
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
        if (this.readyState == 4 && this.status == 202) {
            let data = JSON.parse(this.responseText)
            var message = ''
            if (data["detail"] == "update successful")
                message = "<b>Saved Successfully<b><br/>"
            else if (data["value"] != undefined)
                message = "<b>Error For " + data["value"] + "<b>&emsp;" + data["detail"] + "<br/>"
            else
                message = "<b>Error " + data["detail"] + "<b><br/>"
            document.getElementById("response_admin_student_put").innerHTML = message
            student_refresh_A()
        }
        else {
            console.log(JSON.stringify([jsonarray]))
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
    insert_dept_options_A("dept")
}

function insert_dept_options_A(ele_id) {
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            let data = JSON.parse(this.responseText)
            console.log(data)
            deptSelect = document.getElementById(ele_id);
            let str = ""
            str += `<option selected="selected" disabled="disabled" class="form-control">Department</option>`
            for (let i = 0; i < data.length; i++) {
                str += `<option value="${data[i]['dept']}">${data[i]['dept']}</option>`
            }
            document.getElementById(ele_id).innerHTML = ""
            document.getElementById(ele_id).innerHTML += str

            /*for(let i=0;i<data.length;i++)
              deptSelect.options[deptSelect.options.length] = new Option(data[i].dept,data[i].dept);
            */
        }
    }
    xhttp.open("GET", "/api/" + getCookie("username") + "/department", true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("Content-type", "application/json;charset=UTF-8");
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.send()
}

function student_post_Admin() {
    console.log("entry")
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 201) {
            let data = JSON.parse(this.responseText)
            document.getElementById("stumsg-post_A").innerHTML = "<strong>details</strong>: " + data["detail"]
        }
        x = document.forms["stupost_A"].firstElementChild
        while (x) {
            x.value = null
            x = x.nextElementSibling
        }
        insert_dept_options_A('dept-stu_post_A')
        student_refresh_A()
        document.getElementById('stumsg-post_A').style.color = "green"
        setTimeout(function () {
            $("#stumsg-post_A").fadeOut().empty();
        }, 1000);
    }
    var jsonarray = {}
    let arr = document.forms["stupost_A"].firstElementChild
    while (arr) {
        console.log(arr.value)
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

function admin_refresh()  {
    document.getElementById("student_boxes_main_A").addEventListener('click', setCheckedBoxes_A)
    student_refresh_A()
}