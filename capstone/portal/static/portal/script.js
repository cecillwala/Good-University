document.addEventListener('DOMContentLoaded', () => {
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
                first_name: document.querySelector("#student-first-name").value,
                last_name: document.querySelector("#student-last-name").value,
                phone_number: document.querySelector("#student-phone-number").value,
                nationalID: document.querySelector("#student-national-id").value,
                gender: document.querySelector("#student-gender").value,
                course: document.querySelector("#student-course").value,
                faculty: document.querySelector("#student-faculty").value,
                year: document.querySelector("#student-year").value
            })
        })
        .then(response => response.json())
        .then(status => {
            document.querySelector("#student-first-name").value = '';
            document.querySelector("#student-last-name").value  = '';
            document.querySelector("#student-phone-number").value = '';
            document.querySelector("#student-national-id").value = '';
            document.querySelector("#student-gender").value = '';
            document.querySelector("#student-course").value = '';
            warnings(status, 'single-status', 'Student');
        });
    });
}


function registration_view(){
    ShowPage('#main', '#student-registration');
    const d = new Date();
    month = d.getMonth();
    if (month >= 7){
        console.log(month);
        ShowPage('#student-registration', '#state');
        document.querySelector("#state").innerHTML = `
        <h4>${d.getFullYear()}/${d.getFullYear() + 1} Student Registration ended on the 31st of July.</h4>
        `;
    }
    else{
        ShowPage('#student-registration', '#file-upload');
    }
}


function register_lecturer(){
    ShowPage("#lecturer-registration","#single-lecturer");
    document.querySelector("#lecturer-form").addEventListener('submit', (event) => {
        event.preventDefault();
        fetch('register_lecturer', {
            method:'POST',
            body: JSON.stringify({
                first_name: document.querySelector("#lec-first-name").value,
                last_name: document.querySelector("#lec-last-name").value,
                phone_number: document.querySelector("#lec-phone-number").value,
                nationalID: document.querySelector("#lec-national-id").value,
                gender: document.querySelector("#lec-gender").value,
                faculty: document.querySelector("#lec-faculty").value,
                department: document.querySelector("#lec-department").value,
                year: document.querySelector("#lec-year").value
            })
        })
        .then(response => response.json())
        .then(status => warnings(status, "single-lec-status", 'Lecturer'))
    });
}

