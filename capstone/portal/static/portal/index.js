document.addEventListener('DOMContentLoaded', () => {
    faculty_details();
});

function faculty_details(){
    fetch('faculty_details')
    .then(response => response.json())
    .then(data => console.log(data));
}

