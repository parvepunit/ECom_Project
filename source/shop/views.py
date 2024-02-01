
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from shop.models import Product, Calculation_price
from math import ceil 
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from accounts.decorators import *
from accounts.models import CustomUser, Order, Customer
import json, math, base64, hashlib, requests, datetime


# imports for email
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings



datetoday = datetime.datetime.now()
# Create your views here.


def checkout(request):
    orders = Order.objects.all()

    def phonepeinte(orderId, custId, cost, custMob, custEmail):
        merchId = 'PGTESTPAYUAT'
        salt = '099eb0cd-02cf-4e2a-8aca-3e6c6aff0399'

        req_header = {
                        "merchantId": merchId,
                        "merchantTransactionId": orderId,
                        "merchantUserId": str(custId),
                        "amount": int(cost*100),
                        "redirectUrl": f"https://stickycatstickers.in/shop/order_status/{orderId}/?res={custEmail}",
                        "redirectMode": "GET",
                        "callbackUrl": "",
                        "mobileNumber": str(custMob),
                        "paymentInstrument": {
                            "type": "PAY_PAGE"
                        }
                    }
        

        b64request = base64.b64encode(json.dumps(req_header).encode("utf-8")).decode("utf-8")
        xverify = (hashlib.sha256((b64request+"/pg/v1/pay"+salt).encode())).hexdigest()+"###1"
        
        #Phonepe API Starts
        url = "https://api.phonepe.com/apis/hermes/pg/v1/pay"
        payload = {"request": b64request}
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "X-VERIFY": xverify
        }

        response = requests.post(url, json=payload, headers=headers)
        
        resDict = json.loads(response.text)

        if resDict['code']=='PAYMENT_INITIATED':
            redirectLink = resDict['data']['instrumentResponse']['redirectInfo']['url']
            return redirectLink
        else:
            return "none"
            
            
        #Phonepe API Ends



    def cost_calc(items_dict):
        cost_calc = {'total': 0, 'gst': 0, 'sub_total': 0, 'finalTotal':0, 'round_off':0}
        for item in items_dict:
            price_lookup = Calculation_price.objects.get(
                size=items_dict[item][3])
            cost_calc['sub_total'] += price_lookup.cst_persheet * \
                int(items_dict[item][4])

        cost_calc['sub_total'] = math.floor(cost_calc['sub_total'] * 1.02)
        cost_calc['gst'] = cost_calc['sub_total']*0.18
        cost_calc['total'] = cost_calc['sub_total'] + cost_calc['gst']
        roundoff_val = cost_calc['total']%1
        cost_calc['round_off'] = roundoff_val
        cost_calc['finalTotal'] = cost_calc['total']-roundoff_val+70
        return cost_calc

    def orderdbsave(orderItem, orderName, orderPhone, orderAdd, orderState, orderId, orderAmt):
        if request.user.is_authenticated:
            customerID = customer.id
        else:
            customerID = 1
        items_json = orderItem
        name = orderName
        phone = orderPhone
        address = orderAdd
        delivery_state = orderState
        order_amt = orderAmt
        checkout = Order(customer_id=customerID, order_details=items_json, order_name=name, order_phone=phone, order_address=address,
                         order_deliveryState=delivery_state, order_id=orderId, order_amount=order_amt, order_status='In Process')
        checkout.save()


    if request.user.is_authenticated:

        customer = CustomUser.objects.get(email=request.user)
        address = Customer.objects.filter(user_id=customer)
        # this get function is only used for placing the order for registered user with details in Customer Model
        add_user = Customer.objects.get(user_id=customer.id)

        if request.method == "POST":
            address_status = request.POST.get('address_status', '')
            items_json = request.POST.get('itemJSON', '')
            if len(items_json) > 2 :
                if address_status == 'newadd':
                    order_id = f'{datetoday.strftime("%m%y")}-{orders.count()}'
                    # order_cost = cost_calc(json.loads(items_json))['total']
                    cost_dict = cost_calc(json.loads(items_json))
                    grand_total = int(cost_dict['finalTotal'])

                    
                    order_email = request.user

                    new_phone = request.POST.get('inputPhone', '')
                    chck = request.POST

                    lin = "none"

                    if chck['inputname']=="" or chck['inputAddress']=="" or chck['inputAddress2']=="" or chck['inputPhone']=="" or chck['inputCity']=="" or chck['inputState']=="" or chck['inputZip']=="" :
                        messages.success(request, "Please fill out every detail for new address")
                    else :
                    
                        orderdbsave(
                            items_json,
                            request.POST.get('inputname', ''),
                            request.POST.get('inputPhone', ''),
                            request.POST.get('inputAddress', '') + ", " + request.POST.get('inputAddress2', '') + ", " + request.POST.get(
                                'inputCity', '') + ", " + request.POST.get('inputState', '') + ", " + request.POST.get('zipCode', ''),
                            request.POST.get('inputState', ''),
                            order_id,
                            order_cost
                        )
                    

                        email_dict = json.dumps({'cost_dict':cost_dict, 'email':str(order_email)})
                        b64_parameter = base64.b64encode(email_dict.encode("utf-8")).decode("utf-8")
                        lin = phonepeinte(order_id,customer.id,grand_total,new_phone, b64_parameter)
                        
                    
                    if lin == "none":
                        messages.success(request, "Payment Server Error ! Please try again later")
                        return redirect('checkout')
                    else:
                        return redirect(str(lin))

                elif address_status == 'defaultadd':
                    order_id = f'{datetoday.strftime("%m%y")}-{orders.count()}'

                    cost_dict = cost_calc(json.loads(items_json))

                    grand_total = int(cost_dict['finalTotal'])

                    order_email = request.user

                    orderdbsave(
                        items_json,
                        customer.first_name + " " + customer.last_name,
                        customer.phone_no,
                        add_user.address1 + ", " + add_user.address2 + ", " +
                        add_user.city + ", " + add_user.State + ", " + add_user.zip,
                        add_user.State,
                        order_id,
                        grand_total
                    )

                    email_dict = json.dumps({'cost_dict':cost_dict, 'email':str(order_email)})
                    b64_parameter = base64.b64encode(email_dict.encode("utf-8")).decode("utf-8")

                    lin = phonepeinte(order_id,customer.id,grand_total,customer.phone_no, b64_parameter)

                    # lin = "none"

                    if lin == "none":
                        messages.success(request, "Payment Server Error ! Please try again later")
                        return redirect('checkout')
                    else:
                        return redirect(str(lin))
                   
                else:
                    messages.success(request, "Please Select Address")
            else:
                    messages.success(request, "Opps..!! Your Cart is Empty")

        

        context_auth = {
            'addresses': address,
            'customer': customer
        }
        return render(request, "shop/checkout.html", context_auth)
    else:
        if request.method == "POST":
            items_json = request.POST.get('itemJSON', '')
            order_id = f'{datetoday.strftime("%m%y")}-{orders.count()}'
            order_cost = cost_calc(json.loads(items_json))['total']
            order_newemail = request.POST.get('inputemail', '')
            chck = request.POST

            cost_dict = cost_calc(json.loads(items_json))
            grand_total = int(cost_dict['finalTotal'])
            order_email = request.POST.get('inputemail', '')
            new_phone = request.POST.get('inputPhone', '')

            lin = "none"
            if chck['inputname']=="" or chck['inputAddress']=="" or chck['inputAddress2']=="" or chck['inputPhone']=="" or chck['inputCity']=="" or chck['inputState']=="" or chck['inputZip']=="" :
                messages.success(request, "Please fill out every detail for new address")
            else :
                print('false')


                orderdbsave(
                    items_json,
                    request.POST.get('inputname', ''),
                    request.POST.get('inputPhone', ''),
                    request.POST.get('inputAddress', '') + ", " + request.POST.get('inputAddress2', '') + ", " + request.POST.get(
                        'inputCity', '') + ", " + request.POST.get('inputState', '') + ", " + request.POST.get('zipCode', ''),
                    request.POST.get('inputState', ''),
                    order_id,
                    order_cost
                )



                email_dict = json.dumps({'cost_dict':cost_dict, 'email':str(order_email)})
                b64_parameter = base64.b64encode(email_dict.encode("utf-8")).decode("utf-8")
                lin = phonepeinte(order_id,'1',grand_total,new_phone, b64_parameter)

                
            if lin == "none":
                messages.success(request, "Payment Server Error ! Please try again later")
                return redirect('checkout')
            else:
                return redirect(str(lin))

    if request.method == "GET":


        return render(request, "shop/checkout.html")


