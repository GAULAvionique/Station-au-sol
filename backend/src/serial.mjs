import EventEmitter from "node:events";
import { SerialPort } from "serialport";
import chalk from "chalk";
import { startSerialMock } from "./utils/serialmock.mjs";
import myLogger from "./logger.mjs";

const logger = myLogger.getCustomLogger("Serial");

export default class MySerial extends EventEmitter {
    serialConnected = false;
    serialPort;
    lastEventError;

    constructor({
        path: path,
        baudRate: baudRate = 9600,
        encoding: encoding = "utf-8",
        reconnectSerialTimeout: reconnectSerialTimeout = 1000,
        mockPort: mockPort = false,
    }) {
        super();

        // Serial port settings
        this.path = path;
        this.baudRate = baudRate;

        // Other settings
        this.encoding = encoding;
        this.mockPort = mockPort;
        this.reconnectSerialTimeout = reconnectSerialTimeout;

        // Set testing path if there is a mock port
        this.path = this.mockPort ? "testingPort" : this.path;

        this.startSerial();
    }

    startSerial() {
        if (this.serialConnected) {
            return;
        }

        if (this.path === "testingPort") {
            this.serialPort = startSerialMock();
        } else {
            this.serialPort = new SerialPort({ path: this.path, baudRate: this.baudRate });
        }

        this.setupEvents();
    }

    // Listen to serial port events
    setupEvents() {
        this.serialPort.on("data", (data) => {
            this.emit("rawData", data);
        });

        this.serialPort.on("open", () => {
            this.serialConnected = true;

            this.lastEventError = null;

            logger.info(`Opened on ${chalk.blue(this.path)} at ${chalk.blue(this.baudRate)}`);
        });

        this.serialPort.on("close", (event) => {
            this.serialConnected = false;

            logger.warn(
                `Closed (${chalk.blue(this.path)} at ${chalk.blue(this.baudRate)}) ${event ? chalk.italic(event) : ""}`
            );

            // Try to reconnect
            setTimeout(() => {
                this.startSerial();
            }, this.reconnectSerialTimeout);
        });

        this.serialPort.on("error", (error) => {
            this.serialConnected = false;

            if (error.toString() !== this.lastEventError) {
                logger.error(error, error.message);
            }

            this.lastEventError = error.toString();

            // Try to reconnect
            setTimeout(() => {
                this.startSerial();
            }, this.reconnectSerialTimeout);
        });
    }

    // Update the serial port settings
    updateSettings({ path: path = this.path, baudRate: baudRate = this.baudRate }) {
        this.path = path;
        this.baudRate = baudRate;

        logger.info(`New settings: ${chalk.blue(path)} at ${chalk.blue(baudRate)}`);
        this.serialPort.close();
        this.serialConnected = false;
        // It will reconnect automatically with events
    }

    // Get all the serial paths available
    async getAvailablePaths() {
        try {
            const ports = await SerialPort.list(); // BUG: NOT WORKING ON RASPBERRY PI
            const paths = ports.map((port) => port.path);
            if (this.mockPort) paths.push("testingPort");
            return paths;
        } catch (error) {
            logger.error(`Error getting serial ports: ${error}`);
            return [];
        }
    }
}
