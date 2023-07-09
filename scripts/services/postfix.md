
# http://www.postfix.org/VIRTUAL_README.html#virtual_mailbox
# https://help.ubuntu.com/community/PostfixVirtualMailBoxClamSmtpHowto
# http://wiki2.dovecot.org/HowTo/VirtualUserFlatFilesPostfix
# http://www.mailscanner.info/ubuntu.html



apt-get install dovecot-core dovecot-imapd dovecot-pop3d dovecot-lmtpd dovecot-sieve dovecot-managesieved

echo 'mail_location = maildir:~/Maildir
mail_plugins = quota
auth_username_format = %n
service lmtp {
 unix_listener /var/spool/postfix/private/dovecot-lmtp {
   group = postfix
   mode = 0600
   user = postfix
  }
}' > /etc/dovecot/local.conf


cat > /etc/apt/sources.list.d/mailscanner.list << 'EOF'
deb http://apt.baruwa.org/debian wheezy main
deb-src http://apt.baruwa.org/debian wheezy main
EOF

wget -O - http://apt.baruwa.org/baruwa-apt-keys.gpg | apt-key add -

apt-get update
apt-get install mailscanner



apt-get install postfix
echo 'home_mailbox = Maildir/' >> /etc/postfix/main.cf
echo 'mailbox_transport = lmtp:unix:private/dovecot-lmtp' >> /etc/postfix/main.cf




/etc/init.d/dovecot restart
/etc/init.d/postfix restart

# TODO check postfix and dovecot configs

# TODO crontab that deletes message +30 days on spam folders
