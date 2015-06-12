Example #1 assuming you are using SIP application; the below will basically create a counter for SIP registration traffic and will block the client temporary based on the number of failed attempts; i.e last rule is basically if the client made 3 registration failure attempts under 60 seconds block him;
 
    iptables -A INPUT -p udp --dport 5060 -i eth0 -m state --state NEW -m recent --set 
    iptables -A INPUT -p udp --dport 5060 -i eth0 -m state --state NEW -m recent --rcheck --seconds 600 --hitcount 20 -j DROP 
    iptables -A INPUT -p udp --dport 5060 -i eth0 -m state --state NEW -m recent --rcheck --seconds 300 --hitcount 10 -j DROP
    iptables -A INPUT -p udp --dport 5060 -i eth0 -m state --state NEW -m recent --rcheck --seconds 180 --hitcount 5 -j DROP
    iptables -A INPUT -p udp --dport 5060 -i eth0 -m state --state NEW -m recent --rcheck --seconds 60 --hitcount 3 -j DROP
 
Example #2; assuming that you are running a public web server on your instance; the below will set a counter for HTTP traffic and will block any client with more than 20 attempts in under 60 seconds.
 
    iptables -A INPUT -i eth0 -p tcp --dport 80 -m state --state NEW -m recent --set --name HTTP; 
    iptables -A INPUT -i eth0 -p tcp --dport 80 -m state --state NEW -m recent --update \
                --seconds 60 --hitcount 20 --rttl --name HTTP -j DROP
 
3- Use a software like “Fail2ban” a free open source software, which will automatically create IPtables rules to block IPs based on the volume of the traffic coming from a specific source;
 
Fail2ban website;
[www.fail2ban.org/wiki/index.php/Main_Page](www.fail2ban.org/wiki/index.php/Main_Page "www.fail2ban.org")
