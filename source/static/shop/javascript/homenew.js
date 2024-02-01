function toast2(){
    const toastLiveExample = document.getElementById('liveToast1');
    const toast = new bootstrap.Toast(toastLiveExample);
    toast.show()
}


 


function stickertype(cut){
    document.querySelector('#size_options').innerHTML = ""
    document.querySelector('#qty_options').innerHTML = ""
    if (cut == 'fc') {
        document.querySelector('#sticktype').innerHTML = ' Full Cut'
    } else if (cut == 'hc') {
        document.querySelector('#sticktype').innerHTML = ' Half Cut'
    } else if (cut == 'custom') {
        document.querySelector('#stickshape').innerHTML = ' Custom';
        cut = ['','1.5 X 1.5','2 X 2','2.5 X 2.5','3 X 2','3 X 3','4 X 3','4 X 4','5 X 3','6 X 4']; 
    } else if (cut == 'circle') {
        document.querySelector('#stickshape').innerHTML = ' Circle'
        cut = ['','1 X 1','1.5 X 1.5','2 X 2','2.5 X 2.5','3 X 3','3.5 X 3.5','4 X 4','5 X 5']; 
    } else if (cut == 'oval') {
        document.querySelector('#stickshape').innerHTML = ' Oval'
        cut = ['','2 X 1','2.5 X 1.5', '3 X 1.5','3 X 2','4 X 2','4 X 3','5 X 3','6 X 4']; 
    } else if (cut == 'square') {
        document.querySelector('#stickshape').innerHTML = ' Square'
        cut = ['','1 X 1','1.5 X 1.5','2 X 2','2.5 X 2.5','3 X 3','3.5 X 3.5','4 X 4','5 X 5']; 
    } else if (cut == 'rectangle') {
        document.querySelector('#stickshape').innerHTML = ' Rectangle'
        cut = ['','2 X 1','2.5 X 1.5','3 X 1','3 X 1.5','3 X 2','4 X 2','4 X 3','5 X 3','6 X 4']; 
    } else if (cut == 'normalwhite') {
        document.querySelector('#stickmaterial').innerHTML = ' Normal White'
    } else if (cut == 'pettrans') {
        document.querySelector('#stickmaterial').innerHTML = ' PET (Transparent)' 
    } else if (cut == 'petwhite') {
        document.querySelector('#stickmaterial').innerHTML = ' PET (White)'
    } 
    let sel = document.querySelector('#size_options')
    for (let count in cut) {
        newoption = document.createElement("option");
        newoption.value = cut[count];
        newoption.innerHTML = cut[count] + ' Inch';
        sel.options.add(newoption);
    }
}


function quantity(elem) {
    // console.log(elem.options[1].text);
    
    let qty = document.querySelector('#qty_options');
    if (elem.value == '1 X 1') {
        populate(184);
    } else if (elem.value == '1.5 X 1.5') {
        populate(77);
    } else if (elem.value == '2 X 2') {
        populate(40);
    } else if (elem.value == '2 X 1') {
        populate(85);
    } else if (elem.value == '2.5 X 1.5') {
        populate(44);
    } else if (elem.value == '3 X 1') {
        populate(51);
    } else if (elem.value == '3 X 1.5') {
        populate(33);
    } else if (elem.value == '2.5 X 2.5') {
        populate(24);
    } else if (elem.value == '3 X 3') {
        populate(15);
    } else if (elem.value == '3 X 2') {
        populate(25);
    } else if (elem.value == '3.5 X 3.5') {
        populate(12);
    } else if (elem.value == '4 X 2') {
        populate(16);
    } else if (elem.value == '4 X 3') {
        populate(12);
    } else if (elem.value == '4 X 4') {
        populate(8);
    } else if (elem.value == '5 X 3') {
        populate(10);
    } else if (elem.value == '5 X 5') {
        populate(6);
    } else if (elem.value == '6 X 4') {
        populate(5);
    } else {
        console.log('error')
    }
    document.querySelector('#sitcksize').innerHTML = elem.value 
    function populate(stickqty){
        document.querySelector('#qty_options').innerHTML = ""
        blank_option = document.createElement("option");
        blank_option.innerHTML = "Select Size"
        qty.options.add(blank_option)
        for (let index = 1; index < 21; index++) {
            val = stickqty;
            newoption = document.createElement("option");
            newoption.value = index;
            newoption.innerHTML = index + ' Sheet - ' + val*index + ' Pcs.';
            qty.options.add(newoption);
        }
    }  
}



function addcart(){
    let type = document.querySelector("#sticktype").innerHTML
    let shape = document.querySelector("#stickshape").innerHTML
    let size = document.querySelector("#sitcksize").innerHTML
    let qty = $('#qty_options').val()
    let material = document.querySelector("#stickmaterial").innerHTML
    let stk_image = imgscr
    if (type=="" || shape=="" || size=="" || qty=="" || material=="") {
        alert("Please ensure you complete every step")
    } else {
        // console.log(type + shape + size + qty + material + cost)
        if (cart_pr > 0){
            cart_itm_count[0] += 1
            cart_pr += 1
            cart[cart_pr] = [type, material, shape, size, qty, stk_image]
            localStorage.setItem('cart', JSON.stringify(cart))
            localStorage.setItem('cart_itm_count', JSON.stringify(cart_itm_count))
            location.reload();
        } else{
            cart_itm_count[0] = 1
            cart_pr = 1
            cart[cart_pr] = [type, material, shape, size, qty, stk_image]
            localStorage.setItem('cart', JSON.stringify(cart))
            localStorage.setItem('cart_itm_count', JSON.stringify(cart_itm_count))
            location.reload();
        }
    }
}



$('#qty_options').change(()=>{
    const int_val = $('#size_options').val();
    const qty_sheets = $('#qty_options').val();
    $.post('/datacstfetch/', { name : int_val, qty_sheet : qty_sheets}, function(data, status){
        $('#stickcost').html(data.item['calc'] + " " + "/-");
        $('#stickqty').html(data.item['Qty'] +" " + 'pcs');
    } )
})


const img_card = document.querySelector('#image_loaded')
let imgscr = img_card.getAttribute('src')

img_card.addEventListener('error', (e)=>{
    imgscr = img_card.getAttribute('src')
    e.target.src = '/media/404error.png';
})


