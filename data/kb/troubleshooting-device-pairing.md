# Troubleshooting — Adding and Re-pairing Devices

The Contoso Home Hub supports **Z-Wave**, **Zigbee**, **Matter** and **Wi-Fi**
devices. Only devices on the **Contoso Certified** list (in the app: Devices >
Add device > Certified devices) are supported. Other devices may work but Contoso
support can't troubleshoot them.

## Add a new device

1. In the Contoso Home app: **Devices > Add device**.
2. Choose the device type or scan the device's QR code (Matter devices have one on
   the device or its box).
3. Put the device in pairing mode as described in its instructions.
4. Keep the device **within 10 feet (3 meters) of the hub** while pairing. After
   pairing, it can be moved to its final location.
5. Name the device and assign it to a room.

Pairing usually takes under 2 minutes.

## If pairing fails

1. **Check the battery.** Replace batteries in battery-powered devices; low
   batteries are the most common cause of failed pairing.
2. **Check the plan limit.** Essentials supports up to 25 devices, Plus up to 60.
   The app shows "Device limit reached" when the limit is hit.
3. **Z-Wave devices: exclude first.** A Z-Wave device that was paired to another
   hub before must be excluded (removed) first: Devices > Add device > Z-Wave >
   Exclude device, then put the device in pairing mode. After exclusion, add it
   again.
4. **Zigbee devices: reset the device.** Follow the device maker's reset steps,
   then try again.
5. **Wi-Fi devices:** the hub and the device must use a **2.4 GHz** Wi-Fi network.
   Many Wi-Fi smart devices can't join 5 GHz networks.
6. **Restart the app** and try again.

If a device still won't pair after these steps, contact support.

## Device shows "Unresponsive"

An unresponsive device was paired but the hub can't reach it. Check its battery,
move it closer to the hub, or add a plugged-in Z-Wave or Zigbee device in between
(plugged-in devices relay signals and extend the network).
