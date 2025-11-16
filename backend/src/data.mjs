import EventEmitter from "node:events";
import MyStorage from "./storage.mjs";
import {Buffer} from "node:buffer";
import myLogger from "./logger.mjs";
import Config from "./utils/config.js";

const logger = myLogger.getCustomLogger("Data");

export default class MyData extends EventEmitter {
    stringDataBuffer = "";
    dataBuffer = Buffer.alloc(0);
    startDataTime = Date.now();
    lastDataTime = Date.now();
    config = Config.loadAllConfigs();

    constructor({
                    encoding = "utf-8",
                    lineStart = "$",
                    lineEnding = "\n",
                    dataInterval = 100,
                    storage = new MyStorage(null)
                }={}) {
        super();

        this.bd = storage;

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

    handleDataLine(line, ignore_time = false) {
        if (!ignore_time && (Date.now() - this.lastDataTime < this.dataInterval)) {
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
            const type = Config.typeReading[dataField.type]
            if (dataField.key !== "NULL") {
                dataDict[dataField.key] = line.subarray(current_offset, current_offset + type.len)[type.method]();
            }
            current_offset += type.len;
        }

        dataDict = this.standarizeData(dataDict);

        this.bd.writeFormattedData(dataDict);
        this.emit("data", this.bd.getLastInput());
    }

    //-------------------------------------------------------------------------------

    standarizeData(data) {
        let stdData = {};

        for (const [key, value] of Object.entries(Config.standarizedData)) {
            let raw;
            if (Array.isArray(value.inputKey)) {
                raw = value.inputKey.map(k => data[k]);
            } else if (value.inputKey) {
                raw = data[value.inputKey];
            } else {
                raw = null;
            }
            let finalval = raw;
            if (value.transform) {
                try {
                    finalval = value.transform(this, raw);
                } catch (_) {
                    finalval = null;
                }
            }
            stdData[key] = finalval !== undefined ? finalval : null;
            stdData[key] = !isNaN(finalval) ? finalval : null;
        }

        this.spdLastAltitude = stdData.altitude;
        this.spdLastTime = Date.now();
        return stdData;
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
