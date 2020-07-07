function facpanel_refresh_coordinator() {
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
                for (let j of ["fac_id", "name", "phone", "email", "is_coordinator"])
                    str += ("<td>" + (typeof (data[i][j]) != "boolean" ? data[i][j] : data[i][j] ? '&#9989;' : '&#10060;') + "</td>")
                str += '<td scope="col"><button type="button" class="btn btn-dark active btn" data-toggle="modal" data-target="#coord_faculty_panel_put" onclick="coord_faculty_panel_put_form(this)">' + svgstr + '</button></td></tr>'
            }
            document.getElementById("faculty_panel_body_C").innerHTML = str
        }
    }
    refreshLoader(xhttp)
    var curr_list = returnCurrentList()
    var p_year_code = curr_list[1].slice(0, curr_list[1].indexOf("-"))
    var p_id = curr_list[1].slice((curr_list[1].indexOf("-") + 1))
    var url = '/api/' + getCookie("username") + '/' + p_year_code + '-' + p_id + '/' + 'faculty-panel/';
    xhttp.open("GET", url, true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.send();
}
function coord_faculty_panel_put_form(t) {
    var req = t.parentNode.parentNode.childNodes
    $("#fac_panel_put_C").html("Edit " + req[0].innerHTML)
    var putform = document.getElementById("coord_faculty_panel_details_put").childNodes
    for (let ele of putform)
        if (ele.type == "checkbox") {
            ele.checked = (req[4].innerHTML == "✅" ? true : false)
            break
        }
}
function coord_faculty_panel_put(t) {
    var curr_list = returnCurrentList()
    var pyc = curr_list[1].slice(0, curr_list[1].indexOf("-"))
    var pid = curr_list[1].slice((curr_list[1].indexOf("-") + 1))
    var fac = document.getElementById("fac_panel_put_C").innerHTML.split(" ")[1]
    var jsonarray = { "panel_year_code": pyc, "panel_id": pid, "fac_id": fac }
    for (let ele of t.parentNode.childNodes) {
        if (ele.type == "checkbox") {
            jsonarray["is_coordinator"] = ele.checked
        }
    }
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == XMLHttpRequest.DONE && this.status == 201) {
            setTimeout(() => { $("#coord_faculty_panel_put").modal("hide") }, 2000)
            facpanel_refresh_coordinator()
        }
    }
    refreshLoader(xhttp)
    var curr_list = returnCurrentList()
    var p_year_code = curr_list[1].slice(0, curr_list[1].indexOf("-"))
    var p_id = curr_list[1].slice((curr_list[1].indexOf("-") + 1))
    var url = '/api/' + getCookie("username") + '/' + p_year_code + '-' + p_id + '/' + 'faculty-panel/';
    xhttp.open("PUT", url, true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("Content-type", "application/json;charset=UTF-8");
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.send(JSON.stringify([jsonarray]));
}
function coordinator_refresh() {
    facpanel_refresh_coordinator()
}