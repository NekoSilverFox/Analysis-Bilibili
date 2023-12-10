------ bilibili 数据分析
create database db_bilibili;
use db_bilibili;

-- 加载 词云 数据
create table if not exists db_bilibili.word_cloud(
    word string,
    count int)
    row format serde 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
    with serdeproperties ("separatorChar"=",");
load data local inpath '/home/fox/bilibili/word_cloud.csv' overwrite into table db_bilibili.word_cloud;

-- 清洗 词云 数据 top1000
create table if not exists db_bilibili.word_cloud_top1000 AS
    SELECT word, CAST(count AS int) from word_cloud where word!='helliphellip' order by count DESC LIMIT 1000;

-- 加载 CSV 数据
create table if not exists tb_user_info(
    uid int,
    name string,
    avatar string comment '签名',
    level int,
    sex string,
    sign string comment '签名',
    vip_type int comment '会员类型（已过期不为0, 0为从来不是会员) 0：无 1：月度大会员 2：年度及以上大会员',
    vip_status int comment '会员状态码 0：无 1：有',
    vip_role  int comment '会员类型 0：无 1：月度大会员 3：年度大会员 7：十年大会员 15：百年大会员',
    archive  int comment '用户稿件数',
    fans int comment '粉丝数',
    friend int comment '关注数',
    like_num int comment '获赞数',
    is_senior int comment '是否为硬核会员 0：否 1：是')
    row format serde 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
    with serdeproperties ("separatorChar"="\u0001");

load data local inpath '/home/fox/bilibili/user_etl.csv' overwrite into table tb_user_info;

-- 数据清洗（如果不通过CAST指定类型，则全部会按照字符串导入）
create table db_bilibili.tb_user_info_etl comment 'bilibili user info ETL' STORED AS ORC AS
    select
        CAST(uid AS INT),
        name,
        avatar,
        CAST(level AS INT), -- 明确指定为 INT 类型
        sex,
        sign,
        CAST(vip_type AS INT),
        CAST(vip_status AS INT),
        CAST(vip_role AS INT),
        CAST(archive AS INT),
        CAST(fans AS INT),
        CAST(friend AS INT),
        CAST(like_num AS INT),
        CAST(is_senior AS INT)
    from db_bilibili.tb_user_info
    where  uid IS NOT NULL
        AND level IS NOT NULL
        AND name IS NOT NULL
        AND avatar IS NOT NULL
        AND sex IS NOT NULL
        AND sign IS NOT NULL
        AND vip_type IS NOT NULL
        AND vip_status IS NOT NULL
        AND vip_role IS NOT NULL
        AND archive IS NOT NULL
        AND fans IS NOT NULL
        AND friend IS NOT NULL
        AND like_num IS NOT NULL
        AND is_senior IS NOT NULL;

CREATE table db_bilibili.tb_total_count AS
    select min(uid) as uid_min, max(uid) as uid_max, count(*) as total_etl from tb_user_info_etl;

-- 删除老表
drop table db_bilibili.tb_user_info;

-- 统计等级分布
CREATE TABLE db_bilibili.tb_level_count comment '各等级人数' AS
    SELECT CAST(level AS INT) as level, count(*) AS level_cnt from db_bilibili.tb_user_info_etl group by level order by level DESC;

-- 统计性别比例
CREATE TABLE db_bilibili.tb_sex_count comment '性别比例' AS
    SELECT sex, count(*) AS sex_cnt from db_bilibili.tb_user_info_etl group by sex;

-- 随着等级增加性别的分布
CREATE TABLE if not exists db_bilibili.tb_sex_count_by_lever comment '随着等级增加性别的分布' AS (
    SELECT level, sex, CAST(count(*) AS INT) as sex_cnt from db_bilibili.tb_user_info_etl group by level, sex);

-- 会员类型统计
CREATE TABLE db_bilibili.tb_vip_role_count comment 'Count vip role where level>2' AS
    SELECT CAST(vip_role AS INT) AS vip_role, count(*) AS vip_role_cnt from db_bilibili.tb_user_info_etl where level>2 group by vip_role order by vip_role ASC;

