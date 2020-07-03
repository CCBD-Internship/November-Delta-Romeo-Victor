function cardMaker(panel_year_code, panel_id, panel_name, is_active, ctime) {
    var color
    if (is_active)
        color = 'bg-info'
    else
        color = 'bg-secondary'
    str = '<div class="col mb-4"><div onclick="openmodal(event,this)" class="card ' + color + ' onclick="crumbPusher()"><div class="card-header">' + panel_year_code + '   ' + panel_id + '    </div><div class="card-body"><h5 class="card-title">' + panel_name + '</h5><p>  ' + Date(ctime) + '</p></div></div></div>'
    return str
}

function A_fac_panel_get(p_year_code, p_id) {
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            let data = JSON.parse(this.responseText)
            var str = ''
            var svgstr = '<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-pencil" fill="currentColor" xmlns="http://www.w3.org/2000/svg">'
            svgstr += '<path fill-rule="evenodd" d="M11.293 1.293a1 1 0 0 1 1.414 0l2 2a1 1 0 0 1 0 1.414l-9 9a1 1 0 0 1-.39.242l-3 1a1 1 0 0 1-1.266-1.265l1-3a1 1 0 0 1 .242-.391l9-9zM12 2l2 2-9 9-3 1 1-3 9-9z"/>'
            svgstr += '<path fill-rule="evenodd" d="M12.146 6.354l-2.5-2.5.708-.708 2.5 2.5-.707.708zM3 10v.5a.5.5 0 0 0 .5.5H4v.5a.5.5 0 0 0 .5.5H5v.5a.5.5 0 0 0 .5.5H6v-1.5a.5.5 0 0 0-.5-.5H5v-.5a.5.5 0 0 0-.5-.5H3z"/>'
            svgstr += '</svg>'
            for (let i in data) {
                str += '<tr><td scope="row" style="text-align:right"><input name="fac_panel_boxes_A" class="form-check-input position-static" type="checkbox"></input></td>'
                for (let j of ["fac_id", "name", "email", "phone", "is_coordinator"])
                    str += ("<td>" + data[i][j] + "</td>")
                str += '<td scope="col"><button type="button" class="btn btn-dark active btn" data-toggle="modal" data-target="#admin_faculty_panel_put" onclick="admin_faculty_panel_put_form(this)">' + svgstr + '</button></td></tr>'
            }
            document.getElementById("faculty_panel_body_A").innerHTML = str
        }
    }
    var url = "/api/" + getCookie("username") + "/faculty-panel/?panel_id=" + p_id + "&panel_year_code=" + p_year_code;
    refreshLoader(xhttp)
    xhttp.open("GET", url, true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.send();
}

function openmodal(e, t) {
    var p_year_code = t.textContent.split(' ')[0]
    var p_id = t.textContent.split(' ')[3]
    document.getElementById("Faculty_panel_modal").innerHTML = "<h3>" + p_year_code + " " + p_id + "</h3>"
    var m = $("#A_fac_pan_modal")
    m.modal("show");
    A_fac_panel_get(p_year_code, p_id)
}

function admin_faculty_panel_refresh() {
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            let data = JSON.parse(this.responseText)
            var str = '<div class="row row-cols-1 row-cols-md-3" id="panelcardchild">'
            for (let i in data) {
                str += cardMaker(data[i]["panel_year_code"], data[i]["panel_id"], data[i]["panel_name"], data[i]["is_active"], data[i]["ctime"])
            }
            document.getElementById("NVRD_fac_panel_card").innerHTML = str
        }
    }
    refreshLoader(xhttp)
    xhttp.open("GET", "/api/" + getCookie("username") + "/panel/", true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.send();

}

admin_refresh = admin_faculty_panel_refresh

function Addfacpanel_A() {
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            let data = JSON.parse(this.responseText)
            var str = ""
            for (let i of data) {
                str += "<option value='" + i["fac_id"] + "'>" + i["name"] + "</option>"
            }
            document.getElementById("faclist-facpanel_A").innerHTML = str
        }
    }
    refreshLoader(xhttp)
    xhttp.open("GET", "/api/" + getCookie("username") + "/faculty/?inactive=1", true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.send();
}

