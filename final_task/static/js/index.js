// GET request
fetch("/api/employees_list")
    .then((response) => response.json())
    .then((employees)=> {
        console.log(employees)
        responseReceived(employees)
    })
    .catch((error) => console.log(error))

function responseReceived(employees){
    if(employees.length == 0){
//        let empty = document.getElementById("empty");
//        let text = document.createTextNode("No departments were found");
//        empty.appendChild(text);
    } else {
        let dataToDisplay = formDataToDisplay(employees);
        console.log(dataToDisplay);

        let table = document.createElement('table');
        table.className = "table table-hover table-bordered margin-top";

        for(let i = 0; i < dataToDisplay.length; i++ ) {
          let child = dataToDisplay[i];
          if(i === 0){
            addHeaders(table, Object.keys(child));
          }
          let row = table.insertRow();
          Object.keys(child).forEach(function(k) {
            let cell = row.insertCell();
            if(k==='Salary'){
                cell.appendChild(document.createTextNode(child[k] + "$"));
            } else {
                cell.appendChild(document.createTextNode(child[k]));
            }
          })
        }

        function addHeaders(table, keys) {
          let row = table.insertRow();
          for(let i = 0; i < keys.length; i++ ) {
              keys.forEach(function(k) {
                if(k==='id'){
                    let th = document.createElement("th");
                    let text = document.createTextNode(keys[i]);
                    th.appendChild(text);
                    row.appendChild(th);
                }
              })
          }
        }
        document.getElementById('data').appendChild(table);
    }
}

function formDataToDisplay(data){
    let dataToDisplay = [];
    for(let i = 0; i < data.length; i++){
        let object = data[i];
        let department = {
            'id': object['id'],
            'Name': object['name'],
            'Department': object['department'],
            'Birth date': object['b_date'],
            'Salary': object['salary']
        }
        dataToDisplay.push(department);
    }
    return dataToDisplay;
}