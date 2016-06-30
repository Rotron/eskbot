import os
import sys

import aiml
from twisted.internet import reactor, protocol
from twisted.words.protocols import irc


STARTUP_FILE = './std-startup.xml'  # Move this to some config file maybe
BRAIN_FILE = './bot_brain.brn'


class EskBot(irc.IRCClient):
    nickname = "eskarina"

    def signedOn(self):
        """
        Called once the bot has connected to the IRC server.
        """
        self.join(self.factory.channel)

    def privmsg(self, user, channel, message):
        """
        Despite the name, called when the bot receives any message, be it a
        private message or in a channel.
        """
        user = user.split('!', 1)[0]
        reply_message = self.build_reply(message)

        if channel == self.nickname:
            # This is a private message to me, so I will respond directly to
            # the user.
            self.msg(user, reply_message)

        elif message.startswith(self.nickname + ':'):
            # This message is directed at me, so I will respond.
            self.msg(channel, user + ': ' + reply_message)

    def build_reply(self, message):
        """
        Based on some AI magicks, compose a response to the message sent to me.
        """
        if message.startswith(self.nickname + ':'):
            # Remove my name from the message.
            message = message[len(self.nickname + ':'):].strip()

        # TODO: maybe put this in a try-except block, once I know what errors
        # to expect. For now, let it fail loudly.
        ai_response = self.factory.kernel.respond(message)

        if ai_response:
            return ai_response
        else:
            # Science has failed us. We are on our own.
            return "Perhaps."


class EskBotFactory(protocol.ClientFactory):
    def __init__(self, channel):
        self.channel = channel
        self.setup_aiml_kernel(STARTUP_FILE)

    def setup_aiml_kernel(self, file_to_learn):
        self.kernel = aiml.Kernel()
        if os.path.isfile(BRAIN_FILE):
            self.kernel.bootstrap(brainFile=BRAIN_FILE)
        else:
            self.kernel.bootstrap(
                learnFiles=file_to_learn,
                commands='load aiml b'
            )
            self.kernel.saveBrain(BRAIN_FILE)

    def buildProtocol(self, addr):
        proto = EskBot()
        proto.factory = self
        return proto

    def clientConnectionLost(self, connector, reason):
        # Reconnect if disconnected
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        reactor.stop()


network = sys.argv[1]
port = int(sys.argv[2])
channel = sys.argv[3]
reactor.connectTCP(network, port, EskBotFactory(channel))
reactor.run()
