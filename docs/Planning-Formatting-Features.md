---
layout: docs
title: Planning> Formatting Features
---

Sagefy uses a restricted set of Markdown features. We also add strikethrough, code fences, iframes, and tables.

_No_ inline HTML. Auto escape inline characters.

**Paragraphs** have at least one blank line between them (GFM).

**Emphasis**: one set of `_` for italic, `**` double bullets for bold.

**Strikethrough** using `~~` double tilde characters (GFM).

**Monospace** using the tick \` character.

**Horizonal rule**: Use `---` surrounded by blank lines.

Only three **heading** levels. In some cases, the `h1` tag is already used, so these headings will be all be down 1 level.

  # Heading 1
  ## Heading 2
  ### Heading 3

**Unordered lists** use `-`, **ordered lists** use `1.`. Hanging indent or wrap are both allowed. Supports nesting.

**Links** use the Markdown reference style of `[name][ref]`, and then below `[ref]: http://example.com`.

**Images** similarly use `![name][ref]` then `[ref]: http://example.com/image.png`.

**Footnotes**: Use `[^ref]` inline, and at the bottom use `[^ref]: Some text.`.

**Embedded iframes** use `i[name][ref]` then `[ref]: http://youtube.com/Ij32rjS`.

**Preformatted block (code fence)**: Always use three ticks (GFM).

**Blockquote** with `>`. Can be nested.

**Tables**: Use `|` to split columns, and `-` to split header row.

Later on...
- Syntax highlighting?
- Emoji supported, use `:emoji:` format?
- Inline TeX ?
- Super and sub script? Small text? Quotes? Date times?
- Smart quotes, ellipse, dashes...?
- Image titles & descriptions?
