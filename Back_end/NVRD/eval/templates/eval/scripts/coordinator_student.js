function student_refresh_coordinator() {
    tbody = document.getElementById("student_body")
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
                // str += '<tr><td scope="row" style="text-align:right"><input name="student_boxes_coordinator" class="form-check-input position-static" type="checkbox"></input></td>'
                str += '<tr>'
                for (let j in data[i]) {
                    str += ("<td>" + data[i][j] + "</td>")
                }
                // str += '<td scope="col"><button type="button" class="btn btn-dark active btn" data-toggle="modal" data-target="#modal_coordinator_student_put" onclick="coordinator_student_put_form(this)">' + svgstr + '</button></td></tr>'
                str += '</tr>'
            }
            document.getElementById("student_body_coordinator").innerHTML = str
        }
    }
    var curr_list = returnCurrentList()
    // console.log(curr_list,curr_list[1].slice(0, curr_list[1].indexOf("-")),)
    var panel_id = curr_list[1].slice(0, curr_list[1].indexOf("-"))
    var panel_year_code = curr_list[1].slice((curr_list[1].indexOf("-") + 1))
    refreshLoader(xhttp)
    xhttp.open("GET", "/api/" + getCookie("username") + "/" + panel_id + "-" + panel_year_code + "/student/", true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.send();
}

function student_search_coordinator() {
    tbody = document.getElementById("student_body")
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
                str += '<tr><td scope="row" style="text-align:right"><input name="boxes" class="form-check-input position-static" type="checkbox"></input></td>'
                for (let j in data[i]) {
                    str += ("<td>" + data[i][j] + "</td>")
                }
                str += '<td scope="col"><button type="button" class="btn btn-dark active btn" data-toggle="modal" data-target="#modal_coordinator_student_put" onclick="coordinator_student_put_form(this)">' + svgstr + '</button></td></tr>'
            }
            document.getElementById("student_body_coordinator").innerHTML = str
        }
    }
    refreshLoader(xhttp)
    var srn = document.getElementById("student_search_srn_coordinator").value
    var name = document.getElementById("student_search_name_coordinator").value
    var curr_list = returnCurrentList()
    // console.log(curr_list,curr_list[1].slice(0, curr_list[1].indexOf("-")),)
    var panel_id = curr_list[1].slice(0, curr_list[1].indexOf("-"))
    var panel_year_code = curr_list[1].slice((curr_list[1].indexOf("-") + 1))
    var str = "/api/" + getCookie("username") + "/" + panel_id + "-" + panel_year_code + "/student/"
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

function coordinator_refresh() {
    student_refresh_coordinator()
}