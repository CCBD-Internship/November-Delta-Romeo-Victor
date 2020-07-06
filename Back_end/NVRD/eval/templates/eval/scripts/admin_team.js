function team_refresh_A() {
    tbody = document.getElementById("team_body")
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
                str += '<tr><td scope="row" style="text-align:right"><input name="team_boxes_A" class="form-check-input position-static" type="checkbox"></input></td>'
                for (let j in data[i]) {
                    str += ("<td>" + data[i][j] + "</td>")
                }
                str += '<td scope="col"><button type="button" class="btn btn-dark active btn" data-toggle="modal" data-target="#modal_admin_team_put" onclick="admin_team_put_form(this)">' + svgstr + '</button></td></tr>'
            }
            document.getElementById("team_body_A").innerHTML = str
            checkerInit("team_boxes_main_A", "team_boxes_A")
        }
    }
    refreshLoader(xhttp)
    xhttp.open("GET", "/api/" + getCookie("username") + "/team/", true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.send();
}

function team_search_A() {
    tbody = document.getElementById("team_body")
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
                str += '<tr><td scope="row" style="text-align:right"><input name="team_boxes_A" class="form-check-input position-static" type="checkbox"></input></td>'
                for (let j in data[i]) {
                    str += ("<td>" + data[i][j] + "</td>")
                }
                str += '<td scope="col"><button type="button" class="btn btn-dark active btn" data-toggle="modal" data-target="#modal_admin_team_put" onclick="admin_team_put_form(this)">' + svgstr + '</button></td></tr>'
            }
            document.getElementById("team_body_A").innerHTML = str
            checkerInit("team_boxes_main_A", "team_boxes_A")
        }
    }
    refreshLoader(xhttp)
    var Team_year_code = document.getElementById("team_search_team_year_code_A").value
    var Team_id = document.getElementById("team_search_team_id_A").value
    var Team_name = document.getElementById("team_search_team_name_A").value
    var Panel_year_code = document.getElementById("team_search_panel_year_code_A").value
    var Panel_id = document.getElementById("team_search_panel_id_A").value
    var str = ""
    if (Team_year_code != "") {
        if (str == "")
            str += ("?team_year_code=" + Team_year_code)
        else
            str += ("&team_year_code=" + Team_year_code)
    }
    if (Team_id != "") {
        if (str == "")
            str += ("?team_id=" + Team_id)
        else
            str += ("&team_id=" + Team_id)
    }
    if (Team_name != "") {
        if (str == "")
            str += ("?team_name=" + Team_name)
        else
            str += ("&team_name=" + Team_name)
    }
    if (Panel_year_code != "") {
        if (str == "")
            str += ("?panel_year_code=" + Panel_year_code)
        else
            str += ("&panel_year_code=" + Panel_year_code)
    }
    if (Panel_id != "") {
        if (str == "")
            str += ("?panel_id=" + Panel_id)
        else
            str += ("&panel_id=" + Panel_id)
    }
    xhttp.open("GET", "/api/" + getCookie("username") + "/team/" + str, true);
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

function team_delete_A() {
    tbody = document.getElementById("team_body")
    var checkedBoxes = getCheckedBoxes_A("team_boxes_A");
    if (checkedBoxes.length > 0) {
        a = []
        console.log(a)
        for (i = 0; i < checkedBoxes.length; i++) {
            console.log(checkedBoxes[i].parentElement.parentElement.firstElementChild.nextElementSibling.innerHTML, checkedBoxes[i].parentElement.parentElement.firstElementChild.nextElementSibling.nextElementSibling.innerHTML)
            a.push({ "team_year_code": checkedBoxes[i].parentElement.parentElement.firstElementChild.nextElementSibling.innerHTML, "team_id": checkedBoxes[i].parentElement.parentElement.firstElementChild.nextElementSibling.nextElementSibling.innerHTML })
        }
        var modal = $("#A_team_DeleteconfirmModal");
        modal.modal("show");
        $("#A_team_DeleteconfirmMessage").empty().append("Do you want to delete " + a.length + " teams");
        $('#A_team_DeleteconfirmOk')
            .on('click', function (e) {
                e.preventDefault();
                console.log(a);
                send_delete_A(a);
                $('#A_team_DeleteconfirmModal').modal('hide');
            });
        $("#A_team_DeleteconfirmCancel").on('click', function (e) {
            e.preventDefault();
            $('#A_team_DeleteconfirmModal').modal('hide');
        });
    }
}

