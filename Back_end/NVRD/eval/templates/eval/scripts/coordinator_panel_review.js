coordinator_refresh = panel_review_refresh_coordinator

var PanelReviewValues;

var PRC_setInt = null

function PRC_time_modal(e) {
    $('.alert').alert()
    var title = "Set Review-"
    if (e.target.getAttribute('name')) {
        rno = e.target.getAttribute('name').split('_')[1]
        title += rno
        title += ' Evaluation Timings'
        document.getElementById("PRC_time_title").innerHTML = title
        var open_time = moment(PanelReviewValues[rno - 1]["open_time"])
        var close_time = moment(PanelReviewValues[rno - 1]["close_time"])
        document.getElementById("PRC_time_form").elements[0].value = open_time.format('YYYY-MM-DDThh:mm')
        document.getElementById("PRC_time_form").elements[1].value = close_time.format('YYYY-MM-DDThh:mm')
        $('#PRC_time_modal').modal('show')
    }
}

function PRC_display_modal(e) {
    var title = "Review-"
    rno = e.target.getAttribute("name").split('_')[2]
    title += rno
    title += ' Evaluation Timings'
    document.getElementById("PRC_display_title").innerHTML = title
    document.getElementById("PRC_display_open_time").innerHTML = '<h4><strong><pre><code>' + (new Date(PanelReviewValues[rno - 1]["open_time"])).toLocaleString() + '</code></pre></strong></h4>'
    document.getElementById("PRC_display_close_time").innerHTML = '<h4><strong><pre><code>' + (new Date(PanelReviewValues[rno - 1]["close_time"])).toLocaleString() + '</code></pre></strong></h4>'
    $('#PRC_display_modal').modal('show')
}

function PRC_submit() {
    var rno = parseInt(document.getElementById("PRC_time_title").innerHTML.split('-')[1][0], 10)
    PanelReviewValues[rno - 1]["open_time"] = (new Date(moment(document.getElementById("PRC_time_form").elements[0].value).format())).toISOString()
    PanelReviewValues[rno - 1]["close_time"] = (new Date(moment(document.getElementById("PRC_time_form").elements[1].value).format())).toISOString()
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == XMLHttpRequest.DONE && this.status == 202) {
            panel_review_refresh_coordinator()
            $('#PRC_time_modal').modal('hide')
        }
    }
    var curr_list = returnCurrentList()
    var panel_id = curr_list[1].slice(0, curr_list[1].indexOf("-"))
    var panel_year_code = curr_list[1].slice((curr_list[1].indexOf("-") + 1))
    refreshLoader(xhttp)
    xhttp.open("PUT", "/api/" + getCookie("username") + "/" + panel_id + "-" + panel_year_code + "/panel-review/", true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.setRequestHeader("Content-type", "application/json;charset UTF-8");
    xhttp.send(JSON.stringify(PanelReviewValues))
}

function panel_review_refresh_coordinator() {
    document.getElementById("PRC_time_form_submit").addEventListener('click', PRC_submit)
    for (let i = 1; i <= 5; i++) {
        var card = document.getElementsByName("PRC_" + i.toString())
        for (let j = 0; j < card.length; j++) {
            card[j].addEventListener('click', PRC_time_modal)
        }
        var board = document.getElementsByName("C_R_" + i.toString())
        for (let j = 0; j < board.length; j++) {
            board[j].addEventListener('click', PRC_display_modal)
            board[j].addEventListener('mouseover', PRC_display_status)
        }
    }
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == XMLHttpRequest.DONE && this.status == 200) {
            PanelReviewValues = JSON.parse(this.responseText)
            PRC_setColor()
            if (PRC_setInt != null) {
                clearInterval(PRC_setInt)
            }
            setInterval(PRC_setColor, 2 * 60 * 1000)
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

function PRC_setColor() {
    for (var i = 1; i <= 5; i++) {
        elem = document.getElementById("review_board_" + i.toString())
        if (elem) {
            var open_time = new Date(PanelReviewValues[i - 1]["open_time"])
            var close_time = new Date(PanelReviewValues[i - 1]["close_time"])
            var now = new Date()
            if (now.getTime() < open_time.getTime() && open_time.getTime() < close_time.getTime()) {
                elem.setAttribute('class', 'card bg-warning ')
            }
            else if (now.getTime() > open_time.getTime() && now.getTime() < close_time.getTime()) {
                elem.setAttribute('class', 'card bg-success blink_me')
            }
            else {
                elem.setAttribute('class', 'card bg-danger')
            }
        }
    }
}

function PRC_display_status(e) {
    var title = "Review-"
    rno = e.target.getAttribute("name").split('_')[2]
    title += rno
    title += ' Status'
    document.getElementById("PRC_status_title").innerHTML = title
    var open_time = new Date(PanelReviewValues[parseInt(rno, 10) - 1]["open_time"])
    var close_time = new Date(PanelReviewValues[parseInt(rno, 10) - 1]["close_time"])
    var now = new Date()
    elem = document.getElementById("PRC_status_body")
    if (now.getTime() < open_time.getTime() && open_time.getTime() < close_time.getTime()) {
        elem.textContent = "Evaluation window opens on " + open_time.toLocaleDateString() + " at " + open_time.toLocaleTimeString()
    }
    else if (now.getTime() > open_time.getTime() && now.getTime() < close_time.getTime()) {
        elem.textContent = "Evaluation window is open now!! shall close in approximately " + diff_hours(close_time, now)[0] + " days " + diff_hours(close_time, now)[1] + " hours " + diff_hours(close_time, now)[2] + " minutes"
    }
    else {
        elem.textContent = "Evaluation window was closed on " + close_time.toLocaleDateString() + " at " + close_time.toLocaleTimeString()
    }
}