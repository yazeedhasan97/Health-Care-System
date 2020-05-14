create table private.users (
	id serial PRIMARY key,
	email varchar unique not null,
	name varchar not null,
	password varchar not null,
	age int not null,
	role int not null,
	gender text not null,
	phone varchar unique,
	address varchar,
	image varchar not null
);
drop table private.users;

insert into private.users
	(id, email, name, password, role, gender, age, phone, address, image)
values 
	(1, 'yazeed.hasan.97@gmail.com', 'yazeed hasan', '12345', 0, 'male', 23, '0798529788', '', '../static/img/person.jpg');


select * from private.users;

update private.users set address = '' where email = 'yazeed.hasan.97@gmail.com';
update private.users set role = 2 where email = 'yazeed.79@hotmail.com';
update private.users set image =  '../static/img/person.jpg' where email = 'yazeed.79@hotmail.com';


create table private.doctors (
	id int unique not null REFERENCES private.users(id),
	patiant_count int not null DEFAULT 0,
	major varchar not null
);
drop table private.Doctors;


create table private.patiant (
	id serial primary key,
	name varchar not null,
	age int not null,
	gender text not null,
	phone varchar unique,
	address varchar
);
drop table private.patiant;
select * from private.patiant;

insert into private.patiant
	(id, name, age, gender , phone , address)
values 
	();

DELETE FROM table_name WHERE condition;


create table private.allergies (
	id serial primary key,
	p_id int not null REFERENCES private.patiant(id),
	allergie varchar not null
);
drop table private.allergies;
select * from private.allergies;

create table private.session (
	s_id serial primary key,
	s_date date not null,
	start_time timestamp not null,
	end_time timestamp not null,
	diag varchar not null,
	medicine varchar,
	lab_test varchar,
	u_id int unique not null REFERENCES private.users(id),
	p_id int unique not null REFERENCES private.patiant(id)
);
drop table private.session;
select * from private.session;

insert into private.session
	(s_date, start_time, end_time, diag, medicine, lab_test)
values
	(date(now()), now() - interval '30 minute', now(), 'The patiant have Cancer', 'Kimaks bobles', 'X-Ray', 4, 15)


select s_date, diag, medicine, lab_test from private.session
where u_id = 4 and p_id = 15 order by s_date;




create table private.user_to_pat (
	id serial primary key,
	p_id int unique not null REFERENCES private.patiant(id),
	arrival_time timestamp not null,
	heart_rate decimal not null DEFAULT 70,
	tempreture int not null DEFAULT 37
);
drop table private.user_to_pat;
select * from private.user_to_pat;






