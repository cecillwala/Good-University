document.addEventListener('DOMContentLoaded', () => {
    ShowPage("#main", "#profile");
    document.querySelector("#csv").addEventListener('change', () => first_year_admin());
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
            warnings(status, 'status','Student');
        });
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
                course: document.querySelector("#course").value,
                faculty: document.querySelector("#faculty").value,
                department: document.querySelector("#department").value
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
            warnings(status, 'single-status', 'Student');
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


function upload_lecturers(){
    ShowPage("#main", "#lecturer-registration");
    ShowPage("#lecturer-registration", "#lec-file-upload");
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
        .then(status => warnings(status, "status", "Lecturer"));
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
        .then(status => warnings(status, "single-status", 'Lecturer'))
    });
}

function warnings(status, section, user){
    console.log(status);
    console.log(status.status);
    switch(status.status){
        case 935:
            document.querySelector(`#${section}`).outerHTML = `
        <div class="alert alert-danger" id=${section}>
            <strong>935 ERROR! ${user}(s) ALREADY exists!</strong>
        </div>`;
        case 912:
        document.querySelector(`#${section}`).outerHTML = `
            <div class="alert alert-danger" id=${section}>
                <strong>912 ERROR! Invalid course entered!</strong>
            </div>`;
        case 900:
            document.querySelector(`#${section}`).outerHTML = `
            <div class="alert alert-danger" id=${section}>
                <strong>900 ERROR! File is in the wrong format!</strong>
            </div>`;
        case 905:
            document.querySelector(`#${section}`).outerHTML = `
            <div class="alert alert-danger" id=${section}>
                <strong>905 ERROR! Faculty does NOT exist!</strong>
            </div>`;
        case 200:
            document.querySelector(`#${section}`).outerHTML = `
            <div class="alert alert-success" id=${section}>
                <strong>Success! ${user}'s details uploaded successfully!</strong>
            </div>
            `;
    }
}

function upload_departments(){
    ShowPage("#main", "#dept-registration");
    ShowPage("#dept-registration", "#dept-file-upload");
    document.querySelector("#dept-csv").addEventListener('change', () => {
        console.log(":)");
        document.querySelector("#dept-upload").setAttribute('class','btn btn-outline-success me-2');
        const file_name = document.querySelector("#dept-csv").value.split("\\");
        document.querySelector("#dept-upload").value = file_name[2];
        document.querySelector("#dept-status").outerHTML = `
        <div id="dept-status" class="alert alert-danger">
            <strong>Warning! Submitting file has no reverse process!</strong>
        </div>
        `;
    });
    document.querySelector("#upload-dept-form").addEventListener('submit', (event) => {
        event.preventDefault();
        fetch('upload_depts', {
            method: 'POST',
            body: document.querySelector("#dept-csv").files[0]
        })
        .then(response => response.json())
        .then(status => warnings(status, "dept-status", "Department"));
    });
}


function register_department(){
    ShowPage("#department-registration", "#single-department");
    document.querySelector("#single-department-form").addEventListener('submit', (event) => {
        event.preventDefault();
        fetch('register_department', {
            method: 'POST',
            body: JSON.stringify({
                department: document.querySelector("#department-department").value,
                faculty: document.querySelector("#department-faculty").value
            })
        })
        .then(response => response.json())
        .then(status => warnings(status, "single-department-status", "Department"));
    });
}


function upload_data(data){
    ShowPage("#main", `#${data}-registration`);
    ShowPage(`#${data}-registration`, `#${data}-file-upload`);
    document.querySelector(`#${data}-csv`).addEventListener('change', () => {
        document.querySelector(`#${data}-upload`).setAttribute('class','btn btn-outline-success me-2');
        const file_name = document.querySelector(`#${data}-csv`).value.split("\\");
        document.querySelector(`#${data}-upload`).value = file_name[2];
        document.querySelector(`#${data}-status`).outerHTML = `
        <div id="${data}-status" class="alert alert-danger">
            <strong>Warning! Submitting file has no reverse process!</strong>
        </div>
        `;
    });
    document.querySelector(`#upload-${data}-form`).addEventListener('submit', (event) => {
        event.preventDefault();
        fetch(`upload_${data}s`, {
            method: 'POST',
            body: document.querySelector(`#${data}-csv`).files[0]
        })
        .then(response => response.json())
        .then(status => warnings(status, `${data}-status`, "Department"));
    });
}