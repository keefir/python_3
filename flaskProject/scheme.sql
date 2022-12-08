drop table if exists users;
create table users (
    id integer primary key autoincrement,
    email text not null,
    name text not null,
    login text not null,
    password text not null
);