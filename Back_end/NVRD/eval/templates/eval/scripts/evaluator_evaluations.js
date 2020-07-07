evaluator_refresh = evaluator_evaluations_refresh
var lst = ["srn", "name"];
var time_E = null;
var team_year_code;
var team_id;
var team_name;
var team_desc;
function evaluator_evaluations_refresh() {
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == XMLHttpRequest.DONE && this.status == 200) {
            let data = JSON.parse(this.responseText)
            var str = '<div class="row row-cols-1 row-cols-md-3 w-100" id="C_TFRcardchild">'
            for (let i in data) {
                str += C_team_fac_review_cardmaker(data[i]["team_year_code"], data[i]["team_id"], data[i]["team_name"], data[i]["description"], data[i]["guide"])
            }
            str += '</div>'
            document.getElementById("evaluation_team_cards").innerHTML = str;
            document.getElementById("evaluation_team_cards").style = "display:inline;"
            document.getElementById("evaluation_views").style = "display:none;"
            if (time_E != null) {
                clearInterval(time_E);
                time_E = null;
            }
            panel_review_refresh_Evaluations()
        }
    }
    var curr_list = returnCurrentList()
    var panel_year_code = curr_list[1].slice(0, curr_list[1].indexOf("-"))
    var panel_id = curr_list[1].slice((curr_list[1].indexOf("-") + 1))
    var url;
    url = "/api/" + getCookie("username") + "/" + panel_year_code + "-" + panel_id + "/" + curr_list[2].split('-')[1] + "/team/"
    refreshLoader(xhttp)
    xhttp.open("GET", url, true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.send();
}

// generates a card for a team
function C_team_fac_review_cardmaker(team_year_code, team_id, team_name, description, guide) {
    str = '<div class="col mb-4"><div onclick="E_evaluations_opentip(event,this)" class="card bg-info" ><div class="card-header">' + team_year_code + '   ' + team_id + '    </div><div class="card-body"><h5 class="card-title">Name:  ' + team_name + '</h5><p>  Description:  ' + description + '</p><p>Guide:  ' + guide + '</p></div></div></div>'
    return str
}

