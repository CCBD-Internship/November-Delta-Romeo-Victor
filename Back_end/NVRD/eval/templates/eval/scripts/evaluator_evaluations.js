evaluator_refresh = evaluator_evaluations_refresh
var lst = ["srn", "name"];
var time_E = null;
var team_year_code;
var team_id;
var team_name;
var team_desc;
var Evaluation_format;
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
    document.getElementById("Evaluator_download_button").style = "display:inline-block"
    if (t) {
        team_year_code = t.children[0].textContent.split("   ")[0];
        team_id = t.children[0].textContent.split("   ")[1];
        team_name = t.children[1].children[0].textContent.split(":")[1]
        team_desc = t.children[1].children[1].textContent.split(":")[1]
    }
    document.getElementById('evaluation_views_card_header').textContent = team_year_code + "-" + team_id;
    var curr_list = returnCurrentList()
    var review_number = curr_list[2].split("-")[1];
    var panel_year_code = curr_list[1].split("-")[0]
    var panel_id = curr_list[1].split("-")[1]
    document.getElementById('evaluation_views_card_body_review').textContent = curr_list[2]
    document.getElementById('evaluation_views_card_body_head').textContent = team_name
    document.getElementById('evaluation_views_card_body_description').textContent = team_desc
    document.getElementById('evaluation_views_card_body_fac_id').textContent = "Evaluator: " + User["name"]
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == XMLHttpRequest.DONE && this.status == 200) {
            let data = JSON.parse(this.responseText)
            Evaluation_format = data
            document.getElementById("evaluation_views_card_header_guide").textContent = "Guide: " + Evaluation_format["team"]["guide_id"]
            var thead = ''
            max_vals = {
                1: [-2, -2, -2, 10, 10, 10, 10, 40, -1, -1, -3],
                2: [-2, -2, -2, 10, 10, 10, 10, 40, -1, -1, -3],
                3: [-2, -2, -2, 10, 10, 5, 5, 5, 35, -1, -1, -3],
                4: [-2, -2, -2, 10, 10, 10, 10, 40, -1, -1, -3],
                5: [-2, -2, -2, 10, 10, 10, 10, 40, -1, -1, -3]
            }
            lst = ["srn", "name", "email"]
            for (let i of Object.keys(data["individual_review"][0])) {
                if (lst.indexOf(i) == -1 && ["is_evaluated", "private_comments", "public_comments", "fac_id", "phone"].indexOf(i) == -1) {
                    lst.push(i)
                }
            }
            lst.push("total")
            lst.push("private_comments")
            lst.push("public_comments")
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
                var sum = 0;
                for (let j of lst) {
                    if (max_vals[review_number][c] == -2) {
                        tbody += ("<td name=" + i['srn'] + ">" + i[j] + "</td>")
                    }
                    else if (max_vals[review_number][c] == -1) {
                        tbody += ("<td>" + "<textarea class=\"form-control bg-transparent text-white text-center border-white\" style='min-width: 10em'>" + i[j] + "</textarea></td>")
                    }
                    else if (max_vals[review_number][c] == -3) {
                        tbody += ("<td><input type=\"checkbox\"></td>")
                    }
                    else if (max_vals[review_number][c] > 20) {
                        tbody += ("<td name=\"total_marks\">" + sum + "</td>")
                    }
                    else {
                        tbody += ("<td>" + "<input class=\"form-control bg-transparent text-white text-center\" style='min-width: 5em' type='number' value='" + i[j] + "'  min=\"0\" max='" + max_vals[review_number][c] + "' onchange=\"update_total_marks(event,this)\"></td>")
                        sum += Number(i[j])
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
                for (j = 0; j <= 2; j++) {
                    tbody.children[i].children[j].addEventListener('click', student_photo_modal)
                }
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
    if (elem) {
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
    document.getElementById("Evaluator_download_button").style = "display:none"

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
            else if (col.type == "textarea") {
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


function update_total_marks(e, t) {
    var datas = (e.srcElement.parentElement.parentElement.children)
    var sum = 0
    var tots;
    for (let i of datas) {
        if (i.firstElementChild && i.firstElementChild.tagName == 'INPUT' && i.firstElementChild.type == 'number')
            sum += Number(i.firstElementChild.value)

        if (i.getAttribute('name') == "total_marks")
            tots = i
    }
    tots.textContent = sum
}

// function Evaluator_print() {
//     submit_evaluation()
//     document.getElementById("Evaluator_save_button").style = "display:none"
//     document.getElementById("NVRDbreadcrumb").style = "visibility:hidden"
//     window.print()
//     document.getElementById("Evaluator_save_button").style = "display:inline-block"
//     document.getElementById("NVRDbreadcrumb").style = "visibility:visible"
// }

function Evaluator_print() {
    submit_evaluation()
    document.getElementById("Evaluator_save_button").style = "display:none"
    var my_head = '<title>Evaluation Print</title><link rel="stylesheet" type="text/css" href="https://bootswatch.com/4/darkly/bootstrap.css">'
    var script_init = '<script src="https://lh3.googleusercontent.com/proxy/4j0c0VApd8T3Tx9YvwWhVSUBt0_nTFP9RpMKgnbfVUej1WLbd1_DwcDDPJy2gapdMJCDrOg79Y3aRQ0GtU5DpWhuSb0AdrsUUQUhk8uduj54_Wr-7UFRG2VJtqlto2YXdwKPTzbhrnqYmPJcnc-pyekvqXMdBKwwWYHzJjeo1tH5s13gzv1UXjaRvq5eVZFDsA" crossorigin="anonymous"></script>'
    script_init += '<script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script><script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js"    integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo"    crossorigin="anonymous"></script><script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js"    integrity="sha384-OgVRvuATP1z7JjHLkuOU7Xw704+h835Lr+6QL9UvYjZE3Ipu6Tp75j7Bh/kR0JKI"    crossorigin="anonymous"></script>'
    var logo_div = "<center><img src='https://www.pes.edu/wp-content/uploads/2020/03/pes_logo1.png' style='width:auto;height:auto'></center><br/>";
    var tab = open("", "")
    var req_div = document.getElementById('evaluation_views').innerHTML
    // var original_content = document.body.innerHTML
    tab.document.head.innerHTML += my_head
    tab.document.body.innerHTML +='<style type="text/css" media="print">@page {size:landscape}</style>'
    tab.document.body.innerHTML += script_init
    tab.document.body.innerHTML += logo_div
    tab.document.body.innerHTML += req_div
    setTimeout(function () {
        tab.print();
        // document.body.innerHTML = original_content;
        tab.close()
        document.getElementById("Evaluator_save_button").style = "display:inline-block";
    }, 1000 * .5)
}

function student_photo_modal(e) {
    document.getElementById('student_photo_modal_img').src = "data:image/jpeg;base64," + Evaluation_format["photo"][e.target.getAttribute('name')]
    document.getElementById('student_photo_modal_srn').innerHTML = e.target.getAttribute('name')
    for (i of Evaluation_format["individual_review"]) {
        if (i["srn"] == e.target.getAttribute('name')) {
            document.getElementById('student_photo_modal_name').innerHTML = i["name"]
        }
    }
    $("#student_photo_modal").modal('show')
}