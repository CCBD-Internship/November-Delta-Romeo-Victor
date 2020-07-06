evaluator_refresh=evaluator_evaluations_refresh

function evaluator_evaluations_refresh()
{
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == XMLHttpRequest.DONE && this.status == 200) {
            let data = JSON.parse(this.responseText)
            var str = '<div class="row row-cols-1 row-cols-md-3" id="C_TFRcardchild">'
            for (let i in data) {
                str += C_team_fac_review_cardmaker(data[i]["team_year_code"], data[i]["team_id"], data[i]["team_name"], data[i]["description"], data[i]["guide"])
            }
            str += '</div>'
            document.getElementById("evaluation_team_cards").innerHTML = str
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

function E_evaluations_opentip()
{
    
}

