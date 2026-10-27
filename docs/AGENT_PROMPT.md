# Scheduled run prompt

The agent runs on a schedule (07:52, 17:47 and 22:52 Dubai time on weekdays). Each run starts a Claude Code session with this prompt. Private ids are replaced with placeholders.

```text
Scheduled morning job sourcing run (weekday, Dubai).

1. Read docs/SEARCH_RULES.md first and follow it exactly (employer criteria per market, role fit
   incl. analyst/product roles, link rules, and the "Tracker = Google Sheet" section). Read the
   Google Sheet fresh, apply manual edits (delete "Link expired" rows, mirror statuses locally),
   and read deleted.txt.
2. Source new, live roles posted in the last ~7 days across UAE (priority), India, Germany,
   Netherlands, Ireland, Luxembourg and other good EU locations. Use background agents; give
   them the rules file path.
3. Pick the best <=15, run `python3 tools/tracker.py add <file>`, then append the same rows to
   the Google Sheet as SEARCH_RULES describes.
4. Reply in the project thread with one short message: the count, the ID range and the top 3
   (company, role, resume to send).
5. If the Gmail connector is available, scan the inbox since the last run for application emails
   (confirmations, recruiter replies, assessments, interviews, rejections). Update Status,
   Date applied and Notes in the Google Sheet. Gmail is read only; never send, delete or label.
6. Fridays: read the Dashboard tab; report applications, response rate by market and by resume,
   and one concrete change for next week. Re-check every "To apply" link and delete dead rows.
7. If roles were added, post a one-line alert in the main project chat.
```
