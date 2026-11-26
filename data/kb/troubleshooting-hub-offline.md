# Troubleshooting — Contoso Home Hub Is Offline

When the hub is offline, the Contoso Home app shows a grey **Offline** badge on the
home screen and devices can't be controlled remotely. Automations stored on the hub
keep running locally.

## Hub status light

| Light | Meaning | What to do |
|---|---|---|
| Solid green | Online and working | Nothing |
| Blinking blue | No internet connection | Check the home router (steps below) |
| Solid blue | Running on cellular backup (Plus and Premium) | Fix the home internet; monitoring continues meanwhile |
| Blinking amber | Updating firmware | **Do not unplug.** Updates take up to 10 minutes |
| Solid red | Hardware fault | Contact support |
| No light | No power | Check the power adapter and outlet |

## Steps to bring the hub back online

1. **Check the home internet.** Make sure other devices in the home (phone on
   Wi-Fi, computer) can reach the internet. If not, the problem is the internet
   service, not the hub. Restart the router or contact the internet provider.
2. **Check the hub's connection.** An Ethernet cable from the hub to the router is
   the most reliable connection. If the hub uses Wi-Fi, make sure the Wi-Fi
   password hasn't changed. If it has, update it in the app: Settings > Hub >
   Network.
3. **Power-cycle the hub.** Unplug the hub's power adapter, wait 30 seconds, and
   plug it back in. The hub takes about 2 minutes to start. Never power-cycle while
   the light is blinking amber.
4. **Wait 15 minutes.** If the light is still not solid green after 15 minutes,
   contact support.

## Factory reset

Holding the reset button for 15 seconds erases all paired devices and settings.
**Only do a factory reset when a support agent asks you to.**

## Alarm monitoring while the hub is offline

With cellular backup (Plus, Premium), alarm monitoring continues while the home
internet is down. On Essentials with the monitoring add-on, monitoring stops until
the hub is back online.
