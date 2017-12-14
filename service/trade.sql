/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2017/12/14 16:24:21                          */
/*==============================================================*/


drop table if exists tb_account;

drop table if exists tb_account_asset;

drop table if exists tb_admin;

drop table if exists tb_broker;

drop table if exists tb_dept;

drop table if exists tb_server;

drop table if exists tb_sub_account;

drop table if exists tb_sub_account_asset;

drop table if exists tb_sub_account_trade;

drop table if exists tb_trade;

drop table if exists tb_trader;

drop table if exists tb_trader_asset;

/*==============================================================*/
/* Table: tb_account                                            */
/*==============================================================*/
create table tb_account
(
   account_id           integer not null auto_increment,
   broker               integer not null,
   admin                integer not null,
   name                 char(32) not null,
   user                 char(32) not null,
   pwd                  char(32) not null,
   cfrate               decimal(10,6) not null comment 'commission fee rate',
   cflimit              decimal(10,6) not null comment 'commission fee lower limit',
   bfrate               decimal(10,6) not null comment 'buy fee rate',
   sfrate               decimal(10,6) not null comment 'sell fee rate',
   disable              boolean not null default false,
   ctime                timestamp not null default CURRENT_TIMESTAMP,
   utime                timestamp not null default CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
   stime                bigint default NULL,
   primary key (account_id)
);

/*==============================================================*/
/* Table: tb_account_asset                                      */
/*==============================================================*/
create table tb_account_asset
(
   account              integer not null,
   code                 char(32) not null,
   name                 char(32) not null,
   tcost                decimal(10,2) not null comment 'trade cost',
   acost                decimal(10,2) not null comment 'asset cost',
   count                integer not null,
   available            integer not null,
   ctime                timestamp not null default CURRENT_TIMESTAMP,
   utime                timestamp not null default CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
   stime                bigint default NULL,
   primary key (account, code)
);

/*==============================================================*/
/* Table: tb_admin                                              */
/*==============================================================*/
create table tb_admin
(
   admin_id             integer not null auto_increment,
   name                 char(32) not null,
   user                 char(32) not null,
   pwd                  char(32) not null,
   role                 integer not null comment '0 - admin, 1 - risker, 2 - trader',
   ctime                timestamp not null default CURRENT_TIMESTAMP,
   primary key (admin_id)
);

/*==============================================================*/
/* Table: tb_broker                                             */
/*==============================================================*/
create table tb_broker
(
   broker_id            integer not null auto_increment,
   code                 char(32) not null comment '券商代码',
   name                 char(32) not null comment '券商名称',
   version              char(32) not null comment '客户端版本号',
   disable              boolean not null default false,
   ctime                timestamp not null default CURRENT_TIMESTAMP,
   primary key (broker_id)
);

/*==============================================================*/
/* Table: tb_dept                                               */
/*==============================================================*/
create table tb_dept
(
   dept_id              integer not null auto_increment,
   broker               integer not null,
   code                 char(32) not null comment '营业部代码',
   name                 char(128) not null comment '营业部名称',
   disable              boolean not null default false,
   ctime                timestamp not null default CURRENT_TIMESTAMP,
   primary key (dept_id)
);

/*==============================================================*/
/* Table: tb_server                                             */
/*==============================================================*/
create table tb_server
(
   server_id            integer not null auto_increment,
   broker               integer not null,
   name                 char(128) not null,
   host                 char(128) not null,
   port                 char(32) not null,
   type                 integer not null comment '0 - trade server, 1 - quote server',
   disable              boolean not null default false,
   ctime                timestamp not null default CURRENT_TIMESTAMP,
   primary key (server_id)
);

/*==============================================================*/
/* Table: tb_sub_account                                        */
/*==============================================================*/
create table tb_sub_account
(
   account_id           integer not null auto_increment,
   parent               integer not null,
   admin                integer not null,
   name                 char(32) not null,
   user                 char(32) not null,
   pwd                  char(32) not null,
   smoney               decimal(10,2) not null comment 'start money',
   lmoney               decimal(10,2) not null default 0.0 comment 'left money',
   wline                decimal(5,4) not null comment 'warning line',
   cline                decimal(5,4) not null comment 'close line',
   cfrate               decimal(10,6) not null comment 'commission fee rate',
   cflimit              decimal(10,6) not null comment 'commission fee lower limit',
   bfrate               decimal(10,6) not null comment 'buy fee rate',
   sfrate               decimal(10,6) not null comment 'sell fee rate',
   disable              boolean not null default false,
   ctime                timestamp not null default CURRENT_TIMESTAMP,
   primary key (account_id)
);

