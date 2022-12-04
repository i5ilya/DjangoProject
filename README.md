# DjangoProject

## Basic Django E-Commerce web shop + Servio API

Full functional hosted demo [https://demoservioshop.tk/](https://demoservioshop.tk/) 

* Responsive design (bootstrap)
* Category tree structure
* Shopping cart in sessions
* Add to cart with main by JS-powered function no page reload
* Checkout
* Synchronization of the menu (with a tree structure) with the servo API through the admin interface (django actions) with the issuance of messages to the user about successful or erroneous synchronization (Handling connection errors and errors in api responses)
* Setting up the connection to the API is done through the site admin panel, the database only needs to specify the ID of the root folder from Servio.
* Synchronization of product images (only by url, the image is downloaded and installed automatically)
* Automatic cleaning of images not linked to site products
* AWS linux ubuntu hosted with gunicorn and Nginx


## Some screens from Django Admin:

* Add new Servio API connection:
![](/for_description/add-new-connection.png)

* Connection error:
![](/for_description/no-connection-massage.png)

* Handling errors from API response:
![](/for_description/token-error.png)

* Successful sync massage:
![](/for_description/successful-massage.png)
