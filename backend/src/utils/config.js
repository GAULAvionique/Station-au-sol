import fs from "fs";
import field from "./standarizedDataConfig.js"

export default class Config {

    static standarizedData = field

    static typeReading = {
        "float": {len: 4, method: "readFloatBE"},
        "Uint16": {len: 2, method: "readUint16BE"},
    }

    static loadAllConfigs() {
        const mainConfig = JSON.parse(fs.readFileSync('./src/utils/flightConfig/flightConfig.json', 'utf8'));

        const finalConfig = {
            header: mainConfig.header_byte_config,
            modes: {}
        };

        for (const modeId in mainConfig.mode_details) {
            const filePath = mainConfig.mode_details[modeId];
            const modeData = JSON.parse(fs.readFileSync(filePath, 'utf8'));

            finalConfig.modes[modeId] = modeData;
        }
        return finalConfig;
    }

}