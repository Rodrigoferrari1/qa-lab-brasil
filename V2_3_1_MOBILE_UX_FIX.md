# QA Lab Brasil 2.3.1 - Mobile UX Fix

Local test build.

- Mobile topic navigation moves the viewport directly to loaded content.
- Home resets all expanded navigation groups and subgroups.
- Home reset clears persistent navigation state before re-rendering the navigation tree.
- Desktop behavior otherwise remains unchanged.

## Mobile topic navigation hotfix
- Collapses expanded navigation before route change on mobile.
- After the topic is rendered, scrolls explicitly to the topic header using its document Y position.
- Uses two animation frames plus a corrective pass for mobile browser layout shifts.

- v5: mobile tree navigation links now route through qaMobileOpenTopic; after render the viewport is explicitly moved to the selected topic content.
