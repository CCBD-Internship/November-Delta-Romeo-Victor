// generates a card for a team
function C_team_fac_review_cardmaker(team_year_code,team_id,team_name,description,guide) {
    str = '<div class="col mb-4"><div onclick="C_TFR_openmodal(event,this)" class="card bg-info" ><div class="card-header">' + team_year_code + '   ' + team_id + '    </div><div class="card-body"><h5 class="card-title">Name:  ' + team_name + '</h5><p>  Description:  ' + description + '</p><p>Guide:  '+guide+'</p></div></div></div>'
    return str
}

// fetches all teams in the panel
function C_TFR_refresh() {
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == XMLHttpRequest.DONE && this.status == 200) {
            let data = JSON.parse(this.responseText)
            var str = '<div class="row row-cols-1 row-cols-md-3" id="C_TFRcardchild">'
            for (let i in data) {
                str += C_team_fac_review_cardmaker(data[i]["team_year_code"], data[i]["team_id"], data[i]["team_name"], data[i]["description"], data[i]["guide"])
            }
            str+='</div>'
            document.getElementById("NVRD_coord_team_fac_review_card").innerHTML = str
        }
    }
    refreshLoader(xhttp)
    var curr_list = returnCurrentList()
    var panel_year_code = curr_list[1].slice(0, curr_list[1].indexOf("-"))
    var panel_id = curr_list[1].slice((curr_list[1].indexOf("-") + 1))
    xhttp.open("GET", "/api/" + getCookie("username") +"/"+panel_year_code+"-"+panel_id+ "/team/", true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.send();
}

coordinator_refresh = C_TFR_refresh

// opens modal for selected team
function C_TFR_openmodal(e, t) 
{
    var team_year_code = t.textContent.split(' ')[0]
    var team_id = t.textContent.split(' ')[3]
    document.getElementById("C_TFR_modal_title").innerHTML = "<h3>" + team_year_code + " " + team_id + "</h3>"
    var m = $("#C_TFR_modal")
    m.modal("show");
    var curr_list = returnCurrentList()
    var panel_year_code = curr_list[1].slice(0, curr_list[1].indexOf("-"))
    var panel_id = curr_list[1].slice((curr_list[1].indexOf("-") + 1))
    C_TFR_getFac(panel_year_code, panel_id)
}

// list all faculty for this team
function C_TFR_getFac(p_year_code, p_id) {
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == XMLHttpRequest.DONE && this.status == 200) {
            let data = JSON.parse(this.responseText)
            var svgstr = '<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-trash"fill="currentColor" xmlns="http://www.w3.org/2000/svg"><pathd="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z" /><path fill-rule="evenodd"d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4L4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z" /></svg>'
            var strs=['','','','','']
            for (let i of data) 
            {
                strs[i["review_number"]-1] += '<tr>'
                for (let j of ["fac_id", "fac_name", "fac_email"])
                    strs[i["review_number"]-1] += ("<td>" + i[j] + "</td>")
                strs[i["review_number"]-1] += '<td scope="col"><button type="button" class="btn btn-lg btn-danger active">' + svgstr + '</button></td></tr>'
            }
            if(strs[0] != "") 
                document.getElementById("C_TFR_R1_tbody").innerHTML = strs[0]
            else
                document.getElementById("C_TFR_R1_table").innerHTML="No faculty added"

            if(strs[1]!="") 
                document.getElementById("C_TFR_R2_tbody").innerHTML = strs[1]
            else
                document.getElementById("C_TFR_R2_table").innerHTML="No faculty added"

            if(strs[2]!="") 
                document.getElementById("C_TFR_R3_tbody").innerHTML = strs[2]
            else
                document.getElementById("C_TFR_R3_table").innerHTML="No faculty added"
            if(strs[3]!="") 
                document.getElementById("C_TFR_R4_tbody").innerHTML = strs[3]
            else
                document.getElementById("C_TFR_R4_table").innerHTML="No faculty added"
            if(strs[4]!="") 
                document.getElementById("C_TFR_R5_tbody").innerHTML = strs[4]
            else
                document.getElementById("C_TFR_R5_table").innerHTML="No faculty added"
            console.log(strs)
        }
    }
    var url = "/api/" + getCookie("username") +"/"+p_year_code+"-"+p_id+ "/team-faculty-review/";
    refreshLoader(xhttp)
    xhttp.open("GET", url, true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.send();
}

