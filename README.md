# Personal Efficiency Enhancing Skills

A collection of WorkBuddy Skills designed to enhance personal workflow efficiency.

## Skills

### Resume Tailor (`resume-tailor/`)

**One command to tailor your resume for any job description.**

Input a JD (link or text) -> automatic matching analysis -> interactive resume adjustment -> PDF generation + version audit.

#### Features

- **JD Keyword Extraction**: Automatically parses JD text to extract hard skills, soft skills, domain keywords, and experience requirements
- **Resume Matching**: Analyzes how well your master resume matches the target JD
- **Interactive Adjustment**: 6 decision points where you can guide the tailoring process:
  1. Experience selection (keep/demote)
  2. Wording upgrades (fact-check before escalating)
  3. Quantification gaps (add missing numbers)
  4. Content gaps (prompt you to recall relevant experience)
  5. Merge/split decisions
  6. Final confirmation before PDF generation
- **Version Audit**: Every tailored version is logged with a full diff against the master
- **PDF Output**: Markdown preview -> confirmation -> .docx -> PDF

#### Usage

For WorkBuddy users, install to `~/.workbuddy/skills/resume-tailor/`, then use:

```
Help me tailor my resume for this JD: [paste JD or URL]
```

#### Dependencies

- python-docx (for .docx manipulation)
- pandoc (for PDF generation)

## License

MIT
