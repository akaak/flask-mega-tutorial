drop table if exists business;

create table business (
	id integer primary key autoincrement,
	name text not null,
	description text not null,
	added_date date not null
);