function E_evaluations_opentip(e, t) {
    document.getElementById("evaluation_team_cards").style = "display:none;"
    document.getElementById("evaluation_views").style = "display:inline;"
    document.getElementById("refresh_EE").style = "display:none"
    document.getElementById("back_EE").style = "visibility:visible"
    document.getElementById("reset_EE").style = "display:inline-block"
    document.getElementById("check_all_EE").style = "display:inline-block"
    // str="<table class='table table-striped'><thead><tr><th scope='col'></th><th scope='col'></th><th scope='col'></th><th scope='col'></th></tr></thead><tbody id='C_TFR_R1_tbody'></tbody></table>"
    // document.getElementById('evaluation_views').innerHTML=str
    // console.log(t)
    if (t) {
        team_year_code = t.children[0].textContent.split("   ")[0];
        team_id = t.children[0].textContent.split("   ")[1];
        team_name = t.children[1].children[0].textContent.split(":")[1]
        team_desc = t.children[1].children[1].textContent.split(":")[1]
    }
    // console.log(team_id, team_year_code, team_name)
    document.getElementById('evaluation_views_card_header').textContent = team_year_code + "-" + team_id;
    var curr_list = returnCurrentList()
    var review_number = curr_list[2].split("-")[1];
    var panel_year_code = curr_list[1].split("-")[0]
    var panel_id = curr_list[1].split("-")[1]
    document.getElementById('evaluation_views_card_body_review').textContent = curr_list[2]
    document.getElementById('evaluation_views_card_body_head').textContent = team_name
    document.getElementById('evaluation_views_card_body_description').textContent = team_desc
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == XMLHttpRequest.DONE && this.status == 200) {
            let data = JSON.parse(this.responseText)
            Evaluation_format = data
            var thead = ''
            max_vals = {
                1: [-2, -2, 10, 10, 10, 10, -2, -2, -1, -3],
                2: [-2, -2, 10, 10, 10, 10, -2, -2, -1, -3],
                3: [-2, -2, 10, 10, 5, 5, 5, -2, -2, -1, -3],
                4: [-2, -2, 10, 10, 10, 10, -2, -2, -1, -3],
                5: [-2, -2, 10, 10, 10, 10, -2, -2, -1, -3]
            }
            lst = ["srn", "name"]
            for (let i of Object.keys(data["individual_review"][0])) {
                if (lst.indexOf(i) == -1 && ["is_evaluated", "comments", "fac_id"].indexOf(i) == -1) {
                    lst.push(i)
                }
            }
            lst.push("comments")
            lst.push("is_evaluated")
            var c = 0
            for (let i of lst) {
                var str = ''
                if (max_vals[review_number][c] > 0) {
                    str += ' (' + max_vals[review_number][c] + ')'
                }
                c++;
                thead += '<th scope="col">' + i.replace(/_/g, ' ') + str + '</th>'
            }
            document.getElementById("evaluation_views_table_fields").innerHTML = thead
            var tbody = ''
            for (let i of data["individual_review"]) {
                tbody += "<tr class='w-100'>"
                var c = 0;
                for (let j of lst) {
                    if (max_vals[review_number][c] == -2) {
                        tbody += ("<td>" + i[j] + "</td>")
                    }
                    else if (max_vals[review_number][c] == -1) {
                        tbody += ("<td>" + "<textarea class=\"form-control bg-transparent text-white text-center border-white\" style='min-width: 15em'>" + i[j] + "</textarea></td>")
                    }
                    else if (max_vals[review_number][c] == -3) {
                        tbody += ("<td><input type=\"checkbox\"></td>")
                        // tbody += ("<td>" + "<label class=\"switch\"><input type='checkbox' default='" + i[j] + "' size='10'><span class=\"slider round\"></span></label></td>")
                        // // tbody += "<td>"+"<span class=\"custom-control custom-switch\"><input type=\"checkbox\" class=\"custom-control-input\"><label class=\"custom-control-label\" for=\"customSwitch1\"></label></span>"+"</td>"

                    }
                    else {
                        tbody += ("<td>" + "<input class=\"form-control bg-transparent text-white text-center\" style='min-width: 5em' type='number' value='" + i[j] + "'  min=\"0\" max='" + max_vals[review_number][c] + "'></td>")
                    }
                    c++;
                }
                tbody += "</tr>"
            }
            document.getElementById("evaluation_views_table_body").innerHTML = tbody
            if (data["team_remarks"])
                document.getElementById("evaluator_team_remark").textContent = data["team_remarks"]
            var tbody = document.getElementById("evaluation_views_table_body")
            for (var i = 0; i < tbody.children.length; i++) {
                tbody.children[i].children[tbody.children[i].children.length - 1].firstElementChild.checked = data["individual_review"][i]["is_evaluated"]
            }

        }
    }
    xhttp.open("GET", "/api/" + getCookie("username") + "/" + panel_year_code + "-" + panel_id + "/" + review_number + "/" + team_year_code + "-" + team_id + "/marks-view/", true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.setRequestHeader("Content-type", "application/json;charset=UTF-8");
    xhttp.send();

}

