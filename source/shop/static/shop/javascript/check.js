
if (cart_pr > 0) {
    // filling order summery with cart iterms
    document.querySelector('#itms_value').innerHTML = Object.keys(cart).length
    itemCst = 0.00;
   
    for (item in cart) {
        let name = "Sticker "
        let type = cart[item][0]
        let material = cart[item][1]
        let shape = cart[item][2]
        let size = cart[item][3]
        let qty = cart[item][4]
        // let cost = cart[item][5]
        let stk_image = cart[item][5]

        const int_val = size
        const qty_sheets = qty

        $.post('/datacstfetch/', { name : int_val, qty_sheet : qty_sheets}, function(data, status){
            // stick_cost = data.item['calc']
            stick_cost = data.item
            stick_qty = data.item['Qty']

            // $('#stickcost').html(data.item['calc'] + " " + "/-");
            // $('#stickqty').html(data.item['Qty'] +" " + 'pcs');
        } )
        

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
                                <button type="button" class="btn btn-danger" onclick="rem_item(${item})">Remove</button>
                                <a href="${stk_image}" target="_blank" class="btn btn-success cart">View</a>
                            </div>
                        </div>
                    </div>
                </div>`

        $('#items').append(mystr)
        
        $.ajax({
            type: 'POST',
            url: '/datacstfetch/',
            data: {name : int_val, qty_sheet : qty_sheets},
            success: function(data){
                $('#qty_set'+item).html(data.item['Qty'] + " " + "pcs");
                $('#cst_set'+item).html(data.item['calc']);
                itemCst += parseFloat(data.item['calc'])
            },
            async:false
        })


        
        // itemCst += $('#cst_set'+item).html()
        const img_card = document.querySelector('#image_loaded'+item)
        img_card.addEventListener('error', (e)=>{
            e.target.src = '/media/404error.png';
        })

    }
    var res = Math.round((itemCst + Number.EPSILON) * 100) / 100;
    var roundOff = Math.round((itemCst%1 + Number.EPSILON) * 100) / 100;
    document.querySelector('#itmTotal').innerHTML = res;
    document.querySelector('#itmRoundoff').innerHTML = roundOff;
    $('#amtPayble').append((res-roundOff)+70)
} else {
    $('#items').append("Please add products before you proceed")

}

function rem_item(item_id){
    delete cart[item_id]
    localStorage.setItem('cart', JSON.stringify(cart))
    location.reload();
}


function view_upload(upload_path){
    window.open('upload_path')
}

$('#itemJSON').val(JSON.stringify(cart))

document.querySelector('#addressnew').addEventListener('click', ()=>{
    document.querySelector('#newaddress1').checked=true;
})


document.querySelector('#orderbtn').addEventListener('click', ()=>{
    let radiobtn = document.getElementsByName('useradd')
    console.log('click')
    for (let i = 0; i < radiobtn.length; i++) {
        if (radiobtn[i].checked) {
            $('#address_stat').val(radiobtn[i].value);
            console.log(radiobtn[i].value)
        }
        
        
    }

})

function zipCheck(){
    console.log("Zip Clicked with ajax");

    $.ajax({
        type: 'POST',
        url: '/couriercheck/',
        data: {zip : $('#inputZip').val()},
        success: function(data){
            console.log(data.res)
            if (data.res['status'] == false ) {
                 $('#zipstatus').html("Non Serviceable Area");
                 $('#zipstatus').attr('class','zipres-red');
            } else {
                $('#zipstatus').html('Delivery time : Est. ' + data.res['days'] + ' Days');
                $('#zipstatus').attr('class','zipres-green');
            }

        },
        async:false
    })
}