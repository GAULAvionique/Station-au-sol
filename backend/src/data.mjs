import EventEmitter from "node:events";
import MyStorage from "./storage.mjs";
import {Buffer} from "node:buffer";
import myLogger from "./logger.mjs";
import Config from "./utils/config";

const logger = myLogger.getCustomLogger("Data");

export default class MyData extends EventEmitter {
    stringDataBuffer = "";
    dataBuffer = Buffer.alloc(0);
    startDataTime = Date.now();
    lastDataTime = Date.now();
    config = Config.loadAllConfigs();

    constructor(encoding = "utf-8", lineStart = "$", lineEnding = "\n", dataInterval = 100) {
        super();

        this.bd = new MyStorage(null);

        this.encoding = encoding;
        this.lineStart = lineStart;
        this.lineEnding = lineEnding;
        this.dataInterval = dataInterval;

        this.spdLastTime = Date.now(); // For speed calculation
        this.spdLastAltitude; // For speed calculation
    }

    //-------------------------------------------------------------------------------

    handleRawData(data) {
        this.dataBuffer = Buffer.concat([this.dataBuffer, data]);

        if (this.dataBuffer.length > 10000) {
            this.dataBuffer = Buffer.alloc(0);
        }

        const start = this.dataBuffer.indexOf(this.lineStart);
        const end = this.dataBuffer.indexOf(this.lineEnding, start + 1);

        if (start !== -1 && end !== -1) {
            const line = this.dataBuffer.subarray(start, end + 1);
            this.dataBuffer = this.dataBuffer.subarray(end + 1);
            this.handleDataLine(line);
        }
    }

    //-------------------------------------------------------------------------------

    // Extract values from a packet of data
    handleDataLine(line) {
        // Skip data if under threshold
        if (Date.now() - this.lastDataTime < this.dataInterval) {
            return;
        } else {
            this.lastDataTime = Date.now();
        }

        const headerByte = line[this.config.header.index]
        const offset = this.config.header.mode_field.offset

        const flightMode = headerByte >> offset;

        if (!(flightMode.toString() in this.config.modes)) {
            logger.warn(`Flight mode is unknown. Received : ${flightMode}`);
            return;
        }

        let dataDict = {};

        dataDict["flightMode"] = flightMode

        const mode_data = this.config.modes[flightMode.toString()];

        if (line.length !== mode_data.totalLength) {
            return;
        }

        const flags = mode_data.flag_fields.fields

        for (const flagField of flags) {
            dataDict[flagField.key] = (headerByte >> flagField.offset) & 1;
        }
        const mode_informations = mode_data.dataFields
        let current_offset = Math.ceil((mode_data.flag_fields.size_bits + this.config.header.mode_field.size_bits) / 8) + this.config.header.index;

        for (const dataField of mode_informations) {
            if (dataField.key !== "NULL") {
                const type = Config.typeReading[dataField.type]
                dataDict[dataField.key] = line.subarray(current_offset, current_offset + type.len)[type.method]();
            }
            current_offset += dataField.len;
        }

        dataDict = this.standarizeData(dataDict);

        this.validateData(dataDict);

        this.bd.writeFormattedData(dataDict);
        this.emit("data", this.bd.getLastInput());
    }

    //-------------------------------------------------------------------------------

