# Hard cases

Posts where I paused. These are Claude's pre-labelling calls, so **read each one and decide for yourself**.
Row numbers are 0-based positions in `ask_hn_data/ask_hn_200_posts.json`, i.e. row N+2 in `labels.csv`
(row 1 is the header). The 20 `cold` posts are left out on purpose so they stay unaided.

| # | Post | Could be | Chosen | Why |
|---|---|---|---|---|
| 7 | "Where Are the PHP Hacks?" (asks whether big hacks followed the php2shell patch) | `analysis` / `discussion_question` | `discussion_question` | It leans on a real event, but the fact is background and the post asks for news and reports. |
| 38 | "How to organize teams to ship AI-written code?" | `help_request` / `discussion_question` | `help_request` | It asks "did your team change?" like a poll, but also says "it is not clear how to organize ourselves now". The poster needs an answer for their own team. |
| 44 | "Dark mode for HN please? (2026)" | `help_request` / `hot_take` | `help_request` | There is a lot of venting and a link to the 2020 thread, but the ask is a feature the poster wants. |
| 47 | "What happened to open weights models?" | `hot_take` / `analysis` | `hot_take` | It names Ornith-1.5 and Qwen3.5, but the main claim ("stalled", "scrambling for coin") has no support. The named model is an aside. |
| 54 | "How to deal with shipping AI-written code you don't understand?" (quotes a Meta engineer's post) | `help_request` / `analysis` | `help_request` | It quotes a source, but the poster is asking how to cope. Rule order puts `help_request` first. |
| 73 | "Why people do not want to believe weight loss is possible without GLPs?" | `hot_take` / `discussion_question` | `hot_take` | It is partly a Show HN complaint. It asserts "guaranteed" results and "17,000+ users" with nothing checkable. |
| 103 | "Who else got the Google Workspace Intelligence email?" | `analysis` / `hot_take` | `analysis` | It quotes the email's text and links no source. This is really a reaction post, which my taxonomy has no label for. |
| 119 / 120 / 122 | Three posts asking how people review AI-generated code | `help_request` / `discussion_question` | 119, 120 `discussion_question`; 122 `help_request` | 122 asks for a tool to use. 119 and 120 ask about workflows. This is the least stable call in the set. |

Patterns:
- **Promo posts** (2, 33, 73, 108, 157) fit none of my labels. I folded most into `discussion_question`.
- **Reaction posts** ("Did anyone know about this?", #60, #103) also have no home.
- **131 is an exact repeat of 130** apart from "please" in the title. Delete one before splitting.