function send_delete_A(teams) {
    var JSON_array = []
    for (let i = 0; i < teams.length; ++i)
        JSON_array.push({ "team_year_code": teams[i]['team_year_code'], "team_id": teams[i]['team_id'] })
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 202) {
            team_refresh_A()
        }
        else {
            console.log(JSON_array)
        }
    }
    refreshLoader(xhttp)
    xhttp.open("DELETE", "/api/" + getCookie("username") + "/team/", true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("Content-type", "application/json;charset=UTF-8");
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.send(JSON.stringify(JSON_array));

}

function admin_team_put() {
    var jsonarray = {}
    var modal = document.getElementById("admin_team_details_put").firstElementChild
    while (modal) {
        if (modal.placeholder)
            jsonarray[modal.placeholder] = (modal.value == "null") ? null : (modal.value == "" ? null : modal.value)
        modal = modal.nextElementSibling
    }
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        console.log(this.status)
        if (this.readyState == 4 && this.status == 202) {
            var svg_tick = '<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-check-circle-fill" fill="green" xmlns="http://www.w3.org/2000/svg">'
            svg_tick += '<path fill-rule="evenodd" d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>'
            svg_tick += '</svg>'
            document.getElementById('team_put_svg_A').innerHTML = svg_tick
            var str = this.responseText
            d = JSON.parse(str)
            str = "<b>" + d["detail"] + "</b>"
            console.log(d["assumption"])
            if (d["assumption"])
                for (let i = 0; i < d["assumption"].length; ++i) {
                    console.log(d["assumption"][i])
                    str += "<br>" + d["assumption"][i]["detail"] + "<br>"
                }
            document.getElementById('team_put_toast_admin_header').innerHTML = 'SUCCESS'
            document.getElementById('team_put_toast_admin_body').innerHTML = str
            $('#team_put_toast_admin').toast('show');
            // var message = ''
            // if (data["detail"] == "update successful")
            //     message = "<b>Saved Successfully<b><br/>"
            // else if (data["value"] != undefined)
            //     message = "<b>Error For " + data["value"] + "<b>&emsp;" + data["detail"] + "<br/>"
            // else
            //     message = "<b>Error " + data["detail"] + "<b><br/>"
            // document.getElementById("response_admin_team_put").innerHTML = message
            team_refresh_A()
        }
        else {
            var svg_cross = '<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-x-circle-fill" fill="red" xmlns="http://www.w3.org/2000/svg">'
            svg_cross += '<path fill-rule="evenodd" d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-4.146-3.146a.5.5 0 0 0-.708-.708L8 7.293 4.854 4.146a.5.5 0 1 0-.708.708L7.293 8l-3.147 3.146a.5.5 0 0 0 .708.708L8 8.707l3.146 3.147a.5.5 0 0 0 .708-.708L8.707 8l3.147-3.146z"/>'
            svg_cross += '</svg>'
            document.getElementById('team_put_svg_A').innerHTML = svg_cross
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
            document.getElementById('team_put_toast_admin_header').innerHTML = 'FAILURE'
            document.getElementById('team_put_toast_admin_body').innerHTML = str
            $('#team_put_toast_admin').toast('show');
            console.log(JSON.stringify([jsonarray]))
        }
    }
    refreshLoader(xhttp)
    xhttp.open("PUT", "/api/" + getCookie("username") + "/team/", true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("Content-type", "application/json;charset=UTF-8");
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.send(JSON.stringify([jsonarray]));
}

