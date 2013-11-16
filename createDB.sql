create table user(
user_id int(11) primary key auto_increment,
user_name varchar(20),
poj_name varchar(100) not null,
grade int(11),
class1 varchar(20)
)ENGINE=MyISAM DEFAULT CHARSET=utf8;

create table problem(
pid int(11) primary key auto_increment,
poj_pid int(11) not null
)ENGINE=MyISAM DEFAULT CHARSET=utf8;

create table solution(
user_id int(11),
pid int(11),
primary key(user_id ,pid),
foreign key(user_id) references user(user_id) on delete cascade on update cascade,
foreign key(pid) references problem(pid) on delete cascade on update cascade
)ENGINE=MyISAM DEFAULT CHARSET=utf8;
