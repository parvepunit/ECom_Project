
function popu(iden) {
    let id = '#cart_items' + iden
    let htm = $(String(id)).html()
    console.log(htm)
    let cart = JSON.parse(htm)
    console.log(cart)
    
    $('#ites'+iden).html("")

    for (item in cart) {
        let type = cart[item][0]
        let material = cart[item][1]
        let shape = cart[item][2]
        let size = cart[item][3]
        let qty = cart[item][4]
        // let cost = cart[item][5]
        let stk_image = cart[item][5]

        const int_val = size
        const qty_sheets = qty


        mystr = `<div class="card my-4 " style="max-width: 540px;">
                    <div class="row g-0">
                        <div class="col-md-4">
                            <img src="${stk_image}" id="image_loaded${item}" class="img-fluid rounded-start mt-3 my-2" alt="${stk_image}" height="15rem">
                        </div>
                        <div class="col-md-8">
                            <div class="card-body">
                                <p class="card-text">
                                    <strong>Type :</strong> ${type} <br>
                                    <strong>Material :</strong> ${material} <br>
                                    <strong>Shape :</strong> ${shape} <br>
                                    <strong>Size :</strong> ${size} inch<br>
                                    <strong>Quantity :</strong> <span id="qty_set${item}"></span>  <br>
                                    <strong>Cost :</strong> Rs. <span id="cst_set${item}">  </span> /- <br></br>   
                                </p>
                                <a href="${stk_image}" target="_blank" class="btn btn-success cart">View</a>
                            </div>
                        </div>
                    </div>
                </div>`
                
        $('#ites'+iden).append(mystr)
        
        $.ajax({
            type: 'POST',
            url: '/datacstfetch/',
            data: {name : int_val, qty_sheet : qty_sheets},
            success: function(data){
                $('#qty_set'+item).html(data.item['Qty'] + " " + "pcs");
                $('#cst_set'+item).html(data.item['calc']);
                itemCst += data.item['calc']
            },
            async:false
        })

    }
 

}