function facpanel_post_Admin(e, t) {
    var pyc = document.getElementById("Faculty_panel_modal").firstElementChild.innerHTML.split(' ')[0]
    var pid = document.getElementById("Faculty_panel_modal").firstElementChild.innerHTML.split(' ')[1]
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 201) {
            let data = JSON.parse(this.responseText)
            A_fac_panel_get(pyc, pid)
            Addfacpanel_A()
        }
    }
    var iscord = document.getElementById("isfac_activeforpanel").checked
    var jsonarray = { "panel_year_code": pyc, "panel_id": pid, "fac_id": $("#faclist-facpanel_A").val(), "is_coordinator": iscord }
    refreshLoader(xhttp)
    xhttp.open("POST", "/api/" + getCookie("username") + "/faculty-panel/", true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("Content-type", "application/json;charset UTF-8");
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.send(JSON.stringify([jsonarray]));

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
    var checkboxes = document.getElementsByName("fac_panel_boxes_A");
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

function fac_panel_delete_A() {
    var checkedBoxes = getCheckedBoxes_A("fac_panel_boxes_A");
    if (checkedBoxes.length > 0) {
        a = []
        var pyc = document.getElementById("Faculty_panel_modal").firstElementChild.innerHTML.split(' ')[0]
        var pid = document.getElementById("Faculty_panel_modal").firstElementChild.innerHTML.split(' ')[1]
        for (i = 0; i < checkedBoxes.length; i++) {
            a.push({ "panel_year_code": pyc, "panel_id": pid, "fac_id": checkedBoxes[i].parentElement.parentElement.children[1].textContent })
        }
        var modal = $("#A_fac_panel_DeleteconfirmModal");
        modal.modal("show");
        $("#A_fac_panel_DeleteconfirmMessage").empty().append("Do you want to delete " + a.length + " Faculty from this panel?");
        $('#A_fac_panel_DeleteconfirmOk')
            .on('click', function (e) {
                e.preventDefault();
                fac_panel_send_delete_A(a);
                $('#A_fac_panel_DeleteconfirmModal').modal('hide');
            });
        $("#A_fac_panel_DeleteconfirmCancel").on('click', function (e) {
            e.preventDefault();
            $('#A_fac_panel_DeleteconfirmModal').modal('hide');
        });
    }
}

function fac_panel_send_delete_A(fac) {
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 201) {
            A_fac_panel_get(fac[0]["panel_year_code"], fac[0]["panel_id"])
        }
    }
    refreshLoader(xhttp)
    xhttp.open("DELETE", "/api/" + getCookie("username") + "/faculty-panel/", true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("Content-type", "application/json;charset=UTF-8");
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.send(JSON.stringify(fac));

}

function admin_faculty_panel_put_form(t) {
    var if_checked = document.getElementById("isfac_activeforpanel_put")
    var head = t.parentNode.parentNode.children
    var modal = document.getElementById("admin_faculty_panel_details_put").children
    if_checked.checked = head[5].textContent == "true"
    var fac = document.getElementById("fac_panel_put_A")
    fac.textContent = "Edit Co-ordinator " + head[1].textContent
}

function admin_faculty_panel_put() {
    var pyc = document.getElementById("Faculty_panel_modal").firstElementChild.innerHTML.split(' ')[0]
    var pid = document.getElementById("Faculty_panel_modal").firstElementChild.innerHTML.split(' ')[1]
    var fac = document.getElementById("fac_panel_put_A").textContent.split(' ')[2]
    var jsonarray = { "panel_year_code": pyc, "panel_id": pid, "is_coordinator": document.getElementById("isfac_activeforpanel_put").checked, "fac_id": fac }
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 201) {
            A_fac_panel_get(pyc, pid)
        }
    }
    refreshLoader(xhttp)
    xhttp.open("PUT", "/api/" + getCookie("username") + "/faculty-panel/", true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("Content-type", "application/json;charset=UTF-8");
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.send(JSON.stringify([jsonarray]));
}