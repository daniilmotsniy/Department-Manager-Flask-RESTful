// GET request
let id = document.URL.substring(document.URL.lastIndexOf('/') + 1);

    fetch(`/api/departments/${id}`)
        .then((response) => response.json())
        .then((department)=> {
            responseReceived(department);
        })
        .catch((error) => console.log(error))

function responseReceived(department){
    if(department.length == 0){
//        let empty = document.getElementById("empty");
//        let text = document.createTextNode("No departments were found");
//        empty.appendChild(text);
    } else {
        let name = document.getElementById('name');
        name.setAttribute('value', department['name']);
    }
}

function onClick(){
    let name = document.getElementById('name');

    values = {
        'name': name.value,
    }

    fetch(`/api/departments/${id}`, {
            method: 'PUT',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(values)
        })
        .then((response) => response.json())
        .then((values)=> {
                console.log(values)
                window.location = '/departments';
        })
        .catch((error) => console.log(error))
}