function admin_panel_refresh() {
    tbody = document.getElementById("admin_panel_container")
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
                str += '<tr><td scope="row" style="text-align:right"><input name="panel_boxes_A" class="form-check-input position-static" type="checkbox"></input></td>'
                for (let j in data[i]) {
                    if (j == "ctime") {
                        let date = new Date(data[i][j])
                        str += ("<td>" + date.toLocaleString() + "</td>")
                    }
                    else if (j == "is_active")
                        str += ("<td>" + (data[i][j] ? 'Yes' : 'No') + "</td>")
                    else if (j == "id")
                        continue
                    else
                        str += ("<td>" + data[i][j] + "</td>")
                }
                str += '<td scope="col"><button type="button" class="btn btn-dark active btn" data-toggle="modal" data-target="#admin_panel_put" onclick="admin_panel_put_form(this)">' + svgstr + '</button></td></tr>'
            }
            document.getElementById("admin_panel_container").innerHTML = str
            checkerInit("admin_panels_allcheckboxes","panel_boxes_A")
        }
    }
    refreshLoader(xhttp)
    xhttp.open("GET", "/api/" + getCookie("username") + "/panel/", true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.send();
}
admin_refresh=admin_panel_refresh

function search_panels_A() {
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
                str += '<tr><td scope="row" style="text-align:right"><input name="panel_boxes_A" class="form-check-input position-static" type="checkbox"></input></td>'
                for (let j in data[i]) {
                    if (j == "ctime") {
                        let date = new Date(data[i][j])
                        str += ("<td>" + date.toLocaleString() + "</td>")
                    }
                    else if (j == "is_active")
                        str += ("<td>" + (data[i][j] ? 'Yes' : 'No') + "</td>")
                    else if (j == "id")
                        continue
                    else
                        str += ("<td>" + data[i][j] + "</td>")
                }
                str += '<td scope="col"><button type="button" class="btn btn-dark active btn" data-toggle="modal" data-target="#admin_panel_put" onclick="admin_panel_put_form(this)">' + svgstr + '</button></td></tr>'
            }
            document.getElementById("admin_panel_container").innerHTML = str
            checkerInit("admin_panels_allcheckboxes","panel_boxes_A")
        }
    }
    refreshLoader(xhttp)
    var panelid = document.getElementById("panel_search_panelid_A").value
    var panelyearcode = document.getElementById("panel_search_panelyearcode_A").value
    var isactive = document.getElementById("panel_active").checked.toString()
    var str = "/api/" + getCookie("username") + "/panel/", url = ""
    if (panelyearcode)
        url += "?panel_year_code=" + panelyearcode
    if (panelid)
        if (url)
            url += "&panel_id=" + panelid
        else
            url += "?panel_id=" + panelid
    if (url)
        url += "&active=" + isactive[0].toUpperCase() + isactive.slice(1,)
    else
        url += "?active=" + isactive[0].toUpperCase() + isactive.slice(1,)
    str += url
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
    var checkboxes = document.getElementsByName("panel_boxes_A");
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

function panel_delete_A() {
    var checkedBoxes = getCheckedBoxes_A("panel_boxes_A");
    if (checkedBoxes && checkedBoxes.length > 0) {
        a = []
        for (i = 0; i < checkedBoxes.length; i++) {
            let arr = checkedBoxes[i].parentNode, temp = []
            while (arr) {
                if (arr.textContent)
                    temp.push(arr.textContent)
                arr = arr.nextElementSibling
            }
            a.push({ "panel_year_code": temp[0], "panel_id": temp[1] })
        }
        var modal = $("#A_panel_DeleteconfirmModal");
        modal.modal("show");
        $("#A_panel_DeleteconfirmMessage").empty().append("Do you want to delete " + a.length + " students");
        $('#A_panel_DeleteconfirmOk')
            .on('click', function (e) {
                e.preventDefault();
                sendpanel_delete_A(a);
                $('#A_panel_DeleteconfirmModal').modal('hide');
            });
        $("#A_panel_DeleteconfirmCancel").on('click', function (e) {
            e.preventDefault();
            $('#A_panel_DeleteconfirmModal').modal('hide');
        });
    }
}

function sendpanel_delete_A(panels) {
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 202)
            admin_panel_refresh()
    }
    refreshLoader(xhttp)
    xhttp.open("DELETE", "/api/" + getCookie("username") + "/panel/", true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("Content-type", "application/json;charset=UTF-8");
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.send(JSON.stringify(panels));
}

