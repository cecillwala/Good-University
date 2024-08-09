document.addEventListener('DOMContentLoaded', () => {
    ShowPage("#main", "#profile");
    document.querySelector("#csv").addEventListener('change', () => first_year_admin());
    document.querySelector("#lec-csv").addEventListener('change', () => register_lecturers());
});


function ShowPage(page, section){
   const children = Array.from(document.querySelector(page).children);
    children.forEach(child => {
        child.style.display = 'none';
    });
    document.querySelector(section).style.display = 'block';
} 


function first_year_admin(){
    document.querySelector("#upload").setAttribute('class','btn btn-outline-success me-2');
    const file_name = document.querySelector("#csv").value.split("\\");
    document.querySelector("#upload").value = file_name[2];
    document.querySelector("#status").outerHTML = `
    <div id="status" class="alert alert-danger">
        <strong>Warning! Submitting file has no reverse process!</strong>
    </div>
    `;
    document.querySelector("#upload-form").addEventListener('submit', (event) => {
        event.preventDefault();
        fetch('upload_students', {
            method:'POST',
            body: document.querySelector("#csv").files[0]
        })
        .then(response => response.json())
        .then(status => {
            warnings(status, '#status','Student');
        });
    });
}


function register_lecturers(){
    console.log("Inafika hapa");
    const file_name = document.querySelector("#lec-csv").value.split("\\");
    document.querySelector("#upload").value = file_name[2];
    document.querySelector("#status").outerHTML = `
    <div id="status" class="alert alert-danger">
        <strong>Warning! Submitting file has no reverse process!</strong>
    </div>
    `;
    document.querySelector("#lec-upload-form").addEventListener('submit', (event) => {
        event.preventDefault();
        fetch('upload_lecturers', {
            method: 'POST', 
            body: document.querySelector("#lec-csv").files[0]
        })
        .then(response => response.json())
        .then(status => warnings(status, '#lec-status','Lecturer'));
    });
}


function register_student(){
    ShowPage("#student-registration","#single-student");
    document.querySelector("#student-form").addEventListener('submit', (event) => {
        event.preventDefault();
        fetch('register_student', {
            method: 'POST', 
            body: JSON.stringify({
                first_name: document.querySelector("#first-name").value,
                last_name: document.querySelector("#last-name").value,
                phone_number: document.querySelector("#phone-number").value,
                nationalID: document.querySelector("#national-id").value,
                gender: document.querySelector("#gender").value,
                course: document.querySelector("#course").value
            })
        })
        .then(response => response.json())
        .then(status => {
            document.querySelector("#first-name").value = '';
            document.querySelector("#last-name").value  = '';
            document.querySelector("#phone-number").value = '';
            document.querySelector("#national-id").value = '';
            document.querySelector("#gender").value = '';
            document.querySelector("#course").value = '';
            warnings(status, '#single-status', 'Student');
        });
    });
}

function registration_view(){
    ShowPage('#main', '#student-registration');
    const d = new Date();
    month = d.getMonth();
    // if (month >= 7){
    //     console.log(month);
    //     ShowPage('#student-registration', '#state');
    //     document.querySelector("#state").innerHTML = `
    //     <h4>${d.getFullYear()}/${d.getFullYear() + 1} Student Registration ended on the 31st of July.</h4>
    //     `;
    // }
    // else{
        ShowPage('#student-registration', '#file-upload');
    // }
}


function warnings(status, section, user){
    console.log(status);
    console.log(status.status);
    switch(status.status){
        case 935:
            document.querySelector(section).outerHTML = `
        <div class="alert alert-danger" id=${section}>
            <strong>935 ERROR! ${user}(s) already exists!</strong>
        </div>`;
        case 912:
        document.querySelector(section).outerHTML = `
            <div class="alert alert-danger" id=${section}>
                <strong>912 ERROR! Invalid course entered!</strong>
            </div>`;
        case 900:
            document.querySelector(section).outerHTML = `
            <div class="alert alert-danger" id=${section}>
                <strong>900 ERROR! File is in the wrong format!
                Ensure the following fields are present: first_name, last_name, phone_number, 
                nationalID, gender and course!</strong>
            </div>`;
        case 200:
            document.querySelector(section).outerHTML = `
            <div class="alert alert-success" id=${section}>
                <strong>Success! Student's details uploaded successfully!</strong>
            </div>
            `;
    }
}
