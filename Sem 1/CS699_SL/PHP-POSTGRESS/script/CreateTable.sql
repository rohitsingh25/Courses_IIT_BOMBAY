CREATE TABLE users (
    roll_number varchar(256) PRIMARY KEY, 
    name varchar(256), 
    email_address varchar(256),
    password varchar(256)
);

CREATE TABLE marks (
    lab real,
    midsem real, 
    project real,
    endsem real,
    roll_number varchar(256) PRIMARY KEY,
    FOREIGN KEY (roll_number) REFERENCES users(roll_number)
);