from twisted.internet import reactor, protocol
from twisted.words.protocols import irc

import aiml
import sys


BRAIN_STARTUP_FILE = './brain/std-startup.xml'


class EskBot(irc.IRCClient):
    nickname = "eskarina"

    def signedOn(self):
        """
        Called once the bot has connected to the IRC server.

        Loads the brain, and joins a channel.
        """

        self.join(self.factory.channel)

    def privmsg(self, user, channel, message):
        """
        Despite the name, called when the bot receives any message, be it a
        private message or in a channel.
        """
        user = user.split('!', 1)[0]
        # TODO: figure out what message to respond with. Echo for now.
        reply_message = self.build_reply(message)

        if channel == self.nickname:
            # This is a private message to me, so I will respond directly to
            # the user.
            self.msg(user, reply_message)

        elif message.startswith(self.nickname + ':'):
            # This message is directed at me, so I will respond.

            self.msg(channel, user + ':' + reply_message)

    def build_reply(self, message):
        """
        Based on some AI magics, compose a response to the message sent to me.
        """
        if message.startswith(self.nickname + ':'):
            # Remove my name from the message.
            message = message[len(self.nickname + ':'):]

        ai_response = self.factory.kernel.respond(message)

        return message  # TODO: echoing it back for now.


class EskBotFactory(protocol.ClientFactory):
    def __init__(self, channel):
        self.channel = channel
        self.kernel = aiml.Kernel()
        self.kernel.learn(BRAIN_STARTUP_FILE)
        self.kernel.respond("load aiml b")

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
