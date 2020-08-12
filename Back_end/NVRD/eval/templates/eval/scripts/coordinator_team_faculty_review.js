// generates a card for a team
function C_team_fac_review_cardmaker(team_year_code, team_id, team_name, description, guide) {
    str = '<div class="col mb-4"><div onclick="C_TFR_openmodal(event,this)" class="card bg-info" ><div class="card-header">' + team_year_code + '   ' + team_id + '    </div><div class="card-body"><h5 class="card-title">Name:  ' + team_name + '</h5><p>  Description:  ' + description + '</p><p>Guide:  ' + guide + '</p></div></div></div>'
    return str
}

// fetches all teams in the panel
function C_TFR_refresh() {
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == XMLHttpRequest.DONE && this.status == 200) {
            let data = JSON.parse(this.responseText)
            var str = '<div class="row row-cols-1 row-cols-md-3 w-100" id="C_TFRcardchild">'
            for (let i in data) {
                str += C_team_fac_review_cardmaker(data[i]["team_year_code"], data[i]["team_id"], data[i]["team_name"], data[i]["description"], data[i]["guide"])
            }
            str += '</div>'
            document.getElementById("NVRD_coord_team_fac_review_card").innerHTML = str
        }
    }
    refreshLoader(xhttp)
    var curr_list = returnCurrentList()
    var panel_year_code = curr_list[1].slice(0, curr_list[1].indexOf("-"))
    var panel_id = curr_list[1].slice((curr_list[1].indexOf("-") + 1))
    xhttp.open("GET", "/api/" + getCookie("username") + "/" + panel_year_code + "-" + panel_id + "/team/", true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.send();
}

coordinator_refresh = C_TFR_refresh

// opens modal for selected team
function C_TFR_openmodal(e, t) {
    var team_year_code = t.textContent.split(' ')[0]
    var team_id = t.textContent.split(' ')[3]
    document.getElementById("C_TFR_modal_title").innerHTML = "<h3 id=C_TFR_modal_title_heading>" + team_year_code + " " + team_id + "</h3>"
    var m = $("#C_TFR_modal")
    m.modal("show");
    var curr_list = returnCurrentList()
    var panel_year_code = curr_list[1].slice(0, curr_list[1].indexOf("-"))
    var panel_id = curr_list[1].slice((curr_list[1].indexOf("-") + 1))
    C_TFR_getFac(panel_year_code, panel_id, team_year_code, team_id)
}

// list all faculty for this team
function C_TFR_getFac(p_year_code, p_id, tyc, tid) {
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == XMLHttpRequest.DONE && this.status == 200) {
            let data = JSON.parse(this.responseText)
            var svgstr = '<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-trash"fill="currentColor" xmlns="http://www.w3.org/2000/svg"><pathd="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z" /><path fill-rule="evenodd"d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4L4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z" /></svg>'
            var strs = ['', '', '', '', '']
            var rc = [0, 0, 0, 0, 0]
            for (var i = 0; i < rc.length; ++i)
                rc[i] = 0
            for (let i of data) {
                strs[i["review_number"] - 1] += '<tr>'
                for (let j of ["fac_id", "fac_name", "fac_email"]) {
                    strs[i["review_number"] - 1] += ("<td>" + i[j] + "</td>")
                    rc[i["review_number"] - 1] = 1
                }
                strs[i["review_number"] - 1] += '<td scope="col"><button type="button" class="btn btn-lg btn-danger active" onclick="C_TFR_del(event,this)">' + svgstr + '</button></td></tr>'
            }
            for (var i = 1; i < 6; ++i) {
                if (rc[i - 1] != 0) {
                    document.getElementById("C_TFR_R" + i + "_table").style.display = "inline"
                    document.getElementById("C_TFR_R" + i + "_tbody").innerHTML = strs[i - 1]
                    document.getElementById("C_TFR_R" + i + "_tbody_error").innerHTML = ""
                }
                else {
                    document.getElementById("C_TFR_R" + i + "_table").style.display = "none"
                    document.getElementById("C_TFR_R" + i + "_tbody_error").innerHTML = "<div class=\"card\"><div class=\"card-body\">No faculty added</div></div>"
                }
            }
            add_fac_tfr_coordinator()
        }
    }
    var url = "/api/" + getCookie("username") + "/" + p_year_code + "-" + p_id + "/team-faculty-review/?team_id=" + tid + "&team_year_code=" + tyc;
    refreshLoader(xhttp)
    xhttp.open("GET", url, true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.send();
}

