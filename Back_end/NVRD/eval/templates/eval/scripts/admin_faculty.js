function faculty_refresh_A() {
    tbody = document.getElementById("faculty_body")
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
                str += '<tr>'
                for (let j of ["fac_id", "fac_type", "name", "email", "phone", "is_active", "is_admin", "dept"]) {
                    if (j == "is_active" || j == "is_admin") {
                        if (data[i][j] == true)
                            str += ("<td>" + '&#9989;' + "</td>")
                        else
                            str += ("<td>" + '&#10060;' + "</td>")
                    }
                    else {
                        str += ("<td>" + data[i][j] + "</td>")
                    }
                }
                str += '<td scope="col"><button type="button" class="btn btn-dark active btn" data-toggle="modal" data-target="#modal_admin_faculty_put" onclick="admin_faculty_put_form(this)">' + svgstr + '</button></td></tr>'
            }
            document.getElementById("faculty_body_A").innerHTML = str
        }
    }
    refreshLoader(xhttp)
    xhttp.open("GET", "/api/" + getCookie("username") + "/faculty/", true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.send();
}

function faculty_search_A() {
    tbody = document.getElementById("faculty_body")
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
                str += '<tr>'
                for (let j in data[i]) {
                    str += ("<td>" + data[i][j] + "</td>")
                }
                str += '<td scope="col"><button type="button" class="btn btn-dark active btn" data-toggle="modal" data-target="#modal_admin_faculty_put" onclick="admin_faculty_put_form(this)">' + svgstr + '</button></td></tr>'
            }
            document.getElementById("faculty_body_A").innerHTML = str
        }
    }
    refreshLoader(xhttp)
    var fac_id = document.getElementById("faculty_search_fac_id_A").value
    var str = "/api/" + getCookie("username") + "/faculty/"
    if (fac_id != "")
        str += ("?fac_id=" + fac_id)
    xhttp.open("GET", str, true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.send();
}

function admin_faculty_put() {
    var jsonarray = {}
    var modal = document.getElementById("admin_faculty_details_put").firstElementChild
    while (modal) {
        if (modal.placeholder) {
            // jsonarray[modal.placeholder] = (modal.value == "null") ? null : (modal.value == "" ? null:(modal.value=="on")? modal.checked: modal.value)
            if (modal.value == "null" || modal.value == "") {
                jsonarray[modal.placeholder] = null
            }
            else if (modal.value == "on") {
                jsonarray[modal.placeholder] = modal.checked
            }
            else {
                jsonarray[modal.placeholder] = modal.value
            }
        }
        modal = modal.nextElementSibling
    }
    jsonarray["fac_type"] = document.getElementById('Designation-fac_put_A').value
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == XMLHttpRequest.DONE) {
            if (this.status == 201) {
                var svg_tick = '<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-check-circle-fill" fill="green" xmlns="http://www.w3.org/2000/svg">'
                svg_tick += '<path fill-rule="evenodd" d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>'
                svg_tick += '</svg>'
                document.getElementById('faculty_put_svg_A').innerHTML = svg_tick
                var str = this.responseText
                d = JSON.parse(str)
                str = "<b>" + d["detail"] + "</b>"
                if (d["assumption"])
                    for (let i = 0; i < d["assumption"].length; ++i) {
                        str += "<br>" + d["assumption"][i]["detail"] + "<br>"
                    }
                document.getElementById('faculty_put_toast_admin_header').innerHTML = 'SUCCESS'
                document.getElementById('faculty_put_toast_admin_body').innerHTML = str
                $('#faculty_put_toast_admin').toast('show');
                faculty_refresh_A()
            }
            else {
                var svg_cross = '<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-x-circle-fill" fill="red" xmlns="http://www.w3.org/2000/svg">'
                svg_cross += '<path fill-rule="evenodd" d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-4.146-3.146a.5.5 0 0 0-.708-.708L8 7.293 4.854 4.146a.5.5 0 1 0-.708.708L7.293 8l-3.147 3.146a.5.5 0 0 0 .708.708L8 8.707l3.146 3.147a.5.5 0 0 0 .708-.708L8.707 8l3.147-3.146z"/>'
                svg_cross += '</svg>'
                document.getElementById('faculty_put_svg_A').innerHTML = svg_cross
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
                document.getElementById('faculty_put_toast_admin_header').innerHTML = 'FAILURE'
                document.getElementById('faculty_put_toast_admin_body').innerHTML = str
                $('#faculty_put_toast_admin').toast('show');
            }
        }
    }
    refreshLoader(xhttp)
    xhttp.open("PUT", "/api/" + getCookie("username") + "/faculty/", true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("Content-type", "application/json;charset=UTF-8");
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.send(JSON.stringify([jsonarray]));
}

