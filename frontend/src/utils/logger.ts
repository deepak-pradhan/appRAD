const log = {
    bold: (message: string) => {
        console.log(`\x1b[1m${message}\x1b[0m`);
    },
    hooks: (message: string) => {
        console.log(`[Route] ${message}`);
    }
};

export default log;