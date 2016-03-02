#!/usr/bin/python
import urllib, sys, os
import xbmcaddon, xbmcplugin, xbmcgui
import updatesetting, sync
from xbmc import translatePath, executebuiltin, getInfoLabel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'resources'))
from pyga.ga import track_event, track_page

addonID = "plugin.video.thewiz.wall"
Addon = xbmcaddon.Addon(addonID)
AddonName = Addon.getAddonInfo("name")
pluginhandle = int(sys.argv[1])

def getParams(arg):
	param=[]
	paramstring=arg
	if len(paramstring)>=2:
		params=arg
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:    
				param[splitparams[0]]=splitparams[1]
							
	return param

def getParam(name,params):
	try:
		return urllib.unquote_plus(params[name])
	except:
		pass

def PlayUrl(url):
	item = xbmcgui.ListItem(
		path=url,
		label=xbmc.getInfoLabel("ListItem.Label"),
		label2=xbmc.getInfoLabel("ListItem.Label2"),
		thumbnailImage=xbmc.getInfoLabel("ListItem.Art(thumb)"),
		iconImage=xbmc.getInfoLabel("ListItem.Art(thumb)")
		)
	_infoLabels = {
		"Title": xbmc.getInfoLabel("ListItem.Title"),
		"OriginalTitle": xbmc.getInfoLabel("ListItem.OriginalTitle"),
		"TVShowTitle": xbmc.getInfoLabel("ListItem.TVShowTitle"),
		"Season": xbmc.getInfoLabel("ListItem.Season"),
		"Episode": xbmc.getInfoLabel("ListItem.Episode"),
		"Premiered": xbmc.getInfoLabel("ListItem.Premiered"),
		"Plot": xbmc.getInfoLabel("ListItem.Plot"),
		# "Date": xbmc.getInfoLabel("ListItem.Date"),
		"VideoCodec": xbmc.getInfoLabel("ListItem.VideoCodec"),
		"VideoResolution": xbmc.getInfoLabel("ListItem.VideoResolution"),
		"VideoAspect": xbmc.getInfoLabel("ListItem.VideoAspect"),
		"DBID": xbmc.getInfoLabel("ListItem.DBID"),
		"DBTYPE": xbmc.getInfoLabel("ListItem.DBTYPE"),
		"Writer": xbmc.getInfoLabel("ListItem.Writer"),
		"Director": xbmc.getInfoLabel("ListItem.Director"),
		"Rating": xbmc.getInfoLabel("ListItem.Rating"),
		"Votes": xbmc.getInfoLabel("ListItem.Votes"),
		}
	infoLabels = {}
	for key, value in _infoLabels.iteritems():
		if value:
			infoLabels[key] = value

	poster = xbmc.getInfoLabel("ListItem.Art(poster)")
	if not poster:
		poster = xbmc.getInfoLabel("ListItem.Art(tvshow.poster)")

	item.setArt({
		"poster": poster,
		"banner": xbmc.getInfoLabel("ListItem.Art(banner)"),
		"fanart": xbmc.getInfoLabel("ListItem.Art(fanart)")
		})
	print "******* ART label:{0} t:{1}".format(xbmc.getInfoLabel("ListItem.Label"),xbmc.getInfoLabel("ListItem.Art(thumb)"))
	item.setInfo(type='Video', infoLabels=infoLabels)
	item.setProperty("IsPlayable", "true")
	xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=item)
	xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=False)
	xbmcplugin.endOfDirectory(handle=int(sys.argv[1]))
	xbmc.Player().play(url, item)
	return

wall=None
action=None
if len(sys.argv) >= 2:   
	params = getParams(sys.argv[2])
	wall=getParam("wall", params)
	action=getParam("action", params)
	
streamAddonMV = Addon.getSetting("StreamMovies")
streamAddonTV = Addon.getSetting("StreamTV")

if wall is None:
	Addon.openSettings()
	updatesetting.main()
elif (wall == "update"):
	sync.main()
elif (action == "player"):
	imdb = getParam("imdb",params)
	print "*** {0}: Wall.Player {1} {2}".format(AddonName,wall,imdb)
	
	streamAddonMV = "Quasar"
	streamAddonTV = "Quasar"
	
