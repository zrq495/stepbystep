create table user(
    user_id int(11) primary key auto_increment,
    user_name varchar(20),
    poj_name varchar(100) not null,
    grade int(11),
    class1 varchar(20),
    permission int(11) default 1
)ENGINE=MyISAM DEFAULT CHARSET=utf8;

create table problem(
    pid int(11) primary key auto_increment,
    poj_pid int(11) not null,
    deadline varchar(20),
    cid int(11),
    foreign key(cid) references category(cid) on delete cascade on update cascade
)ENGINE=MyISAM DEFAULT CHARSET=utf8;

create table solution(
    user_id int(11),
    pid int(11),
    actime varchar(20),
    primary key(user_id ,pid),
    foreign key(user_id) references user(user_id) on delete cascade on update cascade,
    foreign key(pid) references problem(pid) on delete cascade on update cascade
)ENGINE=MyISAM DEFAULT CHARSET=utf8;

create table category(
    cid int(11) primary key auto_increment,
    rank varchar(20),
    cname varchar(100)
)ENGINE=MyISAM DEFAULT CHARSET=utf8;

create table startdate(
    id int(11) primary key auto_increment,
    start_date varchar(20),
    half int(11)
)ENGINE=MyISAM DEFAULT CHARSET=utf8;
