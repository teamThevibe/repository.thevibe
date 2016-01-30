# -*- coding: utf-8 -*-
#------------------------------------------------------------
# http://www.youtube.com/user/GoProCamera
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Based on code from youtube addon
#------------------------------------------------------------

import os
import sys
import plugintools
import xbmc
import xbmcgui
import json

start_index = 1
amount = 30
cats = []


def add_cat(name, playlist_id):
	plugintools.add_item( action="main_list" , title=name , url="?pid=" + playlist_id + "&start-index=1&max-results=30" ,thumbnail="" , folder=True )
	cats.append(playlist_id);

# Entry point
def run():
	plugintools.log("UCHaEhu1lOjCfHSHg_R2dpkg.run")
	
	# Get params
	params = plugintools.get_params()
	
	if params.get("action") is None:
		category_list(params)
	elif params.get("action")=="main_list":
		main_list(params)
	else:
		plugintools.log("ACTION: " + params.get("action"))
		action = params.get("action")
		exec action + "(params)"
	
	plugintools.close_item_list()

def play_playlist(params):
	xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play(playlist)
	
	
# Categories
def category_list(params):
	add_cat("הופעות חיות", "PLFw7KwIWHNB0xJHalTpCNNzbKX_FzTdjR")
	add_cat("בדיקה", "PLtKp7FTU0JD4JkXQKTsgzubBgZanCaKXp")
	

playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
page_playlist = []
	
# Main menu
def main_list(params):
	global page_playlist
	plugintools.log("UCHaEhu1lOjCfHSHg_R2dpkg.main_list "+repr(params))
	
	# On first page, pagination parameters are fixed
	if params.get("url") is not None:
		pid = plugintools.find_single_match( params.get("url") ,"pid=(.+?)&")
		pageToken = plugintools.find_single_match( params.get("url") ,"pageToken=(.+)")
		max_results = plugintools.find_single_match( params.get("url") ,"max-results=(\d+)")

		p_url = "https://www.googleapis.com/youtube/v3/playlistItems?pageToken=" + pageToken + "&part=snippet,status&maxResults=" + max_results + "&playlistId=" + pid + "&key=AIzaSyDl9siqp_kPJ0WQelU20VaolNn2PKkTeeY"
		#p_url = "http://gdata.youtube.com/feeds/api/playlists/"+pid+"/?start-index=" + start_index + "&max-results=" + max_results
		plugintools.log("MYPID "+p_url)
		
# Fetch video list from YouTube feed
	data = plugintools.read( p_url )

	# Extract items from feed
	pattern = ""
	matches = plugintools.find_multiple_matches(data,"<entry>(.*?)</entry>")
	
	#"kind": "youtube#playlistItem"
	
	plugintools.add_item( action="play_playlist" , title="נגן את כל הפלייליסט" , url="", folder=False )	

	playlist.clear()
	
	parsed_json = json.loads(data)
	
	next_page_token = None
	try:
		next_page_token = parsed_json["nextPageToken"]
	except KeyError:
		next_page_token = None
		
	results = parsed_json["items"]
	#plugintools.log("LIST LENGTH: "+str(len(results)))
	
	for result in results:
		if result["status"]["privacyStatus"] != "public":
			continue
		
		try:
			# Not the better way to parse XML, but clean and easy
			title = result["snippet"]["title"]
			plot = result["snippet"]["description"]
			thumbnail = result["snippet"]["thumbnails"]["default"]["url"]
			video_id = result["snippet"]["resourceId"]["videoId"]
			
			
			
			url = "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid="+video_id

			liz = xbmcgui.ListItem(title, iconImage=thumbnail, thumbnailImage=thumbnail)
			liz.setInfo( type="Video", infoLabels={ "Title": title} )
			liz.setProperty("IsPlayable","true")
			playlist.add(url,liz)
			
			# Appends a new item to the xbmc item list
			plugintools.add_item( action="play" , title=title , plot=plot , url=url ,thumbnail=thumbnail , folder=True )
		except KeyError:
			continue
	
	# Calculates next page URL from actual URL
	if next_page_token is not None:
		if params.get("url") is not None:
			next_page_url = "?pid=" + pid + "&max-results=" + max_results + "&pageToken=" + next_page_token
			plugintools.add_item( action="main_list" , title="<< עמוד הבא" , url=next_page_url.decode().encode('utf-8'), folder=True )	

def play(params):
	plugintools.play_resolved_url( params.get("url") )

run()