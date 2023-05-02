from . import CONN, CURSOR
import ipdb

class Song:

    def __init__ ( self, name, album ) :
        self.id = None
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
        return song[0] if song else 'Could not find that record.'
    
    def save ( self ) :
        # sql = """
        #     insert into songs ( name, album )
        #     values ( ?, ? )
        # """
        # CURSOR.execute( sql, ( self.name, self.album ) )
        CURSOR.execute( f"insert into songs ( name, album ) values ( '{ self.name }', '{ self.album }' )" )
        self.id = CURSOR.execute( 'select last_insert_rowid() from songs' ).fetchone()[0]
        return Song.find( self.id )

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
        
        if type( song ) == dict :
            for key in attributes:
                if song[key] and key is not 'id' :
                    self[key] = attributes[key]
            CURSOR.execute( f"update songs set name = '{ self.name }', album = '{ self.album }' where id = { self.id }; " )
            updated_song = Song.find( self.id )
            return updated_song
        else :
            return song




