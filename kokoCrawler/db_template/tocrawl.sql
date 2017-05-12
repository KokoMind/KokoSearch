--
-- File generated with SQLiteStudio v3.1.1 on Mon Mar 20 01:37:32 2017
--
-- Text encoding used: UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: tocrawl
DROP TABLE IF EXISTS tocrawl;

CREATE TABLE tocrawl (
    id    INTEGER       NOT NULL
                        PRIMARY KEY,
    url   TEXT          NOT NULL,
    dns   VARCHAR (255) NOT NULL,
    value REAL          NOT NULL
);


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
