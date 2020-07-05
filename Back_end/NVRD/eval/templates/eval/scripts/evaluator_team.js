function team_refresh_evaluator() {
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
                str += '</tr>'
            }
            document.getElementById("team_body_evaluator").innerHTML = str
        }
    }
    var curr_list = returnCurrentList()
    var panel_year_code = curr_list[1].slice(0, curr_list[1].indexOf("-"))
    var panel_id = curr_list[1].slice((curr_list[1].indexOf("-") + 1))
    refreshLoader(xhttp)
    xhttp.open("GET", "/api/" + getCookie("username") + "/" + panel_year_code + "-" + panel_id + "/team/", true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.send();
}

function team_search_evaluator() {
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            let data = JSON.parse(this.responseText)
            var str = ''
            var svgstr = '<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-pencil" fill="currentColor" xmlns="http://www.w3.org/2000/svg">'
            svgstr += '<path fill-rule="evenodd" d="M11.293 1.293a1 1 0 0 1 1.414 0l2 2a1 1 0 0 1 0 1.414l-9 9a1 1 0 0 1-.39.242l-3 1a1 1 0 0 1-1.266-1.265l1-3a1 1 0 0 1 .242-.391l9-9zM12 2l2 2-9 9-3 1 1-3 9-9z"/>'
            svgstr += '<path fill-rule="evenodd" d="M12.146 6.354l-2.5-2.5.708-.708 2.5 2.5-.707.708zM3 10v.5a.5.5 0 0 0 .5.5H4v.5a.5.5 0 0 0 .5.5H5v.5a.5.5 0 0 0 .5.5H6v-1.5a.5.5 0 0 0-.5-.5H5v-.5a.5.5 0 0 0-.5-.5H3z"/>'
            svgstr += '</svg>'
            console.log(data)
            for (let i in data) {
                str += '<tr>'
                for (let j in data[i]) {
                    console.log(data[i][j])
                    str += ("<td>" + data[i][j] + "</td>")
                }
                str += '</tr>'
            }
            document.getElementById("team_body_evaluator").innerHTML = str
        }
    }
    refreshLoader(xhttp)
    var team_year_code = document.getElementById("team_search_team_year_code_evaluator").value
    var team_id = document.getElementById("team_search_team_id_evaluator").value
    var team_name = document.getElementById("team_search_team_name_evaluator").value
    var curr_list = returnCurrentList()
    var panel_id = curr_list[1].slice(0, curr_list[1].indexOf("-"))
    var panel_year_code = curr_list[1].slice((curr_list[1].indexOf("-") + 1))
    var str = ""
    if (team_year_code != "") {
        if (str == "")
            str += ("?team_year_code=" + team_year_code)
        else
            str += ("&team_year_code=" + team_year_code)
    }
    if (team_id != "") {
        if (str == "")
            str += ("?team_id=" + team_id)
        else
            str += ("&team_id=" + team_id)
    }
    if (team_name != "") {
        if (str == "")
            str += ("?team_name=" + team_name)
        else
            str += ("&team_name=" + team_name)
    }
    xhttp.open("GET", "/api/" + getCookie("username") + "/" + panel_id + "-" + panel_year_code + "/team/" + str, true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.send();
}

function evaluator_refresh() {
    team_refresh_evaluator()
}
