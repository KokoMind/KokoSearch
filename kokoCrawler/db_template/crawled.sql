--
-- File generated with SQLiteStudio v3.1.1 on Mon Mar 20 01:31:33 2017
--
-- Text encoding used: UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: crawled
DROP TABLE IF EXISTS crawled;

CREATE TABLE crawled (
    id           INTEGER       NOT NULL
                               PRIMARY KEY,
    thread_id    INTEGER       NOT NULL,
    url          VARCHAR (255) NOT NULL,
    dns          VARCHAR (255) NOT NULL,
    content      TEXT          NOT NULL,
    visited      DATETIME      NOT NULL,
    last_visit   DATETIME      NOT NULL,
    [indexed]    INTEGER       NOT NULL,
    last_indexed DATETIME
);


-- Index: crawled_url
DROP INDEX IF EXISTS crawled_url;

CREATE UNIQUE INDEX crawled_url ON crawled (
    "url"
);


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