    // Fill predefined fields with data
    standarizeData(data) {
        let stdData = {};

        // Time of data in seconds
        stdData.time = numberPrecision((Date.now() - this.startDataTime) / 1000, 3);

        // Flight mode (0: PREFLIGHT, 1: INFLIGHT, 2: POSTFLIGHT)
        stdData.flightMode = data.flightMode !== undefined ? data.flightMode : null;
        // Igniter status (0: ERROR, 1: CONTINUITY)
        stdData.statIgniter1 = data.statIgniter1 !== undefined ? data.statIgniter1 : null;
        stdData.statIgniter2 = data.statIgniter2 !== undefined ? data.statIgniter2 : null;
        stdData.statIgniter3 = data.statIgniter3 !== undefined ? data.statIgniter3 : null;
        stdData.statIgniter4 = data.statIgniter4 !== undefined ? data.statIgniter4 : null;
        // Accelerometer status (0: ERROR, 1: OK)
        stdData.statAccelerometer = data.statAccelerometer !== undefined ? data.statAccelerometer : null;
        // Barometer status (0: ERROR, 1: OK)
        stdData.statBarometer = data.statBarometer !== undefined ? data.statBarometer : null;
        // GPS status (0: ERROR, 1: OK)
        stdData.statGPS = data.statGPS !== undefined ? data.statGPS : null;
        // SD card status (0: ERROR, 1: OK)
        stdData.statSD = data.statSD !== undefined ? data.statSD : null;

        // Temperature of barometer in Celsius
        stdData.temperature = data.temperature !== undefined ? numberPrecision(data.temperature, 2) : null;
        // Altitude from barometer in meters
        stdData.altitude = data.altitude !== undefined ? numberPrecision(data.altitude, 2) : null;
        stdData.altitude_ft = data.altitude !== undefined ? numberPrecision(data.altitude * 3.28084, 2) : null;
        // Vertical speed in m/s
        // stdData.speed = data.speed !== undefined ? numberPrecision(data.speed, 2) : null;
        stdData.speed = numberPrecision(
            (data.altitude - this.spdLastAltitude) / ((Date.now() - this.spdLastTime) / 1000),
            2
        ); // Avg speed
        this.spdLastAltitude = stdData.altitude;
        this.spdLastTime = Date.now();
        // Highest acceleration in m/s
        stdData.acceleration = Math.max(data.accelerationX, data.accelerationY, data.accelerationZ);
        stdData.acceleration = stdData.acceleration !== NaN ? numberPrecision(stdData.acceleration, 2) : null;
        // GPS Fix (0: NO FIX, 1: FIX)
        stdData.gps_fix = data.gps_fix !== undefined ? data.gps_fix : null;
        // Latitude from GPS in degrees
        stdData.latitude = data.latitude !== undefined ? numberPrecision(data.latitude, 8) : null;
        // Longitude from GPS in degrees
        stdData.longitude = data.longitude !== undefined ? numberPrecision(data.longitude, 8) : null;
        // Pitch of the rocket in degrees
        stdData.pitch = data.pitch !== undefined ? numberPrecision(data.pitch, 2) : null;
        // Yaw of the rocket in degrees
        stdData.yaw = data.yaw !== undefined ? numberPrecision(data.yaw, 2) : null;
        // Roll of the rocket in degrees
        stdData.roll = data.roll !== undefined ? numberPrecision(data.roll, 2) : null;
        // Battery 1 voltage in mV
        stdData.batt1_mV = data.lipo1_mV !== undefined ? numberPrecision(data.lipo1_mV, 0) : null;
        // Battery 2 voltage in mV
        stdData.batt2_mV = data.lipo2_mV !== undefined ? numberPrecision(data.lipo2_mV, 0) : null;
        // Battery 3 voltage in mV
        stdData.batt3_mV = data.lipo3_mV !== undefined ? numberPrecision(data.lipo3_mV, 0) : null;

        // console.log(stdData);

        return stdData;
    }

    //-------------------------------------------------------------------------------

    validateData(data) {
        // TODO
        return;
    }

    //-------------------------------------------------------------------------------

    // Extract a line of data
    // data: Buffer
    handleRawMockData(data) {
        // Add data to buffer
        this.stringDataBuffer += data.toString("utf-8");

        if (this.stringDataBuffer.includes("\n")) {
            // Keep text before line ending
            const line = this.stringDataBuffer.split("\n")[0];
            // Remove text before line ending from buffer to avoid processing it twice
            this.stringDataBuffer = this.stringDataBuffer.split("\n")[1];
            // Handle the line of data
            this.handleMockDataLine(line);
        }
    }

    //-------------------------------------------------------------------------------

    handleMockDataLine(line) {
        // Skip data if under threshold
        if (Date.now() - this.lastDataTime < this.dataInterval) {
            return;
        } else {
            this.lastDataTime = Date.now();
        }

        const dataList = line.trim().split(",");

        const dataDict = {
            // "time": dataList[0],
            time: (Date.now() - this.startDataTime) / 1000,
            altitude: dataList[1],
            pitch: dataList[2],
            roll: dataList[3],
            yaw: dataList[4],
            lat: dataList[5],
            lon: dataList[6],
            speed: dataList[7],
            acceleration: dataList[8],
            temperature: dataList[9],
            vibrations: dataList[10],
            landing_force: dataList[11],
            batt_check: dataList[12],
            igniter_check: dataList[13],
            statGPS: dataList[14],
        };
        this.bd.writeFormattedData(dataDict);
        this.emit("data", dataDict);
    }
}

    //-------------------------------------------------------------------------------

function numberPrecision(value, precision) {
    return Number(Number(value).toFixed(precision));
}
