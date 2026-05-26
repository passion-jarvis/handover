# Higgsfield UGC Workflow

## Tools
- Image generation: Higgsfield NanoBanana 2
- Video generation: Higgsfield Cinema Studio

## URLs
- Image: higgsfield.ai/image/nano_banana_2
- Video: higgsfield.ai (Cinema Studio)

## Default Settings
- Aspect ratio: 9:16
- Image count: 8
- Quality: 2K unlimited ON
- Extra free gens: OFF

## Per-Prompt Workflow
For EVERY prompt in a batch, follow these steps exactly. No skipping.

1. Run the JS clear snippet (see below) to reset the prompt bar
2. Take a screenshot and visually confirm the bar is empty
3. If not empty, clear again and re-verify before continuing
4. Type the prompt with `slowly: true`
5. Click Generate
6. Run the JS clear immediately after clicking Generate
7. Wait 7 seconds
8. Move to the next prompt

## JS Clear Snippet
Run this before and after every prompt:

```js
const editor = document.querySelector('[id="hf:tour-image-prompt"] [contenteditable]')
  || document.querySelector('[contenteditable="true"]');

editor.innerHTML = '<p><br></p>';
editor.dispatchEvent(new Event('input', { bubbles: true }));
```

## Session Workflow
1. Navigate to higgsfield.ai/image/nano_banana_2
2. Confirm settings match defaults above before generating anything
3. Run batch using per-prompt workflow above
4. Save all outputs to /images/YYYY-MM-DD/ named by prompt number (char-01.png, char-02.png, etc.)
5. Update SESSION-RESUME.md after every prompt completes

## Rules
- Always clear the prompt bar via JS before typing. Never skip this step.
- Always screenshot after clearing to confirm it's empty.
- Never skip settings confirmation at the start.
- Go straight to generating, no prompt previews.
- Save all outputs to /images/YYYY-MM-DD/
- Update SESSION-RESUME.md progress table after each generation.
