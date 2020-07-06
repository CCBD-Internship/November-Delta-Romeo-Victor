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
            var str = '<div class="row row-cols-1 row-cols-md-3" id="C_TFRcardchild">'
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
    document.getElementById('nav_bar_E').style = "display:none;"
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
            console.log(data)
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
                        tbody += ("<td>" + "<textarea class=\"form-control bg-transparent text-white text-center border-white\" " + i[j] + "></textarea></td>")
                    }
                    else if (max_vals[review_number][c] == -3) {
                        tbody += ("<td><input type=\"checkbox\"></td>")
                        // tbody += ("<td>" + "<label class=\"switch\"><input type='checkbox' default='" + i[j] + "' size='10'><span class=\"slider round\"></span></label></td>")
                        // // tbody += "<td>"+"<span class=\"custom-control custom-switch\"><input type=\"checkbox\" class=\"custom-control-input\"><label class=\"custom-control-label\" for=\"customSwitch1\"></label></span>"+"</td>"

                    }
                    else {
                        tbody += ("<td>" + "<input class=\"form-control bg-transparent text-white text-center\" type='number' value='" + i[j] + "' size='2' min=\"0\" max='" + max_vals[review_number][c] + "'></td>")
                    }
                    c++;
                }
                tbody += "</tr>"
            }
            document.getElementById("evaluation_views_table_body").innerHTML = tbody
            if (data["team_remarks"])
                document.getElementById("evaluator_team_remark").innerHTML = data["team_remarks"]
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
    if (now.getTime() < open_time.getTime() && open_time.getTime() < close_time.getTime())
        elem.textContent = "Evaluation window opens on " + open_time.toLocaleDateString() + " at " + open_time.toLocaleTimeString()
    else if (now.getTime() > open_time.getTime() && now.getTime() < close_time.getTime())
        elem.textContent = "Evaluation window is open now!! shall close in approximately " + diff_hours_E(close_time, now)[0] + " days " + diff_hours_E(close_time, now)[1] + " hours " + diff_hours_E(close_time, now)[2] + " minutes"
    else
        elem.textContent = "Evaluation window was closed on " + close_time.toLocaleDateString() + " at " + close_time.toLocaleTimeString()

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
    var ret = { "individual_review": jsonarray, "review_number": review_number, "team": { "team_year_code": team_year_code, "team_id": team_id }, "team_remarks": document.getElementById("evaluator_team_remark").textContent }
    xhttp.onreadystatechange = function () {
        if (this.readyState == XMLHttpRequest.DONE && this.status == 200) {
            console.log(data)
            E_evaluations_opentip()
        }
        else {

        }
    }
    xhttp.open("PUT", "/api/" + getCookie("username") + "/" + panel_year_code + "-" + panel_id + "/" + review_number + "/" + team_year_code + "-" + team_id + "/marks-view/", true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.setRequestHeader("Content-type", "application/json;charset=UTF-8");
    xhttp.send(JSON.stringify(ret));
}