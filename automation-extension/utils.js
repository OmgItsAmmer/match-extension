window.Utils = {
    getRandomName: () => {
        const names = ['James', 'Emma', 'Liam', 'Olivia', 'Noah', 'Ava', 'William', 'Sophia', 'Lucas', 'Mia', 'Benjamin', 'Isabella', 'Michael', 'Charlotte', 'Mason', 'Amelia', 'Ethan', 'Harper', 'Daniel', 'Evelyn'];
        return names[Math.floor(Math.random() * names.length)];
    },

    getRandomPassword: () => {
        const upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
        const lower = "abcdefghijklmnopqrstuvwxyz";
        const numbers = "0123456789";
        const all = upper + lower + numbers;

        let pwd = "";
        // Ensure all requirements are met
        pwd += upper[Math.floor(Math.random() * upper.length)];
        pwd += lower[Math.floor(Math.random() * lower.length)];
        pwd += numbers[Math.floor(Math.random() * numbers.length)];

        for (let i = 0; i < 7; i++) {
            pwd += all[Math.floor(Math.random() * all.length)];
        }
        return pwd;
    },

    getRandomBirthday: () => {
        // Return MM/DD/YYYY ensuring age > 18
        const year = 1970 + Math.floor(Math.random() * 30); // 1970 - 2000
        const month = String(1 + Math.floor(Math.random() * 12)).padStart(2, '0');
        const day = String(1 + Math.floor(Math.random() * 28)).padStart(2, '0');
        return `${month}/${day}/${year}`;
    },

    getRandomZip: () => {
        const zips = ['75201', '90210', '10001', '60601', '33101', '77001', '85001', '19101', '92101', '75231'];
        return zips[Math.floor(Math.random() * zips.length)];
    },

    delay: (ms) => new Promise(res => setTimeout(res, ms))
};

if (typeof module !== 'undefined') {
    module.exports = Utils;
}
