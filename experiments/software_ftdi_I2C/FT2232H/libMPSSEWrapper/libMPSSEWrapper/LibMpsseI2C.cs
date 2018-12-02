using System;
using System.Runtime.InteropServices;

namespace libMPSSEWrapper
{
  public class LibMpsseException : Exception
  {
    public LibMpsseException(uint status, string message) : base($"{message} (FTDI status {status})") { }
    public LibMpsseException(string message) : base(message) { }
    public LibMpsseException(string message, Exception innerException) : base(message, innerException) { }
  }

  public enum FtResult
  {
    Ok = 0,
    InvalidHandle,
    DeviceNotFound,
    DeviceNotOpened,
    IoError,
    InsufficientResources,
    InvalidParameter,
    InvalidBaudRate,
  }


  [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi)]
  public struct FtDeviceInfo
  {
    public int Flags;
    public int Type;
    public int ID;
    public int LocId;

    [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 16)]
    public string SerialNumber;
    [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 64)]

    public string Description;
    public IntPtr ftHandle;
  }

  [Flags]
  public enum FtConfigOptions
  {

    Mode0 = 0x00000000,
    Mode1 = 0x00000001,
    Mode2 = 0x00000002,
    Mode3 = 0x00000003,


    CsDbus3 = 0x00000000, /*000 00*/
    CsDbus4 = 0x00000004, /*001 00*/
    CsDbus5 = 0x00000008, /*010 00*/
    CsDbus6 = 0x0000000C, /*011 00*/
    CsDbus7 = 0x00000010, /*100 00*/

    CsActivelow = 0x00000020,
  }

  [StructLayout(LayoutKind.Sequential)]
  public struct FtChannelConfig
  {
    public int ClockRate;
    public byte LatencyTimer;
    public FtConfigOptions configOptions;
    public int Pin;
    public short reserved;
  }

  public class LibMpsseI2C
  {

    // http://www.ftdichip.com/Support/SoftwareExamples/MPSSE/LibMPSSE-I2C/LibMPSSE-I2C_source.zip
    // LibMPSSE-I2C_source.zip\LibMPSSE-I2C\LibMPSSE\TopLayer\I2C\inc\ftdi_i2c.h
    /*
    Options to I2C_DeviceWrite & I2C_DeviceRead
    Generate start condition before transmitting
    #define	I2C_TRANSFER_OPTIONS_START_BIT		0x00000001

    Generate stop condition before transmitting
    #define I2C_TRANSFER_OPTIONS_STOP_BIT		0x00000002

    Continue transmitting data in bulk without caring about Ack or nAck from device if this bit
    is not set. If this bit is set then stop transferring the data in the buffer when the device
    nACKs
    #define I2C_TRANSFER_OPTIONS_BREAK_ON_NACK	0x00000004

    libMPSSE-I2C generates an ACKs for every byte read. Some I2C slaves require the I2C
    master to generate a nACK for the last data byte read. Setting this bit enables working with
    such I2C slaves
    #define I2C_TRANSFER_OPTIONS_NACK_LAST_BYTE	0x00000008

    Fast transfers prepare a buffer containing commands to generate START/STOP/ADDRESS
       conditions and commands to read/write data. This buffer is sent to the MPSSE in one shot,
       hence delays between different phases of the I2C transfer are eliminated. Fast transfers
       can have data length in terms of bits or bytes. The user application should call
       I2C_DeviceWrite or I2C_DeviceRead with either
       I2C_TRANSFER_OPTIONS_FAST_TRANSFER_BYTES or
       I2C_TRANSFER_OPTIONS_FAST_TRANSFER_BITS bit set to perform a fast transfer.
       I2C_TRANSFER_OPTIONS_START_BIT and I2C_TRANSFER_OPTIONS_STOP_BIT have
       their usual meanings when used in fast transfers, however
       I2C_TRANSFER_OPTIONS_BREAK_ON_NACK and
       I2C_TRANSFER_OPTIONS_NACK_LAST_BYTE are not applicable in fast transfers
    #define I2C_TRANSFER_OPTIONS_FAST_TRANSFER		0x00000030 // not visible to user

   When the user calls I2C_DeviceWrite or I2C_DeviceRead with this bit set then libMPSSE
   packs commands to transfer sizeToTransfer number of bytes, and to read/write
   sizeToTransfer number of ack bits.If data is written then the read ack bits are ignored, if
   data is being read then an acknowledgement bit(SDA= LOW) is given to the I2C slave
   after each byte read

#define I2C_TRANSFER_OPTIONS_FAST_TRANSFER_BYTES	0x00000010
   When the user calls I2C_DeviceWrite or I2C_DeviceRead with this bit set then libMPSSE
   packs commands to transfer sizeToTransfer number of bits. There is no ACK phase when
   this bit is set

#define I2C_TRANSFER_OPTIONS_FAST_TRANSFER_BITS	0x00000020
   The address parameter is ignored in fast transfers if this bit is set.This would mean that
   the address is either a part of the data or this is a special I2C frame that doesn't require
   an address. However if this bit is not set then 7bit address and 1bit direction will be
    written to the I2C bus each time I2C_DeviceWrite or I2C_DeviceRead is called and a
	 1bit acknowledgement will be read after that, which will however be just ignored
#define I2C_TRANSFER_OPTIONS_NO_ADDRESS		0x00000040
*/
    public const uint I2C_TRANSFER_OPTIONS_START_BIT = 0x01;
    public const uint I2C_TRANSFER_OPTIONS_STOP_BIT = 0x02;
    public const uint I2C_TRANSFER_OPTIONS_BREAK_ON_NACK = 0x04;
    public const uint I2C_TRANSFER_OPTIONS_NACK_LAST_BYTE = 0x08;
    public const uint I2C_TRANSFER_OPTIONS_FAST_TRANSFER_BYTES = 0x10;
    public const uint I2C_TRANSFER_OPTIONS_FAST_TRANSFER_BITS = 0x40;
    public const uint I2C_TRANSFER_OPTIONS_NO_ADDRESS = 0x20;


    private const uint FTC_SUCCESS = 0;
    private const uint FTC_DEVICE_IN_USE = 27;

    private const uint MAX_NUM_DEVICE_NAME_CHARS = 100;
    private const uint MAX_NUM_CHANNEL_CHARS = 5;

    private const uint MAX_NUM_DLL_VERSION_CHARS = 10;
    private const uint MAX_NUM_ERROR_MESSAGE_CHARS = 100;

    // To communicate with the M24C64(8192 byte) EEPROM, the maximum frequency the clock can be set is 375KHz 
    private const uint MAX_FREQ_M24C64_CLOCK_DIVISOR = 79;  // equivalent to 375KHz

    private const uint STANDARD_MODE = 1;
    private const uint FAST_MODE = 2;
    private const uint STRETCH_DATA_MODE = 4;

    private const uint WRITE_CONTROL_BUFFER_SIZE = 256;
    private const uint WRITE_DATA_BUFFER_SIZE = 65536;
    private const uint READ_DATA_BUFFER_SIZE = 65536;

    private const uint MAX_I2C_M24C64_CHIP_SIZE_IN_BYTES = 512;

    private const uint NUM_M24C64_PAGES = 1;
    private const uint NUM_M24C64_BYTES_PER_PAGE = 32;

    private const uint MAX_I2C_24LC16B_CHIP_SIZE_IN_BYTES = 256;

    private const uint NUM_24LC16B_PAGES = 8;
    private const uint NUM_24LC16B_BYTES_PER_PAGE = 256;

    private const uint NO_WRITE_TYPE = 0;
    private const uint BYTE_WRITE_TYPE = 1;
    private const uint PAGE_WRITE_TYPE = 2;

    private const uint BYTE_READ_TYPE = 1;
    private const uint PAGE_READ_TYPE = 2;


    //**************************************************************************
    //
    // TYPE DEFINITIONS
    //
    //**************************************************************************

    public struct FTC_INPUT_OUTPUT_PINS
    {
      public bool bPin1InputOutputState;
      public bool bPin1LowHighState;
      public bool bPin2InputOutputState;
      public bool bPin2LowHighState;
      public bool bPin3InputOutputState;
      public bool bPin3LowHighState;
      public bool bPin4InputOutputState;
      public bool bPin4LowHighState;
    }

    public struct FTH_INPUT_OUTPUT_PINS
    {
      public bool bPin1InputOutputState;
      public bool bPin1LowHighState;
      public bool bPin2InputOutputState;
      public bool bPin2LowHighState;
      public bool bPin3InputOutputState;
      public bool bPin3LowHighState;
      public bool bPin4InputOutputState;
      public bool bPin4LowHighState;
      public bool bPin5InputOutputState;
      public bool bPin5LowHighState;
      public bool bPin6InputOutputState;
      public bool bPin6LowHighState;
      public bool bPin7InputOutputState;
      public bool bPin7LowHighState;
      public bool bPin8InputOutputState;
      public bool bPin8LowHighState;
    }

    public struct FTC_LOW_HIGH_PINS
    {
      public bool bPin1LowHighState;
      public bool bPin2LowHighState;
      public bool bPin3LowHighState;
      public bool bPin4LowHighState;
    }

    public struct FTC_PAGE_WRITE_DATA
    {
      public uint NumPages;
      public uint NumBytesPerPage;
    }

    public struct FTH_LOW_HIGH_PINS
    {
      public bool bPin1LowHighState;
      public bool bPin2LowHighState;
      public bool bPin3LowHighState;
      public bool bPin4LowHighState;
      public bool bPin5LowHighState;
      public bool bPin6LowHighState;
      public bool bPin7LowHighState;
      public bool bPin8LowHighState;
    }

    public struct FTC_CLOSE_FINAL_STATE_PINS
    {
      public bool bTCKPinState;
      public bool bTCKPinActiveState;
      public bool bTDIPinState;
      public bool bTDIPinActiveState;
      public bool bTMSPinState;
      public bool bTMSPinActiveState;
    }



    [StructLayout(LayoutKind.Sequential, Pack = 1)]
    public struct ChannelCfg
    {
      public UInt32 ClockRate;
      public byte LatencyTimer;
      public UInt32 Options;
    }

    // See: http://www.ftdichip.com/Support/Documents/AppNotes/AN_177_User_Guide_For_LibMPSSE-I2C.pdf
    // Built-in Windows API functions to allow us to dynamically load our own DLL.
    [DllImportAttribute("libMPSSE.dll", EntryPoint = "I2C_GetNumChannels", CallingConvention = CallingConvention.Cdecl)]
    static extern uint I2C_GetNumChannels(ref uint NumChannels);

    [DllImportAttribute("libMPSSE.dll", EntryPoint = "I2C_OpenChannel", CallingConvention = CallingConvention.Cdecl)]
    static extern uint I2C_OpenChannel(uint index, ref IntPtr handler);

    [DllImportAttribute("libMPSSE.dll", EntryPoint = "I2C_CloseChannel", CallingConvention = CallingConvention.Cdecl)]
    static extern uint I2C_CloseChannel(IntPtr handler);

    [DllImportAttribute("libMPSSE.dll", EntryPoint = "I2C_InitChannel", CallingConvention = CallingConvention.Cdecl)]
    static extern uint I2C_InitChannel(IntPtr handler, ref ChannelCfg config);

    [DllImportAttribute("libMPSSE.dll", EntryPoint = "I2C_DeviceRead", CallingConvention = CallingConvention.Cdecl)]
    static extern uint I2C_DeviceRead(IntPtr handler, UInt32 deviceAddress, UInt32 sizeToTransfer, byte[] buffer, ref UInt32 sizeTransfered, UInt32 options);

    [DllImportAttribute("libMPSSE.dll", EntryPoint = "I2C_DeviceWrite", CallingConvention = CallingConvention.Cdecl)]
    static extern uint I2C_DeviceWrite(IntPtr handler, UInt32 deviceAddress, UInt32 sizeToTransfer, byte[] buffer, ref UInt32 sizeTransfered, UInt32 options);

    [DllImportAttribute("libMPSSE.dll", EntryPoint = "FT_WriteGPIO", CallingConvention = CallingConvention.Cdecl)]
    static extern uint FT_WriteGPIO(IntPtr handler, byte dir, byte value);

    [DllImportAttribute("libMPSSE.dll", EntryPoint = "FT_ReadGPIO", CallingConvention = CallingConvention.Cdecl)]
    static extern uint FT_ReadGPIO(IntPtr handler, ref byte value);

    [DllImportAttribute("libMPSSE.dll", EntryPoint = "Init_libMPSSE", CallingConvention = CallingConvention.Cdecl)]
    static extern void Init_libMPSSE();

    private uint channel = 0;
    IntPtr FTDIhandler;

    private byte dir = 0;
    private byte gpo = 0;

    private System.Object _lock = new System.Object();

    public bool IsConnected()
    {
      if (FTDIhandler == IntPtr.Zero)
      {
        return false;
      }
      return true;
    }

    public LibMpsseI2C(int channel_ = 0, int clockrate_ = 100000)
    {
      channel = (uint)channel_;
      uint ch = 0;
      uint status = 0;
      if (FTDIhandler != IntPtr.Zero)
      {

        status = I2C_GetNumChannels(ref ch);
        if (status == 0 && ch == 2)
        {
          //MessageBox.Show("FTDI already in use!");
          throw new LibMpsseException(status, $"FTDI already in use!");
        }
      }

      FTDIhandler = new IntPtr();
      Init_libMPSSE();
      I2C_GetNumChannels(ref ch);

      if (ch > channel)
      {
        status = I2C_OpenChannel(channel, ref FTDIhandler);
        if (status != 0)
        {
          //   MessageBox.Show("FTDI error while open channel " + channel);
          I2C_CloseChannel(FTDIhandler);
          throw new LibMpsseException(status, $"FTDI error while open channel {channel}!");
        }
        ChannelCfg chcfg;
        chcfg.ClockRate = (uint)clockrate_;
        chcfg.LatencyTimer = 150;
        /*
        Achtung: AN_177_User_Guide_For_LibMPSSE-I2C.pdf
          BIT0: I2C_DISABLE_3PHASE_CLOCKING
          BIT1: I2C_ENABLE_DRIVE_ONLY_ZERO
        Aus: ftdi_i2c.h
        This member provides a way to enable/disable features
	      specific to the protocol that are implemented in the chip
	      BIT0:3PhaseDataClocking - Setting this bit will turn on 3 phase data clocking for a
		       FT2232H dual hi-speed device or FT4232H quad hi-speed device. Three phase
           data clocking, ensures the data is valid on both edges of a clock
        BIT1: Loopback
        BIT2: Clock stretching
        BIT3-BIT31: Reserved
        */
        const uint OPTIONS_I2C_DISABLE_3PHASE_CLOCKING = 0x01;
        const uint OPTIONS_Loopback = 0x02;
        const uint OPTIONS_ClockStreching = 0x04;
        // chcfg.Options = 3;
        chcfg.Options = 0x00;
        status = I2C_InitChannel(FTDIhandler, ref chcfg);
        if (status != 0)
        {
          //MessageBox.Show("FTDI error while init channel " + ch);
          I2C_CloseChannel(FTDIhandler);
          throw new LibMpsseException(status, $"FTDI error while open channel {channel}!");
        }
      }
      else
      {
        // MessageBox.Show("ERROR while init FTDI only " + ch + " are available, can't set channel " + channel + "!");
        throw new LibMpsseException(status, $"ERROR while init FTDI only {ch} are available, can't set channel {channel}!");
      }
    }

    private void ThrowExceptionIfClosed()
    {
      if (FTDIhandler == IntPtr.Zero)
      {
        throw new LibMpsseException("Is closed!");
      }
    }

    public uint I2Cread(UInt32 deviceAddress, UInt32 sizeToTransfer, byte[] buffer, ref UInt32 sizeTransfered, UInt32 options)
    {
      ThrowExceptionIfClosed();

      lock (_lock)
      {
        return I2C_DeviceRead(FTDIhandler, deviceAddress, sizeToTransfer, buffer, ref sizeTransfered, options);
      }
    }

    public uint I2Cwrite(UInt32 deviceAddress, UInt32 sizeToTransfer, byte[] buffer, ref UInt32 sizeTransfered, UInt32 options)
    {
      ThrowExceptionIfClosed();

      lock (_lock)
      {
        return I2C_DeviceWrite(FTDIhandler, deviceAddress, sizeToTransfer, buffer, ref sizeTransfered, options);
      }
    }

    /// <summary></summary>
    /// <param name="pin">pin number</param>
    /// <param name="dir">0:=input; 1:=output</param>
    /// <returns></returns>
    public uint SetGPIOdir(byte pin, byte dir)
    {
      ThrowExceptionIfClosed();

      if (dir == 1)
      {
        this.dir |= (byte)(1 << pin);
      }
      else
      {
        this.dir &= ((byte)~(1 << pin));
      }
      this.gpo &= ((byte)~(1 << pin));

      lock (_lock)
      {
        return FT_WriteGPIO(FTDIhandler, this.dir, this.gpo);
      }
    }

    public uint SetGPIO(byte pin)
    {
      ThrowExceptionIfClosed();

      this.gpo = (byte)(this.gpo | (byte)(1 << pin));
      lock (_lock)
      {
        return FT_WriteGPIO(FTDIhandler, this.dir, this.gpo);
      }
    }

    public uint ClearGPIO(byte pin)
    {
      ThrowExceptionIfClosed();

      this.gpo &= ((byte)~(1 << pin));
      lock (_lock)
      {
        return FT_WriteGPIO(FTDIhandler, this.dir, this.gpo);
      }
    }

    public uint ReadGPIO(ref byte value)
    {
      ThrowExceptionIfClosed();

      lock (_lock)
      {
        return FT_ReadGPIO(FTDIhandler, ref value);
      }
    }


    public uint Close()
    {
      ThrowExceptionIfClosed();

      uint status = I2C_CloseChannel(FTDIhandler);
      FTDIhandler = IntPtr.Zero;
      return status;
    }

    public int ConnectionState()
    {
      uint ch = 0;
      uint status = 0;
      if (FTDIhandler != IntPtr.Zero)
      {
        status = I2C_GetNumChannels(ref ch);
        if (status == 0 && ch == 2)
        {
          return 0;
        }
        I2C_CloseChannel(FTDIhandler);
        FTDIhandler = IntPtr.Zero;
        return -1;
      }
      return -1;
    }

  }
}
