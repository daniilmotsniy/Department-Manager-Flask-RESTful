// GET request
    fetch("/api/departments_list")
        .then((response) => response.json())
        .then((departments)=> {
            responseReceived(departments);
        })
        .catch((error) => console.log(error))
    fetch("/api/employees_list")
        .then((response2) => response2.json())
        .then((employees)=> {
            employeesReceived(employees);
        })
        .catch((error) => console.log(error))

function responseReceived(departments){
    if(departments.length == 0){
//        let empty = document.getElementById("empty");
//        let text = document.createTextNode("No departments were found");
//        empty.appendChild(text);
    } else {
        let dataToDisplay = [];
        dataToDisplay = formDataToDisplay(departments);
        let table = document.querySelector("table");
        generateTable(table, dataToDisplay, Object.keys(dataToDisplay[0]), 'departments');
        generateTableHead(table, Object.keys(dataToDisplay[0]).slice(1));
    }
}

function employeesReceived(employees){
    if(employees.length == 0){
//        let empty = document.getElementById("empty");
//        let text = document.createTextNode("No departments were found");
//        empty.appendChild(text);
    } else {
        let dataToDisplay = [];
        employeesToDisplay = formEmployeeToDisplay(employees);
        let table = document.querySelector("table");
        editTable(table, employeesToDisplay);
    }
}

function formDataToDisplay(data){
    let dataToDisplay = [];
    for(let i = 0; i < data.length; i++){
        let object = data[i];
        let department = {
            'id': object['id'],
            'Name': object['name'],
        }
        dataToDisplay.push(department);
    }
    return dataToDisplay;
}

function formEmployeeToDisplay(data){
    let dataToDisplay = [];
    for(let i = 0; i < data.length; i++){
         let object = data[i];
         let employee = {
            'Salary': object['salary'],
            'Department': object['department'],
         }
         dataToDisplay.push(employee);
     }
    return dataToDisplay;
}

function sendDeleteRequest(id){
    fetch(`/api/departments/${id}`, {
            method: 'DELETE'
        })
        .then((response) => response.json())
        .then((data)=> {
            window.location.href = `/departments`;
        })
        .catch((error) => console.log(error))
}

function generateTableHead(table, headers){
    let thead = table.createTHead();
    let row = thead.insertRow();
    headers.push('Average');
    headers.push('Edit');
    headers.push('Delete');
    for (let key of headers) {
        let th = document.createElement("th");
        let text = document.createTextNode(key);
        th.appendChild(text);
        row.appendChild(th);
    }
}

function get_avg(department_name, employees_list){
    let sum = 0;
    let count = 0;
    for(let i=0; i < employees_list.length; i++){
        if(employees_list[i]['Department']===department_name){
            sum += employees_list[i]['Salary'];
            count += 1;
        }
    }
    if(count==0)
        return 0;
    return sum/count;
}

function generateTable(table, data, keys, object){
    for(let i = 0; i < data.length; i++) {
        let element = data[i];
        let row = table.insertRow();
        for(let j = 1; j < keys.length; j++) {
            let cell = row.insertCell();
            let text = document.createTextNode(element[keys[j]]);
            cell.appendChild(text);
        }
        // Edit href
        let cell = row.insertCell();
        let a = document.createElement("a");
        a.setAttribute("href", `/${object}/edit_department/${element['id']}`);
        let text = document.createTextNode("Edit");
        a.appendChild(text);
        a.classList.add("btn-outline-info");
        let cont = document.createElement("div");
        cell.appendChild(a);
        // Delete href
        cell = row.insertCell();
        a = document.createElement("a");
        a.setAttribute("onclick", `sendDeleteRequest(${element['id']})`)
        a.setAttribute("href", "#");
        text = document.createTextNode("Delete");
        a.appendChild(text);
        a.classList.add("btn-outline-danger");
        cell.appendChild(a);
    }
}

function editTable(table, data){
    for(let i = 1; i < table.rows.length; i++) {
        let element = data[i-1];
        let row = table.rows[i];
        let cell = row.insertCell(1);
        let text = document.createTextNode('0');
        text = document.createTextNode(get_avg(table.rows[i].cells[0].innerHTML, data) + "$");
        console.log(text)
        cell.appendChild(text);
    }
}
