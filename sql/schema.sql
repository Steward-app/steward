PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE calendars (id integer PRIMARY KEY, name text NOT NULL, calendar_id text NOT NULL, description text);
CREATE TABLE assets (id integer PRIMARY KEY, name text NOT NULL, description text, schedule_id integer, calendar_id integer, FOREIGN KEY (calendar_id) REFERENCES calendars (id), FOREIGN KEY (schedule_id) REFERENCES schedules (id));
CREATE TABLE schedules (id integer PRIMARY KEY, name text NOT NULL, description text, recurrence text NOT NULL);
COMMIT;