// 
function add_fac_tfr_coordinator(e, t) {
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == XMLHttpRequest.DONE && this.status == 200) {
            let data = JSON.parse(this.responseText)
            var str = ""
            for (let i of data) {
                str += "<option value='" + i["fac_id"] + "'>" + i["name"] + "</option>"
            }
            document.getElementById("faclist-C_TFR").innerHTML = str
        }
    }
    refreshLoader(xhttp)
    var curr_list = returnCurrentList()
    var panel_year_code = curr_list[1].slice(0, curr_list[1].indexOf("-"))
    var panel_id = curr_list[1].slice((curr_list[1].indexOf("-") + 1))
    xhttp.open("GET", "/api/" + getCookie("username") + "/" + panel_year_code + "-" + panel_id + "/faculty-panel/", true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.send();
    if (t) {
        var rno = t.parentNode.previousElementSibling.innerText.split('#')[1]
        document.getElementById("C_TFR_post_model_header").innerHTML = "Add faculty to review " + rno
    }
}

function C_TFR_post(e, t) {
    var xhttp = new XMLHttpRequest()
    var curr_list = returnCurrentList()
    var panel_year_code = curr_list[1].slice(0, curr_list[1].indexOf("-"))
    var panel_id = curr_list[1].slice((curr_list[1].indexOf("-") + 1))
    var team_year_code = document.getElementById('C_TFR_modal_title_heading').innerHTML.split(' ')[0]
    var team_id = document.getElementById('C_TFR_modal_title_heading').innerHTML.split(' ')[1]
    xhttp.onreadystatechange = function () {
        if (this.readyState == XMLHttpRequest.DONE) {
            if (this.status == 200) {
                let data = JSON.parse(this.responseText)
                C_TFR_getFac(panel_year_code, panel_id, team_year_code, team_id)
                d = data
                str = "<b>" + d["detail"] + "</b>"
                if (d["assumption"])
                    for (let i = 0; i < d["assumption"].length; ++i) {
                        str += "<br>" + d["assumption"][i]["detail"] + "<br>"
                    }
                document.getElementById('C_TFR_post_toast_header').innerHTML = 'SUCCESS'
                document.getElementById('C_TFR_post_toast_body').innerHTML = str
                var svg_tick = '<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-check-circle-fill" fill="green" xmlns="http://www.w3.org/2000/svg">'
                svg_tick += '<path fill-rule="evenodd" d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>'
                svg_tick += '</svg>'
                document.getElementById('C_TFR_post_svg').innerHTML = svg_tick

                $('#C_TFR_post_toast').toast('show');
            }
            else {
                var svg_cross = '<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-x-circle-fill" fill="red" xmlns="http://www.w3.org/2000/svg">'
                svg_cross += '<path fill-rule="evenodd" d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-4.146-3.146a.5.5 0 0 0-.708-.708L8 7.293 4.854 4.146a.5.5 0 1 0-.708.708L7.293 8l-3.147 3.146a.5.5 0 0 0 .708.708L8 8.707l3.146 3.147a.5.5 0 0 0 .708-.708L8.707 8l3.147-3.146z"/>'
                svg_cross += '</svg>'
                document.getElementById('C_TFR_post_svg').innerHTML = svg_cross
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
                document.getElementById('C_TFR_post_toast_header').innerHTML = 'FAILURE'
                document.getElementById('C_TFR_post_toast_body').innerHTML = str
                $('#C_TFR_post_toast').toast('show');
            }
        }
    }
    var fac_id = document.getElementById("C_TFR_post").children[1].value
    var review_number = document.getElementById("C_TFR_post_model_header").innerHTML.split(' ')[4]
    var jsonarray = { "team_id": team_id, "team_year_code": team_year_code, "fac_id": fac_id, "review_number": review_number }
    refreshLoader(xhttp)
    xhttp.open("POST", "/api/" + getCookie("username") + "/" + panel_year_code + "-" + panel_id + "/team-faculty-review/", true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("Content-type", "application/json;charset UTF-8");
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.send(JSON.stringify([jsonarray]));
}

function C_TFR_del(e, t) {
    var curr_list = returnCurrentList()
    var panel_year_code = curr_list[1].slice(0, curr_list[1].indexOf("-"))
    var panel_id = curr_list[1].slice((curr_list[1].indexOf("-") + 1))
    var team_year_code = document.getElementById('C_TFR_modal_title_heading').innerHTML.split(' ')[0]
    var team_id = document.getElementById('C_TFR_modal_title_heading').innerHTML.split(' ')[1]
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == XMLHttpRequest.DONE) {
            if (this.status == 200) {
                let data = JSON.parse(this.responseText)
                C_TFR_getFac(panel_year_code, panel_id, team_year_code, team_id)
                d = data
                str = "<b>" + d["detail"] + "</b>"
                if (d["assumption"])
                    for (let i = 0; i < d["assumption"].length; ++i) {
                        str += "<br>" + d["assumption"][i]["detail"] + "<br>"
                    }
                document.getElementById('C_TFR_delete_toast_header').innerHTML = 'SUCCESS'
                document.getElementById('C_TFR_delete_toast_body').innerHTML = str
                var svg_tick = '<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-check-circle-fill" fill="green" xmlns="http://www.w3.org/2000/svg">'
                svg_tick += '<path fill-rule="evenodd" d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>'
                svg_tick += '</svg>'
                document.getElementById('C_TFR_delete_svg').innerHTML = svg_tick
                document.getElementById("C_TFR_delete_toast").style.left = e.clientX + "px"
                document.getElementById("C_TFR_delete_toast").style.top = e.clientY + "px"
                $('#C_TFR_delete_toast').toast('show');
            }
            else {
                var svg_cross = '<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-x-circle-fill" fill="red" xmlns="http://www.w3.org/2000/svg">'
                svg_cross += '<path fill-rule="evenodd" d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-4.146-3.146a.5.5 0 0 0-.708-.708L8 7.293 4.854 4.146a.5.5 0 1 0-.708.708L7.293 8l-3.147 3.146a.5.5 0 0 0 .708.708L8 8.707l3.146 3.147a.5.5 0 0 0 .708-.708L8.707 8l3.147-3.146z"/>'
                svg_cross += '</svg>'
                document.getElementById('C_TFR_delete_svg').innerHTML = svg_cross
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
                document.getElementById('C_TFR_delete_toast_header').innerHTML = 'FAILURE'
                document.getElementById('C_TFR_delete_toast_body').innerHTML = str
                document.getElementById("C_TFR_delete_toast").style.left = e.clientX + "px"
                document.getElementById("C_TFR_delete_toast").style.top = e.clientY + "px"
                $('#C_TFR_delete_toast').toast('show');
            }
        }
    }
    var table_id = t.parentElement.parentElement.parentElement.parentElement.parentElement.id
    var review_number;
    if (table_id == "C_TFR_R1_table")
        review_number = 1
    else if (table_id == "C_TFR_R2_table")
        review_number = 2
    else if (table_id == "C_TFR_R3_table")
        review_number = 3
    else if (table_id == "C_TFR_R4_table")
        review_number = 4
    else
        review_number = 5
    var fac_id = t.parentElement.parentElement.children[0].innerHTML
    var jsonarray = { "team_id": team_id, "team_year_code": team_year_code, "fac_id": fac_id, "review_number": review_number }
    refreshLoader(xhttp)
    xhttp.open("DELETE", "/api/" + getCookie("username") + "/" + panel_year_code + "-" + panel_id + "/team-faculty-review/", true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("Content-type", "application/json;charset UTF-8");
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.send(JSON.stringify([jsonarray]));
}
function closemy(e) {
    e.preventDefault()

}