function Addfacpanel_A() {
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == XMLHttpRequest.DONE && this.status == 200) {
            let data = JSON.parse(this.responseText)
            var str = ""
            for (let i of data) {
                str += "<option value='" + i["fac_id"] + "'>" + i["name"] + "</option>"
            }
            document.getElementById("faclist-facpanel_A").innerHTML = str
        }
    }
    refreshLoader(xhttp)
    xhttp.open("GET", "/api/" + getCookie("username") + "/faculty/?inactive=1", true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.send();
}

function facpanel_post_Admin(e, t) {
    var pyc = document.getElementById("Faculty_panel_modal").firstElementChild.innerHTML.split(' ')[0]
    var pid = document.getElementById("Faculty_panel_modal").firstElementChild.innerHTML.split(' ')[1]
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == XMLHttpRequest.DONE && this.status == 201) {
            let data = JSON.parse(this.responseText)
            C_TFR_getFac(pyc, pid)
            Addfacpanel_A()
        }
    }
    var iscord = document.getElementById("isfac_activeforpanel").checked
    var jsonarray = { "panel_year_code": pyc, "panel_id": pid, "fac_id": $("#faclist-facpanel_A").val(), "is_coordinator": iscord }
    refreshLoader(xhttp)
    xhttp.open("POST", "/api/" + getCookie("username") + "/faculty-panel/", true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("Content-type", "application/json;charset UTF-8");
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.send(JSON.stringify([jsonarray]));

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

function fac_panel_delete_A() {
    var checkedBoxes = getCheckedBoxes_A("fac_panel_boxes_A");
    if (checkedBoxes.length > 0) {
        a = []
        var pyc = document.getElementById("Faculty_panel_modal").firstElementChild.innerHTML.split(' ')[0]
        var pid = document.getElementById("Faculty_panel_modal").firstElementChild.innerHTML.split(' ')[1]
        for (i = 0; i < checkedBoxes.length; i++) {
            a.push({ "panel_year_code": pyc, "panel_id": pid, "fac_id": checkedBoxes[i].parentElement.parentElement.children[1].textContent })
        }
        var modal = $("#A_fac_panel_DeleteconfirmModal");
        modal.modal("show");
        $("#A_fac_panel_DeleteconfirmMessage").empty().append("Do you want to delete " + a.length + " Faculty from this panel?");
        $('#A_fac_panel_DeleteconfirmOk')
            .on('click', function (e) {
                e.preventDefault();
                fac_panel_send_delete_A(a);
                $('#A_fac_panel_DeleteconfirmModal').modal('hide');
            });
        $("#A_fac_panel_DeleteconfirmCancel").on('click', function (e) {
            e.preventDefault();
            $('#A_fac_panel_DeleteconfirmModal').modal('hide');
        });
    }
}

function fac_panel_send_delete_A(fac) {
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == XMLHttpRequest.DONE && this.status == 201) {
            C_TFR_getFac(fac[0]["panel_year_code"], fac[0]["panel_id"])
        }
    }
    refreshLoader(xhttp)
    xhttp.open("DELETE", "/api/" + getCookie("username") + "/faculty-panel/", true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("Content-type", "application/json;charset=UTF-8");
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.send(JSON.stringify(fac));

}

function admin_faculty_panel_put_form(t) {
    var if_checked = document.getElementById("isfac_activeforpanel_put")
    var head = t.parentNode.parentNode.children
    var modal = document.getElementById("admin_faculty_panel_details_put").children
    if_checked.checked = head[5].textContent == "true"
    var fac = document.getElementById("fac_panel_put_A")
    fac.textContent = "Edit Co-ordinator " + head[1].textContent
}

function admin_faculty_panel_put() {
    var pyc = document.getElementById("Faculty_panel_modal").firstElementChild.innerHTML.split(' ')[0]
    var pid = document.getElementById("Faculty_panel_modal").firstElementChild.innerHTML.split(' ')[1]
    var fac = document.getElementById("fac_panel_put_A").textContent.split(' ')[2]
    var jsonarray = { "panel_year_code": pyc, "panel_id": pid, "is_coordinator": document.getElementById("isfac_activeforpanel_put").checked, "fac_id": fac }
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == XMLHttpRequest.DONE && this.status == 201) {
            C_TFR_getFac(pyc, pid)
        }
    }
    refreshLoader(xhttp)
    xhttp.open("PUT", "/api/" + getCookie("username") + "/faculty-panel/", true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("Content-type", "application/json;charset=UTF-8");
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.send(JSON.stringify([jsonarray]));
}