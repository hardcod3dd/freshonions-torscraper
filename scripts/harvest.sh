#!/bin/sh
DIR=$( cd "$(dirname "$0")" ; pwd -P )
. $DIR/env.sh
LIST=`mktemp`
LIST2=`mktemp`
TOR2WEB_JSON=`mktemp`
http_proxy="" https_proxy="" wget --no-check-certificate -O $TOR2WEB_JSON https://eqt5g4fuenphqinx.tor2web.org/antanistaticmap/stats/yesterday
$SCRIPTDIR/import_tor2web.py $TOR2WEB_JSON > $LIST
rm "$TOR2WEB_JSON"
#$SCRIPTDIR/extract_from_url.sh 'https://onion.cab/list.php?a=list' >> $LIST
$SCRIPTDIR/extract_from_url.sh 'https://www.reddit.com/r/onions/search?q=url%3A.onion&sort=new&restrict_sr=on' >> $LIST
$SCRIPTDIR/extract_from_url.sh 'https://ahmia.fi/address/' >> $LIST
$SCRIPTDIR/extract_from_url.sh 'https://www.deepdotweb.com/2013/10/28/updated-llist-of-hidden-marketplaces-tor-i2p/' >> $LIST
$SCRIPTDIR/extract_from_url.sh 'https://darkwebnews.com/deep-web-links/' >> $LIST
$SCRIPTDIR/extract_from_url.sh 'https://raw.githubusercontent.com/alecmuffett/onion-sites-that-dont-suck/master/README.md' >> $LIST
$SCRIPTDIR/extract_from_url.sh 'https://en.wikipedia.org/wiki/List_of_Tor_hidden_services' >> $LIST
#$SCRIPTDIR/extract_from_url.sh 'https://www.reddit.com/r/HiddenService/' >> $LIST
#$SCRIPTDIR/extract_from_url.sh 'https://www.reddit.com/r/darknetmarkets/wiki/superlist.json' >> $LIST
$SCRIPTDIR/tor_extract_from_url.sh 'http://tt3j2x4k5ycaa5zt.onion/onions.php?format=text' >> $LIST
$SCRIPTDIR/tor_extract_from_url.sh 'http://skunksworkedp2cg.onion/sites.html' >> $LIST
$SCRIPTDIR/tor_extract_from_url.sh 'http://visitorfi5kl7q7i.onion/onions/' >> $LIST
$SCRIPTDIR/tor_extract_from_url.sh 'http://underdj5ziov3ic7.onion/crawler/index.php?online=1' >> $LIST
$SCRIPTDIR/tor_extract_from_url.sh 'http://7cbqhjnlkivmigxf.onion/' >> $LIST
$SCRIPTDIR/tor_extract_from_url.sh 'http://frwikisfa6myvgyx.onion/index.php?title=Accueil' >> $LIST
$SCRIPTDIR/tor_extract_from_url.sh 'http://7rmath4ro2of2a42.onion' >> $LIST
$SCRIPTDIR/tor_extract_from_url.sh 'http://oxwugzccvk3dk6tj.onion' >> $LIST
$SCRIPTDIR/tor_extract_from_url.sh 'http://oxwugzccvk3dk6tj.onion' >> $LIST
$SCRIPTDIR/tor_extract_from_url.sh 'http://answerszuvs3gg2l64e6hmnryudl5zgrmwm3vh65hzszdghblddvfiqd.onion' >> $LIST
$SCRIPTDIR/tor_extract_from_url.sh 'http://ujnkg4uirpaiqejr.onion/doku.php' >> $LIST
$SCRIPTDIR/purify.sh $LIST > $LIST2
NUMBER=`wc -l $LIST2 | tr -s ' ' | cut -f 1 -d ' '`
echo "Harvested $NUMBER onion links..."
$SCRIPTDIR/push_list.sh $LIST2
rm $LIST $LIST2
