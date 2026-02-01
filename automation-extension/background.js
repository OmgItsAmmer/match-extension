// Background script to manage multiple parallel registration flows

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'startParallelAutomation') {
        const { emails } = request;

        emails.forEach((email, index) => {
            // Delay opening tabs slightly to avoid overwhelming the browser/site
            setTimeout(() => {
                chrome.tabs.create({ url: 'https://match.com/' }, (tab) => {
                    chrome.storage.local.get(['tabEmailMap'], (data) => {
                        const currentMap = data.tabEmailMap || {};
                        currentMap[tab.id] = email;
                        chrome.storage.local.set({ tabEmailMap: currentMap, isRunning: true });
                    });
                });
            }, index * 3000);
        });

        sendResponse({ status: 'started' });
    } else if (request.action === 'getEmailForTab') {
        const tabId = sender.tab.id;
        chrome.storage.local.get(['tabEmailMap'], (data) => {
            const email = data.tabEmailMap ? data.tabEmailMap[tabId] : null;
            sendResponse({ email: email });
        });
        return true; // Keep channel open
    }
});

// Clean up mapping when tabs are closed
chrome.tabs.onRemoved.addListener((tabId) => {
    chrome.storage.local.get(['tabEmailMap'], (data) => {
        if (data.tabEmailMap && data.tabEmailMap[tabId]) {
            const newMap = { ...data.tabEmailMap };
            delete newMap[tabId];
            chrome.storage.local.set({ tabEmailMap: newMap });
        }
    });
});
