document.addEventListener("DOMContentLoaded", () => {
    document.querySelector("#upload").addEventListener('click', () => first_year_admin());
});


function first_year_admin(){
    document.querySelector("#confirm").style.display = 'block';
    document.querySelector("#not-confirmed").addEventListener('click', () => {
        document.querySelector("#confirm").style.display = 'none';
    });
    document.querySelector("#confirmed").addEventListener('click', () => {
        document.querySelector("#confirm").style.display = 'none';
    });
    document.querySelector("#upload-form").addEventListener('submit', (event) => {
        event.preventDefault();
        document.querySelector("#confirm").style.display = 'none';
        const file_name = document.querySelector("#csv").value.split("\\");
        console.log(file_name[2]);
            fetch('upload', {
                method:'POST',
                body: document.querySelector("#csv").files[0]
            })
            .then(response => response.json())
            .then(status => {
                if(status.status == 200){
                    document.querySelector("#status").outerHTML = `
                    <div class="alert alert-success">
                        <strong>Success.</strong> Student's file uploaded successfully.
                    </div>
                    `;
                    document.querySelector("#contents").style.display = 'none';
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