(async function () {
    console.log("Match Profile Automator Content Script Active on: " + window.location.href);


    // Helper to simulate human typing/interaction
    const simulateInteraction = async (element, value) => {
        try {
            element.focus();
            element.click();

            // React Native/Synthetic Event override
            const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
            if (nativeInputValueSetter) {
                nativeInputValueSetter.call(element, value);
            } else {
                element.value = value;
            }

            const events = ["keydown", "keypress", "input", "keyup", "change"];
            for (const eventType of events) {
                element.dispatchEvent(new Event(eventType, { bubbles: true }));
            }

            // Specific for tracking
            const tracker = element._valueTracker;
            if (tracker) tracker.setValue(element.value);

            element.blur();
        } catch (err) {
            console.error("Interaction Error:", err);
        }
    };

    // Helper to upload file from extension assets
    const setFileInput = async (input, filePath) => {
        try {
            const url = chrome.runtime.getURL(filePath);
            const response = await fetch(url);
            const blob = await response.blob();
            const file = new File([blob], filePath.split('/').pop(), { type: blob.type });
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);
            input.files = dataTransfer.files;
            input.dispatchEvent(new Event('change', { bubbles: true }));
            input.dispatchEvent(new Event('input', { bubbles: true }));
        } catch (e) {
            console.error("File Upload Error:", e);
        }
    };

    const simulateSelect = async (element, value) => {
        element.focus();
        element.value = value;
        element.dispatchEvent(new Event('change', { bubbles: true }));
        element.dispatchEvent(new Event('input', { bubbles: true }));
        element.blur();
    };

    // Robust element finder
    const findElement = (selectors) => {
        for (const selector of selectors) {
            const el = document.querySelector(selector);
            if (el) return el;
        }
        return null;
    };

    // Button clicker
    const findAndClickButton = (texts) => {
        // 1. Precise match first with common button elements
        const buttons = Array.from(document.querySelectorAll('button, input[type="submit"], [role="button"], a, [role="link"], div[role="button"], label, [data-testid*="button"], [data-testid*="submit"]'));

        for (const text of texts) {
            const btn = buttons.find(b => (b.innerText || b.textContent || b.value || "").trim().toLowerCase().includes(text.toLowerCase()));
            if (btn) {
                console.log(`Clicking button: ${text}`);
                btn.click();
                return true;
            }
        }

        // 2. SVG Icon match (Special cases)
        // Right Arrow / Next
        if (texts.includes('Right Arrow')) {
            const arrowSvg = document.querySelector('svg[id*="arrow_right"], svg[id*="next"], svg[id*="chevron"], [data-testid*="arrow-right"], [aria-label*="Next"]');
            if (arrowSvg) {
                const btn = arrowSvg.closest('button') || arrowSvg.closest('[role="button"]') || arrowSvg.parentElement;
                if (btn) {
                    console.log("Clicking Right Arrow/Next SVG button...");
                    btn.click();
                    return true;
                }
            }

            // Fallback for right arrow: look for any button with "next" in aria-label
            const nextBtn = document.querySelector('button[aria-label*="Next" i], [role="button"][aria-label*="Next" i]');
            if (nextBtn) {
                console.log("Clicking button with aria-label Next...");
                nextBtn.click();
                return true;
            }
        }

        // Like Button
        if (texts.includes('Like')) {
            const likeSvg = document.querySelector('svg[id*="match-like"], [data-testid*="like"], [aria-label*="Like"]');
            if (likeSvg) {
                const btn = likeSvg.closest('button') || likeSvg.closest('[role="button"]') || likeSvg.parentElement;
                if (btn) {
                    console.log("Clicking Like SVG button...");
                    btn.click();
                    return true;
                }
            }
        }

        // 3. Last resort: search ALL divs if they are likely buttons
        for (const text of texts) {
            const allDivs = Array.from(document.querySelectorAll('div, span'));
            const clickableDiv = allDivs.find(d =>
                (d.innerText || d.textContent || "").trim().toLowerCase() === text.toLowerCase() &&
                (d.onclick || d.className.includes('button') || d.className.includes('btn'))
            );
            if (clickableDiv) {
                console.log(`Clicking clickable div/span: ${text}`);
                clickableDiv.click();
                return true;
            }
        }

        return false;
    };

    // Main Loop
    const runAutomationLoop = async (email) => {
        const url = window.location.href;
        console.log(`[Loop] URL: ${url}`);

        // Define selectors up front
        const genderSelect = findElement(['select#ggs_select', '[name="genderSeek"]', '[data-testid="gender-seek"]']);
        const bdayInput = findElement(['input[data-testid="birthday"]', 'input[name="birthdate"]', '.birth-date-step-input']);
        const nameInput = findElement(['input[data-testid="firstName"]', 'input[name="firstName"]', 'input[name="firstname"]', '[placeholder="First name"]']);
        const emailInput = findElement(['input[name="email"]', 'input[type="email"]']);
        const pwdInput = findElement(['input[name="password"]', 'input[type="password"]']);
        const startBtn = findElement(['button[data-testid="advance"]', 'button.submit']);
        const viewSingles = Array.from(document.querySelectorAll('a, button')).find(el => el.textContent?.toLowerCase().includes('view singles'));

        const isRegistration = !!(genderSelect || bdayInput || nameInput || emailInput || pwdInput || startBtn);
        console.log(`[Loop] isRegistration: ${isRegistration}`);

        if (genderSelect && !genderSelect.dataset.done) {
            console.log("Handling Landing Form...");

            // Gender
            await simulateSelect(genderSelect, (1 + Math.floor(Math.random() * 4)).toString());
            genderSelect.dataset.done = "true";

            // Age (if present)
            const minAge = document.querySelector('select#desktop_landing_ages_lw');
            const maxAge = document.querySelector('select#desktop_landing_ages_hg');
            if (minAge) await simulateSelect(minAge, "25");
            if (maxAge) await simulateSelect(maxAge, "45");

            // Zip Code
            const zipInput = findElement(['input#postalcode_input', 'input[name="postalCode"]', '[data-testid="postal-code"]']);
            if (zipInput && !zipInput.dataset.filled) {
                console.log("Typing Zip Code...");
                const zip = window.Utils.getRandomZip();
                zipInput.focus();
                zipInput.value = "";

                // Type character by character to trigger typeahead
                for (const char of zip) {
                    zipInput.value += char;
                    zipInput.dispatchEvent(new Event('input', { bubbles: true }));
                    zipInput.dispatchEvent(new KeyboardEvent('keydown', { key: char, bubbles: true }));
                    await window.Utils.delay(150);
                }

                // Wait for typeahead suggestion to appear
                await window.Utils.delay(1000);

                // Try to find a suggestion in a dropdown and click it
                const suggestion = document.querySelector('[role="listbox"] [role="option"], .suggestion-item, .typeahead-result, li[id*="suggestion"]');
                if (suggestion) {
                    console.log("Found zip suggestion, clicking...");
                    suggestion.click();
                } else {
                    // Fallback: press ArrowDown and Enter
                    console.log("No suggestion found, trying ArrowDown + Enter fallback...");
                    zipInput.dispatchEvent(new KeyboardEvent('keydown', { key: 'ArrowDown', bubbles: true }));
                    await window.Utils.delay(200);
                    zipInput.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', bubbles: true }));
                }

                zipInput.dataset.filled = "true";
                await window.Utils.delay(500);
            }

            // Submit
            await window.Utils.delay(1000); // Wait for potential validation
            if (startBtn) {
                console.log("Clicking startBtn...");
                startBtn.click();
            } else {
                console.log("Looking for View Singles button after form fill...");
                findAndClickButton(['View Singles', 'Get Started', 'Continue', 'JOIN']);
            }
        }
        else if (viewSingles && !document.querySelector('input')) {
            // Simple landing page
            console.log("Clicking View Singles Link...");
            viewSingles.click();
        }

        // 2. Birthday Step
        if (bdayInput && !bdayInput.dataset.filled) {
            console.log("Filling Birthday...");
            // Sometimes it requires MM/DD/YYYY, sometimes specific format. 
            // We'll try typing slowly.
            bdayInput.focus();
            const bday = window.Utils.getRandomBirthday().replace(/\//g, ''); // Try raw numbers first usually better for masks

            // React 16+ hack for inputs with masks
            for (let i = 0; i < bday.length; i++) {
                const char = bday[i];
                bdayInput.value = bdayInput.value + char;
                bdayInput.dispatchEvent(new InputEvent('input', { data: char, bubbles: true }));
                await window.Utils.delay(100);
            }
            bdayInput.dataset.filled = "true";

            await window.Utils.delay(1000);
            findAndClickButton(["That's it", "Confirm", "Next", "Continue"]);
            // Enter key fallback
            bdayInput.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', keyCode: 13, bubbles: true }));
        }

        // 3. Name Step
        if (nameInput && !nameInput.dataset.filled) {
            console.log("Filling Name...");
            await simulateInteraction(nameInput, window.Utils.getRandomName());
            nameInput.dataset.filled = "true";
            await window.Utils.delay(800);
            findAndClickButton(["That's me", "Next", "Continue"]);
        }

        // 4. Email Step
        if (emailInput && !emailInput.dataset.filled) {
            console.log("Filling Email...");
            await simulateInteraction(emailInput, email);
            emailInput.dataset.filled = "true";
            await window.Utils.delay(800);
            findAndClickButton(["That's the one", "Next", "Continue"]);
        }

        // 5. Password Step
        if (pwdInput && !pwdInput.dataset.filled) {
            console.log("Filling Password...");
            await simulateInteraction(pwdInput, window.Utils.getRandomPassword());
            pwdInput.dataset.filled = "true";
            await window.Utils.delay(800);
            findAndClickButton(["That's it", "Create Account", "Sign Up"]);
        }

        // 5.5 Intro "tell us about yourself" screen
        if (!isRegistration) {
            const introHeader = document.querySelector('[data-testid="desktop-intro-header"]');
            if (introHeader) {
                console.log("Found Intro Screen, clicking 'Click here to get started'...");
                if (findAndClickButton(["Click here to get started"])) {
                    await window.Utils.delay(1000);
                }
            }
        }



        // 6. Photo Upload Step
        const fileInput = document.querySelector('input[type="file"], #photo-to-upload');
        const finalizeBtn = document.querySelector('.css-44m5wj');

        // SPECIAL CASE: photo_upload_additional_photos
        // On this specific page, we ONLY want to click "Continue". Do NOT attempt any photo uploads.
        if (window.location.href.includes('photo_upload_additional_photos')) {
            console.log("On Additional Photos page. Seeking 'Continue' button...");

            // Search all buttons and interactive elements for "Continue" text
            const allBtns = Array.from(document.querySelectorAll('button, [role="button"], span'));
            const continueBtn = allBtns.find(b => {
                const text = (b.innerText || b.textContent || "").toLowerCase().trim();
                return text === 'continue' || (text.includes('continue') && b.classList.contains('css-6nte24'));
            });

            if (continueBtn && continueBtn.offsetParent !== null) {
                console.log("Found 'Continue' on Additional Photos page, clicking...");
                continueBtn.click();
                await window.Utils.delay(2000);
                return setTimeout(() => runAutomationLoop(email), 1000);
            } else {
                console.log("Continue button not found or not ready on Additional Photos page, waiting...");
                // Bail out early MUST return here so it doesn't fall through to general upload logic
                return setTimeout(() => runAutomationLoop(email), 2000);
            }
        }

        // If the finalized upload button is visible (Screens 9, 10, 11), click it!
        if (finalizeBtn && finalizeBtn.offsetParent !== null) {
            console.log("Found specialized photo button (.css-44m5wj), clicking...");
            finalizeBtn.click();
            await window.Utils.delay(2000);
            return setTimeout(() => runAutomationLoop(email), 1000);
        }

        if (fileInput && !fileInput.dataset.filled) {
            console.log("Handling Photo Upload...");

            // Check if it's the primary photo upload screen from the HTML provided (Page 9)
            const photoLabel = document.querySelector('label[for="photo-to-upload"], #photo-to-upload-label');
            if (photoLabel && photoLabel.offsetParent !== null) {
                console.log("Found Photo Upload Label, clicking label to trigger...");
                photoLabel.click();
                await window.Utils.delay(500);
            }

            await setFileInput(fileInput, 'assets/img.png');
            fileInput.dataset.filled = "true";

            // Wait for upload/preview/modal to appear
            await window.Utils.delay(3000);

            // Handle Zoom/Scale if present
            const slider = document.querySelector('input[type="range"], .slider, [role="slider"], .rcl-slider-handle');
            if (slider) {
                console.log("Adjusting Zoom...");
                // In some cases slider is not a simple input range
                if (slider.tagName === 'INPUT') {
                    slider.value = slider.max;
                }
                slider.dispatchEvent(new Event('input', { bubbles: true }));
                slider.dispatchEvent(new Event('change', { bubbles: true }));
                await window.Utils.delay(1000);
            }

            // Re-check for finalize button after setting file
            const finalizeBtnAfter = document.querySelector('.css-44m5wj');
            if (finalizeBtnAfter) {
                finalizeBtnAfter.click();
                await window.Utils.delay(2000);
            }
        }

        // 7. Post-Login Flow (Screens 1-9) & Questions
        // Logic for specific questions (Kids, Education, Smoke)
        // We look for headers or labels
        const pageText = document.body.innerText.toLowerCase();

        // Kids
        if (pageText.includes('kids') || pageText.includes('children')) {
            const kidsSelect = document.querySelector('select');
            if (kidsSelect && !kidsSelect.dataset.done) {
                console.log("Answering Kids question (select)...");
                await simulateSelect(kidsSelect, (1 + Math.floor(Math.random() * 2)).toString());
                kidsSelect.dataset.done = "true";
            } else if (!isRegistration) {
                // If no select, maybe buttons? findAndClickButton will handle it in the generic section or here
                if (findAndClickButton(["Someday", "Want them", "rather not say"])) {
                    await window.Utils.delay(1000);
                }
            }
        }

        // Education
        if (pageText.includes('education') || pageText.includes('degree')) {
            const eduSelect = document.querySelector('select');
            if (eduSelect && !eduSelect.dataset.done) {
                console.log("Answering Education question (select)...");
                await simulateSelect(eduSelect, (2 + Math.floor(Math.random() * 2)).toString());
                eduSelect.dataset.done = "true";
            } else if (!isRegistration) {
                if (findAndClickButton(["Bachelors", "rather not say"])) {
                    await window.Utils.delay(1000);
                }
            }
        }

        // Smoke
        if (pageText.includes('smoke')) {
            const smokeSelect = document.querySelector('select');
            if (smokeSelect && !smokeSelect.dataset.done) {
                console.log("Answering Smoke question (select)...");
                await simulateSelect(smokeSelect, "1");
                smokeSelect.dataset.done = "true";
            } else if (!isRegistration) {
                if (findAndClickButton(["No", "Non-smoker", "rather not say"])) {
                    await window.Utils.delay(1000);
                }
            }
        }


        if (!isRegistration) {
            console.log("Handling Post-Login Screens (Step 7)...");
            let actionTaken = false;

            try {
                // 7.1 Auto-Answer Questions (Radio/Buttons)
                const radioButtons = Array.from(document.querySelectorAll('button[role="radio"], [role="radio"] button, .radio-button, button.ZKm8POHBkPYSkSnv9F6n'));
                const unSelectedRadio = radioButtons.filter(b => b.getAttribute('aria-checked') === 'true').length === 0;

                if (!actionTaken && radioButtons.length > 0 && unSelectedRadio) {
                    console.log("Found Radio buttons, selecting one...");
                    // Try to find a group container
                    const parent = radioButtons[0].closest('[role="list"], .rGpBpe5FwChyweCjkHNQ') || radioButtons[0].parentElement;
                    const groupOptions = Array.from(parent.querySelectorAll('button[role="radio"], button.ZKm8POHBkPYSkSnv9F6n'));
                    if (groupOptions.length > 0) {
                        const randomOption = groupOptions[Math.floor(Math.random() * groupOptions.length)];
                        console.log(`Clicking option: ${randomOption.textContent}`);
                        randomOption.click();
                        actionTaken = true;
                        await window.Utils.delay(1000);
                    }
                }

                // 7.2 Auto-Answer Questions (Checkboxes)
                const checkboxes = Array.from(document.querySelectorAll('input[type="checkbox"]'));
                const anyChecked = checkboxes.some(c => c.checked);

                if (!actionTaken && checkboxes.length > 0 && !anyChecked) {
                    console.log("Found checkboxes, selecting some...");
                    // Select 1-2 random options
                    const numToSelect = Math.min(checkboxes.length, 1 + Math.floor(Math.random() * 2));
                    const shuffled = checkboxes.sort(() => 0.5 - Math.random());
                    for (let i = 0; i < numToSelect; i++) {
                        shuffled[i].click();
                    }
                    actionTaken = true;
                    await window.Utils.delay(1000);
                }

                // 7.3 Click Primary Action (Continue / Next / Skip)
                if (!actionTaken) {
                    // Try Skip first if we are stuck or as a fallback
                    // But usually we want to Continue if we selected something
                    const continueBtn = findElement(['button:not([disabled])', 'button[role="button"]:not([disabled])', '.css-u0k5dv:not([disabled])', '.css-44m5wj:not([disabled])']);
                    const btnText = continueBtn ? continueBtn.textContent?.toLowerCase() : '';

                    if (continueBtn && (btnText.includes('continue') || btnText.includes('next') || btnText.includes('save') || btnText.includes('it\'s me') || btnText.includes('upload'))) {
                        console.log("Clicking primary action button...");
                        continueBtn.click();
                        actionTaken = true;
                    } else if (findAndClickButton(['Skip', 'Skip for now', 'No thanks', "rather not say", "Maybe later"])) {
                        console.log("Stuck or no primary button, clicking Skip...");
                        actionTaken = true;
                    }
                }

                // 7.4 Arrow Fallback
                if (!actionTaken && findAndClickButton(['Right Arrow', 'Next Page', 'Arrow'])) {
                    actionTaken = true;
                }

                if (actionTaken) {
                    await window.Utils.delay(1500);
                }
            } catch (innerErr) {
                console.error("Error in Post-Login logic:", innerErr);
            }
        }

        // Loop
        setTimeout(() => runAutomationLoop(email), 2000);
    };

    // Initialization
    const init = () => {
        chrome.storage.local.get(['tabEmailMap', 'isRunning'], (data) => {
            if (!data.isRunning) return;

            chrome.runtime.sendMessage({ action: 'getEmailForTab' }, (response) => {
                if (response && response.email) {
                    console.log(`[Automator] Started for ${response.email}`);
                    runAutomationLoop(response.email);
                } else {
                    console.log("[Automator] No email assigned, retrying in 2s...");
                    setTimeout(init, 2000);
                }
            });
        });
    };

    init();

})();
