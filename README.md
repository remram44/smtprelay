# NYU SMTP Relay

This is a little SMTP server that can be used to send email in NYU, without triggering the "Failed NYU Email Security check" warning.

It can only be used within the NYU network, and only serves a purpose if sending emails from an NYU address.

## Explanation

NYU has a security check that is applied to email **both from and to NYU email addresses**. In that situation, if the email wasn't sent through an approved NYU email server, the warning will be added to the subject line: `[Failed NYU Email Security Check]`.

To avoid this, we can deliver email to `@nyu.edu` addresses through the NYU MX server. However, those servers will refuse to relay, so you have to deliver email to other addresses through another service, for example SendGrid.

This is what this program does: it acts as an email server, listening for incoming email from your applications or scripts, check whether they are sent to a `@nyu.edu` address, and sends them either through NYU MX server or an external SMTP server.

## Configuration

TODO
