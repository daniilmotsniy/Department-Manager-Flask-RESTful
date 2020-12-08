function onClick(){
    let name = document.getElementById('name');

    values = {
        'name': name.value,
    }

    fetch(`/api/departments_list`, {
            method: 'POST',
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