create database product_List;

show databases;

use product_List;

show tables;
drop table products;

create table `products`(
    `product_id` int not null auto_increment,
    `product_name` varchar(255) not null,
    `product_description` varchar(1023) not null,
    `product_category` varchar(255) not null,
    `product_price` decimal(15,2) not null,
    `product_image` varchar(255) not null,
    primary key(`product_id`)
);


INSERT INTO products(
    `product_name`,
    `product_description`,
    `product_category`,
    `product_price`,
    `product_image`
)VALUES(
	"PS5",
    "É um PS5 mermão, que mais tu quer saber?",
    "Videogame, né animal?",
    5499.99,
    "5IjvCH5cYUSF8ePcjJm1KQ==.jpg"
    );
    
    
    select * from products;
    