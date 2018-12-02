namespace libMPSSEWrapper
{
  /// <summary>
  /// https://datasheets.maximintegrated.com/en/ds/MAX30205.pdf
  /// https://www.mikroe.com/fever-click
  /// </summary>
  public class I2C_Maxim30205 : I2C_EEprom
  {

    // https://www.mikroe.com/fever-click
    // 0x48>>1 == 0x90
    public const byte ADDRESS = 0x48;

    private const byte REG_TEMP = 0x00;
    private const byte REG_CONFIG = 0x01;
    private const byte REG_T_HYST = 0x02;
    private const byte REG_T_OS = 0x03;

    private const byte REG_CONFIG_ONESHOT = 0x80;
    private const byte REG_CONFIG_TIMEOUT = 0x40;
    private const byte REG_CONFIG_DATAFORMAT = 0x20;
    private const byte REG_CONFIG_FAULTQUEUE = 0x18;
    private const byte REG_CONFIG_OSPOLARITY = 0x04;
    private const byte REG_CONFIG_COMPARATOR = 0x02;
    private const byte REG_CONFIG_SHUTDOWN = 0x01;

    private const int TEMP_64C = 0x4000;

    /// <summary>
    /// 
    /// </summary>
    /// <param name="channel">0: A, 1: B</param>
    /// <param name="clockrate">100000</param>
    public I2C_Maxim30205(LibMpsseI2C i2c, byte address) : base(i2c, address)
    {
    }

    public double ReadTemperatureOneShot()
    {
      WriteEEprom(REG_CONFIG, REG_CONFIG_ONESHOT | REG_CONFIG_SHUTDOWN);

      uint sizeToTransfer = 2;
      byte[] dataRead = new byte[sizeToTransfer];
      ReadEEprom(REG_TEMP, dataRead);

      uint temp = (uint)((dataRead[0] << 8) | dataRead[1]);
      double fTemp = temp * 64.0 / 0x4000;
      return fTemp;
    }
  }
}