function admin_panel_put_form(arg) {
    var head = arg.parentNode.parentNode.firstElementChild.nextElementSibling
    var dest = document.getElementById("admin_panel_putform").firstElementChild
    var arr = []
    while (head) {
        if (head.textContent)
            arr.push(head.textContent)
        head = head.nextElementSibling
    }
    while (dest) {
        if (dest.placeholder) {
            dest.value = arr.shift()
        }
        else if (dest.type == "checkbox") {
            dest.checked = (arr.shift()) ? true : false
        }
        dest = dest.nextElementSibling
    }
}

function admin_panel_put() {
    var data = document.getElementById("admin_panel_putform").firstElementChild
    var jsonarray = {}
    while (data) {
        if (data.placeholder && data.placeholder != "ctime" && data.placeholder != "id")
            jsonarray[data.placeholder] = data.value
        else if (data.type == "checkbox")
            jsonarray["is_active"] = data.checked
        data = data.nextElementSibling
    }
    jsonarray["panel_name"] = (jsonarray["panel_name"]) ? jsonarray["panel_name"] : null
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 202) {
            let d = JSON.parse(this.responseText)
            var svg_tick = '<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-check-circle-fill" fill="green" xmlns="http://www.w3.org/2000/svg">'
            svg_tick += '<path fill-rule="evenodd" d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>'
            svg_tick += '</svg>'
            document.getElementById('panel_put_svg_A').innerHTML = svg_tick
            var str = "<b>" + d["detail"] + "</b>"
            if (d["assumption"])
                for (let i = 0; i < d["assumption"].length; ++i) {
                    str += "<br>" + d["assumption"][i]["detail"] + "<br>"
                }
            document.getElementById('panel_put_toast_admin_header').innerHTML = 'SUCCESS'
            document.getElementById('panel_put_toast_admin_body').innerHTML = str
            $('#panel_put_toast_admin').toast('show');
            admin_panel_refresh()
        }
    }
    xhttp.open("PUT", "/api/" + getCookie("username") + "/panel/", true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("Content-type", "application/json;charset=UTF-8");
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.send(JSON.stringify([jsonarray]))
}
function admin_panel_post() {
    var data = document.getElementById("admin_student_details_post").firstElementChild
    var temparray = {}
    while (data) {
        if (data.placeholder)
            temparray[data.placeholder] = data.value
        data = data.nextElementSibling
    }
    var arr = []
    if (temparray["number_of_panels"] > 10 || !temparray["number_of_panels"])
        return
    for (let i = 0; i < temparray["number_of_panels"]; i++)
        arr.push({ "panel_year_code": temparray["panel_year_code"] })
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 201) {
            let d = JSON.parse(this.responseText)
            var svg_tick = '<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-check-circle-fill" fill="green" xmlns="http://www.w3.org/2000/svg">'
            svg_tick += '<path fill-rule="evenodd" d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>'
            svg_tick += '</svg>'
            document.getElementById('panel_post_svg_A').innerHTML = svg_tick
            var str = "<b>" + d["detail"] + "</b>"
            if (d["assumption"])
                for (let i = 0; i < d["assumption"].length; ++i) {
                    str += "<br>" + d["assumption"][i]["detail"] + "<br>"
                }
            document.getElementById('panel_post_toast_admin_header').innerHTML = 'SUCCESS'
            document.getElementById('panel_post_toast_admin_body').innerHTML = str
            $('#panel_post_toast_admin').toast('show');
            admin_panel_refresh()
        }
        else if (this.readyState == 4) {
            var svg_cross = '<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-x-circle-fill" fill="red" xmlns="http://www.w3.org/2000/svg">'
            svg_cross += '<path fill-rule="evenodd" d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-4.146-3.146a.5.5 0 0 0-.708-.708L8 7.293 4.854 4.146a.5.5 0 1 0-.708.708L7.293 8l-3.147 3.146a.5.5 0 0 0 .708.708L8 8.707l3.146 3.147a.5.5 0 0 0 .708-.708L8.707 8l3.147-3.146z"/>'
            svg_cross += '</svg>'
            document.getElementById('panel_post_svg_A').innerHTML = svg_cross
            d = JSON.parse(this.responseText)
            var str = ''
            for (let i = 0; i < d.length; ++i) {
                if (typeof (d[i]["detail"]) == "string")
                    str += "<br>" + d[i]["detail"] + "<br>"
                else {
                    let k = Object.keys(d[i]["detail"])
                    for (let j = 0; j < k.length; ++j)
                        str += "<br>" + k[j] + ":" + d[i]["detail"][k[j]] + "<br>"
                }
            }
            document.getElementById('panel_post_toast_admin_header').innerHTML = 'FAILURE'
            document.getElementById('panel_post_toast_admin_body').innerHTML = str
            $('#panel_post_toast_admin').toast('show');
        }
    }
    xhttp.open("POST", "/api/" + getCookie("username") + "/panel/", true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("Content-type", "application/json;charset=UTF-8");
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.send(JSON.stringify(arr))
}