function admin_team_put_form(arg) {
    var head = arg.parentNode.parentNode.children
    var modal = document.getElementById("admin_team_details_put").children
    document.getElementById("response_admin_team_put").innerHTML = ""
    modal[1].value = head[1].innerHTML
    modal[3].value = head[2].innerHTML
    modal[5].value = head[3].innerHTML
    modal[7].value = head[4].innerHTML
    modal[9].value = head[5].innerHTML
    modal[11].value = head[6].innerHTML
    modal[13].value = head[7].innerHTML
}


function team_post_Admin() {
    console.log("entry")
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 202) {
            let data = JSON.parse(this.responseText)
            var svg_tick = '<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-check-circle-fill" fill="green" xmlns="http://www.w3.org/2000/svg">'
            svg_tick += '<path fill-rule="evenodd" d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>'
            svg_tick += '</svg>'
            document.getElementById('team_post_svg_A').innerHTML = svg_tick
            var str = JSON.stringify(JSON.parse(this.responseText), null, 4);
            d = JSON.parse(str)
            str = "<b>" + d["detail"] + "</b>"
            console.log(d["assumption"])
            if (d["assumption"])
                for (let i = 0; i < d["assumption"].length; ++i) {
                    console.log(d["assumption"][i])
                    str += "<br>" + d["assumption"][i]["detail"] + "<br>"
                }
            document.getElementById('team_post_toast_admin_header').innerHTML = 'SUCCESS'
            document.getElementById('team_post_toast_admin_body').innerHTML = str
            $('#team_post_toast_admin').toast('show');
        }
        else {
            var svg_cross = '<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-x-circle-fill" fill="red" xmlns="http://www.w3.org/2000/svg">'
            svg_cross += '<path fill-rule="evenodd" d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-4.146-3.146a.5.5 0 0 0-.708-.708L8 7.293 4.854 4.146a.5.5 0 1 0-.708.708L7.293 8l-3.147 3.146a.5.5 0 0 0 .708.708L8 8.707l3.146 3.147a.5.5 0 0 0 .708-.708L8.707 8l3.147-3.146z"/>'
            svg_cross += '</svg>'
            document.getElementById('team_post_svg_A').innerHTML = svg_cross
            var str = JSON.stringify(JSON.parse(this.responseText), null, 4);
            console.log(str)
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
            document.getElementById('team_post_toast_admin_header').innerHTML = 'FAILURE'
            document.getElementById('team_post_toast_admin_body').innerHTML = str
            $('#team_post_toast_admin').toast('show');
            console.log(JSON.stringify([jsonarray]))
        }
        x = document.forms["teampost_A"].firstElementChild
        while (x) {
            x.value = null
            x = x.nextElementSibling
        }
        team_refresh_A()
    }
    var jsonarray = {}
    let arr = document.forms["teampost_A"].firstElementChild
    while (arr) {
        console.log(arr.value)
        if (arr.type != "checkbox" && arr.value)
            jsonarray[(arr.id).slice(0, arr.id.indexOf("-"))] = (arr.value == "null") ? null : (arr.value == "" ? null : arr.value)
        else if (arr.type == "checkbox")
            jsonarray[(arr.id).slice(0, arr.id.indexOf("-"))] = arr.checked
        arr = arr.nextElementSibling
    }
    refreshLoader(xhttp)
    xhttp.open("POST", "/api/" + getCookie("username") + "/team/", true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("Content-type", "application/json;charset=UTF-8");
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.send(JSON.stringify([jsonarray]));
}

admin_refresh = team_refresh_A

