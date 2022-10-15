CREATE DATABASE mapeventProject CHARACTER SET utf8;

USE mapeventProject;
create table mapeventApp(
id int,
name varchar(222),
date_time varchar(222)
);

ALTER TABLE mapeventApp ENGINE=INNODB;

ALTER TABLE mapeventApp MODIFY date_time DATETIME(6);

select * from mapeventProject.auth_user;
replace into auth_user
set is_superuser = 1;
select * from mapeventProject.auth_user;