/*==============================================================*/
/* Table: tb_sub_account_asset                                  */
/*==============================================================*/
create table tb_sub_account_asset
(
   account              integer not null,
   code                 char(32) not null,
   name                 char(32) not null,
   tcost                decimal(10,2) not null comment 'trade cost',
   acost                decimal(10,2) not null comment 'asset cost',
   count                integer not null,
   available            integer not null,
   ctime                timestamp not null default CURRENT_TIMESTAMP,
   primary key (account, code)
);

/*==============================================================*/
/* Table: tb_sub_account_trade                                  */
/*==============================================================*/
create table tb_sub_account_trade
(
   trade_id             integer not null auto_increment,
   account              integer not null,
   code                 char(32) not null,
   name                 char(32) not null,
   count                integer not null,
   price                decimal(10,2) not null,
   ptype                integer not null,
   `option`             integer not null,
   dtime                bigint not null,
   dcount               integer not null,
   dprice               decimal(10,2) not null,
   cfee                 decimal(10,6) not null comment 'commission fee',
   tfee                 decimal(10,6) not null comment 'trade fee',
   status               integer not null,
   ctime                timestamp not null default CURRENT_TIMESTAMP,
   utime                timestamp not null default CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
   stime                bigint default NULL,
   primary key (trade_id)
);

/*==============================================================*/
/* Table: tb_trade                                              */
/*==============================================================*/
create table tb_trade
(
   trade_id             integer not null auto_increment,
   trader               integer not null,
   account              integer not null,
   code                 char(32) not null,
   name                 char(32) not null,
   count                integer not null,
   price                decimal(10,2) not null,
   ptype                integer not null,
   `option`             integer not null,
   dtime                bigint not null,
   dcount               integer not null,
   dprice               decimal(10,2) not null,
   cfee                 decimal(10,6) not null comment 'commission fee',
   tfee                 decimal(10,6) not null comment 'trade fee',
   status               integer not null,
   ctime                timestamp not null default CURRENT_TIMESTAMP,
   utime                timestamp default CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
   stime                bigint default NULL,
   primary key (trade_id)
);

/*==============================================================*/
/* Table: tb_trader                                             */
/*==============================================================*/
create table tb_trader
(
   trader_id            integer not null auto_increment,
   admin                integer not null,
   name                 char(32) not null,
   user                 char(32) not null,
   pwd                  char(32) not null,
   smoney               decimal(10,2) not null comment 'start money',
   lmoney               decimal(10,2) not null default 0.0 comment 'left money',
   disable              boolean not null default false,
   ctime                timestamp not null default CURRENT_TIMESTAMP,
   primary key (trader_id)
);

/*==============================================================*/
/* Table: tb_trader_asset                                       */
/*==============================================================*/
create table tb_trader_asset
(
   trader               integer not null,
   account              integer not null,
   code                 char(32) not null,
   name                 char(32) not null,
   count                integer not null,
   available            integer not null,
   ctime                timestamp not null default CURRENT_TIMESTAMP,
   primary key (trader, account, code)
);

alter table tb_account add constraint FK_Reference_16 foreign key (admin)
      references tb_admin (admin_id) on delete restrict on update restrict;

alter table tb_account add constraint FK_Reference_7 foreign key (broker)
      references tb_broker (broker_id) on delete restrict on update restrict;

alter table tb_account_asset add constraint FK_Reference_2 foreign key (account)
      references tb_account (account_id) on delete restrict on update restrict;

alter table tb_dept add constraint FK_Reference_8 foreign key (broker)
      references tb_broker (broker_id) on delete restrict on update restrict;

alter table tb_server add constraint FK_Reference_9 foreign key (broker)
      references tb_broker (broker_id) on delete restrict on update restrict;

alter table tb_sub_account add constraint FK_Reference_10 foreign key (parent)
      references tb_account (account_id) on delete restrict on update restrict;

alter table tb_sub_account add constraint FK_Reference_18 foreign key (admin)
      references tb_admin (admin_id) on delete restrict on update restrict;

alter table tb_sub_account_asset add constraint FK_Reference_11 foreign key (account)
      references tb_sub_account (account_id) on delete restrict on update restrict;

alter table tb_sub_account_trade add constraint FK_Reference_12 foreign key (account)
      references tb_sub_account (account_id) on delete restrict on update restrict;

alter table tb_trade add constraint FK_Reference_13 foreign key (trader, account, code)
      references tb_trader_asset (trader, account, code) on delete restrict on update restrict;

alter table tb_trader add constraint FK_Reference_17 foreign key (admin)
      references tb_admin (admin_id) on delete restrict on update restrict;

alter table tb_trader_asset add constraint FK_Reference_14 foreign key (trader)
      references tb_trader (trader_id) on delete restrict on update restrict;

alter table tb_trader_asset add constraint FK_Reference_15 foreign key (account, code)
      references tb_account_asset (account, code) on delete restrict on update restrict;

