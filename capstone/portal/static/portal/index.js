document.addEventListener('DOMContentLoaded', () => {
    faculty_details();
    ShowPage("#main", "#options");
});


function ShowPage(page, section){
    const children = document.querySelector(page).children;
    Array.from(children).forEach(child => {
        child.style.display = 'none';
    })
    document.querySelector(section).style.display = 'flex';
}


async function faculty_details(){
    //get faculty details
    const response = await fetch('faculty_details'); 
    const data  = await response.json();
    console.log(data);
    document.querySelector("#menu").innerHTML ='';
    data.forEach(faculty => {
        let button = document.createElement('button');
        let div = document.createElement('div'); 
        button.setAttribute('class', 'menu-options');
        div.innerHTML = `School Of ${faculty.name}`;
        button.append(div);
        document.querySelector("#menu").append(button);
        button.addEventListener('click', () => options_view(faculty));
    });
}

function options_view(faculty){
    document.querySelector("#options").innerHTML = '';
    let faculty_name = document.createElement('h3');
    faculty_name.innerHTML = `School Of ${faculty.name}: `;
    let hr = document.createElement('hr');
    document.querySelector("#options").append(faculty_name, hr);
    let dept = document.createElement('button');
    dept.setAttribute('class', 'menu-options');
    dept.addEventListener('click', async () => {
        document.querySelector("#departments").innerHTML = '';
        const head = document.createElement('h3');
        head.innerHTML = 'Departments: ';
        document.querySelector("#departments").append(head);
        const response = await fetch(`faculty_departments/${faculty.faculty}`);
        const details = await response.json();
        details.forEach(department => {
            document.querySelector("#dept-options").innerHTML = '';
            let depts = document.createElement('button');
            depts.setAttribute('class', 'menu-options');
            depts.addEventListener('click', () => {
                let dept_name = document.createElement('h3');
                dept_name.innerHTML = `${department}: `;
                let lecs = document.createElement('button');
                lecs.innerHTML = 'Lecturers';
                lecs.setAttribute('class', 'menu-options');
                lecs.addEventListener('click', () => department_lecturers(department));
                let topics = document.createElement('button');
                topics.innerHTML = 'Units';
                topics.setAttribute('class', 'menu-options');
                topics.addEventListener('click', async () => department_units(department));

                let br = document.createElement('br');
                document.querySelector("#dept-options").append(dept_name, lecs, br, topics);
                ShowPage("#main", "#dept-details");
                ShowPage("#dept-details","#dept-options");
            });
            depts.innerHTML = department;
            let br = document.createElement('br');
            document.querySelector("#departments").append(depts, br);
        });
        ShowPage("#main", "#departments")
    });
    let course = document.createElement('button');
    course.setAttribute('class', 'menu-options');
    const dept_div = document.createElement('div');
    dept_div.innerHTML = 'Departments';
    dept.append(dept_div);
    const course_div = document.createElement('div');
    course_div.innerHTML = 'Courses';
    let br = document.createElement('br');
    course.append(course_div);
    course.addEventListener('click', async () => {
        document.querySelector("#courses").innerHTML = '';
        const head = document.createElement('h3');
        head.innerHTML = 'Courses: ';
        document.querySelector("#courses").append(head);
        const response = await fetch(`faculty_courses/${faculty.faculty}`);
        const details = await response.json();
        details.forEach(course => {
            let crse = document.createElement('button');
            crse.setAttribute('class', 'menu-options');
            crse.innerHTML = course;
            crse.addEventListener('click', () => course_units(course));
            document.querySelector("#courses").append(crse);
        });
        ShowPage("#main", "#courses");
    });
    document.querySelector("#options").append(dept, br, course);
    ShowPage("#main", "#options");
}


