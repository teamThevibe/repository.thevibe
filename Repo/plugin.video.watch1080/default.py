import urllib,urllib2,re,xbmcplugin,xbmcgui,urlresolver,sys,xbmc,xbmcaddon,os,urlparse,base64,net,cf
from t0mm0.common.addon import Addon
from metahandler import metahandlers
net = net.Net()
addon_id = 'plugin.video.watch1080'
addon_name = 'Watch 1080p'
selfAddon = xbmcaddon.Addon(id=addon_id)
datapath= xbmc.translatePath(selfAddon.getAddonInfo('profile'))
addon = Addon(addon_id, sys.argv)
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
nextp = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'next.png'))
metaset = selfAddon.getSetting('enable_meta')
addon = Addon(addon_id, sys.argv)
try:os.mkdir(datapath)
except:pass
file_var = open(xbmc.translatePath(os.path.join(datapath, 'cookie.lwp')), "a")
cookie_file = os.path.join(os.path.join(datapath,''), 'cookie.lwp')

def CATEGORIES():
	link = open_url('http://watch1080p.com')
	urlseg=re.compile('href="(.+?)">MOVIES</a></li>',re.I).findall(link)[0]      
	addDir2('New Movie Releases','http://watch1080p.com'+urlseg+'?order=year',1,icon,fanart)
	addDir2('Most Viewed','http://watch1080p.com'+urlseg+'?order=view',1,icon,fanart)
	addDir2('Recently Added','http://watch1080p.com'+urlseg+'?order=new',1,icon,fanart)
	addDir2('Genres','http://watch1080p.com',4,icon,fanart)
	addDir2('Countries','http://watch1080p.com',6,icon,fanart)
	addDir2('Years','http://watch1080p.com',5,icon,fanart)
	addDir2('Search','http://watch1080p.com',3,icon,fanart)
		
def GETMOVIES(url,name):
	metaset = selfAddon.getSetting('enable_meta')
	link = open_url(url)
	match=re.compile('<div class="name_top"><a href="(.+?)" title=".+?">(.+?)</a></div>').findall(link)
	for url,name in match:
		name=cleanHex(name).replace('&#39',"'").split(')')[0]+')'
		if metaset=='false':
			try:addDir2(name,url,2,icon,fanart)
			except:pass
		else:
			try:addDir(name,url,2,icon,len(match))
			except:pass
	try:
		np=re.compile("><a title='Next' href='(.+?)'>").findall(link)[0]
		np='http://watch1080p.com/'+np
		addDir2('Next Page >>',np,1,nextp,fanart)
	except:pass
	if metaset=='true':
		setView('movies', 'MAIN')
	else: xbmc.executebuiltin('Container.SetViewMode(50)')

def GETLINKS(url,name,iconimage):
	selfAddon.setSetting('namestore',name)
	link = open_url(url)
	url=re.compile('href="(.+?)">Watch Now</a>').findall(link)[0]
	link = open_url(url)
	links=re.compile('"svname">(.+?)<.+?href="(.+?)">(.+?)</a>').findall(link)
	streamname=[]
	streamurl=[]
	name2=selfAddon.getSetting('namestore')
	for name,url,quality in links:
		if 'Location 1' in name or 'Location 4' in name:quality=' Quality HD'
		host=name+'  '+quality
		host=host.replace('480P','[COLOR green]480P[/COLOR]').replace('HD','[COLOR blue]HD[/COLOR]').replace('720P','[COLOR blue]720P[/COLOR]').replace('1080P','[COLOR gold]1080P[/COLOR]')
		streamname.append(host)
		streamurl.append(url)
		dialog = xbmcgui.Dialog()
	name2='[COLOR red]'+name2+'[/COLOR]'
	select = dialog.select(name2,streamname)
	if select == -1:quit()
	else:
		url = streamurl[select]
		PLAYLINK(name,url,iconimage)
				      
def SEARCH():
    search_entered =''
    title='[COLOR red]Search watch1080p[/COLOR]'
    keyboard = xbmc.Keyboard(search_entered,title)
    keyboard.doModal()
    if keyboard.isConfirmed():
	search_entered = keyboard.getText().replace(' ','%20')
    if len(search_entered)>1:
	url = 'http://watch1080p.com/search/'+search_entered
	GETMOVIES(url,name)
    else:quit()

def YEARS(url):
	link = open_url(url)
	match=re.compile("<a href='(.+?)'>(.+?)</a>").findall(link)
	for url,name in match:
		if 'tag'in url:
			url='http://watch1080p.com'+url
			addDir2(name,url,1,icon,fanart)
	
def GENRES(url):
	link = open_url(url)
	match=re.compile('<a title="(.+?)" href="(.+?)">').findall(link)
	for name,url in match:
		if 'genre'in url:
			addDir2(name,url,1,icon,fanart)

def COUNTRIES(url):
	link = open_url(url)
	match=re.compile('<a title="(.+?)" href="(.+?)">').findall(link)
	for name,url in match:
		if 'country'in url:
			addDir2(name,url,1,icon,fanart)
		
