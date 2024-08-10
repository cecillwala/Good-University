document.addEventListener('DOMContentLoaded', () => {

});


function ShowPage(page, section){
    const children = Array.from(document.querySelector(page).children);
    children.forEach(child => {
        child.style.display = 'none';
    });
    document.querySelector(section).style.display = 'block';
}


function upload_lecturers(){
    ShowPage("#main", "#lecturer-registration");
    ShowPage("#lecturer-registration", "#file-upload");
    document.querySelector("#lec-csv").addEventListener('change', () => {
        document.querySelector("#upload").setAttribute('class','btn btn-outline-success me-2');
        const file_name = document.querySelector("#lec-csv").value.split("\\");
        document.querySelector("#upload").value = file_name[2];
        document.querySelector("#status").outerHTML = `
        <div id="status" class="alert alert-danger">
            <strong>Warning! Submitting file has no reverse process!</strong>
        </div>
        `;
    });
    document.querySelector("#file-upload").addEventListener('submit', (event) => {
        event.preventDefault();
        fetch('upload_lecturers', {
            method: 'POST',
            body: document.querySelector("#lec-csv").files[0]
        })
        .then(response => response.json())
        .then(status => warnings(status, "#status"));
    });
}


function register_lecturer(){
    ShowPage("#lecturer-registration","#single-lecturer");
    document.querySelector("#lecturer-form").addEventListener('submit', (event) => {
        event.preventDefault();
        fetch('register_lecturer', {
            method:'POST',
            body: JSON.stringify({
                first_name: document.querySelector("#first-name").value,
                last_name: document.querySelector("#last-name").value,
                phone_number: document.querySelector("#phone-number").value,
                nationalID: document.querySelector("#national-id").value,
                gender: document.querySelector("#gender").value,
                faculty: document.querySelector("#faculty").value,
                department: document.querySelector("#department").value
            })
        })
        .then(response => response.json())
        .then(status => warnings(status, "#single-status"))
    });
}


function warnings(status, section){
    console.log(status);
    console.log(status.status);
    switch(status.status){
        case 935:
            document.querySelector(section).outerHTML = `
        <div class="alert alert-danger" id=${section}>
            <strong>935 ERROR! User(s) already exists!</strong>
        </div>`;
        case 912:
        document.querySelector(section).outerHTML = `
            <div class="alert alert-danger" id=${section}>
                <strong>912 ERROR! Invalid department entered!</strong>
            </div>`;
        case 900:
            document.querySelector(section).outerHTML = `
            <div class="alert alert-danger" id=${section}>
                <strong>900 ERROR! File is in the wrong format!
                Ensure the following fields are present: first_name, last_name, phone_number, 
                nationalID, gender, faculty, department, course!</strong>
            </div>`;
        case 200:
            document.querySelector(section).outerHTML = `
            <div class="alert alert-success" id=${section}>
                <strong>Success! User's details uploaded successfully!</strong>
            </div>
            `;
    }
}