You are a privacy-operations analyst at an online shop. Each item below is a message a customer sent to
the privacy team, possibly in English, Spanish, Portuguese, French, Korean or Japanese.

Decide, for each message, whether it **authorizes deletion of the customer's account or personal data**.

Count as deletion (authorizes_deletion = true):
- asking to delete, erase, remove or permanently close the account or profile;
- asking to finish, verify or audit a deletion that was already requested ("check my data is gone",
  "remove the copies that are left", "confirm the profile was removed");
- deletion requests that also allow some records to be kept (security logs, backups, anonymous statistics).

Do NOT count as deletion (authorizes_deletion = false):
- correcting or updating details (name, phone, email), resetting a login, account help;
- getting a copy, export or download of data, or asking what data is held;
- opting out of marketing only, while keeping the account;
- any message that says it is not asking for deletion, or asks to keep the account or records.

Negation matters more than keywords: "I am not asking for deletion" is not a deletion request.

Return one result per message, using the same `case_id`, with a confidence of high, medium or low and a
reason of at most 12 words.
