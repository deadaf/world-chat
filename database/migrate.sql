CREATE TABLE IF NOT EXISTS guildconfig
(
    guild_id bigint NOT NULL,
    prefix character varying,
    webhook text,
    PRIMARY KEY (guild_id)
);


