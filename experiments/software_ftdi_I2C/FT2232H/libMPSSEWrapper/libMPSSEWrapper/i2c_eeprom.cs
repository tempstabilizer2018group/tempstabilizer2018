namespace libMPSSEWrapper
{
  /// <summary>
  /// https://www.chd.at/blog/electronic/FTDI-in-CS
  /// http://www.ftdichip.com/Support/Documents/AppNotes/AN_177_User_Guide_For_LibMPSSE-I2C.pdf
  /// </summary>
  public class I2C_EEprom
  {
    protected LibMpsseI2C i2c;
    protected byte address;

    public I2C_EEprom(LibMpsseI2C i2c_, byte address_)
    {
      i2c = i2c_;
      address = address_;
    }

    public void WriteEEprom(byte register, byte value)
    {
      uint sizeTransfered = 0;
      byte[] dataWrite = new byte[] { register, value };
      i2c.I2Cwrite(address, (uint)dataWrite.Length, dataWrite, ref sizeTransfered, options: LibMpsseI2C.I2C_TRANSFER_OPTIONS_START_BIT | LibMpsseI2C.I2C_TRANSFER_OPTIONS_STOP_BIT | LibMpsseI2C.I2C_TRANSFER_OPTIONS_BREAK_ON_NACK | LibMpsseI2C.I2C_TRANSFER_OPTIONS_FAST_TRANSFER_BYTES);
      if (sizeTransfered != dataWrite.Length)
      {
        throw new LibMpsseException($"Wrote {sizeTransfered} bytes but expected {dataWrite.Length}!");
      }
    }

    public void ReadEEprom(byte register, byte[] dataRead)
    {
      uint sizeTransfered = 0;

      byte[] dataWrite = new byte[] { register };
      i2c.I2Cwrite(address, (uint)dataWrite.Length, dataWrite, ref sizeTransfered, options: LibMpsseI2C.I2C_TRANSFER_OPTIONS_START_BIT | LibMpsseI2C.I2C_TRANSFER_OPTIONS_BREAK_ON_NACK | LibMpsseI2C.I2C_TRANSFER_OPTIONS_FAST_TRANSFER_BYTES);
      if (sizeTransfered != dataWrite.Length)
      {
        throw new LibMpsseException($"Wrote {sizeTransfered} bytes but expected {dataWrite.Length}!");
      }

      i2c.I2Cread(address, (uint)dataRead.Length, dataRead, ref sizeTransfered, options: LibMpsseI2C.I2C_TRANSFER_OPTIONS_START_BIT | LibMpsseI2C.I2C_TRANSFER_OPTIONS_STOP_BIT /* | LibMpsseI2C.I2C_TRANSFER_OPTIONS_NACK_LAST_BYTE | LibMpsseI2C.I2C_TRANSFER_OPTIONS_FAST_TRANSFER_BYTES */);
      if (sizeTransfered != dataRead.Length)
      {
        throw new LibMpsseException($"Read {sizeTransfered} bytes but expected {dataRead.Length}!");
      }
    }
  }
  }
