export default class Config {

    static typeReading = {
        "float": {len: 4, method: "readFloatBE"},
        "Uint16": {len: 2, method: "readUint16BE"},
    }

    static loadAllConfigs() {
        const mainConfig = JSON.parse(fs.readFileSync('backend/src/utils/flightConfig/flightConfig.json', 'utf8'));

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

    static columns = {
        "time": ['DOUBLE DEFAULT NULL', 0],
        "flightMode": ['INTEGER DEFAULT NULL', 0],
        "statIgniter1": ['DOUBLE DEFAULT NULL', 0],
        "statIgniter2": ['DOUBLE DEFAULT NULL', 0],
        "statIgniter3": ['DOUBLE DEFAULT NULL', 0],
        "statIgniter4": ['DOUBLE DEFAULT NULL', 0],
        "statAccelerometer": ['DOUBLE DEFAULT NULL', 0],
        "statBarometer": ['DOUBLE DEFAULT NULL', 0],
        "statGPS": ['DOUBLE DEFAULT NULL', 0],
        "statSD": ['DOUBLE DEFAULT NULL', 0],
        "temperature": ['DOUBLE DEFAULT NULL', 0],
        "altitude": ['DOUBLE DEFAULT NULL', 0],
        "altitude_ft": ['DOUBLE DEFAULT NULL', 0],
        "speed": ['DOUBLE DEFAULT NULL', 0],
        "acceleration": ['DOUBLE DEFAULT NULL', 0],
        "gps_fix": ['DOUBLE DEFAULT NULL', 0],
        "latitude": ['DDOUBLE DEFAULT NULL', 0],
        "longitude": ['DOUBLE DEFAULT NULL', 0],
        "pitch": ['DOUBLE DEFAULT NULL', 0],
        "yaw": ['DOUBLE DEFAULT NULL', 0],
        "roll": ['DOUBLE DEFAULT NULL', 0],
        "batt1_mV": ['DOUBLE DEFAULT NULL', 0],
        "batt2_mV": ['DOUBLE DEFAULT NULL', 0],
        "batt3_mV": ['DOUBLE DEFAULT NULL', 0]
    }


}