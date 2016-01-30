import os, shutil, re, unicodedata
import xbmc, xbmcgui, xbmcaddon, xbmcvfs
if sys.version_info < (2, 7):
    import simplejson
else:
    import json as simplejson

ADDON = xbmcaddon.Addon()
ADDONID = ADDON.getAddonInfo('id')
ADDONNAME = ADDON.getAddonInfo('name')
ADDONVERSION = ADDON.getAddonInfo('version')
LANGUAGE = ADDON.getLocalizedString

def log(txt):
    if isinstance (txt,str):
        txt = txt.decode("utf-8")
    message = u'%s: %s' % (ADDONID, txt)
    xbmc.log(msg=message.encode("utf-8"), level=xbmc.LOGDEBUG)

def clean_filename(filename):
    illegal_char = '^<>:"/\|?*'
    for char in illegal_char:
        filename = filename.replace( char , '' )
    return filename

class Main:
    def __init__ ( self ):
        self._load_settings()
        self._init_variables()
        self._delete_directories()
        self._create_directories()
        if self.directoriescreated == 'true':
            self._copy_artwork()

    def _load_settings( self ):
        self.moviefanart = ADDON.getSetting( "moviefanart" )
        self.tvshowfanart = ADDON.getSetting( "tvshowfanart" )
        self.musicvideofanart = ADDON.getSetting( "musicvideofanart" )
        self.artistfanart = ADDON.getSetting( "artistfanart" )
        self.moviethumbs = ADDON.getSetting( "moviethumbs" )
        self.tvshowbanners = ADDON.getSetting( "tvshowbanners" )
        self.tvshowposters = ADDON.getSetting( "tvshowposters" )
        self.seasonthumbs = ADDON.getSetting( "seasonthumbs" )
        self.episodethumbs = ADDON.getSetting( "episodethumbs" )
        self.musicvideothumbs = ADDON.getSetting( "musicvideothumbs" )
        self.artistthumbs = ADDON.getSetting( "artistthumbs" )
        self.albumthumbs = ADDON.getSetting( "albumthumbs" )
        self.source = ADDON.getSetting( "source" )
        if self.source == 'true':
            self.path = ADDON.getSetting( "path" ).decode("utf-8")
        else:
            self.path = ''
        self.directory = ADDON.getSetting( "directory" ).decode("utf-8")

    def _init_variables( self ):
        self.moviefanartdir = 'MovieFanart'
        self.tvshowfanartdir = 'TVShowFanart'
        self.musicvideofanartdir = 'MusicVideoFanart'
        self.artistfanartdir = 'ArtistFanart'
        self.moviethumbsdir = 'MovieThumbs'
        self.tvshowbannersdir = 'TVShowBanners'
        self.tvshowpostersdir = 'TVShowPosters'
        self.seasonthumbsdir = 'SeasonThumbs'
        self.episodethumbsdir = 'EpisodeThumbs'
        self.musicvideothumbsdir = 'MusicVideoThumbs'
        self.artistthumbsdir = 'ArtistThumbs'
        self.albumthumbsdir = 'AlbumThumbs'
        self.directoriescreated = 'true'
        self.dialog = xbmcgui.DialogProgress()
        if self.directory == '':
            self.directory = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('profile')).decode('utf-8')
        if self.path != '':
            path = os.path.split( os.path.dirname( self.path ) )[1]
            self.directory = os.path.join( self.directory, path )
        self.artworklist = []
        if self.moviefanart == 'true':
            self.moviefanartpath = os.path.join( self.directory, self.moviefanartdir )
            self.artworklist.append( self.moviefanartpath )
        if self.tvshowfanart == 'true':
            self.tvshowfanartpath = os.path.join( self.directory, self.tvshowfanartdir )
            self.artworklist.append( self.tvshowfanartpath )
        if self.musicvideofanart == 'true':
            self.musicvideofanartpath = os.path.join( self.directory, self.musicvideofanartdir )
            self.artworklist.append( self.musicvideofanartpath )
        if self.artistfanart == 'true':
            self.artistfanartpath = os.path.join( self.directory, self.artistfanartdir )
            self.artworklist.append( self.artistfanartpath )
        if self.moviethumbs == 'true':
            self.moviethumbspath = os.path.join( self.directory, self.moviethumbsdir )
            self.artworklist.append( self.moviethumbspath )
        if self.tvshowbanners == 'true':
            self.tvshowbannerspath = os.path.join( self.directory, self.tvshowbannersdir )
            self.artworklist.append( self.tvshowbannerspath )
        if self.tvshowposters == 'true':
            self.tvshowposterspath = os.path.join( self.directory, self.tvshowpostersdir )
            self.artworklist.append( self.tvshowposterspath )
        if self.seasonthumbs == 'true':
            self.seasonthumbspath = os.path.join( self.directory, self.seasonthumbsdir )
            self.artworklist.append( self.seasonthumbspath )
        if self.episodethumbs == 'true':
            self.episodethumbspath = os.path.join( self.directory, self.episodethumbsdir )
            self.artworklist.append( self.episodethumbspath )
        if self.musicvideothumbs == 'true':
            self.musicvideothumbspath = os.path.join( self.directory, self.musicvideothumbsdir )
            self.artworklist.append( self.musicvideothumbspath )
        if self.artistthumbs == 'true':
            self.artistthumbspath = os.path.join( self.directory, self.artistthumbsdir )
            self.artworklist.append( self.artistthumbspath )
        if self.albumthumbs == 'true':
            self.albumthumbspath = os.path.join( self.directory, self.albumthumbsdir )
            self.artworklist.append( self.albumthumbspath )

    def _delete_directories( self ):
        if xbmcvfs.exists( self.directory ):
            dirs, files = xbmcvfs.listdir( self.directory )
            for item in dirs:
                try:
                    shutil.rmtree( os.path.join(self.directory, item) )
                except:
                    pass

    def _create_directories( self ):
        if not xbmcvfs.exists( self.directory ):
            try:
                xbmcvfs.mkdir( self.directory )
            except:
                self.directoriescreated = 'false'
                log( 'failed to create artwork directory' )
        if self.directoriescreated == 'true':
            for path in self.artworklist:
                try:
                    xbmcvfs.mkdir( path )
                except:
                    self.directoriescreated = 'false'
                    log( 'failed to create directories' )

    def _copy_artwork( self ):
        self.dialog.create( ADDONNAME )
        self.dialog.update(0)
        if not self.dialog.iscanceled():
            if self.moviefanart == 'true':
                self._copy_moviefanart()
        if not self.dialog.iscanceled():
            if self.tvshowfanart == 'true':
                self._copy_tvshowfanart()
        if not self.dialog.iscanceled():
            if self.musicvideofanart == 'true':
                self._copy_musicvideofanart()
        if not self.dialog.iscanceled():
            if (self.artistfanart == 'true') and (self.path == ''):
                self._copy_artistfanart()
        if not self.dialog.iscanceled():
            if self.moviethumbs == 'true':
                self._copy_moviethumbs()
        if not self.dialog.iscanceled():
            if self.tvshowbanners == 'true':
                self._copy_tvshowbanners()
        if not self.dialog.iscanceled():
            if self.tvshowposters == 'true':
                self._copy_tvshowposters()
        if not self.dialog.iscanceled():
            if self.seasonthumbs == 'true':
                self._copy_seasonthumbs()
        if not self.dialog.iscanceled():
            if self.episodethumbs == 'true':
                self._copy_episodethumbs()
        if not self.dialog.iscanceled():
            if self.musicvideothumbs == 'true':
                self._copy_musicvideothumbs()
        if not self.dialog.iscanceled():
            if (self.artistthumbs == 'true') and (self.path == ''):
                self._copy_artistthumbs()
        if not self.dialog.iscanceled():
            if (self.albumthumbs == 'true') and (self.path == ''):
                self._copy_albumthumbs()
        self.dialog.close()

    def _copy_moviefanart( self ):
        count = 0
        processeditems = 0
        json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"properties": ["file", "title", "fanart", "year"], "filter": {"field": "path", "operator": "contains", "value": "%s"}}, "id": 1}' % self.path)
        json_query = unicode(json_query, 'utf-8', errors='ignore')
        json_response = simplejson.loads(json_query)
        if json_response.has_key('result') and (json_response['result'] != None) and (json_response['result'].has_key('movies')):
            totalitems = len( json_response['result']['movies'] )
            for item in json_response['result']['movies']:
                if self.dialog.iscanceled():
                    log('script cancelled')
                    return
                processeditems = processeditems + 1
                self.dialog.update( int( float( processeditems ) / float( totalitems ) * 100), LANGUAGE(32001) + ': ' + str( count + 1 ) )
                name = item['title']
                year = str(item['year'])
                artwork = item['fanart']
                tmp_filename = name + ' (' + year + ')' + '.jpg'
                filename = clean_filename( tmp_filename )
                if artwork != '':
                    try:
                        xbmcvfs.copy( xbmc.translatePath( artwork ), os.path.join( self.moviefanartpath, filename ) )
                        count += 1
                    except:
                        log( 'failed to copy moviefanart' )
        log( 'moviefanart copied: %s' % count )

    def _copy_tvshowfanart( self ):
        count = 0
        processeditems = 0
        json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "params": {"properties": ["title", "fanart"], "filter": {"field": "path", "operator": "contains", "value": "%s"}}, "id": 1}' % self.path)
        json_query = unicode(json_query, 'utf-8', errors='ignore')
        json_response = simplejson.loads(json_query)
        if json_response.has_key('result') and (json_response['result'] != None) and (json_response['result'].has_key('tvshows')):
            totalitems = len( json_response['result']['tvshows'] )
            for item in json_response['result']['tvshows']:
                if self.dialog.iscanceled():
                    log('script cancelled')
                    return
                processeditems = processeditems + 1
                self.dialog.update( int( float( processeditems ) / float( totalitems ) * 100), LANGUAGE(32002) + ': ' + str( count + 1 ) )
                name = item['title']
                artwork = item['fanart']
                tmp_filename = name + '.jpg'
                filename = clean_filename( tmp_filename )
                if artwork != '':
                    try:
                        xbmcvfs.copy( xbmc.translatePath( artwork ), os.path.join( self.tvshowfanartpath, filename ) )
                        count += 1
                    except:
                        log( 'failed to copy tvshowfanart' )
        log( 'tvshowfanart copied: %s' % count )

    def _copy_musicvideofanart( self ):
        count = 0
        processeditems = 0
        json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMusicVideos", "params": {"properties": ["title", "fanart", "artist"], "filter": {"field": "path", "operator": "contains", "value": "%s"}}, "id": 1}' % self.path)
        json_query = unicode(json_query, 'utf-8', errors='ignore')
        json_response = simplejson.loads(json_query)
        if json_response.has_key('result') and (json_response['result'] != None) and (json_response['result'].has_key('musicvideos')):
            totalitems = len( json_response['result']['musicvideos'] )
            for item in json_response['result']['musicvideos']:
                if self.dialog.iscanceled():
                    log('script cancelled')
                    return
                processeditems = processeditems + 1
                self.dialog.update( int( float( processeditems ) / float( totalitems ) * 100), LANGUAGE(32003) + ': ' + str( count + 1 ) )
                name = item['title']
                artwork = item['fanart']
                if item['artist']: # bug workaround, musicvideos can end up in the database without an artistname
                    artist = item['artist'][0]
                    tmp_filename = artist + ' - ' + name + '.jpg'
                else:
                    tmp_filename = name + '.jpg'
                filename = clean_filename( tmp_filename )
                if artwork != '':
                    try:
                        xbmcvfs.copy( xbmc.translatePath( artwork ), os.path.join( self.musicvideofanartpath, filename ) )
                        count += 1
                    except:
                        log( 'failed to copy musicvideofanart' )
        log( 'musicvideofanart copied: %s' % count )

    def _copy_artistfanart( self ):
        count = 0
        processeditems = 0
        json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "AudioLibrary.GetArtists", "params": {"properties": ["fanart"]}, "id": 1}')
        json_query = unicode(json_query, 'utf-8', errors='ignore')
        json_response = simplejson.loads(json_query)
        if json_response.has_key('result') and (json_response['result'] != None) and (json_response['result'].has_key('artists')):
            totalitems = len( json_response['result']['artists'] )
            for item in json_response['result']['artists']:
                if self.dialog.iscanceled():
                    log('script cancelled')
                    return
                processeditems = processeditems + 1
                self.dialog.update( int( float( processeditems ) / float( totalitems ) * 100), LANGUAGE(32004) + ': ' + str( count + 1 ) )
                name = item['label']
                artwork = item['fanart']
                tmp_filename = name + '.jpg'
                filename = clean_filename( tmp_filename )
                if artwork != '':
                    try:
                        xbmcvfs.copy( xbmc.translatePath( artwork ), os.path.join( self.artistfanartpath, filename ) )
                        count += 1
                    except:
                        log( 'failed to copy artistfanart' )
        log( 'artistfanart copied: %s' % count )

    def _copy_moviethumbs( self ):
        count = 0
        processeditems = 0
        json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"properties": ["title", "thumbnail", "year"], "filter": {"field": "path", "operator": "contains", "value": "%s"}}, "id": 1}' % self.path)
        json_query = unicode(json_query, 'utf-8', errors='ignore')
        json_response = simplejson.loads(json_query)
        if json_response.has_key('result') and (json_response['result'] != None) and (json_response['result'].has_key('movies')):
            totalitems = len( json_response['result']['movies'] )
            for item in json_response['result']['movies']:
                if self.dialog.iscanceled():
                    log('script cancelled')
                    return
                processeditems = processeditems + 1
                self.dialog.update( int( float( processeditems ) / float( totalitems ) * 100), LANGUAGE(32005) + ': ' + str( count + 1 ) )
                name = item['title']
                year = str(item['year'])
                artwork = item['thumbnail']
                tmp_filename = name + ' (' + year + ')' + '.jpg'
                filename = clean_filename( tmp_filename )
                if artwork != '':
                    try:
                        xbmcvfs.copy( xbmc.translatePath( artwork ), os.path.join( self.moviethumbspath, filename ) )
                        count += 1
                    except:
                        log( 'failed to copy moviethumb' )
        log( 'moviethumbs copied: %s' % count )

    def _copy_tvshowbanners( self ):
        count = 0
        processeditems = 0
        json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "params": {"properties": ["title", "art"], "filter": {"field": "path", "operator": "contains", "value": "%s"}}, "id": 1}' % self.path)
        json_query = unicode(json_query, 'utf-8', errors='ignore')
        json_response = simplejson.loads(json_query)
        if json_response.has_key('result') and (json_response['result'] != None) and (json_response['result'].has_key('tvshows')):
            totalitems = len( json_response['result']['tvshows'] )
            for item in json_response['result']['tvshows']:
                if self.dialog.iscanceled():
                    log('script cancelled')
                    return
                processeditems = processeditems + 1
                self.dialog.update( int( float( processeditems ) / float( totalitems ) * 100), LANGUAGE(32013) + ': ' + str( count + 1 ) )
                name = item['title']
                artwork = item['art'].get('banner')
                tmp_filename = name + '.jpg'
                filename = clean_filename( tmp_filename )
                if artwork != '':
                    try:
                        xbmcvfs.copy( xbmc.translatePath( artwork ), os.path.join( self.tvshowbannerspath, filename ) )
                        count += 1
                    except:
                        log( 'failed to copy tvshowbanner' )
        log( 'tvshowbanners copied: %s' % count )

    def _copy_tvshowposters( self ):
        count = 0
        processeditems = 0
        json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "params": {"properties": ["title", "art"], "filter": {"field": "path", "operator": "contains", "value": "%s"}}, "id": 1}' % self.path)
        json_query = unicode(json_query, 'utf-8', errors='ignore')
        json_response = simplejson.loads(json_query)
        if json_response.has_key('result') and (json_response['result'] != None) and (json_response['result'].has_key('tvshows')):
            totalitems = len( json_response['result']['tvshows'] )
            for item in json_response['result']['tvshows']:
                if self.dialog.iscanceled():
                    log('script cancelled')
                    return
                processeditems = processeditems + 1
                self.dialog.update( int( float( processeditems ) / float( totalitems ) * 100), LANGUAGE(32014) + ': ' + str( count + 1 ) )
                name = item['title']
                artwork = item['art'].get('poster')
                tmp_filename = name + '.jpg'
                filename = clean_filename( tmp_filename )
                if artwork != '':
                    try:
                        xbmcvfs.copy( xbmc.translatePath( artwork ), os.path.join( self.tvshowposterspath, filename ) )
                        count += 1
                    except:
                        log( 'failed to copy tvshowposter' )
        log( 'tvshowposters copied: %s' % count )

    def _copy_seasonthumbs( self ):
        count = 0
        tvshowids = []
        json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "params": {"filter": {"field": "path", "operator": "contains", "value": "%s"}}, "id": 1}' % self.path)
        json_query = unicode(json_query, 'utf-8', errors='ignore')
        json_response = simplejson.loads(json_query)
        if json_response.has_key('result') and (json_response['result'] != None) and (json_response['result'].has_key('tvshows')):
            for item in json_response['result']['tvshows']:
                if self.dialog.iscanceled():
                    log('script cancelled')
                    return
                tvshowid = item['tvshowid']
                tvshowids.append(tvshowid)
            for tvshowid in tvshowids:
                processeditems = 0
                json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetSeasons", "params": {"properties": ["thumbnail", "showtitle"], "tvshowid":%s}, "id": 1}' % tvshowid)
                json_query = unicode(json_query, 'utf-8', errors='ignore')
                json_response = simplejson.loads(json_query)
                if json_response.has_key('result') and (json_response['result'] != None) and (json_response['result'].has_key('seasons')):
                    totalitems = len( json_response['result']['seasons'] )
                    for item in json_response['result']['seasons']:
                        if self.dialog.iscanceled():
                            log('script cancelled')
                            return
                        processeditems = processeditems + 1
                        self.dialog.update( int( float( processeditems ) / float( totalitems ) * 100), LANGUAGE(32007) + ': ' + str( count + 1 ) )
                        name = item['label']
                        tvshow = item['showtitle']
                        artwork = item['thumbnail']
                        tmp_filename = tvshow + ' - ' + name + '.jpg'
                        filename = clean_filename( tmp_filename )
                        if artwork != '':
                            try:
                                xbmcvfs.copy( xbmc.translatePath( artwork ), os.path.join( self.seasonthumbspath, filename ) )
                                count += 1
                            except:
                                log( 'failed to copy seasonthumb' )
        log( 'seasonthumbs copied: %s' % count )

    def _copy_episodethumbs( self ):
        count = 0
        processeditems = 0
        json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": {"properties": ["title", "thumbnail", "season", "episode", "showtitle"], "filter": {"field": "path", "operator": "contains", "value": "%s"}}, "id": 1}' % self.path)
        json_query = unicode(json_query, 'utf-8', errors='ignore')
        json_response = simplejson.loads(json_query)
        if json_response.has_key('result') and (json_response['result'] != None) and (json_response['result'].has_key('episodes')):
            totalitems = len( json_response['result']['episodes'] )
            for item in json_response['result']['episodes']:
                if self.dialog.iscanceled():
                    log('script cancelled')
                    return
                processeditems = processeditems + 1
                self.dialog.update( int( float( processeditems ) / float( totalitems ) * 100), LANGUAGE(32008) + ': ' + str( count + 1 ) )
                name = item['title']
                tvshow = item['showtitle']
                artwork = item['thumbnail']
                season = item['season']
                episode = item['episode']
                episodenumber = "s%.2d%.2d" % (int( season ), int( episode ))
                tmp_filename = tvshow + ' - ' + episodenumber + ' - ' + name + '.jpg'
                filename = clean_filename( tmp_filename )
                if artwork != '':
                    try:
                        xbmcvfs.copy( xbmc.translatePath( artwork ), os.path.join( self.episodethumbspath, filename ) )
                        count += 1
                    except:
                        log( 'failed to copy episodethumb' )
        log( 'episodethumbs copied: %s' % count )

    def _copy_musicvideothumbs( self ):
        count = 0
        processeditems = 0
        json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMusicVideos", "params": {"properties": ["title", "thumbnail", "artist"], "filter": {"field": "path", "operator": "contains", "value": "%s"}}, "id": 1}' % self.path)
        json_query = unicode(json_query, 'utf-8', errors='ignore')
        json_response = simplejson.loads(json_query)
        if json_response.has_key('result') and (json_response['result'] != None) and (json_response['result'].has_key('musicvideos')):
            totalitems = len( json_response['result']['musicvideos'] )
            for item in json_response['result']['musicvideos']:
                if self.dialog.iscanceled():
                    log('script cancelled')
                    return
                processeditems = processeditems + 1
                self.dialog.update( int( float( processeditems ) / float( totalitems ) * 100), LANGUAGE(32009) + ': ' + str( count + 1 ) )
                name = item['title']
                artwork = item['thumbnail']
                if item['artist']: # bug workaround, musicvideos can end up in the database without an artistname
                    artist = item['artist'][0]
                    tmp_filename = artist + ' - ' + name + '.jpg'
                else:
                    tmp_filename = name + '.jpg'
                filename = clean_filename( tmp_filename )
                if artwork != '':
                    try:
                        xbmcvfs.copy( xbmc.translatePath( artwork ), os.path.join( self.musicvideothumbspath, filename ) )
                        count += 1
                    except:
                        log( 'failed to copy musicvideothumb' )
        log( 'musicvideothumbs copied: %s' % count )

    def _copy_artistthumbs( self ):
        count = 0
        processeditems = 0
        json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "AudioLibrary.GetArtists", "params": {"properties": ["thumbnail"]}, "id": 1}')
        json_query = unicode(json_query, 'utf-8', errors='ignore')
        json_response = simplejson.loads(json_query)
        if json_response.has_key('result') and (json_response['result'] != None) and (json_response['result'].has_key('artists')):
            totalitems = len( json_response['result']['artists'] )
            for item in json_response['result']['artists']:
                if self.dialog.iscanceled():
                    log('script cancelled')
                    return
                processeditems = processeditems + 1
                self.dialog.update( int( float( processeditems ) / float( totalitems ) * 100), LANGUAGE(32010) + ': ' + str( count + 1 ) )
                name = item['label']
                artwork = item['thumbnail']
                tmp_filename = name + '.jpg'
                filename = clean_filename( tmp_filename )
                if artwork != '':
                    try:
                        xbmcvfs.copy( xbmc.translatePath( artwork ), os.path.join( self.artistthumbspath, filename ) )
                        count += 1
                    except:
                        log( 'failed to copy artistthumb' )
        log( 'artistthumbs copied: %s' % count )

    def _copy_albumthumbs( self ):
        count = 0
        processeditems = 0
        json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "AudioLibrary.GetAlbums", "params": {"properties": ["title", "thumbnail", "artist"]}, "id": 1}')
        json_query = unicode(json_query, 'utf-8', errors='ignore')
        json_response = simplejson.loads(json_query)
        if json_response.has_key('result') and (json_response['result'] != None) and (json_response['result'].has_key('albums')):
            totalitems = len( json_response['result']['albums'] )
            for item in json_response['result']['albums']:
                if self.dialog.iscanceled():
                    log('script cancelled')
                    return
                processeditems = processeditems + 1
                self.dialog.update( int( float( processeditems ) / float( totalitems ) * 100), LANGUAGE(32011) + ': ' + str( count + 1 ) )
                name = item['title']
                artist = item['artist'][0]
                artwork = item['thumbnail']
                tmp_filename = artist + ' - ' + name + '.jpg'
                filename = clean_filename( tmp_filename )
                if artwork != '':
                    try:
                        xbmcvfs.copy( xbmc.translatePath( artwork ), os.path.join( self.albumthumbspath, filename ) )
                        count += 1
                    except:
                        log( 'failed to copy albumthumb' )
        log( 'albumthumbs copied: %s' % count )

if ( __name__ == "__main__" ):
    log('script version %s started' % ADDONVERSION)
    Main()
log('script stopped')
