import datetime

from flask_login import UserMixin
from flask_bcrypt import generate_password_hash
from peewee import *

DATABASE = SqliteDatabase( 'social.db' )

class User( UserMixin, Model ):
    username = CharField( unique = True )
    email = CharField( unique = True )
    password = CharField( max_length = 120 )
    joined_at = DateTimeField( default = datetime.datetime.now )

    class Meta:
        database = DATABASE
        order_by = ( "-joined_at", )

    def get_post( self ):
        return Post.select().where( Post.user == self )

    def get_stream( self ):
        return Post.select().where( ( Post.user << self.following() ) | ( Post.user == self ) )

    def following( self ):
        """ Los usuarios que estamos siguiendo """
        return (
            User.select().join( Relationship, on = Relationship.to_user ).where(  Relationship.from_user == self )
        )

    def followers( self ):
        """ Obtener los uausrios que me siguen """
        return (
            User.select().join( Relationship, on = Relationship.from_user ).where(  Relationship.to_user == self )
        )
    
    @classmethod
    def create_user( cls, username, email, password ) : 
        try:
            with DATABASE.transaction():
                cls.create( username = username, email = email, password = generate_password_hash( password ) )
        except IntegrityError:
            raise ValueError( 'User already exist' )

class Post( Model ):
    user = ForeignKeyField( User, related_name = 'posts' )
    timestamp = DateTimeField( default = datetime.datetime.now )
    content = TextField()

    class Meta:
        database = DATABASE
        order_by = ( "-joined_at", )

class Relationship( Model ):
    from_user = ForeignKeyField( User, related_name = "repationships" )
    to_user = ForeignKeyField( User, related_name = "related_to" )

    class Meta:
        database = DATABASE
        indexes = ( ( ( 'from_user', 'to_user' ), True ), )
        


def initialize():
    DATABASE.connect()
    DATABASE.create_tables( [ User, Post, Relationship ] , safe = True)
    DATABASE.close()