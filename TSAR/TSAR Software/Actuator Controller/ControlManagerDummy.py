import serial, ctypes

import tkinter as tk
from tkinter import messagebox

# Constants
RECEIVE_PAYLOAD_LENGTH = 5 # The length in bytes of the actuator commands
RECEIVE_PACKET_LENGTH = 7 + RECEIVE_PAYLOAD_LENGTH # The length in bytes of the preamble, payload, and 
SEND_PAYLOAD_LENGTH = 6
SEND_PACKET_LENGTH = SEND_PAYLOAD_LENGTH + 10
MAXIMUM_LIFETIME_CHECKSUM_ERRORS = 25 

def combine(a, b):
	return a + (b << 8)

def checksum(message):
	result = 0
	for i in message:
		result += (i*i*i)%251

	return result

class Application(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)
		self.pack()

		self.serial = None

		while True:
			try:
				self.serial = serial.Serial("COM3", 9600, timeout=3)
				break
			except serial.serialutil.SerialException:
				retry = messagebox.askretrycancel("Cannot connect", "Unable to connect to Actuator Controller.")
				if not retry:
					return

		self.safest_next_failure_mode = 255
		self.command = 0

		### INCOMING HEARTBEAT ###
		heartbeat_in_group = tk.LabelFrame(self, text="Incoming heartbeat")
		heartbeat_in_group.pack(side=tk.LEFT)

		tk.Label(heartbeat_in_group, text="Valid:").grid(row=0)
		tk.Label(heartbeat_in_group, text="Safest next failure mode:").grid(row=1)
		tk.Label(heartbeat_in_group, text="Failure mode:").grid(row=2)
		tk.Label(heartbeat_in_group, text="Failure cause:").grid(row=3)
		tk.Label(heartbeat_in_group, text="Consecutive checksum error count:").grid(row=4)
		tk.Label(heartbeat_in_group, text="Lifetime checksum error count:").grid(row=5)
		tk.Label(heartbeat_in_group, text="Sensors:").grid(row=6)
		tk.Label(heartbeat_in_group, text="Checksum:").grid(row=7)

		self.valid = tk.StringVar()
		tk.Label(heartbeat_in_group, textvariable=self.valid).grid(row=0, column=1)

		self.safest_next_failure_mode_label = tk.StringVar()
		tk.Label(heartbeat_in_group, textvariable=self.safest_next_failure_mode_label).grid(row=1, column=1)

		self.failure_mode = tk.StringVar()
		tk.Label(heartbeat_in_group, textvariable=self.failure_mode).grid(row=2, column=1)

		self.failure_cause = tk.StringVar()
		tk.Label(heartbeat_in_group, textvariable=self.failure_cause).grid(row=3, column=1)

		self.consecutive_checksum_error_count = tk.StringVar()
		tk.Label(heartbeat_in_group, textvariable=self.consecutive_checksum_error_count).grid(row=4, column=1)

		self.lifetime_checksum_error_count = tk.StringVar()
		tk.Label(heartbeat_in_group, textvariable=self.lifetime_checksum_error_count).grid(row=5, column=1)

		self.sensors = tk.StringVar()
		tk.Label(heartbeat_in_group, textvariable=self.sensors).grid(row=6, column=1)

		self.checksum = tk.StringVar()
		tk.Label(heartbeat_in_group, textvariable=self.checksum).grid(row=7, column=1)


		### OUTGOING HEARTBEAT ###
		heartbeat_out_group = tk.LabelFrame(self, text="Outgoing heartbeat")
		heartbeat_out_group.pack(side=tk.LEFT)
		
		self.enable_heartbeat = tk.IntVar()
		tk.Checkbutton(heartbeat_out_group, variable=self.enable_heartbeat, text="Enable heartbeat",
		               onvalue=True, offvalue=False, command=self.send_heartbeat).grid(row=0, columnspan=3)

		self.safest_next_failure_mode_var = tk.IntVar()
		self.safest_next_failure_mode_var.set(self.safest_next_failure_mode)
		tk.Label(heartbeat_out_group, text="Safest next failure mode:").grid(row=1, column=0)
		tk.Spinbox(heartbeat_out_group, textvariable=self.safest_next_failure_mode_var,
		           from_=0, to=255, width=3).grid(row=1, column=1)
		tk.Button(heartbeat_out_group, text="Set", command=self.set_safest_next_failure_mode, width=6).grid(row=1, column=2)

		self.command_var = tk.IntVar()
		self.command_var.set(self.command)
		tk.Label(heartbeat_out_group, text="Command:").grid(row=2, column=0)
		tk.Spinbox(heartbeat_out_group, textvariable=self.command_var,
		           from_=0, to=255, width=3).grid(row=2, column=1)
		tk.Button(heartbeat_out_group, text="Set", command=self.set_command, width=6).grid(row=2, column=2)

		### START FUNCTIONS ###
		self.get_packet()

	def read_packet(self):
		while self.serial.read(1) != b'\n':
			pass

		# return b'\n' + s.read(SEND_PACKET_LENGTH-1)
		return Packet(b'\n' + self.serial.read(SEND_PACKET_LENGTH-1))

	def get_packet(self):
		packet = None
		while (self.serial.in_waiting >= SEND_PACKET_LENGTH):
			packet = self.read_packet()

		self.after(100, self.get_packet)

		# print(packet)
		if packet:
			self.valid.set(str(bool(packet.valid)))
			self.safest_next_failure_mode_label.set(packet.safest_next_failure_mode)
			self.failure_mode.set(packet.failure_mode)
			self.failure_cause.set(packet.failure_cause)
			self.consecutive_checksum_error_count.set(packet.consecutive_checksum_error_count)
			self.lifetime_checksum_error_count.set(packet.lifetime_checksum_error_count)
			self.sensors.set(packet.sensors)
			self.checksum.set(packet.checksum)

	def send_heartbeat(self):
		data = bytes([ord("\n"), self.safest_next_failure_mode, self.command]) + bytes([0, 1, 2, 3, 4])

		# Calculate and append checksum
		data += bytes(ctypes.c_uint32(checksum(data)))

		# Send heartbeat
		self.serial.write(data)

		# Schedule next heartbeat
		if self.enable_heartbeat.get():
			self.after(400, self.send_heartbeat)

		# Show confirmation dialog
		if self.command != 0:
			c = self.command
			self.command = 0
			messagebox.showinfo("Command sent", "Command {} successfully sent.".format(c))

	def set_safest_next_failure_mode(self):
		if not 0 <= self.safest_next_failure_mode_var.get() <= 255:
			messagebox.showerror("Error", "Safest next failure mode not within bounds! Setting it to closest boundary value.")

		self.safest_next_failure_mode = min(255, max(0, self.safest_next_failure_mode_var.get()))
		self.safest_next_failure_mode_var.set(self.safest_next_failure_mode)

	def set_command(self):
		if not 0 <= self.command_var.get() <= 255:
			messagebox.showerror("Error", "Command not within bounds! Setting it to closest boundary value.")

		self.command = min(255, max(0, self.command_var.get()))
		self.command_var.set(self.command)

