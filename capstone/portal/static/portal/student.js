document.addEventListener('DOMContentLoaded', () => {
    ShowPage("#main", "#profile");
});


function ShowPage(page, section){
    const children = Array.from(document.querySelector(page).children);
    children.forEach(child => {
        child.style.display = 'none';
    })
    document.querySelector(section).style.display = 'block';
}


async function unit_registration(){
    ShowPage("#main", "#unit-registration");
    const response = await fetch("unit_registration")
    const units = await response.json();
    console.log(units);
    let units_div = document.createElement('div');
    units_div.setAttribute('class', 'list');
    units.all_units.forEach(unit => {
        let unit_div = document.createElement('div');
        let unit_txt = document.createElement('div');
        let register_unit = document.createElement('button');
        let hr = document.createElement('hr');
        unit_div.setAttribute('class', 'row-flex');
        register_unit.setAttribute('class', 'other-btns');
        register_unit.innerHTML = 'Register Unit';

        for(let i = 0; i < units.registered_units.length; i++){
            if(units.registered_units[i].unit_code == unit.unit_code){
                register_unit.innerHTML = 'Registered';
                register_unit.setAttribute('disabled', true);
                register_unit.setAttribute('class', 'other-btns-disabled');
            }
        }

        if(register_unit.innerHTML == 'Register Unit'){
            register_unit.addEventListener('click', () => {
                fetch("unit_registration", {
                    method:'PUT',
                    body: JSON.stringify(unit.unit_code)
                })
                unit_registration();
            });
        }
    
        unit_txt.innerHTML = `${unit.unit_code}: ${unit.unit}`;
        unit_div.append(unit_txt, register_unit);
        units_div.append(unit_div, hr);
    })
    document.querySelector("#unit-registration").innerHTML = '';
    document.querySelector("#unit-registration").append(units_div);   
}


async function accomodation_registration(){
    let response = await fetch('accom_registration');
    let status = await response.json();
    console.log(status);
    ShowPage("#main", "#accom-registration");
    if(status.status == 300){
        ShowPage("#accom-registration", "#accom-upload");
        document.querySelector("#book-room").addEventListener('submit', (event) => {
            event.preventDefault();
            fetch("accom_registration", {
                method:'POST',
                body: JSON.stringify({
                    house: document.querySelector("#house").value,
                    room: document.querySelector("#room").value,
                    bed:document.querySelector("#bed").value     
                })
            })
            .then(response => response.json())
            .then(status => {
                    console.log(status);
                    accomodation_registration();
            });
        });
    }
    else{
        document.querySelector("#status").outerHTML = `
        <div id="status">
            <div class="alert alert-success">
                ALERT! Accomodation Registration completed!
            </div>
            <br>
            <h6>hostel<h6>
            <div class="list">
                <div>Hostel: ${status.house}</div>
                <hr>
                <div>Room: ${status.room}</div>
                <hr>
                <div>Bed: ${status.bed}</div>
            </div>
        </div>`;
        ShowPage("#accom-registration", "#status");
    }
}

async function lecturer_units(){
    ShowPage("#main", "#lec-units");
    ShowPage("#lec-units", "#units-list");
    const response = await fetch("lec_units");
    const details = await response.json();
    console.log(details);
    let units_div = document.createElement('div');
    let header = document.createElement('h5');
    header.innerHTML = 'Your Units:';
    let hr = document.createElement('hr');
    details.units.forEach(unit => {
        let unit_div = document.createElement('div');
        let unit_txt = document.createElement('button');
        unit_txt.setAttribute('class', 'other-btns');
        let hr = document.createElement('hr');
        unit_txt.addEventListener('click', async () => {
            let response = await fetch(`unit_details/${unit.unit_code}`);
            let contents = await response.json();
            console.log(contents);
            const children = Array.from(document.querySelector("#unit-details").children);
            children.forEach(child => {
                child.innerHTML = '';
            });
            const course_tag = document.createElement('h6');
            const student_tag = document.createElement('h6');
            const lecs_tag = document.createElement('h6');
            course_tag.innerHTML = "Courses: ";
            student_tag.innerHTML = "Students: ";
            lecs_tag.innerHTML = "Lecturers: ";
            document.querySelector("#unit-courses").append(course_tag);
            document.querySelector("#unit-students").append(student_tag);
            document.querySelector("#unit-lecs").append(lecs_tag);
            console.log(unit);
            document.querySelector("#unit").innerHTML = `${unit.unit_code}: ${unit.unit}`;
            if(unit.courses.length <= 0){
                document.querySelector("#unit-courses").outerHTML = `
                <div id='unit-courses'>
                    <div class="alert alert-warning">
                        <strong>ALERT!</strong> No course is taking this unit!
                    </div>
                </div>`;
            }
            else{
                unit.courses.forEach(course => {
                    document.querySelector("#unit-courses").append(course)
                });
            }

            if(unit.professors.length <= 0){
                document.querySelector("#unit-lecs").outerHTML = `
                <div id='unit-lecs' class="list">
                    <h6>Lecturers: </h6>
                    <div class="alert alert-warning">
                        <strong>ALERT!</strong> No lecturer is teaching this unit!
                    </div>
                </div>`;
            }
            else{
                unit.professors.forEach(prof => {
                    document.querySelector("#unit-lecs").append(prof)
                });
            }
            if(unit.students.length <= 0){
                document.querySelector("#unit-students").outerHTML = `
                <div id='unit-students' class='list'>
                    <h6>Students: </h6>
                    <div class="alert alert-warning">
                        <strong>ALERT!</strong> No students are taking this unit!
                    </div>
                </div>`;
            }
            else{
                unit.students.forEach(student => {
                    document.querySelector("#unit-students").append(student)
                });
            }
            ShowPage('#lec-units', '#unit-details');
        });

        unit_txt.innerHTML = `${unit.unit_code}: ${unit.unit}`;
        unit_div.append(unit_txt);
        units_div.append(unit_div, hr);
    });

    document.querySelector("#units-list").innerHTML = '';
    document.querySelector("#units-list").append(header, hr, units_div);  
    
}