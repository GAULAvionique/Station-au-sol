/**
 * @class Server
 * @classdesc Manages the backend architecture by assigning actions to signals emitted by various components.
 * Coordinates communication between the serial interface, data handler, storage system, and client connections.
 */

import MyWebServer from "./src/webserver.mjs";
import MyStorage from "./src/storage.mjs";
import MySocket from "./src/socket.mjs";
import MySerial from "./src/serial.mjs";
import MyData from "./src/data.mjs";

import myLogger from "./src/logger.mjs";
const logger = myLogger.getCustomLogger();

const DEV_MODE = process.argv.includes("--dev");
const MOCK_MODE = process.argv.includes("--mock");

class App {
    constructor() {
        this.webServer = new MyWebServer();
        this.storage = new MyStorage();
        this.socket = new MySocket({
            HTTPServer: this.webServer.getHTTPServer(),
            // Allow connections to the socket from port 5173 if dev mode enabled
            corsEnabled: DEV_MODE,
        });
        this.serial = new MySerial({
            path: "COM3", // Windows
            // 'path': "/dev/ttyUSB0", // Raspberry Pi
            mockPort: MOCK_MODE, // Create a testing serial port is mock mode is enabled
        });
        this.mainLogger = myLogger;
        this.data = new MyData();

        this.eventListeners();
    }

    /**
     * Sets up various event listeners for handling signals emitted by different components of the backend architecture.
     *
     * Events handled:
     *
     * - **Raw Data (`rawData`):**
     *   Triggered when the serial port receives raw data. The raw data is stored in a file and processed either in
     *   mock mode or normal mode.
     *   - **Emitted by:** `serial`
     *   - **Payload:** `data` (string)
     *
     * - **Serial Events (`serialEvent`):**
     *   Triggered for communication events like connection open, close, or errors during interaction with the rocket.
     *   - **Emitted by:** `serial`
     *   - **Payload:** `event` (object)
     *
     * - **Formatted Data (`data`):**
     *   Triggered when the data handler completes data formatting. The formatted data is stored in a CSV file and sent to clients.
     *   - **Emitted by:** `data`
     *   - **Payload:** `data` (object)
     *
     * - **Data Events (`dataEvent`):**
     *   Triggered for errors or information during data formatting.
     *   - **Emitted by:** `data`
     *   - **Payload:** `event` (object)
     *
     * - **Client Requests Available Serial Paths (`getAvailablePaths`):**
     *   Triggered when a client requests the available serial port paths.
     *   - **Emitted by:** `socket`
     *   - **Callback Payload:** `{ availablePaths: string[], currentPath: string }`
     *
     * - **Client Sends New Settings (`newSettings`):**
     *   Triggered when a client sends new serial port settings.
     *   - **Emitted by:** `socket`
     *   - **Payload:** `settings` (object)
     */
    eventListeners() {
        // Raw data from the serial port
        // data: string
        this.serial.on("rawData", (data) => {
            // Add raw data to a file
            this.storage.writeRawData(data);
            // Handle data
            if (MOCK_MODE) {
                this.data.handleRawMockData(data);
            } else {
                this.data.handleRawData(data);
            }
        });

        // Formatted data from the data handler
        // data: dictionary
        this.data.on("data", (data) => {
            // Send data to clients
            this.socket.sendData(data);
        });

        // Log events from the logger
        this.mainLogger.on("log", (log) => {
            // Send logs to clients
            this.socket.send("log", log);
        });

        // Client requests available serial paths
        this.socket.on("getAvailablePaths", (callback) => {
            this.serial.getAvailablePaths().then((paths) => {
                // Send available serial paths to the client
                callback({
                    availablePaths: paths,
                    currentPath: this.serial.path,
                });
            });
        });

        // Client sends new settings
        this.socket.on("newSettings", (settings) => {
            // Update serial port settings
            this.serial.updateSettings(settings);
        });
    }
}

if (DEV_MODE) {
    logger.info("Developpment server (cors enabled)");
}

const app = new App();
