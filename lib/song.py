from typing import Any
from . import CONN, CURSOR
import ipdb

class Song:

    def __init__ ( self, name, album, id=None ) :
        self.id = id
        self.name = name
        self.album = album
    
    @classmethod
    def create_table ( self ) :
        sql = """
            CREATE TABLE IF NOT EXISTS songs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                album TEXT
            )
        """
        CURSOR.execute( sql )

    global song_into_dict
    def song_into_dict ( song ) :
        return dict( id = song[0], name = song[1], album = song[2] )
    
    @classmethod
    def all ( self ) :
        songs = CURSOR.execute( 'select * from songs' )
        return [ song_into_dict( song ) for song in songs ]

    @classmethod
    def find( self, id ) :
        songs = CURSOR.execute( f'select * from songs where id = {id} ' )
        song = [ song_into_dict( song ) for song in songs ]
        song_instance = Song( name = song[0]['name'], album = song[0]['album'], id = song[0]['id'] )
        return song_instance if song else 'Could not find that record.'
    
    def save ( self ) :
        # sql = """
        #     insert into songs ( name, album )
        #     values ( ?, ? )
        # """
        # CURSOR.execute( sql, ( self.name, self.album ) )
        CURSOR.execute( f"insert into songs ( name, album ) values ( '{ self.name }', '{ self.album }' )" )
        self.id = CURSOR.execute( 'select last_insert_rowid() from songs' ).fetchone()[0]
        return self

    @classmethod
    def create ( cls, name, album ) :
        song = Song( name, album )
        return song.save()
    
    @classmethod
    def destroy ( cls, id ) :
        song = Song.find( id )
        if type( song ) == dict :
            CURSOR.execute( 'delete from songs where id = {}'.format( song['id'] ) )
            return 'Song with id {} was deleted.'.format( song['id'] )
        else :
            return song
        
    # update doesn't work right now for some reason
    def update ( self, **attributes ) :
        song = Song.find( self.id )
        if song and type( song ) == Song :
            for key in attributes:
                if song.__getattribute__( key ) and key is not 'id' :
                    setattr( self, key, attributes[key] )
            CURSOR.execute( f"update songs set name = '{ self.name }', album = '{ self.album }' where id = { self.id }; " )
            updated_song = Song.find( self.id )
            return updated_song
        else :
            return song