function diff_hours_E(dt2, dt1) {

    var diff = (dt2.getTime() - dt1.getTime()) / 1000;
    var days = diff / (24 * 60 * 60)
    diff %= (24 * 60 * 60)
    var hour = diff / (60 * 60);
    diff %= (60 * 60);
    var minute = diff / 60;
    return [Math.floor(days), Math.floor(hour), Math.abs(Math.round(minute))];

}
function time_refresh(open_time, close_time) {
    var now = new Date()
    var elem = document.getElementById("disptime-evalutator")
    if (now.getTime() < open_time.getTime() && open_time.getTime() < close_time.getTime()) {
        elem.innerHTML = "<pre>Evaluation window opens on " + open_time.toLocaleDateString() + " at " + open_time.toLocaleTimeString() + "</pre>"
        elem.setAttribute("style", "")
    }
    else if (now.getTime() > open_time.getTime() && now.getTime() < close_time.getTime()) {
        elem.innerHTML = "<pre>Evaluation window is open now!! shall close in approximately " + diff_hours_E(close_time, now)[0] + " days " + diff_hours_E(close_time, now)[1] + " hours " + diff_hours_E(close_time, now)[2] + " minutes" + "</pre>"
        elem.setAttribute("style", "color:#11EAA1")
    }
    else {
        elem.innerHTML = "<pre>Evaluation window was closed on " + close_time.toLocaleDateString() + " at " + close_time.toLocaleTimeString() + "</pre>"
        elem.setAttribute("style", "")
    }

}
function panel_review_refresh_Evaluations() {
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            let data = JSON.parse(this.responseText)
            let curr_list = returnCurrentList()
            let review_no = curr_list[2].split("-")[1]
            let info = data[review_no - 1]
            var open_time = new Date(info["open_time"]), close_time = new Date(info["close_time"])
            time_E = setInterval(time_refresh, 60000, open_time, close_time)
            time_refresh(open_time, close_time)

        }
    }
    var curr_list = returnCurrentList()
    var panel_id = curr_list[1].slice(0, curr_list[1].indexOf("-"))
    var panel_year_code = curr_list[1].slice((curr_list[1].indexOf("-") + 1))
    refreshLoader(xhttp)
    xhttp.open("GET", "/api/" + getCookie("username") + "/" + panel_id + "-" + panel_year_code + "/panel-review/", true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.send()
}


