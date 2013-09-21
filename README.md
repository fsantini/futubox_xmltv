futubox_xmltv
=============

Downloading EPG for Futubox streaming service
This program downloads the Electronic Program Guide (EPG) information from the Futubox website and formats them in the XMLTV format to be read by (for example) XBMC.

Requirements:

This program requires a working Python installation (tested with v2.7), python-lxml and python-urllib2.

Configuration:

The program needs to read from the two csv files included in the distribution. You can modify the paths to these files and to the output xml file directly from the futubox_xmltv.py program

Usage:

As a first step, you need to prepare the futubox playlist. Make sure to DISABLE parental control in your futubox settings and then download the m3u playlist as described in the Futubox FAQ here: http://futuboxhd.com/faq/ . If you don't want adult channels you can still remove them from the playlist AFTER the conversion.

Run the script futubox_convert_playlist.py in order to prepare the playlist correctly with the following syntax
  python futubox_convert_playlist.py <original_playlist.m3u> <output_playlist.m3u>

Run the futubox_xmltv.py script:
  python futubox_xmltv.py

This script will generate a futubox_guide.xml file.

If you are using XBMC with IPTVSimple plugin, configure the plugin to read the channels from the converted m3u and the EPG from the futubox_guide.xml file.

Known problems:

Ths futubox_xmltv.py script needs to be executed every day, because Futubox only provides channel information one day at a time. You can either run it manually or automate it with a cron job.

The IPTVSimple plugin has troubles displaying the EPG timeline after midnight. I think this is a bug of the plugin.