-- 硬核会员统计
CREATE TABLE db_bilibili.tb_senior_count comment 'Count senior vip' AS
    SELECT CAST(is_senior AS INT) AS is_senior, count(*) AS is_senior_cnt from db_bilibili.tb_user_info_etl where level=6 group by is_senior;

-- 点赞最多的 top 50
CREATE TABLE db_bilibili.tb_likes_top50 comment '点赞最多的 top 50' AS
    SELECT
        uid,
        name,
        avatar,
        CAST(level AS INT), -- 明确指定为 INT 类型
        sex,
        sign,
        CAST(vip_type AS INT),
        CAST(vip_status AS INT),
        CAST(vip_role AS INT),
        CAST(archive AS INT),
        CAST(fans AS INT),
        CAST(friend AS INT),
        CAST(like_num AS INT),
        CAST(is_senior AS INT)
    from db_bilibili.tb_user_info_etl order by like_num DESC Limit 50;

-- 粉丝最多的 top 50
CREATE TABLE db_bilibili.tb_fans_top50 comment 'Fans top 50' AS
    SELECT
        uid,
        name,
        avatar,
        CAST(level AS INT), -- 明确指定为 INT 类型
        sex,
        sign,
        CAST(vip_type AS INT),
        CAST(vip_status AS INT),
        CAST(vip_role AS INT),
        CAST(archive AS INT),
        CAST(fans AS INT),
        CAST(friend AS INT),
        CAST(like_num AS INT),
        CAST(is_senior AS INT)
    from db_bilibili.tb_user_info_etl ORDER BY fans DESC Limit 50;

-- 好友最多的 top 50
CREATE TABLE db_bilibili.tb_friend_top50 comment '好友最多的 top 50' AS
    SELECT
        uid,
        name,
        avatar,
        CAST(level AS INT), -- 明确指定为 INT 类型
        sex,
        sign,
        CAST(vip_type AS INT),
        CAST(vip_status AS INT),
        CAST(vip_role AS INT),
        CAST(archive AS INT),
        CAST(fans AS INT),
        CAST(friend AS INT),
        CAST(like_num AS INT),
        CAST(is_senior AS INT)
    from db_bilibili.tb_user_info_etl ORDER BY friend DESC Limit 50;

-- 稿件数最多的 top 50
CREATE TABLE db_bilibili.tb_archive_top50 comment '稿件数最多的 top 50' AS
    SELECT

        name,
        avatar,
        CAST(level AS INT), -- 明确指定为 INT 类型
        sex,
        sign,
        CAST(vip_type AS INT),
        CAST(vip_status AS INT),
        CAST(vip_role AS INT),
        CAST(archive AS INT),
        CAST(fans AS INT),
        CAST(friend AS INT),
        CAST(like_num AS INT),
        CAST(is_senior AS INT)
    from db_bilibili.tb_user_info_etl ORDER BY archive DESC Limit 50;

-- 随着用户稿件数量增加，点赞量和播放量的关系，并且 level>3
CREATE TABLE db_bilibili.tb_rel_archive_fan_likes comment '粉丝数与播放量与稿件数量关系' AS
    select uid,
           CAST(level AS INT),
           CAST(vip_role AS INT),
           CAST(archive AS INT),
           CAST(fans AS INT),
           CAST(friend AS INT),
           CAST(like_num AS INT),
           CAST(is_senior AS INT)
           from db_bilibili.tb_user_info_etl where level>3 and archive>10 and like_num>100 and fans>100;

-- 开过会员的人数和类型
CREATE TABLE db_bilibili.tb_count_vip_type comment '开过会员的人数和类型' AS
    SELECT CAST(count(*) AS INT) as cnt, CAST(vip_type AS INT) AS vip_type
    FROM tb_user_info_etl
    GROUP BY vip_type;

-- 开过会员的人数和类型和等级
CREATE TABLE db_bilibili.tb_count_level_vip_type comment '开过会员的人数和类型' AS
    SELECT level, CAST(count(*) AS INT) as cnt, CAST(vip_type AS INT) AS vip_type
    FROM tb_user_info_etl
    GROUP BY level, vip_type;
