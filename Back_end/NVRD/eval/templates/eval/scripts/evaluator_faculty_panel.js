function facpanel_refresh_evaluator() {
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == XMLHttpRequest.DONE && this.status == 200) {
            let data = JSON.parse(this.responseText)
            var str = ''
            for (let i in data) {
                str += "<tr>"
                for (let j of ["fac_id", "name", "phone", "email", "is_coordinator"])
                    str += ("<td>" + (typeof (data[i][j]) != "boolean" ? data[i][j] : data[i][j] ? '&#9989;' : '&#10060;') + "</td>")
                str += "</tr>"
            }
            document.getElementById("faculty_panel_body_E").innerHTML = str
        }
    }
    var curr_list = returnCurrentList()
    var p_year_code = curr_list[1].slice(0, curr_list[1].indexOf("-"))
    var p_id = curr_list[1].slice((curr_list[1].indexOf("-") + 1))
    refreshLoader(xhttp)
    var url = '/api/' + getCookie("username") + '/' + p_year_code + '-' + p_id + '/' + 'faculty-panel/';
    xhttp.open("GET", url, true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.send();
}

function evaluator_refresh() {
    facpanel_refresh_evaluator()
}