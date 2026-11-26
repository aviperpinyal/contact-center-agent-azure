# Outages and Service Status

## Checking service status

The current status of Contoso services (app, cloud, video storage, Monitoring
Center) is published at **status.contoso-home.example**. The page lists active
incidents, affected services and regions, and the last update time.

## How we notify customers

During an outage that affects customers, Contoso Home Services sends:
- A push notification in the Contoso Home app
- An SMS to the account's primary phone number
- Updates on the status page at least every 60 minutes until the issue is resolved

## Contoso outage vs. home internet outage

- **Contoso outage:** a problem with Contoso's cloud or app. Listed on the status
  page. The hub keeps running automations locally, and alarm signals still reach
  the Monitoring Center.
- **Home internet outage:** a problem with the customer's internet provider. Not
  listed on the Contoso status page. See `troubleshooting-hub-offline.md`. Plus and
  Premium hubs switch to cellular backup automatically.

## Service credits

If a Contoso outage makes the app or remote control unavailable for **more than
4 consecutive hours**, affected customers can request a credit of **1/30 of their
monthly plan fee for each day affected**.
- Credits must be requested within **30 days** of the outage, by phone, chat, or in
  the app (Account > Billing > Request credit).
- Outages of the customer's own internet service are not eligible for credits.
- Credits are applied to the next bill.

## Planned maintenance

Planned maintenance happens on **Tuesdays between 1 a.m. and 3 a.m. Central time**
and is announced in the app at least **48 hours** in advance. Alarm monitoring is
never interrupted by planned maintenance.