class Packet:
	def __init__(self, packet):
		self._data = packet
		self.valid = packet[0] == 10 # Check for starting newline
		self.safest_next_failure_mode = packet[1]
		self.failure_mode = packet[2]
		self.failure_cause = packet[3]
		self.consecutive_checksum_error_count = packet[4]
		self.lifetime_checksum_error_count = packet[5]
		self.sensors = list(bytes(packet[6:-4]))
		self.checksum = packet[-4:].hex()

	def __hash__(self):
		return hash(self._data)

	def __str__(self):
		return f"""Packet(
	valid = {self.valid}
	safest_next_failure_mode = {self.safest_next_failure_mode}
	failure_mode = {self.failure_mode}
	failure_cause = {self.failure_cause}
	consecutive_checksum_error_count = {self.consecutive_checksum_error_count}
	lifetime_checksum_error_count = {self.lifetime_checksum_error_count}
	sensors = {self.sensors[:4] + [combine(self.sensors[4], self.sensors[5])]}
	checksum = {self.checksum}
)"""

if __name__ == "__main__":
	root = tk.Tk()
	app = Application(root)
	if app.serial:
		root.mainloop()

	import sys
	sys.exit()


# while True:
# 	print("Loop count:", loop_count // 10)
# 	data = bytes([ord("\n"), 255, 15]) + bytes([loop_count // 10, 0, 0, 0, 0])
# 	print(data.hex())
# 	data += bytes(ctypes.c_uint32(checksum(data)))
# 	s.write(data)
# 	# print("Sending packet: " + data.hex())
# 	loop_count += 1

# 	packet = None
# 	while (s.in_waiting >= SEND_PACKET_LENGTH):
# 		packet = read_packet(s)
# 	# if packet != None:
# 		# print("Data:", packet._data.hex())
# 	print(packet)
# 	print("\n")

# 	if hash(packet) != old_hash:
# 		print(packet)
# 		old_hash = hash(packet)

# 	time.sleep(.4)
