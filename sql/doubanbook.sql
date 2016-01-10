CREATE TABLE `book` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `bookname` varchar(100) NOT NULL COMMENT '书名',
  `bookurl` varchar(150) NOT NULL COMMENT '书入口',
  `bookimg` varchar(150) DEFAULT NULL COMMENT '书图片',
  `bookinfo` varchar(250) DEFAULT NULL COMMENT '书出版信息',
  `bookstar` varchar(45) DEFAULT NULL COMMENT '书评价星数',
  `bookno` varchar(45) NOT NULL COMMENT '书编号',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='书表';

CREATE TABLE `booktag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bookname` varchar(100) DEFAULT NULL COMMENT '书名',
  `bookno` varchar(45) DEFAULT NULL COMMENT '书编号',
  `booktag` varchar(45) DEFAULT NULL COMMENT '书标签',
  `bookkind` varchar(45) DEFAULT NULL COMMENT '书分类',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='书标签';

CREATE TABLE `bookdetial` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bookname` varchar(100) NOT NULL COMMENT '书名',
  `bookno` varchar(45) NOT NULL COMMENT '书编号',
  `bookinfo` text COMMENT '书出版信息',
  `bookintro` text COMMENT '书介绍',
  `authorintro` text COMMENT '作者介绍',
  `peoples` int(11) DEFAULT NULL COMMENT '评价人数',
  `starts` varchar(100) DEFAULT NULL COMMENT '星级情况',
  `other` text COMMENT '其他信息',
  `mulu` mediumtext COMMENT '图书目录',
  `comments` mediumtext COMMENT '评论人',
  PRIMARY KEY (`id`),
  UNIQUE KEY `bookno_UNIQUE` (`bookno`)
) ENGINE=InnoDB AUTO_INCREMENT=18149 DEFAULT CHARSET=utf8 COMMENT='图书详情表';
