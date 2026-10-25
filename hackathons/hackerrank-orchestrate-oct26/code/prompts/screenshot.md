You are reading a screenshot of an internal admin tool at an online shop. It is evidence in a data-deletion
audit. Extract the facts it shows; do not judge whether a deletion is complete.

List every record that is identified on screen by an internal resource id. Resource ids look like
`account_5762`, `search_428`, `support_1034`, `analytics_7438`, `data_flow_1121`, `backup_9287`,
`export_1260`, `audit_record_003`, `tombstone_17`, `marketing_001`, `legal_hold_12`.

For each record give:
- `resource_id`: exactly as printed;
- `emails`, `user_refs` (like `user_13`) and `phones` shown **for that record** (its row, its detail panel),
  not identifiers that belong to other rows;
- `state`: the record's visible state, one of
  `present` (record shown and existing), `absent` (screen says not found or deleted),
  `redacted` (record kept but personal fields removed or masked), `anonymized` (no personal identifiers),
  `flow_enabled`, `flow_disabled` (connectors/integrations), `restore_allowed`, `restore_blocked`
  (backups), or `unknown`;
- `shows_personal_data`: true if a name, email or phone of a person is displayed for the record.

Also give `screen` (a short name for the tool) and `captured_at` if a date or time is printed on screen
(ISO-8601 when possible, otherwise as printed, otherwise empty).

Only report what is visible. If a value is unreadable, leave it out.
