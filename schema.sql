CREATE TABLE Owner (
    ssn INT PRIMARY KEY NOT NULL,
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL,
    birthday DATE NOT NULL,
    address VARCHAR(50) NOT NULL
);

CREATE TABLE Gun (
    serial_number INT PRIMARY KEY NOT NULL,
    type VARCHAR(20) NOT NULL,
    ssn INT NOT NULL,
    model VARCHAR(30) NOT NULL,
    caliber VARCHAR(30) NOT NULL
);

CREATE TABLE Seller (
    name VARCHAR(50) NOT NULL,
    address VARCHAR(50) NOT NULL ,
    ssn INT NOT NULL,
    serial_number INT PRIMARY KEY NOT NULL
);

CREATE TABLE Manufacturer (
    name VARCHAR(50) PRIMARY KEY NOT NULL,
    country_of_origin VARCHAR(30) NOT NULL,
    model VARCHAR(30) NOT NULL,
    caliber VARCHAR(30) NOT NULL
);