async function department_lecturers(department){
    document.querySelector("#dept-lecs").innerHTML = '';
    let dept_name = document.createElement('h3');
    dept_name.innerHTML = `${department}: `;
    document.querySelector("#dept-lecs").append(dept_name);
    const response = await fetch(`department_lecturers/${department}`)
    const lecturers = await response.json();
    lecturers.forEach(lec => {
        let lec_div = document.createElement('div');
        let lec_txt = document.createElement('div');
        let make_hod = document.createElement('button');
        let hr = document.createElement('hr');
        if(lec.is_hod){
            make_hod.innerHTML = 'Remove Head Of Department';
        }
        else{
            make_hod.innerHTML = 'Make Head Of Department';
        }
        lec_div.setAttribute('class', 'row-flex');
        make_hod.setAttribute('class', 'other-btns');
        make_hod.addEventListener('click', async () => {
            const response = await fetch('make_hod', {
                method: 'PUT',
                body: JSON.stringify({
                    "lecturer": `${lec.username}`,
                    "status": lec.is_hod
                })
            })
            const status = await response.json();
                console.log(status);
                department_lecturers(department);
        });
        lec_txt.innerHTML = `${lec.username}`;
        lec_div.append(lec_txt, make_hod);
        document.querySelector("#dept-lecs").append(lec_div, hr);
    });
    ShowPage("#dept-details", "#dept-lecs");
}


async function department_units(department){
    document.querySelector("#dept-units-list").innerHTML = '';
    let dept_name = document.createElement('h3');
    dept_name.innerHTML = `${department}: `;
    document.querySelector("#dept-units-list").append(dept_name);
    const response = await fetch(`department_units/${department}`);
    const units = await response.json();
    units.forEach(unit => {
        let hr = document.createElement('hr');
        let unit_txt = document.createElement('div');
        let unit_div = document.createElement("div");
        let remove_unit = document.createElement('button');
        remove_unit.setAttribute('class', 'other-btns');
        unit_div.setAttribute('class', 'row-flex');
        remove_unit.innerHTML = 'Remove Unit';
        remove_unit.addEventListener('click', async () => {
            const response = await fetch(`remove_dept_unit`, {
                method: "PUT",
                body: JSON.stringify({
                    unit:unit.unit_code
                })
            })
            const status = response.json();
            console.log(status);
            department_units(department);
        })
        unit_txt.innerHTML = `${unit.unit_code}: ${unit.unit}`;
        unit_div.append(unit_txt, remove_unit)
        document.querySelector("#dept-units-list").append(unit_div, hr);
    });
    document.querySelector("#dept-unit-form").addEventListener('submit', async (event) => {
        event.preventDefault();
        const response = await fetch("add_dept_unit", {
            method:"PUT",
            body:JSON.stringify({
                unit:document.querySelector("#add-dept-unit").value,
                department:department
            })
        });
        const status = await response.json();
        console.log(status);
        department_units(department);
    });
    ShowPage("#dept-details", "#dept-units");
}


async function course_units(course){
    document.querySelector("#course-units").innerHTML = '';
    const head = document.createElement('h3');
    head.innerHTML = 'Units: ';
    const response = await fetch(`course_units/${course}`);
    const units =  await response.json();
    document.querySelector("#course-units").append(head);
    units.forEach(unit => {
        let unit_div = document.createElement('div');
        let unit_txt = document.createElement('div');
        let hr = document.createElement('hr'); 
        let remove_unit = document.createElement('button');
        remove_unit.setAttribute('class', 'other-btns');
        unit_div.setAttribute('class', 'row-flex');
        remove_unit.innerHTML = 'Remove Unit';
        remove_unit.addEventListener('click', async () => {
            const response = await fetch(`remove_course_unit`, {
                method: "PUT",
                body: JSON.stringify({
                    unit:unit.unit_code,
                    course:course
                })
            })
            const status = response.json();
            console.log(status);
            course_units(course);
        });
        unit_txt.innerHTML = `${unit.unit_code}: ${unit.unit}`;
        unit_div.append(unit_txt, remove_unit);
        document.querySelector("#course-units").append(unit_div, hr);
    });
    ShowPage("#main", "#course-details");

    document.querySelector("#course-unit-form").addEventListener('submit', async (event) => {
        event.preventDefault();
        const response = await fetch("add_course_unit", {
            method:"PUT",
            body:JSON.stringify({
                unit:document.querySelector("#add-course-unit").value,
                course:course
            })
        });
        const status = await response.json();
        console.log(status);
        course_units(course);
    });
}
