from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Float, VARCHAR, SmallInteger
from sqlalchemy import ForeignKey

db_string = "postgresql://postgres:31427183108@localhost:5432/lab12"
engine = create_engine(db_string)
Base = declarative_base()


# class Author(Base):
#     __tablename__ = "authors"
#     id = Column(Integer, primary_key=True)
#     name = Column(String(50))
#     surname = Column(String(50))
#     born_name = Column(Date)
#
#     def __repr__(self):
#         return "<authors(id='{0}', name={1}, surname={2}, born_date={3})>".format(
#             self.id, self.name, self.surnamey, self.born_date)


class Users(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    email = Column(String(50))

    def __repr__(self):
        return "<users(id='{0}', email={1}>".format(
            self.id, self.email)


class Hosts(Base):
    __tablename__ = "hosts"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    def __repr__(self):
        return "<hosts(id='{0}', user_id={1}>".format(
            self.id, self.user_id)


class Bookings(Base):
    __tablename__ = "bookings"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    place_id = Column(Integer, ForeignKey('places.id'))
    start_date = Column(Date)
    end_date = Column(Date)
    price_per_night = Column(Float)

    def __repr__(self):
        return "<bookings(id='{0}', user_id={1},  place_id={2},  start_date={3},  end_date={4},  price_per_night={5},>".format(
            self.id, self.user_id, self.place_id, self.start_date, self.end_date, self.price_per_night)


class Reviews(Base):
    __tablename__ = "reviews"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey('bookings.id'))
    rating = Column(SmallInteger)
    review_body = Column(String(200))

    def __repr__(self):
        return "<reviews(id='{0}', booking_id={1}, rating={2}, review_body={3})>".format(
            self.id, self.booking_id, self.rating, self.review_body)


class Places(Base):
    __tablename__ = "places"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    host_id = Column(Integer, ForeignKey('hosts.id'))
    address = Column(String(50))
    city_id = Column(Integer, ForeignKey('cities.id'))

    def __repr__(self):
        return "<places(id='{0}', name={1}, surname={2}, born_date={3})>".format(
            self.id, self.host_id, self.address, self.city_id)


class Cities(Base):
    __tablename__ = "cities"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    country_id = Column(Integer, ForeignKey('countries.id'))

    def __repr__(self):
        return "<cities(id='{0}', name={1}, country_id={2}>".format(
            self.id, self.name, self.country_id)


class Countries(Base):
    __tablename__ = "countries"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    country_code = Column(String(50))
    name = Column(String(50))

    def __repr__(self):
        return "<countries(id='{0}', country_code={1}, name={2})>".format(
            self.id, self.country_code, self.name)

# Base.metadata.create_all(engine)
