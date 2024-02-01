This is an e-commerce website developed by me as a part of my work, We used this Website to take online orders for custom stickers.<br><br>
**General Flow of Customer:-** <br>
1. Uploading a custom design for Stickers <br>
(in the upload section we would accept file formats like pdf, cdr, ai, and all the image compression formats and save them into our user uploads folder)<br>
2. Selecting the shape, size, material, qty.<br>
(here we would allow the customer to select the desired specification for their stickers and the amount will be calculated and shown. _fetching and calculating is done by Ajax request_)<br>
3. Adding to the cart.<br>
(after adding their stickers to the cart users can view the uploaded design and specs and if the user is already logged in then in the delivery address section their default address (which was entered during the signup) will be shown and a possibility to add a new delivery address.)<br>
4. Placing Order.<br>
(after clicking the place order button, payment gateway API will be called which will redirect the customer to the payment gateway page where after the successful payment of the order user will be redirected to the final landing page.)<br>
5. Final Landing page.<br>
(On the final page there will be another check by the server to look for the successful payment by the customer, depending upon the reply from the gateway server API respective payment status will be displayed _ie payment success, payment failed, payment pending_ and various other details according to the status will be displayed. if the payment is a success an automated email will be generated about the order and sent to the user.)<br><br>

**User Profile Section**<br>
Here the customer can change their default address and can view their past orders and their invoices, here user can also get the tracking information about the order_(Which will also be provided in an automated email when the order is shipped)_.<br><br>

**Admin Page** _(only viewed by the admin)_<br>
The admin dashboard is the place where anything regarding the customer and their orders can be changed and viewed, whenever the product is shipped the tracking ID is updated through the admin page.<br>
   
