var helptext = [
    "You can search the whole training sessions database for sessions completed on a specific date.\n\n" +
    "You can also inspect the data of your own latest training session on this page.",

    "After adding a few moves to the database, you can execute searches by providing a move name (or a part of it).\n\n" +
    "For example, searching with the phrase 'at' would return both 'squAT' and 'seATed dumbbell lATeral raise'.",

    "You can add a new exercise move to the database by providing a suitable name and clicking the 'Add' button.",

    "When you want to enter a new training session to the database, click the 'Start creating' button.\n\n" +
    "Select a move and add reps and the weights you used. When you are done, enter the set by clicking 'Add set'.\n\n" +
    "When you are satisfied with the whole session, click 'Save workout session' and save the session to database!\n\n" +
    "You can explore all saved sessions on the 'Search for sessions' page."

];

function showHelp(caller) {
    var text = "";
    if (caller == "searchsessions") {
        text = helptext[0];
    }

    if (caller == "allmoves") {
        text = helptext[1];
    }
    if (caller == "addmove") {
        text = helptext[2];
    }
    if (caller == "addsession") {
        text = helptext[3];
    }

    alert(text);
}

setTimeout(() => {
    // When we get a box showing save result on addsession page OR error message on searchsessions page, hide the box after 5 secs
    var resultbox = document.getElementById("resultbox");
    if (resultbox)
        resultbox.style.display = "none";
}, 5000);

function startCreating() {
    var sessionform = document.getElementById("session_form");

    if (sessionform.style.display === "none") {
        sessionform.style.display = "block";
    } else {
        sessionform.style.display = "none";
    }
}

function createTable(data) {
    var resultparagraph = document.getElementById("resultdiv");
    resultparagraph.innerHTML = ""; // remove existing content
    var resulttable = document.createElement("table");

    var header = document.createElement("thead");
    resulttable.appendChild(header);
    var headerRow = document.createElement("tr");
    resulttable.appendChild(headerRow);

    header = document.createElement("th");
    headerRow.appendChild(header);
    header.innerHTML = "ID";
    header = document.createElement("th");
    headerRow.appendChild(header);
    header.innerHTML = "Move name";

    var tableBody = document.createElement("tbody");
    resulttable.appendChild(tableBody);
    
    for (var i = 0; i < data.length; i++) {
        var row = document.createElement("tr");
        tableBody.appendChild(row);
        var cell1 = document.createElement("td"); // cell for move id
        row.appendChild(cell1);
        cell1.innerHTML = data[i].id;
        var cell2 = document.createElement("td"); // cell for move name
        row.appendChild(cell2);
        cell2.innerHTML = data[i].move_name;
    }

    resultparagraph.appendChild(resulttable);
}