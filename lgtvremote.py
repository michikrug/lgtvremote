import getopt
import socket
import sys
from http import HTTPStatus
from http.client import HTTPConnection
from time import sleep
from xml.etree import ElementTree


class LGTVRemote():
    def __init__(self, ip_address, pairing_key=None):
        self.ip_address = ip_address
        self.pairing_key = pairing_key
        self.session_id = None

        if not self.ip_address:
            raise LGTVRemote.AddressMissingError

        if self.pairing_key:
            self.get_session()
        else:
            self.request_pairing_key()

    @staticmethod
    def discover_tv(attempts=10):
        request = 'M-SEARCH * HTTP/1.1\r\n' \
                  'HOST: 239.255.255.250:1900\r\n' \
                  'MAN: "ssdp:discover"\r\n' \
                  'MX: 2\r\n' \
                  'ST: urn:schemas-upnp-org:device:MediaRenderer:1\r\n\r\n'

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(1)

        while attempts > 0:
            attempts -= 1
            sock.sendto(request.encode(), ('239.255.255.250', 1900))
            try:
                response, address = sock.recvfrom(512)
            except:
                continue

            if 'LG' in response.decode():
                sock.close()
                return address[0]

        sock.close()
        raise LGTVRemote.NoTVFoundError

    def send_request(self, endpoint, content=None, extra_headers={}):
        try:
            http = HTTPConnection(self.ip_address, port=8080, timeout=3)
            headers = {'Content-Type': 'application/atom+xml'}
            headers.update(extra_headers)
            http.request('POST' if content else 'GET', endpoint, content, headers=headers)
            response = http.getresponse()
            if response.status == HTTPStatus.UNAUTHORIZED:
                raise LGTVRemote.NotAuthorizedError
            if response.status != HTTPStatus.OK:
                raise LGTVRemote.CommunicationError
            return response.read()
        except socket.timeout:
            raise LGTVRemote.TimeoutError

    def set_pairing_key(self, pairing_key):
        self.pairing_key = pairing_key
        self.get_session()

    def request_pairing_key(self):
        content = """
        <?xml version="1.0" encoding="utf-8"?>
        <auth>
            <type>AuthKeyReq</type>
        </auth>
        """
        self.send_request('/roap/api/auth', content)

    def get_session(self):
        content = """
        <?xml version="1.0" encoding="utf-8"?>
        <auth>
            <type>AuthReq</type>
            <value>{0}</value>
        </auth>
        """.format(self.pairing_key)
        response = self.send_request('/roap/api/auth', content)
        try:
            self.session_id = ElementTree.XML(response).find('session').text
        except:
            self.session_id = None
            raise LGTVRemote.WrongPairingKeyError

    def send_command(self, code):
        if self.session_id is None:
            raise LGTVRemote.NotAuthorizedError
        content = """
        <?xml version="1.0" encoding="utf-8"?>
        <command>
            <name>HandleKeyInput</name>
            <value>{0}</value>
        </command>
        """.format(code)
        self.send_request('/roap/api/command', content)

    def send_commands(self, codes, delay=0.2):
        for code in codes:
            self.send_command(code)
            sleep(delay)

    def get_data(self, target):
        if self.session_id is None:
            raise LGTVRemote.NotAuthorizedError
        # e.g. 'channel_list'
        response = self.send_request('/roap/api/data?target={0}'.format(target))
        return response

    class WrongPairingKeyError(Exception):
        """
        Exception raised when a wrong pairing key was given
        """

        pass

    class NotAuthorizedError(Exception):
        """
        Exception raised when no session id was retrieved but action requires one
        """

        pass

    class TimeoutError(Exception):
        """
        Exception raised when request runs into timeout
        """

        pass

    class CommunicationError(Exception):
        """
        Exception raised when request returns with unexpected response
        """

        pass

    class NoTVFoundError(Exception):
        """
        Exception raised when unable to find any LG TVs on the network
        """

        pass

    class AddressMissingError(Exception):
        """
        Exception raised when no IP address of the TV was given
        """

        pass

    POWER = 1
    NUM_0 = 2
    NUM_1 = 3
    NUM_2 = 4
    NUM_3 = 5
    NUM_4 = 6
    NUM_5 = 7
    NUM_6 = 8
    NUM_7 = 9
    NUM_8 = 10
    NUM_9 = 11
    UP = 12
    DOWN = 13
    LEFT = 14
    RIGHT = 15
    OK = 20
    HOME = 21
    MENU = 22
    BACK = 23
    VOLUME_UP = 24
    VOLUME_DOWN = 25
    MUTE = 26
    CHANNEL_UP = 27
    CHANNEL_DOWN = 28
    BLUE = 29
    GREEN = 30
    RED = 31
    YELLOW = 32
    PLAY = 33
    PAUSE = 34
    STOP = 35
    FF = 36
    REW = 37
    SKIP_FF = 38
    SKIP_REW = 39
    REC = 40
    REC_LIST = 41
    LIVE = 43
    EPG = 44
    INFO = 45
    ASPECT = 46
    EXT = 47
    PIP = 48
    SUBTITLE = 49
    PROGRAM_LIST = 50
    TEXT = 51
    MARK = 52
    _3D = 400
    _3D_LR = 401
    DASH = 402
    PREV = 403
    FAV = 404
    QUICK_MENU = 405
    TEXT_OPTION = 406
    AUDIO_DESC = 407
    NETCAST = 408
    ENERGY_SAVE = 409
    AV = 410
    SIMPLINK = 411
    EXIT = 412
    RESERVE = 413
    PIP_CHANNEL_UP = 414
    PIP_CHANNEL_DOWN = 415
    PIP_SWITCH = 416
    APPS = 417


if __name__ == "__main__":
    opts = None

    try:
        opts, args = getopt.getopt(sys.argv[1:], "ha:p:c:", [
                                   "address=", "pairing-key=", "command="])
    except getopt.GetoptError:
        pass

    address = None
    pairingkey = None
    command = None
    command_code = None

    for opt, arg in opts:
        if opt == '-h':
            print('lgtvremote.py -a <address> -p <pairing-key> -c <command>')
            exit()
        elif opt in ("-a", "--address"):
            address = arg
        elif opt in ("-p", "--pairing-key"):
            pairingkey = arg
        elif opt in ("-c", "--command"):
            command = arg

    if not pairingkey:
        print('No pairing key given\nWill just request one without any command invoked')

    elif not command:
        print('No command given')
        exit(1)

    else:

        try:
            command_code = int(command)
        except ValueError:
            try:
                command_code = vars(LGTVRemote)[command]
            except KeyError:
                print('Command not available')
                exit(1)

    try:
        if not address:
            address = LGTVRemote.discover_tv()
            print('Found LG TV at {0}'.format(address))

        lgtv = LGTVRemote(address, pairingkey)
        if pairingkey:
            lgtv.send_command(command_code)

    except LGTVRemote.WrongPairingKeyError:
        print('Wrong pairing key')
        exit(1)

    except LGTVRemote.CommunicationError:
        print('TV returned an error')
        exit(1)

    except LGTVRemote.TimeoutError:
        print('TV not responding')
        exit(1)

    except LGTVRemote.NoTVFoundError:
        print('No LG TV found')
        exit(1)

    except LGTVRemote.AddressMissingError:
        print('No IP address given')
        exit(1)
