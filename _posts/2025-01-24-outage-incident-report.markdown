---
layout: post
title:  "outage incident report"
date:   2025-01-24 10:06:00 -05:00
categories: outage report
---

### We are back online as of 9:55 AM, January 24th, 2025

## What Happened
In the early hours of the morning (3:00 AM, to be exact), requests to the API on our end began failing. Upon investigation, I discovered that the wallet account had been blocked by the master server due to VPN usage. DuinoCoin explicitly prohibits VPN and alternate account usage. One account was indeed an alternate account I attempted to create for testing the faucet. However, upon account creation, I received an error calling me out for using an alternate account. That account was promptly deleted.

## The Fix
I reached out to a staff member on the DuinoCoin Discord to get the accounts unlinked. This process took some time. In the interim, I placed the faucet into global lockdown mode to prevent its use. My first message to the staff was sent at 4:21 AM. The issue was resolved, and the faucet was brought back online at 9:50 AM. 

Unfortunately, the global lockdown screen was not displaying for all users. Additionally, a power outage at the host occurred around 6:00 AM and was not resolved until 8:30 AM. Although Cloudflare had already cached the lockdown page, it did not propagate to all users. When it rains, it pours.

## TL;DR
There was an outage from 3:00 AM to nearly 10:00 AM on January 24th, 2025. The faucet is back up and running now.

Thank you for your patience.  
I'm going to bed.  

\- tbwcjw
