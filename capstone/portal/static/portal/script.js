document.addEventListener('DOMContentLoaded', () => {
    ShowPage("#main", "#profile");
    dept_details();
});


function ShowPage(page, section){
   const children = Array.from(document.querySelector(page).children);
    children.forEach(child => {
        child.style.display = 'none';
    });
    document.querySelector(section).style.display = 'block';
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
        break;
        case 912:
        document.querySelector(`#${section}`).outerHTML = `
            <div class="alert alert-danger" id=${section}>
                <strong>912 ERROR! Invalid course entered!</strong>
            </div>`;
            break;
        case 900:
            document.querySelector(`#${section}`).outerHTML = `
            <div class="alert alert-danger" id=${section}>
                <strong>900 ERROR! File is in the wrong format!</strong>
            </div>`;
            break;
        case 905:
            document.querySelector(`#${section}`).outerHTML = `
            <div class="alert alert-danger" id=${section}>
                <strong>905 ERROR! Faculty does NOT exist!</strong>
            </div>`;
            break;
        case 200:
            document.querySelector(`#${section}`).outerHTML = `
            <div class="alert alert-success" id=${section}>
                <strong>Success! ${user}'s details uploaded successfully!</strong>
            </div>`;
            break;
        default:
            document.querySelector(`#${section}`).outerHTML = `
            <div class="alert alert-danger" id=${section}>
                <strong>UNKNOWN ERROR!Something Went horribly wrong!</strong>
            </div>`;
    }
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
        .then(status => warnings(status, `${data}-status`, `${data[0].toUpperCase()}${data.slice(1)}`));
    });
}


async function dept_details(){
    const response = await fetch("dept_details");
    const lecs = await response.json();
    console.log(lecs);

    document.querySelector("#dept-lec-view").addEventListener('click', () => {
        ShowPage("#main", "#lecturers");
        document.querySelector("#lecturers").innerHTML = '';
        lecs.lecturers.forEach(lec => {
            let lec_btn = document.createElement('button');
            let hr = document.createElement('hr');
            lec_btn.addEventListener('click', () => {
                ShowPage("#main", "#lec");
                let units_div = document.createElement('div');
                units_div.setAttribute('class', 'list');
                if(lec.units.length <= 0){
                    units_div.innerHTML = `${lec.first_name} ${lec.last_name} is not teaching any units.`;
                }
                else{
                    lec.units.forEach(unit => {
                        let unit_div = document.createElement('div');
                        unit_div.innerHTML = `${unit.unit_code}: ${unit.unit}`;
                        units_div.append(unit_div, hr);
                    });
                }
                document.querySelector("#lec-profile").innerHTML = '';
                document.querySelector("#lec-profile").append(lec.first_name, hr, lec.last_name, hr, lec.phone_number, hr, units_div);

                document.querySelector("#add-lec-unit").addEventListener('submit', (event) => {
                    event.preventDefault();
                    fetch('assign_unit', {
                        method: 'PUT',
                        body: JSON.stringify({
                            unit: document.querySelector("#unit").value,
                            lecturer:lec.username
                        })
                    })
                    .then(response => response.json())
                    .then(status => console.log(status));
                });
            });
            lec_btn.setAttribute('class', 'btn btn-light');
            lec_btn.innerHTML = lec.username;
            document.querySelector("#lecturers").append(lec_btn, hr);
        });
    });

}