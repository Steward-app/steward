BEGIN TRANSACTION;
CREATE TABLE `snoozes` (
	`id`	INTEGER NOT NULL,
	`name`	TEXT NOT NULL,
	`length`	TEXT NOT NULL,
	PRIMARY KEY(id)
);
CREATE TABLE "schedules" (
	`id`	INTEGER NOT NULL,
	`name`	text NOT NULL,
	`description`	text,
	`recurrence`	text NOT NULL,
	PRIMARY KEY(id)
);
CREATE TABLE "maintenances" (
	`id`	INTEGER NOT NULL,
	`name`	TEXT NOT NULL,
	`description`	TEXT,
	`schedule`	INTEGER NOT NULL,
	`snooze`	TEXT NOT NULL,
	`asset`	INTEGER NOT NULL,
	PRIMARY KEY(id),
	FOREIGN KEY(`schedule`) REFERENCES schedules ( id ),
	FOREIGN KEY(`snooze`) REFERENCES snoozes ( id ),
	FOREIGN KEY(`asset`) REFERENCES assets ( id )
);
CREATE TABLE "calendars" (
	`id`	INTEGER NOT NULL,
	`name`	text NOT NULL,
	`api_id`	text NOT NULL,
	`description`	text,
	PRIMARY KEY(id)
);
CREATE TABLE "assets" (
	`id`	INTEGER NOT NULL,
	`name`	text NOT NULL,
	`description`	text,
	`calendar_id`	integer NOT NULL,
	PRIMARY KEY(id),
	FOREIGN KEY(`calendar_id`) REFERENCES calendars ( id )
);
COMMIT;
