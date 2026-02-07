document.addEventListener('DOMContentLoaded', () => {
    const tabCountInput = document.getElementById('tabCount');
    const startBtn = document.getElementById('startBtn');
    const statusDiv = document.getElementById('status');

    function generateRandomString(length) {
        const chars = 'abcdefghijklmnopqrstuvwxyz0123456789';
        let result = '';
        for (let i = 0; i < length; i++) {
            result += chars.charAt(Math.floor(Math.random() * chars.length));
        }
        return result;
    }

    function generateRandomEmails(count) {
        const emails = [];
        const domain = 'gmail.com';
        for (let i = 0; i < count; i++) {
            // Random prefix: 8-12 characters
            const prefix = generateRandomString(8 + Math.floor(Math.random() * 5));
            // Random suffix: 3-5 digits
            const suffix = Math.floor(100 + Math.random() * 9000);
            emails.push(`${prefix}${suffix}@${domain}`);
        }
        return emails;
    }

    startBtn.addEventListener('click', () => {
        const count = parseInt(tabCountInput.value, 10);

        if (isNaN(count) || count < 1) {
            showStatus('Please enter a valid number of tabs.', 'error');
            return;
        }

        if (count > 10) {
            showStatus('Maximum 10 parallel tabs allowed for stability.', 'error');
            return;
        }

        const emails = generateRandomEmails(count);

        showStatus(`Generating ${count} profiles...`, 'info');

        // Store emails and reset state
        chrome.storage.local.set({
            emails,
            tabEmailMap: {},
            isRunning: true
        }, () => {
            // Trigger background automation
            chrome.runtime.sendMessage({
                action: 'startParallelAutomation',
                emails: emails
            }, (response) => {
                showStatus(`Launched ${count} tabs. Check browser windows!`, 'success');
            });
        });
    });

    function showStatus(msg, type) {
        statusDiv.textContent = msg;
        statusDiv.className = type;
        statusDiv.style.display = 'block';
    }
});
