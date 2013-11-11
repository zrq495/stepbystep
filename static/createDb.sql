create table category(
CID int(11) primary key auto_increment,
CName varchar(100)
)ENGINE=MyISAM DEFAULT CHARSET=utf8;

create table SubCategory(
SubCID int(11) primary key auto_increment,
SubCName varchar(100),
CID int(11),
foreign key(CID) references category(CID) on delete cascade on update cascade
)ENGINE=MyISAM DEFAULT CHARSET=utf8;

create table user(
UID int(11) primary key auto_increment,
UserName varchar(100),
Password varchar(200),
Email varchar(100),
Permission int(11)
)ENGINE=MyISAM DEFAULT CHARSET=utf8;

create table problem(
ID int(11) primary key auto_increment,
OJName varchar(100),
PID varchar(10),
AddUserID int(11),
PUrl varchar(200),
foreign key(AddUserID) references user(UID) on delete cascade on update cascade
)ENGINE=MyISAM DEFAULT CHARSET=utf8;

create table solution(
SID int(11) primary key auto_increment,
SUrl varchar(200),
PID int(11),
AddUserID int(11),
foreign key(PID) references problem(ID) on delete cascade on update cascade,
foreign key(AddUserID) references user(UID) on delete cascade on update cascade
)ENGINE=MyISAM DEFAULT CHARSET=utf8;

create table ProCate(
ID int(11) primary key auto_increment,
PID int(11),
SubCID int(11),
foreign key(PID) references problem(ID) on delete cascade on update cascade,
foreign key(SubCID) references SubCategory(SubCID) on delete cascade on update cascade
)ENGINE=MyISAM DEFAULT CHARSET=utf8;
