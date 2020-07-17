var student_portal_store
var student_portal_setInt = null

function student_portal_refresh_admin() {
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == XMLHttpRequest.DONE && this.status == 200) {
            student_portal_store = JSON.parse(this.responseText)
            if (student_portal_setInt) {
                clearInterval(student_portal_setInt)
            }
            student_portal_status_display()
            student_portal_setInt = setInterval(student_portal_status_display, 60 * 1000)
        }
    }
    refreshLoader(xhttp)
    xhttp.open("GET", "/api/" + getCookie("username") + "/student-portal/", true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.send()
}

function student_portal_display_modal() {
    document.getElementById("student_portal_display_title").innerHTML = "Student Portal Timings"
    document.getElementById("student_portal_display_open_time").innerHTML = '<h4><strong><pre><code>' + (new Date(student_portal_store["open_time"])).toLocaleString() + '</code></pre></strong></h4>'
    document.getElementById("student_portal_display_close_time").innerHTML = '<h4><strong><pre><code>' + (new Date(student_portal_store["close_time"])).toLocaleString() + '</code></pre></strong></h4>'
    $('#student_portal_display_modal').modal('show')
}

function student_portal_submit() {
    student_portal_store["open_time"] = (new Date(moment(document.getElementById("student_portal_time_form").elements[0].value).format())).toISOString()
    student_portal_store["close_time"] = (new Date(moment(document.getElementById("student_portal_time_form").elements[1].value).format())).toISOString()
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == XMLHttpRequest.DONE && this.status == 202) {
            student_portal_refresh_admin()
            $('#student_portal_time_modal').modal('hide')
        }
    }
    refreshLoader(xhttp)
    xhttp.open("PUT", "/api/" + getCookie("username") + "/student-portal/", true);
    xhttp.setRequestHeader("Authorization", "Bearer " + getCookie("token"));
    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.setRequestHeader("Content-type", "application/json;charset UTF-8");
    xhttp.send(JSON.stringify(student_portal_store))
}

function student_portal_time_modal(e) {
    var title = "Set Student Portal Timings"
    document.getElementById("student_portal_time_title").innerHTML = title
    var open_time = moment(student_portal_store["open_time"])
    var close_time = moment(student_portal_store["close_time"])
    document.getElementById("student_portal_time_form").elements[0].value = open_time.format('YYYY-MM-DDThh:mm')
    document.getElementById("student_portal_time_form").elements[1].value = close_time.format('YYYY-MM-DDThh:mm')
    $('#student_portal_time_modal').modal('show')

}

function student_portal_status_display() {
    document.getElementById("student_portal_status_title").innerHTML = "Status"
    var open_time = new Date(student_portal_store["open_time"])
    var close_time = new Date(student_portal_store["close_time"])
    var now = new Date()
    if (now.getTime() > open_time.getTime() && now.getTime() < close_time.getTime()) {
        document.getElementById('student_portal_board').setAttribute('class', 'card bg-success blink_me_sp')
    }
    else {
        document.getElementById('student_portal_board').setAttribute('class', 'card bg-danger')
    }
    elem = document.getElementById("student_portal_status_body")
    if (now.getTime() < open_time.getTime() && open_time.getTime() < close_time.getTime()) {
        elem.textContent = "Student Portal closed"
    }
    else if (now.getTime() > open_time.getTime() && now.getTime() < close_time.getTime()) {
        elem.textContent = "Student Portal open now!! shall close in approximately " + diff_hours(close_time, now)[0] + " days " + diff_hours(close_time, now)[1] + " hours " + diff_hours(close_time, now)[2] + " minutes"
    }
    else {
        elem.textContent = "Student Portal closed"
    }
}

admin_refresh = student_portal_refresh_admin