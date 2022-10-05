# NYU SMTP Relay

This is a little SMTP server that can be used to send email in NYU, without triggering the "Failed NYU Email Security check" warning.

It can only be used within the NYU network, and only serves a purpose if sending emails from an NYU address.

## Explanation

NYU has a security check that is applied to email **both from and to NYU email addresses**. In that situation, if the email wasn't sent through an approved NYU email server, the warning will be added to the subject line: `[Failed NYU Email Security Check]`.

To avoid this, we can deliver email to `@nyu.edu` addresses through the NYU MX server. However, those servers will refuse to relay, so you have to deliver email to other addresses through another service, for example SendGrid.

This is what this program does: it acts as an email server, listening for incoming email from your applications or scripts, check whether they are sent to a `@nyu.edu` address, and sends them either through NYU MX server or an external SMTP server.

## Configuration

Configuration is done through environment variables. Each server is numbered, starting from 1, with no gaps. Servers are tried in ordered, the first server whose `DESTINATION_REGEX` matches is used.

* `OUTBOUND_1_DESTINATION_REGEX`: A regular expression, in Python syntax, that is matched with the address. The regex is anchored at the start and end of the address, no need to use `^` and `$`.
* `OUTBOUND_1_HOST`: The host name or IP address of the server
* `OUTBOUND_1_PORT`: The port number of the server, usually 25, 587, or 465
* `OUTBOUND_1_SSL`: Connect with TLS, `yes` or `no`
* `OUTBOUND_1_STARTTLS`: Whether to use the `STARTTLS` mechanism after connecting, `yes` or `no`
* `OUTBOUND_1_USER`: The user name to log in with, leave empty or unset to not log in
* `OUTBOUND_1_PASSWORD`: The password to log in with, leave empty or unset to not log in

Example configuration for NYU:

```
OUTBOUND_1_DESTINATION_REGEX=".*@nyu\\.edu" \
OUTBOUND_1_HOST="67.231.153.242" \
OUTBOUND_1_PORT="25" \
OUTBOUND_1_SSL="no" \
OUTBOUND_1_STARTTLS="no" \
OUTBOUND_2_DESTINATION_REGEX=".*" \
OUTBOUND_2_HOST="smtp.sendgrid.net" \
OUTBOUND_2_PORT="465" \
OUTBOUND_2_SSL="yes" \
OUTBOUND_2_STARTTLS="no" \
OUTBOUND_2_USER="apikey" \
OUTBOUND_2_PASSWORD="SG.Your.SendGrid.Api.Key.Here" \
python3 nyusmtprelay.py
```
