import aiosmtplib
from aiosmtpd.controller import Controller
import asyncio
import contextlib
import logging
import os
import re
import smtplib
import sys


__version__ = '0.1.0'


logger = logging.getLogger('smtprelay')


# Read servers from environment
def read_servers():
    servers = []
    i = 1
    while f'OUTBOUND_{i}_HOST' in os.environ:
        def asbool(arg):
            if arg.lower() in ('yes', 'true', '1'):
                return True
            elif arg.lower() in ('no', 'false', '0'):
                return False
            else:
                raise ValueError(f'Invalid yes/no value: {arg!r}')

        servers.append({
            'destination_regex': re.compile(
                os.environ[f'OUTBOUND_{i}_DESTINATION_REGEX'] + '$',
            ),
            'host': os.environ[f'OUTBOUND_{i}_HOST'],
            'port': int(os.environ[f'OUTBOUND_{i}_PORT'], 10),
            'ssl': asbool(os.environ[f'OUTBOUND_{i}_SSL']),
            'starttls': asbool(os.environ[f'OUTBOUND_{i}_STARTTLS']),
            'user': os.environ.get(f'OUTBOUND_{i}_USER'),
            'password': os.environ.get(f'OUTBOUND_{i}_PASSWORD'),
        })

        i += 1

    logger.info('Loaded %d servers', len(servers))

    return servers

servers = read_servers()


def find_server(destination):
    for server in servers:
        if server['destination_regex'].match(destination):
            return server
    return None


async def send_mail(server, addresses, envelope):
    await aiosmtplib.send(
        envelope.content,
        envelope.mail_from,
        addresses,
        hostname=server['host'],
        port=server['port'],
        username=server['user'],
        password=server['password'],
        use_tls=server['ssl'],
        start_tls=server['starttls'],
    )


class MailHandler():
    async def handle_RCPT(
        self,
        server,
        session,
        envelope,
        address,
        rcpt_options,
    ):
        if find_server(address) is None:
            logger.info('Refusing to send to %r', address)
            return '550 not relaying to that domain'
        envelope.rcpt_tos.append(address)
        return '250 OK'

    async def handle_DATA(self, server, session, envelope):
        # Batch mails per server
        mail_per_server = {}
        for address in envelope.rcpt_tos:
            server = find_server(address)
            try:
                _, addresses = mail_per_server[id(server)]
            except KeyError:
                addresses = []
                mail_per_server[id(server)] = server, addresses
            addresses.append(address)

        # Log
        if logger.isEnabledFor(logging.INFO):
            logger.info(
                'Sending message to: %s',
                '; '.join(
                    server['host'] + ':'
                    + ', '.join(addresses)
                    for server, addresses in mail_per_server.values()
                ),
            )

        # Send
        for server, addresses in mail_per_server.values():
            await send_mail(server, addresses, envelope)

        return '250 Message accepted for delivery'


def main():
    # Don't accept any arguments
    assert len(sys.argv) == 1

    logging.basicConfig(level=logging.INFO)

    port = 2525
    loop = asyncio.new_event_loop()
    logger.info('Listening on port %d', port)
    controller = Controller(MailHandler(), hostname='0.0.0.0', port=port)
    controller.start()
    loop.run_forever()


if __name__ == '__main__':
    main()
