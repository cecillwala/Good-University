document.addEventListener('DOMContentLoaded', () => {
    ShowPage("#profile");
    document.querySelector("#csv").addEventListener('change', () => first_year_admin());
});


function ShowPage(page){
   const children = Array.from(document.querySelector("#main").children);
    children.forEach(child => {
        child.style.display = 'none';
    });
    document.querySelector(page).style.display = 'block';
} 


function first_year_admin(){
    const file_name = document.querySelector("#csv").value.split("\\");
    document.querySelector("#upload").value = file_name[2];
    document.querySelector("#status").outerHTML = `
    <div id="status" class="alert alert-warning">
        <strong>Warning!</strong> Submitting file has no reverse process.
    </div>
    `;
    document.querySelector("#upload-form").addEventListener('submit', (event) => {
        event.preventDefault();
        fetch('upload', {
            method:'POST',
            body: document.querySelector("#csv").files[0]
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