function admin_TFR_upload_csv(event) {
    const selectedFile = document.getElementById('admin_TFR_upload_file').files[0];
    const reader = new FileReader();
    reader.onload = function () {
        var TFR_create_json = []
        var linearray = reader.result.split('\n');
        for (var i = 0; i < linearray.length; i++) {
            if (linearray[i] != "") {
                lst = linearray[i].split(',')
                for (var j = 3; j < lst.length; j++) {
                    TFR_create_json.push({ 'team_year_code': lst[0], 'team_id': lst[1], 'review_number': lst[2], 'fac_id': lst[j] })
                }
            }
        }
        console.log(JSON.stringify(TFR_create_json))
        var xhttp = new XMLHttpRequest()
        xhttp.onreadystatechange = function () {
            if (this.readyState == XMLHttpRequest.DONE) {
                document.getElementById("admin_TFR_upload_file").value = null
                console.log(this.responseText)
            }
        }
        var curr_list = returnCurrentList()
        var panel_year_code = curr_list[1].slice(0, curr_list[1].indexOf("-"))
        var panel_id = curr_list[1].slice((curr_list[1].indexOf("-") + 1))
        refreshLoader(xhttp)
        xhttp.open("POST", "/api/" + getCookie("username") + "/" + panel_year_code + "-" + panel_id + "/team-faculty-review/", true);
        xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
        xhttp.setRequestHeader("Content-type", "application/json;charset=UTF-8");
        xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
        xhttp.send(JSON.stringify(TFR_create_json));
    }
    reader.readAsText(selectedFile);
}