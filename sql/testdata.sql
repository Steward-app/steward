PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
INSERT INTO "calendars" VALUES(1,'Kaino','primary',NULL);
INSERT INTO "assets" VALUES(1,'Vesikukka',NULL,1,1);
INSERT INTO "schedules" VALUES(1,'Weekly',NULL,'RRULE:FREQ=WEEKLY');
COMMIT;
