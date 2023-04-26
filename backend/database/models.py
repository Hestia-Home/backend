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
    reader_sensors = relationship("ReadSensor", back_populates="station")
    control_sensors = relationship("ControlSensor", back_populates="station")

    def __repr__(self):
        return f"User Subject: id={self.id!r}, name={self.name!r}, user_id={self.user_id!r}"


class ReadSensor(Base):
    __tablename__ = "read_sensor"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    data = Column(String)
    time = Column(TIMESTAMP, default=datetime.utcnow)
    status = Column(Boolean, default=False)
    station_id = Column(Integer, ForeignKey("station.id"))

    station = relationship("Station", back_populates="reader_sensors")

    def __repr__(self):
        return f"Reader Sensor: name={self.name!r}, time={self.time!r}, status={self.status!r}"


class ControlSensor(Base):
    __tablename__ = "control_sensor"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    data = Column(String)
    time = Column(TIMESTAMP, default=datetime.utcnow)
    status = Column(Boolean, default=False)
    station_id = Column(Integer, ForeignKey("station.id"))

    station = relationship("Station", back_populates="control_sensors")

    def __repr__(self):
        return f"Control Sensor: name={self.name!r}, time={self.time!r}, status={self.status!r}"
