import network
import machine
import urequests
import time


class Simplified():
	def __init__(self):
		self.rtc = machine.RTC()
		self.wlan = network.WLAN(mode=network.WLAN.STA, antenna=network.WLAN.INT_ANT)
		self.timeSynchonized = False

	def test(self):
		# self.wlan.ifconfig(config='dhcp')
		print('a')
		self.wlan.connect("waffenplatzstrasse26", auth=(network.WLAN.WPA2, "guguseli"))
		print('b')

		for i in range(100):
		# while True:
			print('i=%d' % i)
			self.rtcNow = self.rtc.now()

			if self.wlan.isconnected():
				print('isconnected')

				if not self.timeSynchonized:
					self.rtc.ntp_sync("pool.ntp.org")
					self.timeSynchonized = True

				else:
					data = '{"id": %s, "time": "%s-%02d-%02dT%02d:%02d:%02d.%03d+00:00"}' % (machine.rng(), self.rtcNow[0], self.rtcNow[1], self.rtcNow[2], self.rtcNow[3], self.rtcNow[4], self.rtcNow[5], self.rtcNow[6] // 1000)
					print(data)
					try:
						response = urequests.post("https://posttestserver.com/post.php", data = data)
						print(response.text)
					except Exception as e:
						print(e)
						time.sleep(1)
			
node = Simplified()
node.test()
