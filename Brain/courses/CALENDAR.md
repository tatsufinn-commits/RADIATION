# TERM CALENDAR — live LMS feed mirror
**Status: NOT YET GENERATED — the daily cron is unarmed.**

This file is machine-written by `scripts/ics_normalize.py --public` from the live
LMS feed. It does not exist yet because arming requires, in order:

1. rotate the feed URL exposed in commit `4a98e59` (history keeps it — rotation at source);
2. store the new URL as the Actions secret `RADIATION_ICS_URL`;
3. let the calendar cron run (or trigger it manually).

Until then the authoritative schedule is the neighbour file `SCHEDULE.md`
(the Commander's own transcription, published by amendment A1).
No URL belongs in this file — ever. Validator check 22 fails the tree if one appears.
