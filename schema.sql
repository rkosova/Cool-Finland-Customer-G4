drop table if exists users;
drop table if exists deliveries;


create table users (
 	id integer primary key autoincrement,
 	email text not null,
 	password text not null,
 	c_name text not null,
 	rep_n text not null,
 	rep_ln text not null,
 	rep_pnum text not null
);


create table deliveries (
	id integer primary key autoincrement,
	customer_id integer,
	weight_amount float(3) not null,
	delivery_date datetime not null,
	foreign key (customer_id) references users (id)
);