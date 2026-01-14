// Set up a daily alarm for check-in
chrome.runtime.onInstalled.addListener(() => {
    // Determine time until 5 PM
    const now = new Date();
    let nextCheckIn = new Date();
    nextCheckIn.setHours(17, 0, 0, 0); // 5:00 PM

    if (now > nextCheckIn) {
        nextCheckIn.setDate(nextCheckIn.getDate() + 1);
    }

    const delayInMinutes = (nextCheckIn.getTime() - now.getTime()) / 60000;

    chrome.alarms.create("dailyCheckIn", {
        delayInMinutes: delayInMinutes,
        periodInMinutes: 1440 // 24 hours
    });
});

chrome.alarms.onAlarm.addListener((alarm) => {
    if (alarm.name === "dailyCheckIn") {
        chrome.notifications.create({
            type: "basic",
            iconUrl: "icon.png", // We'll need an icon eventually
            title: "SAM Check-in",
            message: "Hey, how was your day?",
            priority: 2
        });
    }
});

chrome.notifications.onClicked.addListener(() => {
    // Open the popup or a tab when notification is clicked
    // Note: Popups cannot be opened programmatically, so we might open a tab or just expect user to click extension icon.
    // implementing opening a panel or window is complex in MV3, simply acknowledging for now.
    console.log("Notification clicked");
});
