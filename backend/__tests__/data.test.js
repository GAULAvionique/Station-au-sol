import MyData from "../src/data.mjs";
import DataGenerator from "./utils/dataGenerator.js";
import test from 'node:test';
import assert from 'node:assert/strict';
import {once} from 'node:events';

const dataGenerator = new DataGenerator()

test('Handle data line with flightMode 0 valid length', {timeout: 200}, async () => {
    const handler = new MyData();
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
    const handler = new MyData();
    let inputBuffer = dataGenerator.flight_mode_0_generator();
    inputBuffer = inputBuffer.subarray(0, inputBuffer.length - 4)
    let emitted = false;
    handler.on('data', () => emitted = true);

    handler.handleDataLine(inputBuffer, true);

    assert.equal(emitted, false)
});

test('Handle data line with flightMode 0 too long', async () => {
    const handler = new MyData();
    let inputBuffer = dataGenerator.flight_mode_0_generator();
    inputBuffer = Buffer.concat([inputBuffer, Buffer.alloc(1)])
    let emitted = false;
    handler.on('data', () => emitted = true);

    handler.handleDataLine(inputBuffer, true);

    assert.equal(emitted, false)
});