document.addEventListener('DOMContentLoaded', () => {
    const csvFileInput = document.getElementById('csvFile');
    const startBtn = document.getElementById('startBtn');
    const statusDiv = document.getElementById('status');
    const fileInfoDiv = document.getElementById('fileInfo');

    let emails = [];

    csvFileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = (event) => {
            const text = event.target.result;
            const rows = text.split('\n').map(row => row.trim()).filter(row => row !== '');

            if (rows.length === 0) {
                showStatus('CSV file is empty.', 'error');
                return;
            }

            const header = rows[0].toLowerCase();
            if (!header.includes('emailaddress')) {
                showStatus('CSV must contain a column named "emailaddress".', 'error');
                return;
            }

            const emailIndex = header.split(',').findIndex(h => h.includes('emailaddress'));

            emails = rows.slice(1).map(row => {
                const columns = row.split(',');
                return columns[emailIndex] ? columns[emailIndex].replace(/"/g, '').trim() : null;
            }).filter(email => email && email.includes('@'));

            if (emails.length === 0) {
                showStatus('No valid emails found in CSV.', 'error');
            } else {
                fileInfoDiv.textContent = `Found ${emails.length} emails.`;
                showStatus('Ready to start parallel automation!', 'success');
                startBtn.disabled = false;
                chrome.storage.local.set({ emails, tabEmailMap: {}, isRunning: false });
            }
        };
        reader.readAsText(file);
    });

    startBtn.addEventListener('click', () => {
        chrome.runtime.sendMessage({
            action: 'startParallelAutomation',
            emails: emails
        }, (response) => {
            showStatus(`Starting ${emails.length} tabs in parallel...`, 'info');
        });
    });

    function showStatus(msg, type) {
        statusDiv.textContent = msg;
        statusDiv.className = type;
    }
});
