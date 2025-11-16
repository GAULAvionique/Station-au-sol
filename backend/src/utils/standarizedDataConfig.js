const fields = {
    time: {
        sql: "DOUBLE DEFAULT NULL",
        inputKey: null,
        transform: (dataClass, _) => numberPrecision((Date.now() - dataClass.startDataTime) / 1000, 3)
    },

    flightMode: {
        sql: "INTEGER DEFAULT NULL",
        inputKey: "flightMode"
    },

    statIgniter1: {
        sql: "DOUBLE DEFAULT NULL",
        inputKey: "statIgniter1"
    },

    statIgniter2: {
        sql: "DOUBLE DEFAULT NULL",
        inputKey: "statIgniter2"
    },

    statIgniter3: {
        sql: "DOUBLE DEFAULT NULL",
        inputKey: "statIgniter3"
    },

    statIgniter4: {
        sql: "DOUBLE DEFAULT NULL",
        inputKey: "statIgniter4"
    },

    statAccelerometer: {
        sql: "DOUBLE DEFAULT NULL",
        inputKey: "statAccelerometer"
    },

    statBarometer: {
        sql: "DOUBLE DEFAULT NULL",
        inputKey: "statBarometer"
    },

    statGPS: {
        sql: "DOUBLE DEFAULT NULL",
        inputKey: "statGPS"
    },

    statSD: {
        sql: "DOUBLE DEFAULT NULL",
        inputKey: "statSD"
    },

    temperature: {
        sql: "DOUBLE DEFAULT NULL",
        inputKey: "temperature",
    },

    altitude: {
        sql: "DOUBLE DEFAULT NULL",
        inputKey: "altitude",
        transform: (_, v) => numberPrecision(v, 2)
    },

    altitude_ft: {
        sql: "DOUBLE DEFAULT NULL",
        inputKey: "altitude",
        transform: (_, v) => numberPrecision(v * 3.28084, 2)
    },

    acceleration: {
        sql: "DOUBLE DEFAULT NULL",
        inputKey: ["accelerationX", "accelerationY", "accelerationZ"],
        transform: (_, [x, y, z]) => numberPrecision(Math.max(x, y, z), 2)
    },

    speed: {
        sql: "DOUBLE DEFAULT NULL",
        inputKey: "altitude",
        transform: (dataClass, v) => numberPrecision(
            (v - dataClass.spdLastAltitude) / ((Date.now() - dataClass.spdLastTime) / 1000),
            2
        )
    },

    latitude: {
        sql: "DOUBLE DEFAULT NULL",
        inputKey: "latitude",
        transform: (_, v) => numberPrecision(v, 8)
    },
    longitude: {
        sql: "DOUBLE DEFAULT NULL",
        inputKey: "longitude",
        transform: (_, v) => numberPrecision(v, 8)
    },

    gps_fix:{
        sql: "DOUBLE DEFAULT NULL",
        inputKey: "gps_fix",
    },

    pitch:{
        sql: "DOUBLE DEFAULT NULL",
        inputKey: "pitch",
        transform: (_, v) => numberPrecision(v,2)
    },

    yaw:{
        sql: "DOUBLE DEFAULT NULL",
        inputKey: "yaw",
        transform: (_, v) => numberPrecision(v,2)
    },

    roll:{
        sql: "DOUBLE DEFAULT NULL",
        inputKey: "roll",
        transform: (_, v) => numberPrecision(v,2)
    },

    batt1_mV: {
        sql: "DOUBLE DEFAULT NULL",
        inputKey: "lipo1_mV",
        transform: (_, v) => numberPrecision(v, 0)
    },
    batt2_mV: {
        sql: "DOUBLE DEFAULT NULL",
        inputKey: "lipo2_mV",
        transform: (_, v) => numberPrecision(v, 0)
    },
    batt3_mV: {
        sql: "DOUBLE DEFAULT NULL",
        inputKey: "lipo3_mV",
        transform: (_, v) => numberPrecision(v, 0)
    }
};


function numberPrecision(value, precision) {
    return Number(Number(value).toFixed(precision));
}

export default fields
