CREATE TABLE `st_market` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `trade_date` date NOT NULL COMMENT '交易日期',
  `type` char(2) NOT NULL COMMENT '市场类型 1-上海a股',
  `type_name` varchar(255) DEFAULT NULL COMMENT '市场类型 中文',
  `total_value` decimal(15,2) DEFAULT NULL COMMENT '市场总市值',
  `total_num` decimal(15,2) DEFAULT NULL COMMENT '成交量（万股）',
  `total_money` decimal(15,2) DEFAULT NULL COMMENT '成交金额',
  `pe` decimal(8,2) DEFAULT NULL COMMENT '平均市盈率',
  `modify_time` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=innodb  DEFAULT CHARSET=utf8;


CREATE TABLE `st_stock` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `trade_date` date NOT NULL COMMENT '交易日期',
  `code` varchar(20) NOT NULL COMMENT '股票代码',
  `name` varchar(255) DEFAULT NULL COMMENT '股票名称',
  `place` varchar(255) DEFAULT NULL COMMENT '交易所',
  `pe` decimal(8,2) DEFAULT NULL COMMENT '市盈率',
  `pb` decimal(8,2) DEFAULT NULL COMMENT '市净率',
  `ps` decimal(8,2) DEFAULT NULL COMMENT '市销率',
  `price` decimal(10,2) DEFAULT NULL COMMENT '收盘价格',
  `modify_time` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=innodb  DEFAULT CHARSET=utf8;