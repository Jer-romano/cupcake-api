const BASE_URL = "http://localhost:5000/api";

function generateCupcakeHTML(cupcake) {
    let image = $(`<img src=${cupcake["image"]}
    alt="A picture of a ${cupcake["flavor"]} cupcake" />`);
    let li = $("<li></li>");
    let div = $(`<div class="c-info">
                    <h3>Flavor: ${cupcake["flavor"]}</h3>
                      <h4>Size: ${cupcake["size"]}</h4>
                    <h4>Rating: ${cupcake["rating"]}</h4>
                    </div>`);
    li.append(image);
    li.append(div);
    let btn_div = $(` <div class="c-info">
                    <button class="btn btn-primary update-btn"
                    data-id="${cupcake["id"]}">Update</button>
                    <button class="btn btn-danger delete-btn"
                     data-id="${cupcake["id"]}">Delete</button>
                    </div>
                    <hr>`);
    li.append(btn_div);
    return li;
}
async function addCupcakesOnPageLoad() {
    let resp;
    try {
        resp = await axios.get(`${BASE_URL}/cupcakes`);

    } catch(error) {
        console.error(`An error occurred: ${error}`);
    }

    for(let cupcake of resp.data.cupcakes) {
        let newLi = generateCupcakeHTML(cupcake);
        $("#cupcake-list").append(newLi);
    }
}
 
async function addCupcake(event) {
    event.preventDefault();
    console.log("Inside addCupcake")
    let resp, cupcake;
    try {
        let formData = $("#add-form").serializeArray();
        let jsonData = {};
        formData.forEach((field) => {
            jsonData[field.name] = field.value;
        });
        resp = await axios.post(`${BASE_URL}/cupcakes`, jsonData, {
            headers: {'content-type': 'application/json',
                        "Access-Control-Allow-Origin": "*"}
        });
        cupcake = resp.data["cupcake"];
        console.log("*************************************\n", cupcake);
    } catch(error) {
        console.error(`An error occurred: ${error}`);
    }
    let li = generateCupcakeHTML(cupcake);
    $("#cupcake-list").append(li);
}
$("#add-form").on("submit", addCupcake);

async function deleteCupcake(event) {
    event.preventDefault();
    try {
        let cupcakeId = $(this).data("id");
        let resp = axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
    } catch(error) {
        console.error("An error occured: ", error);
    }
    let $li = $(this).closest("li.cupcake-entry");
    $li.remove();
}
$(".delete-btn").click(deleteCupcake);

$(addCupcakesOnPageLoad);
// "flavor": $("#flavor").val(),
// "image": $("#imager").val(),
// "size": $("#size").val(),
// "rating": $("#rating").val()