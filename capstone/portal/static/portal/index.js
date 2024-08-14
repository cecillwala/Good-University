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
                    let depts = document.createElement('button');
                    depts.setAttribute('class', 'btn btn-light');
                    depts.innerHTML = department.department;
                    depts.addEventListener('click', () => {
                        ShowPage("#main", "#dept-details");
                        document.querySelector("#dept-name").innerHTML = department.department;
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
