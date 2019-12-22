/* This file contains table definitions 
 */

create database msdb if not exists msdb;
use msdb;

-- nian ganzhi
/*
60 ganzhi table
from:甲子
to:癸亥
id :
initial value :0 
end value:59
*/
create table if not exists nianganzhi (
    id integer unsigned not null auto_increment primary key,
    ganzhi char(8) not null,
    sitian varchar(12) not null,
    zaiquan varchar(12) not null,
    dayun varchar(12) not null,
    zhuyun varchar(128) not null,
    keyun varchar(128) not null,
    zhuqi varchar(128) not null,
    keqi varchar(128) not null,
    index showing_ganzhi(ganzhi)
) engine=InnoDB DEFAULT CHARSET=utf8;


