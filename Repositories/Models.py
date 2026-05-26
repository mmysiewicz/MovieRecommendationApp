from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# Tabele asocjacyjne

Movie_Genre = Table("Movie_Genre",
                    Base.metadata,
                    Column("Movie_Id", Integer, ForeignKey("Movie.Id"), primary_key=True),
                    Column("Genre_id", Integer, ForeignKey("Genre.Id"), primary_key=True)
                    )

Movie_Country = Table("Movie_Country",
                      Base.metadata,
                      Column("Movie_Id", Integer, ForeignKey("Movie.Id"), primary_key=True),
                      Column("Country_id", Integer, ForeignKey("Country.Id"), primary_key=True)
                      )

Rate = Table("Rate",
             Base.metadata,
             Column("Movie_Id", Integer, ForeignKey("Movie.Id"), primary_key=True),
            Column("User_id", Integer, ForeignKey("User.Id"), primary_key=True),
             Column("Score", Integer))

# Tabele

class User(Base):
    __tablename__ = "User"
    Id = Column(Integer, primary_key=True)
    Login = Column(String(50))
    Password = Column(String(50))

    Movies = relationship("Movie", secondary=Rate, back_populates="Users")


class Movie(Base):
    __tablename__ = "Movie"
    Id = Column(Integer, primary_key=True)
    Title = Column(String(50))
    Description = Column(String)

    Genres = relationship("Genre", secondary=Movie_Genre, back_populates="Movies")
    Countries = relationship("Country", secondary=Movie_Country, back_populates="Movies")
    Users = relationship("User", secondary=Rate, back_populates="Movies")

    MoviePersons = relationship("MoviePerson", back_populates="Movie")


class Genre(Base):
    __tablename__ = "Genre"
    Id = Column(Integer, primary_key=True)
    Name = Column(String(50))

    Movies = relationship("Movie", secondary = Movie_Genre, back_populates="Genres")


class Country(Base):
    __tablename__ = "Country"
    Id = Column(Integer, primary_key=True)
    Name = Column(String(50))

    Movies = relationship("Movie", secondary = Movie_Country, back_populates="Countries")


class Person(Base):
    __tablename__ = "Person"
    Id = Column(Integer, primary_key=True)
    Firstname = Column(String(50))
    Surname = Column(String(50))

    MoviePersons = relationship("Movie", back_populates="Person")


class Role(Base):
    __tablename__ = "Role"
    Id = Column(Integer, primary_key=True)
    Name = Column(String(50))

    MoviePersons = relationship("MoviePerson", back_populates="Role")


# Tabela asocjacyjna z polem:

class MoviePerson(Base):
    __tablename__ = "Movie_Person"

    Movie_Id = Column(Integer, ForeignKey("Movie.Id"), primary_key=True)
    Person_id = Column(Integer, ForeignKey("Person.Id"), primary_key=True)
    Role_id = Column(Integer, ForeignKey("Role.Id"))

    Movie = relationship("Movie", back_populates="MoviePersons")
    Person = relationship("Person", back_populates="MoviePersons")
    Role = relationship("Role", back_populates="MoviePersons")


