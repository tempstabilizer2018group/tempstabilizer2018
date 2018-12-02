using libMPSSEWrapper;
using System;
using System.Threading;

namespace Test
{
  class Program
  {
    static void Main(string[] args)
    {
      int channel = 0; // 0: A, 1: B
      LibMpsseI2C i2c = new LibMpsseI2C(channel, 100000);
      I2C_Maxim30205 max30205 = new I2C_Maxim30205(i2c, I2C_Maxim30205.ADDRESS);

      while (true)
      {
        double fTemp = max30205.ReadTemperatureOneShot();
        Console.WriteLine($"fTemp: {fTemp:0.0000}");
        Thread.Sleep(1000);
      }
    }
  }
}