def home(request):
    context = {}
    if request.method == 'POST':
        try:
            uploaded_file = request.FILES["designUpload"]
            fs = FileSystemStorage(location='media/user_upload',
                                base_url='media/user_upload')
            name = fs.save(uploaded_file.name, uploaded_file)

            context['name'] = name
            messages.success(request, ("Upload Sucessfull"))
        except:
            messages.success(request, ("File was not uploaded, please check file format and upload again."))
    return render(request, 'shop/index.html', context)


@csrf_exempt
def datacstfetch(request):
    name = request.POST.get('name')
    qty_sheets = request.POST.get('qty_sheet')
    sizes = Calculation_price.objects.all()
    calc = 0
    qty = 0
    json_str = {"calc": 0, "Qty": 0}

    for sze in sizes:
        if sze.size == name:
            qty_sheet = int(qty_sheets)
            qty_stick = int(sze.qty_persheet)
            cst_sheet = int(sze.cst_persheet)
            calc = math.floor(((qty_sheet * cst_sheet)*1.02))
            gst = calc*0.18
            qty = qty_stick * qty_sheet
            json_str['calc'] = ("%.2f" %(calc+gst))
            json_str['Qty'] = qty

            return JsonResponse({'item': json_str})
        
@csrf_exempt
def couriercheck(request):
    zip = request.POST.get('zip')
    json_str = {"status": False, "days": 0}
    
    url = "https://apiv2.shiprocket.in/v1/external/courier/serviceability/"

    token = settings.SHIPROCKET_TOKEN

    payload= json.dumps({
    "pickup_postcode": 462016,
    "delivery_postcode" : zip,
    "cod" : 0,
    "weight":1
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    res_dict = json.loads(response.text)
    
    try:
        json_str['days'] = res_dict['data']['available_courier_companies'][0]['estimated_delivery_days']
        json_str['status'] = True
        return JsonResponse({'res': json_str})
    except:
        return JsonResponse({'res': json_str})



def email_temp(request):
    order = Order.objects.get(order_id="0223-7")
    order_items = json.loads(order.order_details)
    
    context = {'order_id': order.order_id, 'cart': order_items}
    return render(request, 'tracking_email.html', context)
 
    # return render(request, 'shop/datafetch.html', {'item' : json.dumps(json_str) })


@csrf_exempt
def order_status(request, orderId):
    order = Order.objects.get(order_id=orderId)
    # res = request.GET.get('res')
    
    # if res != None:
    #     res_dict = json.loads(base64.b64decode(res.encode('ascii')).decode('ascii'))
    #     email_dict = res_dict['cost_dict']
    #     email_email= res_dict['email']
    #     email_to = [str(email_email)]


    # def sendmail(orderId, orderGst, orderSubTotal, orderTotal, grandTotal, roundOff, orderEmail):
    #     html_template = 'email.html'
    #     html_msg = render_to_string(html_template, {'order_id': orderId, 'cart': json.loads(
    #         order.order_details), 'gst': "%.2f" %orderGst, 'sub_total': "%.2f" %orderSubTotal, 'total': "%.2f" %orderTotal, 'round_off': "%.2f" %roundOff, 'grand_total':"%.2f" %grandTotal})
    #     subject = "Your Stickycat Order #" + orderId
    #     recipient = email_to
    #     email_from = settings.EMAIL_HOST_USER
    #     message = EmailMessage(subject, html_msg, email_from, recipient)
    #     message.content_subtype = 'html'
    #     message.send()

    
    merchId = settings.MERCH_ID
    salt = settings.MERCH_SALT
    # url = f"https://api.phonepe.com/apis/hermes/pg/v1/status/{merchId}/{orderId}"

    # xverify = (hashlib.sha256(("/pg/v1/status/"+merchId+"/"+orderId+salt).encode())).hexdigest()+"###1"

    # headers = {
    #     "accept": "application/json",
    #     "Content-Type": "application/json",
    #     "X-VERIFY": xverify,
    #     "X-MERCHANT-ID": merchId
    # }

    # response = requests.get(url, headers=headers)
    # try:
    # res_dict = json.loads(response.text)
    res_dict = {
        "success": True,
        "code": "PAYMENT_PENDING",
        "message": "Payment Failed",
        "data": {
            "merchantId": "FKRT",
            "merchantTransactionId": "MT7850590068188104",
            "transactionId": "T2111221437456190170379",
            "amount": 100,
            "state": "FAILED",
            "responseCode": "ZU",
            
        }
        }


    # try:
    if res_dict['code'] == 'PAYMENT_SUCCESS':
        # order.payment_status = 'PAYMENT_SUCCESS'
        # order.payment_instrument = res_dict['data']['paymentInstrument']
        # order.pg_transact_id = res_dict['data']['merchantTransactionId']
        # order.save()

        final_dict = {
            'status': 'PAYMENT_SUCCESS',
            'transaction_id':res_dict['data']['transactionId'],
            'order_id':res_dict['data']['merchantTransactionId'],
            'amount':res_dict['data']['amount']/100,
        }
        # if res != None:
        #     sendmail(orderId,email_dict['gst'],email_dict['sub_total'],email_dict['total'],email_dict['finalTotal'],email_dict['round_off'],email_email)

        return render(request,'shop/payment.html', context={'final_dict':final_dict})

    elif res_dict['code'] == 'PAYMENT_PENDING':
        order.payment_status = 'PAYMENT_PENDING'
        order.save()
        final_dict = {
            'status': 'PAYMENT_PENDING',
            'order_id' : orderId
            
        }

        return render(request,'shop/payment.html', context={'final_dict':final_dict})

    else :
        order.payment_status = 'FAILED'
        order.save()
        final_dict = {
            'status': 'FAILED',
            'transaction_id':res_dict['data']['transactionId'],
            'order_id':res_dict['data']['merchantTransactionId'],
            'amount':res_dict['data']['amount']/ 100,
        }

        return render(request,'shop/payment.html', context={'final_dict':final_dict})
    

    # except:

    #     if res_dict['message'] == 'Request failed.' and res_dict['status'] == '500':
    #         final_dict = {
    #                 'status': 'NOT_placed',
    #                 'order_id' : orderId
    #             }
        
    #         return render(request,'shop/payment.html', context={'final_dict':final_dict})
    #     else:
    #         final_dict = {
    #                 'status': 'SERVER_ERROR',
    #                 'order_id' : orderId
    #             }
        
    #         return render(request,'shop/payment.html', context={'final_dict':final_dict})


def tracking(request):

    def shipingdetail (awb_no) :
        url = f"https://apiv2.shiprocket.in/v1/external/courier/track/awb/{awb_no}"

        token = settings.SHIPROCKET_TOKEN

        payload={}
        headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        res_dict = json.loads(response.text)
        return res_dict
    

    if request.method == 'POST':

        awb = request.POST.get('awb')
        radio = request.POST.get('flexRadioDefault')    


        try:
            if radio=='awb':
                res_dict = shipingdetail(awb)
                context = {
                    'status' : res_dict['tracking_data']['shipment_track'][0],
                    'history' : res_dict['tracking_data']['shipment_track_activities']
                }
                return render (request, 'shop/tracking.html', context)
            elif radio=='id':
                order = Order.objects.get(order_id=awb)
                res_dict = shipingdetail(order.order_trackingId)
                context = {
                    'status' : res_dict['tracking_data']['shipment_track'][0],
                    'history' : res_dict['tracking_data']['shipment_track_activities']
                }
            
                return render (request, 'shop/tracking.html', context)

        except:
            messages.success(request, ("Aahh! There is no activities found in our DB. Please have some patience it will be updated soon or Check your input."))



    return render (request, 'shop/tracking.html')
    
    

