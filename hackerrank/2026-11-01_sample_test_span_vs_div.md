# HackerRank Sample Test: `<span>` vs `<div>` (Subjective)

**2026-11-01.** This was the practice test on the HackerRank test platform, done before the micro1 Eval Hackathon. It is not graded. Its purpose was to try the file-upload question and the subjective answer editor.

**Note:** Claude drafted this answer at my request. It's an HTML concept I'd studied before, but not in this much depth.

## Question
What is the difference between `<span>` and `<div>`?

## Answer (submitted)
Both `<div>` and `<span>` are generic containers with no meaning of their own. They are used to group content so that it can be styled with CSS or selected with JavaScript. The difference is how they sit on the page:

- `<div>` is a **block-level** element. It starts on a new line and stretches to the full width available. It is used for larger sections such as a header, a card or a column.
- `<span>` is an **inline** element. It stays inside the line of text and is only as wide as its content. It is used for a word or phrase within a sentence, for example to colour one word.

A `<div>` can contain `<span>` elements, but a `<span>` should not contain a `<div>`.

```html
<div>This whole line is one block.</div>
<p>Only <span style="color:red">this word</span> turns red.</p>
```

## Reference note
| | `<div>` | `<span>` |
|---|---|---|
| Display | block | inline |
| New line? | yes | no |
| Width | full width | only as wide as its content |
| Use | page sections | words inside text |

CSS can change this: `display: inline` / `display: block` makes either tag behave like the other. The defaults are what the question is about.
