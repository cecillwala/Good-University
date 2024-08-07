document.addEventListener('DOMContentLoaded', () => {
    ShowPage("#main", "#profile");
    document.querySelector("#csv").addEventListener('change', () => first_year_admin());
    document.querySelector("#upload-student").addEventListener('click', () => register_student());
    document.querySelector("#lec-csv").addEventListener('change', () => register_lecturers());
    const d =new Date();
});


function ShowPage(page, section){
   const children = Array.from(document.querySelector(page).children);
    children.forEach(child => {
        child.style.display = 'none';
    });
    document.querySelector(section).style.display = 'block';
} 


function first_year_admin(){
    const file_name = document.querySelector("#csv").value.split("\\");
    document.querySelector("#upload").value = file_name[2];
    document.querySelector("#status").outerHTML = `
    <div id="status" class="alert alert-danger">
        <strong>Warning!</strong> Submitting file has no reverse process.
    </div>
    `;
    document.querySelector("#upload-form").addEventListener('submit', (event) => {
        event.preventDefault();
        fetch('upload', {
            method:'POST',
            body: {file: document.querySelector("#csv").files[0],
                    user: document
            }
        })
        .then(response => response.json())
        .then(status => {
            console.log(status);
            if(status.status == 200){
                document.querySelector("#csv").setAttribute('disabled', true);
                document.querySelector("#status").outerHTML = `
                <div class="alert alert-success">
                    <strong>Success.</strong> Student's file uploaded successfully.
                </div>
                `;
            }
            else{
                document.querySelector("#status").outerHTML = `
                <div class="alert alert-danger">
                    <strong>Danger!</strong> Indicates a dangerous or potentially negative action.
                </div>`;
            }
        });
    });
}


function register_lecturers(){
    console.log("Inafika hapa");
    const file_name = document.querySelector("#lec-csv").value.split("\\");
    document.querySelector("#upload").value = file_name[2];
    document.querySelector("#status").outerHTML = `
    <div id="status" class="alert alert-danger">
        <strong>Warning!</strong> Submitting file has no reverse process.
    </div>
    `;
    document.querySelector("#lec-upload-form").addEventListener('submit', (event) => {
        event.preventDefault();
        fetch('upload_lecturers', {
            method: 'POST', 
            body: document.querySelector("#lec-csv").files[0]
        })
        .then(response => response.json())
        .then(status => {
            if(status == 200){
                document.querySelector('#status').outerHTML = `
                <div class="alert alert-success">
                    <strong>Success.</strong> Lecturer's file uploaded successfully.
                </div>
                `;
            }
            else{
                document.querySelector("#status").outerHTML = `
                <div class="alert alert-danger">
                    <strong>Danger!</strong> Indicates a dangerous or potentially negative action.
                </div>
                `;
            }
        })
    });
}


function register_student(){
    ShowPage("#student-registration","#single-student");
    document.querySelector("#student").addEventListener('submit', (event) => {
        event.preventDefault();
        fetch('register_student', {
            method: 'POST', 
            body: JSON.stringify({
                first_name: document.querySelector("#first-name").value,
                last_name: document.querySelector("#last-name").value,
                phone_number: document.querySelector("#national-id").value,
                course: document.querySelector("#course").value
            })
        })
        .then(response => response.json())
        .then(status => console.log(status));
        ShowPage("#student-registration", "#file-upload");
    });
}

function registration_view(){
    ShowPage('#main', '#student-registration');
    ShowPage('#student-registration', '#file-upload');
}