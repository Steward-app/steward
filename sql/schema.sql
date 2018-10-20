BEGIN TRANSACTION;
CREATE TABLE "users" (
	`id`	INTEGER NOT NULL,
	`name`	TEXT NOT NULL,
	`token`	TEXT NOT NULL,
	PRIMARY KEY(id)
);
CREATE TABLE `snoozes` (
	`id`	INTEGER NOT NULL,
	`name`	TEXT NOT NULL,
	`length`	TEXT NOT NULL,
	PRIMARY KEY(id)
);
CREATE TABLE "shares" (
	`id`	INTEGER NOT NULL,
	`group_id`	INTEGER NOT NULL,
	`user_id`	INTEGER NOT NULL,
	PRIMARY KEY(id),
	FOREIGN KEY(`group_id`) REFERENCES groups ( id ),
	FOREIGN KEY(`user_id`) REFERENCES users ( id )
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
CREATE TABLE "groups" (
	`id`	INTEGER NOT NULL,
	`name`	TEXT NOT NULL,
	`description`	TEXT,
	`calendar_id`	TEXT NOT NULL,
	`owner_id`	INTEGER NOT NULL,
	PRIMARY KEY(id),
	FOREIGN KEY(`owner_id`) REFERENCES users ( id )
);
CREATE TABLE "assets" (
	`id`	INTEGER NOT NULL,
	`name`	text NOT NULL,
	`description`	text,
	`group_id`	integer NOT NULL,
	PRIMARY KEY(id),
	FOREIGN KEY(`group_id`) REFERENCES groups ( id )
);
COMMIT;