function admin_faculty_put_form(arg) {
    var head = arg.parentNode.parentNode.children
    var modal = document.getElementById("admin_faculty_details_put").children
    document.getElementById("response_admin_faculty_put").innerHTML = ""
    insert_dept_options_A('dept-fac_put_A')
    modal[1].value = head[0].innerHTML
    modal[3].value = head[2].innerHTML
    modal[5].value = head[3].innerHTML
    modal[7].value = head[4].innerHTML
    modal[11].value = head[1].innerHTML
    modal[14].checked = head[5].innerHTML == "✅"
    modal[17].checked = head[6].innerHTML == "✅"
}

function insert_dept_options_A(ele_id) {
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            let data = JSON.parse(this.responseText)
            deptSelect = document.getElementById(ele_id);
            let str = ""
            str += '<option selected="selected" disabled="disabled" class="form-control">Department</option>'
            for (let i = 0; i < data.length; i++) {
                str += '<option value=\"' + data[i]['dept'] + '\">' + data[i]['dept'] + '</option>'
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

function faculty_post_Admin() {
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4) {
            if (this.status == 201) {
                let data = JSON.parse(this.responseText)
                var svg_tick = '<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-check-circle-fill" fill="green" xmlns="http://www.w3.org/2000/svg">'
                svg_tick += '<path fill-rule="evenodd" d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>'
                svg_tick += '</svg>'
                document.getElementById('faculty_post_svg_A').innerHTML = svg_tick
                var str = JSON.stringify(JSON.parse(this.responseText), null, 4);
                d = JSON.parse(str)
                str = "<b>" + d["detail"] + "</b>"
                if (d["assumption"])
                    for (let i = 0; i < d["assumption"].length; ++i) {

                        str += "<br>" + d["assumption"][i]["detail"] + "<br>"
                    }
                document.getElementById('faculty_post_toast_admin_header').innerHTML = 'SUCCESS'
                document.getElementById('faculty_post_toast_admin_body').innerHTML = str
                $('#faculty_post_toast_admin').toast('show');
            }
            else {
                var svg_cross = '<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-x-circle-fill" fill="red" xmlns="http://www.w3.org/2000/svg">'
                svg_cross += '<path fill-rule="evenodd" d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-4.146-3.146a.5.5 0 0 0-.708-.708L8 7.293 4.854 4.146a.5.5 0 1 0-.708.708L7.293 8l-3.147 3.146a.5.5 0 0 0 .708.708L8 8.707l3.146 3.147a.5.5 0 0 0 .708-.708L8.707 8l3.147-3.146z"/>'
                svg_cross += '</svg>'
                document.getElementById('faculty_post_svg_A').innerHTML = svg_cross
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
                document.getElementById('faculty_post_toast_admin_header').innerHTML = 'FAILURE'
                document.getElementById('faculty_post_toast_admin_body').innerHTML = str
                $('#faculty_post_toast_admin').toast('show');
            }
            x = document.forms["facpost_A"].firstElementChild
            while (x) {
                x.value = null
                x = x.nextElementSibling
            }
            insert_dept_options_A('dept-fac_post_A')
            faculty_refresh_A()
        }
    }
    var jsonarray = {}
    let arr = document.forms["facpost_A"].firstElementChild
    while (arr) {
        if (arr.type != "checkbox" && arr.value)
            jsonarray[(arr.id).slice(0, arr.id.indexOf("-"))] = (arr.value == "null") ? null : (arr.value == "" ? null : arr.value)
        else if (arr.type == "checkbox")
            jsonarray[(arr.id).slice(0, arr.id.indexOf("-"))] = arr.checked
        arr = arr.nextElementSibling
    }
    jsonarray["fac_type"] = document.getElementById('Designation-fac_post_A').value
    refreshLoader(xhttp)
    xhttp.open("POST", "/api/" + getCookie("username") + "/faculty/", true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("Content-type", "application/json;charset=UTF-8");
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.send(JSON.stringify([jsonarray]));
}
admin_refresh = faculty_refresh_A