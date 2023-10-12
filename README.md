# MyShop
#### Video Demo:  https://youtu.be/DfG3kgzQPzo
#### Description:

My project is a small online shop. I used flask, python, javascript, html, and css to build this project.
 My project contains some main pages.
> The _register_ page.

On this page, a user can create an account if he or she does not have one,
by adding a unique username, a password, and a configuration of the password. After registration, the website drives the user to the _home page_.

> The _login_ page.

If the user already has an account, he or she can log in to the website via this page by entering their username, and password.
After this, the website will drive the user to the _home page_.

> The main page _home page_.

To open this page the user must be registered or logged in to the website with a valid username and password.
Products are presented on this page, which allows the user to display the information about the product the user has chosen and allows him or her to
rate it.
Also, users can add the product to their cart from this page, there is a section on the right of the page, when the user selects a product all the
information about this product is presented in this section, and the button that allows the user to add the product to the cart.
In addition, there is a menu button on the top right of all pages, that allows users to transport between different pages.
One more thing, there are the search field and filter selection buttons that allow users to filter the products they want to buy or looking for.



>The _cart_ page.

On this page, the user can find all products he or she has selected before on ``_home page_``, and the user can click the info button to display the
information of the selected product on the right side of the page same as on the home page.
Users can remove any product from their cart by clicking the remove button that appears after selecting a product.
There is a long button under the nav bar that shows the price of all products in the cart and the user can complete the buying process by clicking
on this button. After clicking on this button all the products in the cart will disappear and the cart will be empty.
This process will be recorded on the ``"product I bought"`` section, that section user can reach from the profile page.


>The _profile_ page.

This page displays the user information like their username, profile image, email, phone number, and two links that drive the user to the history of
their purchases processes and the products that the user is selling, first link has text: ``"product I bought"`` and the other has text: ``"product I sell"``.

>The _operations_ page.

The user can visit this page by clicking on the ``"product I bought"`` link on the `_profile_ page`. This page displays all user's purchases processes
in an organized table, representing in this table the product name, date, price, and quantity of this product at this time.



> The _admin_ page.

The user can visit this page by clicking on the `"product I sell"` link on the `_profile_ page`. This page display all products the user put to sell on this website if found. And this page allows the user to add products to sell them on this website by clicking on the adding button.
After clicking on that button, a small form appears on the right side of the page, this form takes some information about the product the user wants to sell like name, image, price, quantity, category of the product, and a small description. After filling in this piece of information, the user can click on the `"add product"` button to add this product.
