drop table if exists users;


create table users (
 	id integer primary key autoincrement,
 	email text not null,
 	password text not null,
 	name text not null,
 	p_number text not null
);
