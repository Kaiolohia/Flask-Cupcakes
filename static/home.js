$CONTENT = $('.content')

async function getCupcakes() {
    let res =  await axios.get('/api/cupcakes')
    for (cupcake in res.data.cupcakes) {
        $CONTENT.append(viewCupcake(res.data.cupcakes[cupcake]))
    }
}

function viewCupcake(res) {
    return `<div class="col-4">
    <figure class="figure" id="${res.id}">
        <img src="${res.image}" class="figure-img img-thumbnail rounded">
        <figcaption class="figure-caption"><b>${res.flavor}, size: ${res.size}, ${res.rating} / 10</b></figcaption>
    </figure>
    </div>`
}

function main() {
    getCupcakes()
}

$(document).ready(main())