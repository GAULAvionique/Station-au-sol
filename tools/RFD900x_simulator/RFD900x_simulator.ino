/**
 * Code pour simuler les données reçues de la fusée avec un Arduino.
 *
 * La fusée envoie les valeurs des capteurs par le RFD900x vers la station au
 * sol, qui reçoit ces données avec le RFD900x connecté en serial. Il peut donc
 * être simulé avec un arduino.
 * 
 * (i): position dans le paquet complet
 * [j]: position dans le rocket_data
 *
 */

void setup()
{
  Serial.begin(9600);
}

void loop()
{
  // Statut des différents composants
  // Header(8bit): Mode(2bit)Igniter1(1bit)Igniter2(1bit)Accelerometer(1bit)Barometer(1bit)Gps(1bit)SD(1bit)
  
  // PREFLIGHT
  //
  // $(char8bit) (0)
  // Header(8bit) (1)
  // Altitude(m)(float32bit) (2) [0]
  // Temp(°C)(float32bit) (6) [4]
  // AngleRoll(°)(float32bit) (10) [8]
  // AnglePitch(°)(float32bit) (14) [12]
  // NULL(32bit) (18) [16]
  // V_Lipo1(mV)(uint16bit) (22) [20]
  // V_Lipo2(mV)(uint16bit) (24) [22]
  // V_Lipo3(mV)(uint16bit) (26) [24]
  // 5V_AN(mV)(uint16bit) (28) [26]
  // *(char8bit) (30)
  // CRC(16bit) (31)
  // <LF>(char8bit) (33)

  // PREFLIGHT
  uint8_t preflightdata[] = {
      '$',                                            // $
      0b00101111,                                     // Preflight mode, igniter2 bad, everything else good
      0b01000100, 0b10001101, 0b01001010, 0b01001110, // Altitude = 1130.322m
      0b01000010, 0b00000000, 0b10101000, 0b00111110, // Temp = 32.1643°C
      0b11000010, 0b11100011, 0b00011110, 0b11001000, // AngleRoll = -113.56012°
      0b01000010, 0b00000011, 0b11001000, 0b01010110, // AnglePitch = 32.94564°
      0b00000000, 0b00000000, 0b00000000, 0b00000000, // NULL
      0b00010011, 0b01010110,                         // V_Lipo1 = 4950mV
      0b00010011, 0b00010110,                         // V_Lipo2 = 4886mV
      0b00010011, 0b10000111,                         // V_Lipo3 = 4999mV
      0b00010011, 0b10001000,                         // 5V_AN = 5000mV
      '*',                                            // *
      0x00, 0x00,                                     // CRC (NULL)
      0x0A                                            // <LF>
  };
  for (int i = 0; i < sizeof(preflightdata); i++)
  {
    Serial.write(preflightdata[i]);
  }
  delay(1000);

  // INFLIGHT
  //
  // $(char8bit) (0)
  // Header(8bit) (1)
  // Altitude(m)(float32bit) (2) [0]
  // Temp(°C)(float32bit) (6) [4]
  // Time_raw(HHMMSS)(int32bits) (10) [8] // NOT USED
  // Latitude(float32bit) (14) [12]
  // Longitude(float32bit) (18) [16]
  // GyroX(°)(float32bit) (22) [20]
  // GyroY(°)(float32bit) (26) [24]
  // GyroZ(°)(float32bit) (30) [28]
  // AccX(m/s²)(float32bit) (34) [32]
  // AccY(m/s²)(float32bit) (38) [36]
  // AccZ(m/s²)(float32bit) (42) [40]
  // KalmanAngleRoll(°)(float32bit) (46) [44]
  // KalmanAnglePitch(°)(float32bit) (50) [48]
  // *(char8bit) (54)
  // CRC(16bit) (55)
  // <LF>(char8bit) (57)

  // FLIGHT
  uint8_t flightdata[] = {
      '$',                                              // $
      0b01111111,                                       // Inflight mode, all good
      0b01000100, 0b11010110, 0b00111010, 0b01010110,   // Altitude = 1713.823m
      0b01000010, 0b00111001, 0b11110111, 0b01010001,   // Temp = 32.1643°C
      0b00000000, 0b00000000, 0b00000000, 0b00000000,   // Time_raw
      0b01000010, 0b00111011, 0b00100000, 0b01101011,   // Latitude = 46.78166
      0b11000010, 0b10001110, 0b10001101, 0b10101101,   // Longitude = -71.27671
      0b01000000, 0b10010110, 0b00110110, 0b10011010,   // GyroX = 4.694165°
      0b11000000, 0b11100110, 0b00100010, 0b00011111,   // GyroY = -7.191665°
      0b00111111, 0b00010101, 0b10001000, 0b01101110,   // GyroZ = 0.584113°
      0b00111110, 0b00101001, 0b11001010, 0b00011001,   // AccX = 0.16581m/s²
      0b10111111, 0b01111010, 0b01100101, 0b01101011,   // AccY = -0.97811m/s²
      0b00111110, 0b10000000, 0b10010001, 0b10011111,   // AccZ = 0.251111m/s²
      0b11000011, 0b01110101, 0b10100101, 0b10100000,   // KalmanAngleRoll = -245.64698°
      0b01000010, 0b01100011, 0b11001001, 0b10101011,   // KalmanAnglePitch = 56.94694°
      '*',                                              // *
      0x00, 0x00,                                       // CRC (NULL)
      0x0A                                              // <LF>
  };
  for (int i = 0; i < sizeof(flightdata); i++)
  {
    Serial.write(flightdata[i]);
  }
  delay(1000);

  // POSTFLIGHT
  // $(char8bit) (0)
  // Header(8bit) (1)
  // Altitude(m)(float32bit) (2) [0]
  // Time_raw(HHMMSS)(int32bits) (6) [4] // NOT USED
  // Latitude(float32bit) (10) [8]
  // Longitude(float32bit) (14) [12]
  // V_Lipo1(mV)(uint16bit) (18) [16]
  // V_Lipo2(mV)(uint16bit) (20) [18]
  // V_Lipo3(mV)(uint16bit) (22) [20]
  // 5V_AN(mV)(uint16bit) (24) [22]
  // *(char8bit) (26)
  // CRC(16bit) (27)
  // <LF>(char8bit) (29)

  // POSTFLIGHT
  uint8_t postflightdata[] = {
      '$',                                              // $
      0b10111111,                                       // Postflight mode, all good
      0b01000100, 0b11010110, 0b00111010, 0b01010110,   // Altitude = 1713.823m
      0b00000000, 0b00000000, 0b00000000, 0b00000000,   // Time_raw
      0b01000010, 0b00111011, 0b00100000, 0b01111110,   // Latitude = 46.78173
      0b11000010, 0b10001110, 0b10010010, 0b01011011,   // Longitude = -71.28585
      0b00010000, 0b01111000,                           // V_Lipo1 = 4216mV
      0b00010001, 0b00000011,                           // V_Lipo2 = 4355mV
      0b00010000, 0b10110111,                           // V_Lipo3 = 4279mV
      0b00010001, 0b11111000,                           // 5V_AN = 4600mV
      '*',                                              // *
      0x00, 0x00,                                       // CRC (NULL)
      0x0A                                              // <LF>
  };
  for (int i = 0; i < sizeof(postflightdata); i++)
  {
    Serial.write(postflightdata[i]);
  }
  delay(1000);
}