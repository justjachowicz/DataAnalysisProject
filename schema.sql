DROP TABLE IF EXISTS life_quality;

CREATE TABLE life_quality (
    id integer primary key autoincrement,
    country text,
    year integer,
    life_quality real
);

DROP TABLE IF EXISTS schizophrenia;

CREATE TABLE schizophrenia (
  id integer primary key autoincrement,
  country text,
  year integer,
  schizophrenia_index real
);

DROP TABLE IF EXISTS bipolarDisorder;

CREATE TABLE bipolarDisorder (
  id integer primary key autoincrement,
  country text,
  year integer,
  bipolar_disorder_index real
);

DROP TABLE IF EXISTS eatingDisorder;

CREATE TABLE eatingDisorder (
  id integer primary key autoincrement,
  country text,
  year integer,
  eating_disorder_index real
);

DROP TABLE IF EXISTS depression;

CREATE TABLE depression (
  id integer primary key autoincrement,
  country text,
  year integer,
  depression_index real
);