function warnings(status, section, user){
    console.log(status);
    console.log(status.status);
    switch(status.status){
        case 200:
            document.querySelector(`#${section}`).outerHTML = `
            <div class="alert alert-success" id=${section}>
                <strong>Success! ${user}'s details uploaded successfully!</strong>
            </div>`;
            break;
        case 935:
            document.querySelector(`#${section}`).outerHTML = `
        <div class="alert alert-danger" id=${section}>
            <strong>935 ERROR! ${user}(s) ALREADY exists!</strong>
        </div>`;
        break;
        case 912:
        document.querySelector(`#${section}`).outerHTML = `
            <div class="alert alert-danger" id=${section}>
                <strong>912 ERROR! Invalid ${user} entered!</strong>
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
        case 239:
            document.querySelector(`#${section}`).outerHTML = `
            <div class="alert alert-danger" id=${section}>
                <strong>239 Error! File format not supported!/No file Chosen!</strong>
            </div>`;
            break;
        default:
            document.querySelector(`#${section}`).outerHTML = `
            <div class="alert alert-danger" id=${section}>
                <strong>Unkown Error!Something Went horribly wrong!</strong>
            </div>`;
    }
}


function register_course(){
    ShowPage("#course-registration", "#single-course");
    document.querySelector('#course-form').addEventListener('submit', async (event) => {
        event.preventDefault();
        const response = await fetch("register_course", {
            method:'POST',
            body: JSON.stringify({
                course:document.querySelector("#course-course").value,
                faculty:document.querySelector("#course-faculty").value
            })
        });
        const status = await response.json();
        warnings(status, 'single-course-status', 'Course');
    });
}

function register_unit(){
    ShowPage("#unit-registration", "#single-unit");
    document.querySelector("#unit-form").addEventListener('submit', async (event) => {
        event.preventDefault();
        const response = await fetch("register_unit", {
            method:"POST",
            body: JSON.stringify({
                unit:document.querySelector("#unit-unit").value,
                unit_code:document.querySelector("#unit-unit-code").value,
                department:document.querySelector("#unit-department").value,
                period:document.querySelector("#unit-period").value,
                course:document.querySelector("#unit-course").value
            })
        });
        const status = await response.json();
        warnings(status, "single-unit-status", "Unit");

    })
}

function register_room(){
    ShowPage("#room-registration", "#single-room");
    document.querySelector("#room-form").addEventListener('submit', async (event) => {
        event.preventDefault();
        const response = await fetch("register_room", {
            method:"POST",
            body:JSON.stringify({
                hostel:document.querySelector("#room-hostel").value,
                room:document.querySelector("#room-room").value,
                bed:document.querySelector("#room-bed").value
            })
        });
        const status = await response.json();
        warnings(status, "single-room-status", "Room");
    })
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
        document.querySelector(`#${data}-upload`).setAttribute('class','btn btn-success me-2');
        const file_name = document.querySelector(`#${data}-csv`).value.split("\\");
        if(file_name[2] != undefined){
        document.querySelector(`#${data}-upload`).value = file_name[2];
        }
        else{
            document.querySelector(`#${data}-upload`).value = 'No File Chosen';   
        }
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
    ShowPage("#main", "#profile");
    const response = await fetch("dept_details");
    const lecs = await response.json();
    console.log(lecs);

    //Lecturers btn
    document.querySelector("#dept-lec-view").addEventListener('click', () => {
        ShowPage("#main", "#lecturers");
        document.querySelector("#lecturers").innerHTML = '';
        lecs.lecturers.forEach(lec => {
            let lec_btn = document.createElement('button');
            let hr = document.createElement('hr');
            lec_btn.addEventListener('click', () => lecturer_details(lec));
            lec_btn.setAttribute('class', 'other-btns');
            lec_btn.innerHTML = lec;
            document.querySelector("#lecturers").append(lec_btn, hr);
        });
    });

    document.querySelector("#dept-units-view").addEventListener('click', () => {
        ShowPage('#main', '#dept-units');
        ShowPage("#dept-units", "#dept-unit-list");
        document.querySelector("#dept-unit-list").innerHTML ='';
        lecs.units.forEach(unit => {
            const unit_btn = document.createElement('button');
            let hr = document.createElement('hr');
            unit_btn.setAttribute('class', 'other-btns');
            unit_btn.innerHTML = `${unit.unit_code}: ${unit.unit}`;
            unit_btn.addEventListener('click', () => unit_details(unit.unit_code));
            document.querySelector("#dept-unit-list").append(unit_btn, hr);
        });
    });

}


async function lecturer_details(lec){
    const response = await fetch(`lec_details/${lec}`)
    const lec_details = await response.json();
    console.log(lec_details);
    let units_div = document.createElement('div');
    let hr = document.createElement('hr');
    units_div.setAttribute('class', 'list');
    document.querySelector("#add-lec-unit").outerHTML = `
    <form method="post" id="add-lec-unit">
        <input type="text" placeholder="Add Unit" id="add-unit">
        <input type="submit" class="other-btns" value="Add Unit">
    </form>`;
    let unit_div = document.createElement('div');
    if(lec_details.units.length <= 0){
        unit_div.innerHTML = `<div class="alert alert-warning">
                <strong>ALERT! </strong>${lec_details.first_name} ${lec_details.last_name} is not teaching any units.
            </div>`;
    }
    else{
        lec_details.units.forEach(unit => {
            let unit_div = document.createElement('div');
            let unit_txt = document.createElement('div');
            let remove_unit = document.createElement('button');
            let hr = document.createElement('hr');
            unit_div.setAttribute('class', 'row-flex');
            remove_unit.setAttribute('class', 'other-btns');
            remove_unit.innerHTML = 'Remove Unit';
            remove_unit.addEventListener('click', () => {
                fetch(`remove_unit/${unit.unit_code}/${lec}`, {
                    method:"PUT"
                })
                .then(response => response.json())
                .then(status => {
                    console.log(status);
                    lecturer_details(lec);
                })
            });
            unit_txt.innerHTML = `${unit.unit_code}: ${unit.unit}`;
            unit_div.append(unit_txt, remove_unit);
            units_div.append(unit_div, hr);
        });
    }
    document.querySelector("#lec-profile").innerHTML = '';
    document.querySelector("#lec-profile").append(lec_details.first_name, hr, lec_details.last_name, hr, `+${lec_details.phone_number}`, hr, units_div);
    document.querySelector("#add-lec-unit").addEventListener('submit', (event) => {
        event.preventDefault();
        fetch('assign_unit', {
            method: 'PUT',
            body: JSON.stringify({
                unit: document.querySelector("#add-unit").value,
                lecturer:lec
            })
        })
        .then(response => response.json())
        .then(status => {
            console.log(status);
        });
        lecturer_details(lec);
    });
    ShowPage("#main", "#lec");
}


async function unit_details(unit){
    ShowPage("#dept-units", "#dept-unit-details");
    const children = Array.from(document.querySelector("#dept-unit-details").children);
    children.forEach(child => {
        child.innerHTML = '';
    });
    const response = await fetch(`unit_details/${unit}`);
    const units = await response.json();
    const course_tag = document.createElement('h6');
    const student_tag = document.createElement('h6');
    const lecs_tag = document.createElement('h6');
    course_tag.innerHTML = "Courses: ";
    student_tag.innerHTML = "Students: ";
    lecs_tag.innerHTML = "Lecturers: ";
    document.querySelector("#dept-unit-courses").append(course_tag);
    document.querySelector("#dept-unit-students").append(student_tag);
    document.querySelector("#dept-unit-lecs").append(lecs_tag);
    console.log(units);
    document.querySelector("#dept-unit-unit").innerHTML = `${units.unit_code}: ${units.unit}`;
    if(units.courses.length <= 0){
        document.querySelector("#dept-unit-courses").outerHTML = `
        <div id='dept-unit-courses'>
            <div class="alert alert-warning">
                <strong>ALERT!</strong> No course is taking this unit!
            </div>
        </div>`;
    }
    else{
        units.courses.forEach(course => {
            document.querySelector("#dept-unit-courses").append(course)
        });
    }

    if(units.professors.length <= 0){
        document.querySelector("#dept-unit-lecs").outerHTML = `
        <div id='dept-unit-lecs' class="list">
            <h6>Lecturers: </h6>
            <div class="alert alert-warning">
                <strong>ALERT!</strong> No lecturer is teaching this unit!
            </div>
        </div>`;
    }
    else{
        units.professors.forEach(prof => {
            document.querySelector("#dept-unit-lecs").append(prof)
        });
    }
    if(units.students.length <= 0){
        document.querySelector("#dept-unit-students").outerHTML = `
        <div id='dept-unit-students' class='list'>
            <h6>Students: </h6>
            <div class="alert alert-warning">
                <strong>ALERT!</strong> No students are taking this unit!
            </div>
        </div>`;
    }
    else{
        units.students.forEach(student => {
            document.querySelector("#dept-unit-students").append(student)
        });
    }
}
