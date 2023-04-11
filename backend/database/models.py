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
    subjects = relationship("UserSubject", back_populates="user")

    def __repr__(self):
        return f"User(id={self.id!r}, username={self.username!r}, email={self.email!r})"


class UserCategory(Base):
    __tablename__ = "user_category"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)

    users = relationship("User", back_populates="user_category")

    def __repr__(self):
        return f"User Category: id={self.id!r}, name={self.name!r}"


class UserSubject(Base):
    __tablename__ = "user_subject"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)

    user = relationship("User", back_populates="subjects")
    reader_devices = relationship("ReaderDevice", back_populates="subject")
    control_devices = relationship("ControlDevice", back_populates="subject")

    def __repr__(self):
        return f"User Subject: id={self.id!r}, name={self.name!r}, user_id={self.user_id!r}"


class ReaderDevice(Base):
    __tablename__ = "reader_device"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    subject_id = Column(Integer, ForeignKey("user_subject.id"))

    subject = relationship("UserSubject", back_populates="reader_devices")
    sensors = relationship("ReadSensor", back_populates="reader_device")

    def __repr__(self):
        return f"Reader Device: id={self.id!r}, name={self.name!r}, subject_id={self.subject_id!r}"


class ControlDevice(Base):
    __tablename__ = "control_device"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    subject_id = Column(Integer, ForeignKey("user_subject.id"))

    subject = relationship("UserSubject", back_populates="control_devices")
    sensors = relationship("ControlSensor", back_populates="control_device")

    def __repr__(self):
        return f"Control Device: id={self.id!r}, name={self.name!r}, subject_id={self.subject_id!r}"


class ReadSensor(Base):
    __tablename__ = "read_sensor"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    data = Column(LargeBinary)
    time = Column(TIMESTAMP, default=datetime.utcnow)
    status = Column(Boolean, default=False)
    device_id = Column(Integer, ForeignKey("reader_device.id"))

    reader_device = relationship("ReaderDevice", back_populates="sensors")

    def __repr__(self):
        return f"Reader Device: name={self.name!r}, time={self.time!r}, status={self.status!r}"


class ControlSensor(Base):
    __tablename__ = "control_sensor"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    data = Column(LargeBinary)
    time = Column(TIMESTAMP, default=datetime.utcnow)
    status = Column(Boolean, default=False)
    device_id = Column(Integer, ForeignKey("control_device.id"))

    control_device = relationship("ControlDevice", back_populates="sensors")

    def __repr__(self):
        return f"Control Device: name={self.name!r}, time={self.time!r}, status={self.status!r}"
