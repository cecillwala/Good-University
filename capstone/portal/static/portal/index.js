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
    console.log(data)
    document.querySelector("#menu").innerHTML ='';
    data.forEach(faculty => {
        let button = document.createElement('button');
        let div = document.createElement('div'); 
        button.setAttribute('class', 'btn btn-light menu-options');
        //faculty.key -> faculty_name
        div.innerHTML = `School Of ${Object.keys(faculty)[0]}`;
        button.append(div);

        button.addEventListener('click', () => {
            ShowPage("#main", "#options");
            document.querySelector("#options").innerHTML = '';
            let dept = document.createElement('button');
            dept.setAttribute('class', 'grid-item btn btn-light');
            dept.addEventListener('click', () => {
                ShowPage("#main", "#departments");
                document.querySelector("#departments").innerHTML = '';
                const head = document.createElement('h3');
                head.innerHTML = 'Departments: ';
                document.querySelector("#departments").append(head);
                Object.values(faculty)[0].departments.forEach(department => {
                    document.querySelector("#dept-options").innerHTML = '';
                    let depts = document.createElement('button');
                    depts.setAttribute('class', 'btn btn-light');
                    depts.innerHTML = department.department;
                    depts.addEventListener('click', () => {
                        let dept_name = document.createElement('h3');
                        dept_name.innerHTML = `${department.department}: `;
                        let lecs = document.createElement('button');
                        lecs.innerHTML = 'Lecturers';
                        lecs.setAttribute('class', 'grid-item btn btn-light');
                        let topics = document.createElement('button');
                        topics.innerHTML = 'Units';
                        topics.setAttribute('class', 'grid-item btn btn-light');
                        ShowPage("#main", "#dept-details");
                        ShowPage("#dept-details","#dept-options");
                        document.querySelector("#dept-options").append(dept_name, lecs, topics);
                        lecs.addEventListener('click', () => {
                            document.querySelector("#dept-lecs").innerHTML = '';
                            ShowPage("#dept-details", "#dept-lecs");
                            document.querySelector("#dept-lecs").append(dept_name);
                            department.lecturers.forEach(lec => {
                                let lec_div = document.createElement('div');
                                let lec_txt = document.createElement('div');
                                let make_hod = document.createElement('button');
                                let hr = document.createElement('hr');
                                make_hod.innerHTML = 'Make HOD';
                                lec_div.setAttribute('class', 'row-flex');
                                make_hod.addEventListener('click', () => {
                                    if(make_hod.innerHTML === 'Make HOD'){
                                        fetch('make_hod', {
                                            method: 'PUT',
                                            body: JSON.stringify({
                                                "lecturer": `${lec}`,
                                                "status": true
                                            })
                                        })
                                        .then(response => response.json())
                                        .then(status => console.log(status));
                                        make_hod.innerHTML = 'Remove HOD';
                                    }
                                    else{
                                        fetch('make_hod', {
                                            method: 'PUT',
                                            body: JSON.stringify({
                                                "lecturer": `${lec}`,
                                                "status": false
                                            })
                                        })
                                        .then(response => response.json())
                                        .then(status => console.log(status));
                                        make_hod.innerHTML = 'Make HOD';
                                    }
                                })
                                make_hod.setAttribute('class', 'btn btn-light');
                                lec_txt.innerHTML = `${lec}`;
                                lec_div.append(lec_txt, make_hod);
                                document.querySelector("#dept-lecs").append(lec_div, hr);
                            });
                        });
                        topics.addEventListener('click', () => {
                            document.querySelector("#dept-units").innerHTML = '';
                            ShowPage("#dept-details", "#dept-units");
                            document.querySelector("#dept-units").append(dept_name);
                            department.units.forEach(unit => {
                                let unit_div = document.createElement("div");
                                unit_div.innerHTML = `${unit.unit_code}: ${unit.unit}`;
                                document.querySelector("#dept-units").append(unit_div);
                            });
                        });
                    });
                    document.querySelector("#departments").append(depts);
                });
            });
            let course = document.createElement('button');
            course.setAttribute('class', 'grid-item btn btn-light');
            course.addEventListener('click', () => {
                ShowPage("#main", "#courses");
                document.querySelector("#courses").innerHTML = '';
                const head = document.createElement('h3');
                head.innerHTML = 'Courses: ';
                document.querySelector("#courses").append(head);
                Object.values(faculty)[0].courses.forEach(course => {
                    let crse = document.createElement('button');
                    crse.setAttribute('class', 'btn btn-light');
                    crse.innerHTML = course.course;
                    crse.addEventListener('click', () => {
                        ShowPage("#main", "#course-details");
                        document.querySelector("#add-unit").addEventListener('submit', async (event) => {
                            event.preventDefault();
                            const result = await fetch("add_unit", {
                                 method:'POST',
                                 body: JSON.stringify({
                                    course: course.course,
                                    unit: document.querySelector("#unit").value
                                })
                            })
                            const answer = await result.json();
                            console.log(answer);
                        })
                        document.querySelector("#course-units").innerHTML = '';
                        const head = document.createElement('h3');
                        head.innerHTML = 'Units: ';
                        document.querySelector("#course-units").append(head);
                        course.units.forEach(unit => {
                            let unit_div = document.createElement('div');
                            let unit_txt = document.createElement('div');
                            let remove_btn = document.createElement('button');
                            let hr = document.createElement('hr');
                            remove_btn.innerHTML = 'Remove Unit';
                            unit_div.setAttribute('class', 'row-flex');
                            remove_btn.setAttribute('class', 'btn btn-light');
                            remove_btn.addEventListener('click', async () => {
                               let feedback = await fetch('remove_unit', {
                                    method: 'PUT',
                                    body: JSON.stringify({
                                        unit: unit.unit_code,
                                        course: course.course
                                    })
                                })
                                feedback = await feedback.json();
                                console.log(feedback);
                                crse.click();
                            })
                            unit_txt.innerHTML = `${unit.unit_code}: ${unit.unit}`;
                            unit_div.append(unit_txt, remove_btn);
                            document.querySelector("#course-units").append(unit_div, hr);
                        })
                    });
                    document.querySelector("#courses").append(crse);
                });
            });
            const dept_div = document.createElement('div');
            dept_div.innerHTML = 'Departments';
            dept.append(dept_div);
            const course_div = document.createElement('div');
            course_div.innerHTML = 'Courses';
            course.append(course_div);
            document.querySelector("#options").append(dept, course);
        });
        document.querySelector("#menu").append(button);
    });
}
