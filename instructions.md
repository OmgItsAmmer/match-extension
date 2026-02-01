## Features
- **Parallel Automation**: Opens one tab for EVERY email in your CSV and fills them simultaneously.
- **Unique Assignment**: Automatically tracks and assigns a unique email from your CSV to each tab.
- **Smart Form Filling**: Robust handling for all steps (Login, Birthdate, Name, Email, Password).
- **Security Compliant**: Generates passwords meeting all security rules (Upper, Lower, Numbers, Length).

## CSV Format
Your CSV file must have at least one column named `emailaddress`.
Example:
```csv
emailaddress
user1@example.com
user2@example.com
```

## How to Install (Chrome/Edge)
1. Open Chrome and go to `chrome://extensions/`.
2. Enable **Developer mode** (toggle in the top right).
3. Click **Load unpacked**.
4. Select the `automation-extension` folder from this project directory.

## How to Run
1. Open the **Match Profile Automator** extension from your browser toolbar.
2. Upload your CSV file containing email addresses.
3. Click **START AUTOMATION**.
4. Navigate to the Match registration page (`https://www.match.com/registration/en-us`).
5. The extension will start filling out the fields automatically.
6. **Note**: Stay on the tab while it's working to ensure best performance.

## Testing Locally
If you are running the Match frontend locally (e.g., on `localhost:3000`), the extension is configured to work there as well. Just ensure the selectors match the components.

## Error Handling
- If a step is not detected, check if the Match UI has changed and update the selectors in `content.js`.
- Ensure your CSV is not empty and has the correct header.

---
*Created by Antigravity*
