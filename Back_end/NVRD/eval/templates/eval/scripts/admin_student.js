function student_refresh() {
    tbody = document.getElementById("student_body")

    var xhttp = new XMLHttpRequest()
    console.log('hi')
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            let data = JSON.parse(this.responseText)
            console.log(data)
            for (let i in data) {
                // document.getElementById("student_body").innerHTML += '<tr><th scope="row">1</th>'
                var str='<tr><th scope="row">1</th>'
                for (let j in data[i]) {
                    str += ("<td>" + data[i][j] + "</td>")
                }
                str+='</tr>'
                document.getElementById("student_body").innerHTML += str
            }
        }
    }
    // let facid = document.getElementById("username").value
    // let panel_id = document.getElementById("panel_id_stu_get").value
    // let panel_year_code = document.getElementById("panel_year_code_stu_get").value
    // let review_number = document.getElementById("review_number_stu_get").value
    // let srn = document.getElementById("srn_stu_get").value
    // let name = document.getElementById("name_stu_get").value

    xhttp.open("GET", "/api/" + 'kvs1' + "/" + "PN_2020" + "-" + '0000000001' + "/student/", true);
    // var url = ""
    // if (srn)
    //     url += "?srn=" + srn
    // if (name)
    //     url += "&name=" + name
    // if (name && !url)
    //     if (!url)
    //         url += "&name=" + name

    // if (panel_id && (panel_year_code && review_number))
    //     xhttp.open("GET", "/api/" + facid + "/" + panel_year_code + "-" + panel_id + "/" + review_number + "/student/" + url, true);
    // if (panel_id && panel_year_code)

    // else
    //     xhttp.open("GET", "/api/" + facid + "/student/" + url, true);
    /*if(!token)
    {
      alert("Please Get A token First")
      return
    }*/

    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTkzMjY0NjYwLCJqdGkiOiI5YWU1Mzk0YTEzMTU0YzczYmFjZDMzMjljMzk5MjAzOSIsInVzZXJfaWQiOjJ9.foXlT0sK9fvzyxLc6CPBUzxy0vDZFaekBOxhqZaQz50"
    xhttp.setRequestHeader("Authorization", "Bearer " + token);
    xhttp.send();

}