function admin_team_upload_csv(event) {
    const selectedFile = document.getElementById('admin_team_upload_file').files[0];
    console.log(selectedFile)
    const reader = new FileReader();
    reader.onload = function () {
        var result = []
        var team_fields = ["team_year_code", "team_name", "description", "guide", "panel_year_code", "panel_id", "dept"]
        var stud_fields = ["srn", "name", "email", "phone"]
        var linearray = reader.result.split('\n');
        for (var i = 1; i < linearray.length; i++) {
            if (linearray[i] != "") {
                var dict = {};
                var arr = linearray[i].split(',')
                for (var j = 0; j < 7; j++) {
                    dict[team_fields[j]] = (arr[j] == '' || arr[j] == 'null') ? null : arr[j]
                }
                dict["student"] = []
                for (var j = 0; j < (arr.length - 7) / 4; j++) {
                    if (arr[j * 4 + 7] != '') {
                        var stud_dict = {}
                        for (var k = 0; k < 4; k++) {
                            stud_dict[stud_fields[k]] = arr[j * 4 + 7 + k]
                        }
                        dict["student"].push(stud_dict)
                    }
                }
                result.push(dict)
            }
        }
        var xhttp = new XMLHttpRequest()
        xhttp.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 201) {
                team_refresh_A()
                var svg_tick = '<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-check-circle-fill" fill="green" xmlns="http://www.w3.org/2000/svg">'
                svg_tick += '<path fill-rule="evenodd" d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>'
                svg_tick += '</svg>'
                document.getElementById('team_csv_svg_A').innerHTML = svg_tick
                document.getElementById('team_csv_toast_admin_header').innerHTML = 'SUCCESS'
                document.getElementById('team_csv_toast_admin_body').innerHTML = "Assumptions made while inserting are listed below"
                $('#team_csv_toast_admin').toast('show');
                document.getElementById('admin_team_upload_response').textContent = JSON.stringify(JSON.parse(this.responseText), null, 4)
            }
            else {
                var svg_cross = '<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-x-circle-fill" fill="red" xmlns="http://www.w3.org/2000/svg">'
                svg_cross += '<path fill-rule="evenodd" d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-4.146-3.146a.5.5 0 0 0-.708-.708L8 7.293 4.854 4.146a.5.5 0 1 0-.708.708L7.293 8l-3.147 3.146a.5.5 0 0 0 .708.708L8 8.707l3.146 3.147a.5.5 0 0 0 .708-.708L8.707 8l3.147-3.146z"/>'
                svg_cross += '</svg>'
                document.getElementById('team_csv_svg_A').innerHTML = svg_cross
                document.getElementById('team_csv_toast_admin_header').innerHTML = 'FAILURE'
                document.getElementById('team_csv_toast_admin_body').innerHTML = "Errors are listed below"
                $('#team_csv_toast_admin').toast('show');
                // document.getElementById('admin_team_upload_response').textContent=JSON.stringify(JSON.parse(this.responseText),null,4)
                str = ''
                var data = JSON.parse(this.responseText)
                console.log(data)

                str += '<table id="A_teamcsv_Table" class="table table-bordered">'
                str += '<th>Team</th><th>Student</th><th>details</th>'
                for (let i in data) {
                    console.log(data[i]['value'])
                    str += '<tr><td>' + JSON.stringify(data[i]["value"][0]) + '</td>'
                    if (data[i].value[1])
                        str += '<td>' + JSON.stringify(data[i].value[1]) + '</td>'
                    else
                        str += '<td></td>'
                    str += '<td>' + JSON.stringify(data[i]["detail"]) + '</td></tr>'
                }
                str += '</table>'
                document.getElementById('admin_team_upload_response').innerHTML = str
            }
        }
        refreshLoader(xhttp)
        xhttp.open("POST", "/api/" + getCookie("username") + "/team-bulk/", true);
        xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
        xhttp.setRequestHeader("Content-type", "application/json;charset=UTF-8");
        xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
        xhttp.send(JSON.stringify(result));
    }
    reader.readAsText(selectedFile);
}

function handleFileLoad(event) {
    console.log(event);
    console.log(event.target.result)
    document.getElementById('admin_team_upload_response').textContent = event.target.result;
}