function submit_evaluation(e, t) {
    var team_year_code = document.getElementById("evaluation_views_card_header").innerHTML.split("-")[0]
    var team_id = document.getElementById("evaluation_views_card_header").innerHTML.split("-")[1]
    var curr_list = returnCurrentList()
    var review_number = curr_list[2].split("-")[1];
    var panel_year_code = curr_list[1].split("-")[0]
    var panel_id = curr_list[1].split("-")[1]
    var xhttp = new XMLHttpRequest()
    var jsonarray = []
    trows = document.getElementById("evaluation_views_table_body").children

    for (let i of trows)
        jsonarray.push({})
    jsonarray["fac_id"] = getCookie("username")
    theads = document.getElementById("evaluation_views_table_fields").children
    for (i of lst) {
        for (var j = 0; j < jsonarray.length; ++j)
            jsonarray[j][i] = ''
    }
    var c = 0;
    for (let i of trows) {
        var vals = []
        for (let j of i.children)
            if (j.firstElementChild) {
                if (j.firstElementChild.type == 'checkbox')
                    vals.push(j.firstElementChild.checked)
                else
                    vals.push(j.firstElementChild.value)
            }
            else
                vals.push(j.textContent)
        for (var j = 0; j < vals.length; ++j) {
            key = lst[j]
            jsonarray[c][key] = vals[j]
        }
        c++;
    }
    var ret = { "individual_review": jsonarray, "review_number": review_number, "team": { "team_year_code": team_year_code, "team_id": team_id }, "team_remarks": document.getElementById("evaluator_team_remark").value }
    xhttp.onreadystatechange = function () {
        if (this.readyState == XMLHttpRequest.DONE) {
            var svg_tick = '<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-check-circle-fill" fill="green" xmlns="http://www.w3.org/2000/svg">'
            svg_tick += '<path fill-rule="evenodd" d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>'
            svg_tick += '</svg>'
            var svg_cross = '<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-x-circle-fill" fill="red" xmlns="http://www.w3.org/2000/svg">'
            svg_cross += '<path fill-rule="evenodd" d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-4.146-3.146a.5.5 0 0 0-.708-.708L8 7.293 4.854 4.146a.5.5 0 1 0-.708.708L7.293 8l-3.147 3.146a.5.5 0 0 0 .708.708L8 8.707l3.146 3.147a.5.5 0 0 0 .708-.708L8.707 8l3.147-3.146z"/>'
            svg_cross += '</svg>'
            // document.getElementById('evaluation_toast_E').setAttribute("style","display:inline")
            if (e != 'local') {
                if (this.status == 400) {
                    document.getElementById('evaluation_toast_E_header').innerHTML = 'FAILURE'
                    document.getElementById('evaluation_toast_E_body').innerHTML = 'Input Form values are incorrect'
                    document.getElementById('evaluation_toast_E_svg').innerHTML = svg_cross
                    $('#evaluation_toast_E').toast('show');
                }
                else if (this.status == 403) {
                    document.getElementById('evaluation_toast_E_header').innerHTML = 'FAILURE'
                    document.getElementById('evaluation_toast_E_body').innerHTML = 'Not authorized to modify Form according to schedule'
                    document.getElementById('evaluation_toast_E_svg').innerHTML = svg_cross
                    $('#evaluation_toast_E').toast('show');
                }
                else if (this.status == 202) {
                    document.getElementById('evaluation_toast_E_header').innerHTML = 'SUCCESS'
                    document.getElementById('evaluation_toast_E_body').innerHTML = 'Form submitted successfully!!'
                    document.getElementById('evaluation_toast_E_svg').innerHTML = svg_tick
                    $('#evaluation_toast_E').toast('show');
                }
            }
            // document.getElementById('evaluation_toast_E').setAttribute("style","display:none")
            E_evaluations_opentip()
        }
    }
    refreshLoader(xhttp)
    xhttp.open("PUT", "/api/" + getCookie("username") + "/" + panel_year_code + "-" + panel_id + "/" + review_number + "/" + team_year_code + "-" + team_id + "/marks-view/", true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.setRequestHeader("Content-type", "application/json;charset=UTF-8");
    xhttp.send(JSON.stringify(ret));
}

function back_to_cards_E() {
    document.getElementById("evaluation_team_cards").style = "display:inline-block;"
    document.getElementById("evaluation_views").style = "display:none;"
    document.getElementById("refresh_EE").style = "display:inline-block"
    document.getElementById("back_EE").style = "visibility:hidden"
    document.getElementById("reset_EE").style = "display:none"
    document.getElementById("check_all_EE").style = "display:none"
    evaluator_evaluations_refresh()
}

function check_all_E() {
    var tbody = document.getElementById("evaluation_views_table_body")
    for (var i = 0; i < tbody.children.length; i++) {
        tbody.children[i].children[tbody.children[i].children.length - 1].firstElementChild.checked = true
    }
    document.getElementById('evaluation_toast_E_header').innerHTML = 'ALL STUDENTS CHECKED'
    document.getElementById('evaluation_toast_E_body').innerHTML = 'all students to be considered as evaluated'
    document.getElementById('evaluation_toast_E_svg').innerHTML = ''
    $('#evaluation_toast_E').toast('show');
}

function reset_all_E() {
    var tbody = document.getElementById("evaluation_views_table_body")
    for (var i = 0; i < tbody.children.length; i++) {
        var row = tbody.children[i]
        for (var j = 0; j < row.children.length; j++) {
            var col = row.children[j].firstChild
            if ((col.type && col.getAttribute("type") == "text")) {
                col.value = ""
            }
            else if ((col.type && col.getAttribute("type") == "number")) {
                col.value = 0
            }
            else if (col.type && col.getAttribute("type") == "checkbox") {
                col.checked = false
            }
            else if( col.type == "textarea"){
                col.value = "not yet scored"
            }
        }
    }
    document.getElementById("evaluator_team_remark").value = ""
    document.getElementById('evaluation_toast_E_header').innerHTML = 'ALL VALUES RESET AND SAVED'
    document.getElementById('evaluation_toast_E_body').innerHTML = 'all parameters are set to initial state and SAVED!!'
    document.getElementById('evaluation_toast_E_svg').innerHTML = ''
    $('#evaluation_toast_E').toast('show');
    submit_evaluation('local')
}