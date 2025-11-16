export default class DataGenerator {
    START_BYTE = 0x24; // '$'
    END_BYTE = 0x0A;  // '\n'
    static TEMPERATURE = 125.5
    static ALTITUDE = 25.01
    static ROLL = 11.1
    static PITCH = 4.23
    static LIPO1_MV = 12
    static LIPO2_MV = 34
    static LIPO3_MV = 56
    static AN_MV = 78

    flight_mode_0_generator() {
        const line = Buffer.alloc(34);

        line.writeUInt8(this.START_BYTE, 0);
        line.writeUInt8(0b00111111, 1);
        line.writeFloatBE(DataGenerator.TEMPERATURE, 2);
        line.writeFloatBE(DataGenerator.ALTITUDE, 6);
        line.writeFloatBE(DataGenerator.ROLL, 10);
        line.writeFloatBE(DataGenerator.PITCH, 14);
        line.writeUInt16BE(DataGenerator.LIPO1_MV, 18);
        line.writeUInt16BE(DataGenerator.LIPO2_MV, 20);
        line.writeUInt16BE(DataGenerator.LIPO3_MV, 22);
        line.writeUInt16BE(DataGenerator.AN_MV, 24);
        line.writeUInt8(this.END_BYTE, 33);
        return line;
    }
}