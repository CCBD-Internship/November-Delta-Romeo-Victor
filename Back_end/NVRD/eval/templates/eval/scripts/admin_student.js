function student_refresh() {
    insert_dept_options()
    tbody = document.getElementById("student_body")
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            let data = JSON.parse(this.responseText)
            var str = ''
            for (let i in data) {
                str += '<tr><td><input name=\"boxes\" class=\"form-check-input position-static\" type=\"checkbox\"></input></td>'
                for (let j in data[i]) {
                    str += ("<td>" + data[i][j] + "</td>")
                }
                str += '<td scope="col"><button type="button" class="btn btn-info btn" data-toggle="modal" data-target="#myModal" onclick="open_put_form(this)">Edit</button></td></tr>'
            }
            document.getElementById("student_body").innerHTML = str
        }
    }
    xhttp.open("GET", "/api/" + '7474' + "/student/", true);
    xhttp.setRequestHeader("Authorization", "Bearer " + token);
    xhttp.send();
}

function getCheckedBoxes(chkboxName) {
    var checkboxes = document.getElementsByName(chkboxName);
    var checkboxesChecked = [];
    for (var i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked) {
            checkboxesChecked.push(checkboxes[i]);
        }
    }
    return checkboxesChecked.length > 0 ? checkboxesChecked : null;
}

function student_delete() {
    tbody = document.getElementById("student_body")
    var checkedBoxes = getCheckedBoxes("boxes");
    if (checkedBoxes.length > 0) {
        a = []
        for (i = 0; i < checkedBoxes.length; i++) { a.push(checkedBoxes[i].parentElement.parentElement.innerHTML.split("<td>")[2].split('</td>')[0]) }
        var modal = $("#A_Student_DeleteconfirmModal");
        modal.modal("show");
        $("#A_Student_DeleteconfirmMessage").empty().append("Do you want to delete " + a.length + " students");
        $('#A_Student_DeleteconfirmOk')
            .on('click', function (e) {
                e.preventDefault();
                console.log(a);
                send_delete(a);
                $('#A_Student_DeleteconfirmModal').modal('hide');
            });
        $("#A_Student_DeleteconfirmCancel").on('click', function (e) {
            e.preventDefault();
            $('#A_Student_DeleteconfirmModal').modal('hide');
        });
    }
}

function send_delete(students) {
    var JSON_array = []
    for (let i = 0; i < students.length; ++i)
        JSON_array.push({ "srn": students[i] })
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 202) {
            student_refresh()
        }
    }
    xhttp.open("DELETE", "/api/" + '7474' + "/student/", true);
    xhttp.setRequestHeader("Authorization", "Bearer " + token);
    xhttp.setRequestHeader("Content-type", "application/json;charset=UTF-8");
    xhttp.send(JSON.stringify(JSON_array));

}

function student_put() {
    var jsonarray = {}
    var modal = document.getElementById("details_put").firstElementChild
    while (modal) {
        if (modal.placeholder)
            jsonarray[modal.placeholder] = modal.value
        else if (modal.id)
            jsonarray[modal.id] = modal.value
        modal = modal.nextElementSibling
    }
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 202) {
            let data = JSON.parse(this.responseText)
            var message = ''
            for (let i in data) {
                message += "<b>" + " " + data[i] + "<br />" + "<\b>"
            }
            document.getElementById("A_student_put_response").innerHTML = message
        }
    }
    xhttp.open("PUT", "/api/" + '7474' + "/student/", true);
    xhttp.setRequestHeader("Content-type", "application/json;charset=UTF-8");
    xhttp.setRequestHeader("Authorization", "Bearer " + token);
    xhttp.send(JSON.stringify([jsonarray]));

}

function open_put_form(arg) {
    var head = arg.parentNode.parentNode.firstElementChild.nextElementSibling
    var modal = document.getElementById("details_put").firstElementChild
    while (head) {
        if (!head.scope && modal) {
            modal.value = head.innerHTML
            modal = modal.nextElementSibling
        }
        head = head.nextElementSibling
    }
    dept_get()
}

function dept_get() {
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            let data = JSON.parse(this.responseText), str = ""
            for (let i = 0; i < data.length; i++) {
                str += `<option value="${data[i]['dept']}">${data[i]['dept']}</option>`
            }
            document.getElementById("dept").innerHTML = ""
            document.getElementById("dept").innerHTML += str
        }
    }
    xhttp.open("GET", "/api/7474/department/", true);
    xhttp.send()
}

function insert_dept_options() {
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            let data = JSON.parse(this.responseText)
            deptSelect = document.getElementById('dept-stu_post');
            for (let i = 0; i < data.length; i++)
                deptSelect.options[deptSelect.options.length] = new Option(data[i].dept, data[i].dept);
        }
    }
    xhttp.open("GET", "/api/" + 7474 + "/department", true);
    xhttp.send()
}

function student_post() {
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 201) {
            let data = JSON.parse(this.responseText)
            document.getElementById("stumsg-post").innerHTML = "<strong>details</strong>: " + data["detail"]
        }
    }
    var jsonarray = {}
    let arr = document.forms["stupost"].firstElementChild
    while (arr) {
        console.log(arr.value)
        if (arr.type != "checkbox" && arr.value)
            jsonarray[(arr.id).slice(0, arr.id.indexOf("-"))] = arr.value
        else if (arr.type == "checkbox")
            jsonarray[(arr.id).slice(0, arr.id.indexOf("-"))] = arr.checked
        arr = arr.nextElementSibling
    }
    xhttp.open("POST", "/api/" + 7474 + "/student/", true);
    xhttp.setRequestHeader("Authorization", "Bearer " + token);
    xhttp.setRequestHeader("Content-type", "application/json;charset=UTF-8");
    xhttp.send(JSON.stringify([jsonarray]));
}