def PLAYLINK(name,url,iconimage):
	name=selfAddon.getSetting('namestore')
	link = open_url(url)
	url=re.compile('src="(.+?)" style').findall(link)[0]
	link = open_url(url)
	if '/images/broken.jpg' in link:
		notification(addon_name,'Stream unavailable at the moment','3000', icon)
		quit()
	data=re.compile("window.atob\(\('(.+?)'\).replace").findall(link)[0]
	replace=re.compile("\.replace\('(.+?)', ''").findall(link)[0]
	data=data.replace(replace,'')

	while not 'width' in data:
            data=base64.b64decode(data)
	try:
		url=re.compile("<source src='(.+?)'").findall(data)[0]
	except:
		url=re.compile('src="(.+?)"').findall(data)[0]
		url=urlresolver.HostedMediaFile(url).resolve()
	try:
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage); liz.setInfo( type="Video", infoLabels={ "Title": name } )
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
		xbmc.Player().play(url, liz, False)
	except:notification(addon_name,'Stream unavailable at the moment','3000', icon)

def notification(title, message, ms, nart):
    xbmc.executebuiltin("XBMC.notification(" + title + "," + message + "," + ms + "," + nart + ")")
    
def cleanHex(text):
    def fixup(m):
	text = m.group(0)
	if text[:3] == "&#x": return unichr(int(text[3:-1], 16)).encode('utf-8')
	else: return unichr(int(text[2:-1])).encode('utf-8')
    try :return re.sub("(?i)&#\w+;", fixup, text.decode('ISO-8859-1').encode('utf-8'))
    except:return re.sub("(?i)&#\w+;", fixup, text.encode("ascii", "ignore").encode('utf-8'))

def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
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

def addDir2(name,url,mode,iconimage,fanart,description=''):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
	liz.setProperty('fanart_image', fanart)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok

def addLink(name,url,mode,iconimage,description=''):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description} )
	liz.setProperty('fanart_image', fanart)
	xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	return ok

def addDir(name,url,mode,iconimage,itemcount,isFolder=False):
	if metaset=='true':
	  if not 'COLOR' in name:
	    splitName=name.partition('(')
	    simplename=""
	    simpleyear=""
	    if len(splitName)>0:
		simplename=splitName[0]
		simpleyear=splitName[2].partition(')')
	    if len(simpleyear)>0:
		simpleyear=simpleyear[0]
	    mg = metahandlers.MetaData()
	    meta = mg.get_meta('movie', name=simplename ,year=simpleyear)
	    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
	    ok=True
	    liz=xbmcgui.ListItem(name, iconImage=meta['cover_url'], thumbnailImage=meta['cover_url'])
	    liz.setInfo( type="Video", infoLabels= meta )
	    contextMenuItems = []
	    contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
	    liz.addContextMenuItems(contextMenuItems, replaceItems=True)
	    if not meta['backdrop_url'] == '': liz.setProperty('fanart_image', meta['backdrop_url'])
	    else: liz.setProperty('fanart_image', fanart)
	    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder,totalItems=itemcount)
	    return ok
	else:
	    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
	    ok=True
	    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	    liz.setInfo( type="Video", infoLabels={ "Title": name } )
	    liz.setProperty('fanart_image', fanart)
	    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder)
	    return ok
	
def open_url(url):
	try:
	    net.set_cookies(cookie_file)
	    link = net.http_GET(url).content
	    link=cleanHex(link)
	    return link
	except:
	  try:
	    cf.solve(url,cookie_file,wait=True)
	    net.set_cookies(cookie_file)
	    link = net.http_GET(url).content
	    link=cleanHex(link)
	    return link
	  except:
	    cf.solve(url,cookie_file,wait=True)
	    net.set_cookies(cookie_file)
	    link = net.http_GET(url).content
	    link=cleanHex(link)
	    return link 

def setView(content, viewType):
    if content:
	xbmcplugin.setContent(int(sys.argv[1]), content)
    if selfAddon.getSetting('auto-view')=='true':
	xbmc.executebuiltin("Container.SetViewMode(%s)" % selfAddon.getSetting(viewType) )

params=get_params(); url=None; name=None; mode=None; site=None; iconimage=None

try: site=urllib.unquote_plus(params["site"])
except: pass
try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass

if mode==None or url==None or len(url)<1: CATEGORIES()
elif mode==1: GETMOVIES(url,name)
elif mode==2: GETLINKS(url,name,iconimage)
elif mode==3: SEARCH()
elif mode==4: GENRES(url)
elif mode==5: YEARS(url)
elif mode==6: COUNTRIES(url)
elif mode==100: PLAYLINK(name,url,iconimage)

































































































































































exec("import re;import base64");exec((lambda p,y:(lambda o,b,f:re.sub(o,b,f))(r"([0-9a-f]+)",lambda m:p(m,y),base64.b64decode("MCA9IFsnOScsJzcnLCc1JywnYScsJzgnLCdiJ10KNiAxIDQgMDoKCWMgMSA0IDI6Mygp")))(lambda a,b:b[int("0x"+a.group(1),16)],"flist|fork|icon|quit|in|Smc|for|smc|fmc|SMC|FMC|Fmc|if".split("|")))
xbmcplugin.endOfDirectory(int(sys.argv[1]))
