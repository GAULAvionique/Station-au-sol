import MyData from "../src/data.mjs";
import DataGenerator from "./utils/dataGenerator.js";
import assert from 'node:assert/strict';
import {once} from 'node:events';
import {test, describe, beforeEach} from "node:test";

describe("Data class tests", () => {
    const dataGenerator = new DataGenerator()
    let handler = new MyData();

    test('Handle data line with flightMode 0 valid length', {timeout: 200}, async () => {
        const inputBuffer = dataGenerator.flight_mode_0_generator();
        const emitted = once(handler, 'data');

        handler.handleDataLine(inputBuffer, true);

        const [dataDict] = await emitted;

        assert.equal(dataDict.altitude, DataGenerator.ALTITUDE)
        assert.equal(dataDict.temperature, DataGenerator.TEMPERATURE)
        assert.equal(dataDict.pitch, DataGenerator.PITCH)
        assert.equal(dataDict.roll, DataGenerator.ROLL)
    });

    test('Handle data line with flightMode 0 too short', async () => {
        let inputBuffer = dataGenerator.flight_mode_0_generator();
        inputBuffer = inputBuffer.subarray(0, inputBuffer.length - 4)
        let emitted = false;
        handler.on('data', () => emitted = true);

        handler.handleDataLine(inputBuffer, true);

        assert.equal(emitted, false)
    });

    test('Handle data line with flightMode 0 too long', async () => {
        let inputBuffer = dataGenerator.flight_mode_0_generator();
        inputBuffer = Buffer.concat([inputBuffer, Buffer.alloc(1)])
        let emitted = false;
        handler.on('data', () => emitted = true);

        handler.handleDataLine(inputBuffer, true);

        assert.equal(emitted, false)
    });

    test('Standarize data with correctly formed data should correctly standarize', {timeout: 200}, async () => {
        const inputBuffer = dataGenerator.flight_mode_0_generator();
        const emitted = once(handler, 'data');

        handler.handleDataLine(inputBuffer, true);

        const [dataDict] = await emitted;

        const standarizedData = handler.standarizeData(dataDict)

        assert.equal(standarizedData.altitude, Number(Number(DataGenerator.ALTITUDE).toFixed(2)))
        assert.equal(standarizedData.temperature, DataGenerator.TEMPERATURE)
        assert.equal(standarizedData.acceleration, null)
    });

    test('Standarize data with empty dict still standarize but everything is null', {timeout: 200}, async () => {
        const dataDict = {}

        const standarizedData = handler.standarizeData(dataDict)

        assert.equal(standarizedData.altitude, null)
        assert.equal(standarizedData.temperature, null)
        assert.equal(standarizedData.acceleration, null)
    });
})