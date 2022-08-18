CREATE TABLE IF NOT EXISTS `webpage_info`
(
    `id`                bigint(20) auto_increment NOT NULL COMMENT 'id',
    `url`               varchar(1000)             NOT NULL COMMENT 'short url in comments',
    `url_hash`          varchar(32)               NOT NULL DEFAULT '' COMMENT 'md5(url)',
    `landing_page`      varchar(3000)             NOT NULL DEFAULT '' COMMENT 'first landing page of short url',
    `intermediate_urls` mediumtext                NOT NULL COMMENT '从 short url 到 first landing page 中间经过的 URLs',
    `html`              mediumtext                NOT NULL COMMENT 'HTML源码',
    `text`              mediumtext                NOT NULL COMMENT 'webpage中的文本内容',
    `vpn`               varchar(50)               NOT NULL DEFAULT '' COMMENT '访问时使用的vpn节点',

    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8 COMMENT ='webpage_info';

alter table webpage_info
    convert to character set utf8mb4;