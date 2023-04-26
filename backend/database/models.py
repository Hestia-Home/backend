from datetime import datetime

from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, ForeignKey, LargeBinary
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

metadata = Base.metadata


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    username = Column(String(30), nullable=False)
    create_at = Column(TIMESTAMP, default=datetime.utcnow)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    user_type = Column(Integer, ForeignKey("user_category.id"))

    user_category = relationship("UserCategory", back_populates="users")
    stations = relationship("Station", back_populates="user")

    def __repr__(self):
        return f"User(id={self.id!r}, username={self.username!r}, email={self.email!r})"


class UserCategory(Base):
    __tablename__ = "user_category"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)

    users = relationship("User", back_populates="user_category")

    def __repr__(self):
        return f"User Category: id={self.id!r}, name={self.name!r}"


class Station(Base):
    __tablename__ = "station"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)

    user = relationship("User", back_populates="stations")
    sensors = relationship("Sensor", back_populates="station")

    def __repr__(self):
        return f"Station: id={self.id!r}, name={self.name!r}, user_id={self.user_id!r}"


class Sensor(Base):
    __tablename__ = "sensor"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    sensor_type = Column(Integer, ForeignKey("sensor_types.id"))
    data = Column(String)
    command = Column(String)
    time = Column(TIMESTAMP, default=datetime.utcnow)
    status = Column(Boolean, default=False)
    station_id = Column(Integer, ForeignKey("station.id"))

    sensor_types = relationship("SensorTypes", back_populates="sensors")
    station = relationship("Station", back_populates="sensors")

    def __repr__(self):
        return f"Sensor: name={self.name!r}, time={self.time!r}, status={self.status!r}"


class SensorTypes(Base):
    __tablename__ = "sensor_types"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)

    sensors = relationship("Sensor", back_populates="sensor_types")

    def __repr__(self):
        return f"Sensor Types: id={self.id!r}, name={self.name!r}"