if (wall == "movies"):
	imdb = getParam("imdb",params)
	trakt = getParam("trakt",params)
	year = getParam("year",params)
	name = getParam("name",params)
	title = getParam("title",params)
	url = getParam("url",params)
	slug = getParam("slug",params)

	directPlay = Addon.getSetting("DirectPlay")

	if (streamAddonMV=="Exodus"):
		stream ='plugin://plugin.video.exodus/?action=play&imdb={0}&meta={1}&year={2}&title={3}'.format(imdb,urllib.quote('{"thumb":"%s","code": "%s","originaltitle": "%s"}' % (xbmc.getInfoLabel("ListItem.Art(thumb)"),imdb,title),safe=''),year,title.replace(' ','%20'))
	if (streamAddonMV=="Pulsar"):
		if (directPlay=="false"):
			stream ="plugin://plugin.video.pulsar/movie/{0}/play".format(imdb)
		else:
			stream ="plugin://plugin.video.pulsar/movie/{0}/links".format(imdb)
	if (streamAddonMV=="Quasar"):
		if (directPlay=="false"):
			stream ="plugin://plugin.video.quasar/movie/{0}/play".format(imdb)
		else:
			stream ="plugin://plugin.video.quasar/movie/{0}/links".format(imdb)
	if (streamAddonMV=="SALTS"):
		stream ="plugin://plugin.video.salts/?trakt_id={0}&dialog=True&mode=get_sources&video_type=Movie&title={1}&year={2}&slug={3}".format(trakt,title.replace(' ','+'),year,slug)
	if (streamAddonMV=="UMP"):
		stream ='plugin://plugin.program.ump/?info={"code": "'+format(imdb)+'","originaltitle": "'+title.replace(' ','%20')+'","title": "'+title.replace(' ','%20')+'"}&args={}&module=imdb&content_type=video&page=urlselect'
	PlayUrl(stream)
	print "*** {0}: Wall.Play: Movie({1} - {2}) {3} {4}:{5}".format(AddonName,imdb,title,streamAddonMV,name,stream)
	track_event("movie", "play", title.replace("+", " "), streamAddonMV)
	track_page("/movie"+"/{0} ({1})/{2}".format(title.replace("+", " "),year,streamAddonMV))
	
if (wall == "tv"):
	date = getParam("date",params)
	episode = getParam("episode",params)
	trakt = getParam("trakt",params)
	genre = getParam("genre",params)
	imdb = getParam("imdb",params)
	name = getParam("name",params)
	season = getParam("season",params)
	show = getParam("show",params)
	title = getParam("title",params)
	tvdb = getParam("tvdb",params)
	tmdb = getParam("tmdb",params)
	year = getParam("year",params)
	#title_salts = getParam("title_salts",params)
	year = getParam("year",params)
	slug = getParam("slug",params)
	
	directPlay = Addon.getSetting("DirectPlay")

	if (streamAddonTV=="Exodus"):
		stream ='plugin://plugin.video.exodus/?action=play&imdb={0}&meta={1}&year={2}&title={3}&season={4}&episode={5}&tvshowtitle={6}&tvdb={7}'.format(imdb,urllib.quote('{"thumb":"%s","code": "%s","imdb":"%s","tvshowtitle": "%s","tvdb":"%s","year":"%s","season":"%s","episode":"%s"}' % (xbmc.getInfoLabel("ListItem.Art(thumb)"),imdb,imdb,title,tvdb,year,season,episode),safe=''),year,title.replace(' ','%20'),season,episode,title,tvdb)
	if (streamAddonTV=="Pulsar"):
		if (directPlay=="false"):
			stream ="plugin://plugin.video.pulsar/show/{0}/season/{1}/episode/{2}/play".format(tvdb,season,episode)
		else:
			stream ="plugin://plugin.video.pulsar/show/{0}/season/{1}/episode/{2}/links".format(tvdb,season,episode)
	if (streamAddonTV=="Quasar"):
		if (directPlay=="false"):
			stream ="plugin://plugin.video.quasar/show/{0}/season/{1}/episode/{2}/play".format(tmdb,season,episode)
		else:
			stream ="plugin://plugin.video.quasar/show/{0}/season/{1}/episode/{2}/links".format(tmdb,season,episode)
	if (streamAddonTV=="SALTS"):
		stream ="plugin://plugin.video.salts/?ep_airdate=2012-05-14&episode={0}&dialog=True&title={1}&ep_title=NULL&season={2}&video_type=Episode&mode=get_sources&year={3}&trakt_id={4}".format(episode,title,season,year,trakt)
 
	PlayUrl(stream) 	
	print "*** {0}: Wall.Play: TV({1} - {2}) {3} {4}".format(AddonName,tvdb,name,streamAddonTV,stream)
	track_event("tv", "play", name.replace("+", " ") ,streamAddonTV)
	track_page('/tv/{0}/S{1}/E{2}/{3}'.format(show.replace("+", " "),str(season).zfill(2),str(episode).zfill(2),streamAddonTV))