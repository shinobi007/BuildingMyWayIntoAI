# Human-in-the-loop AI review provenance

AI support is used transparently from the beginning, including code suggestions, text and technical investigations. The existing portable Stage 9 prompt lives in `Day1/FinalVersion/docs/stage9_initial_ai_prompt.md`; the exact Stage 8 archived evidence bundle is preserved locally in the existing runs.

`framework/ledgers/ai_reviews.csv` records review stage, source bundle, instructions, output/summary, whether a human checked original requirements, limitations and decision. An AI comparison is an assessment, not evidence that an employer accepted an application or that a résumé requirement is met.

Possible later enhancements: structured prompts and model outputs, human-corrected JSON, source-span evidence, disagreement logs, evaluated extraction accuracy, repeatable model API, multi-model comparison. **None require a paid AI API before first applications.**
