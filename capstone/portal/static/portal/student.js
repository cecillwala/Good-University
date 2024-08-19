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
        register_unit.setAttribute('class', 'btn btn-light');
        register_unit.innerHTML = 'Register Unit';

        for(let i = 0; i < units.registered_units.length; i++){
            if(units.registered_units[i].unit_code == unit.unit_code){
                register_unit.innerHTML = 'Registered';
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