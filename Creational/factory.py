import json
import xml.etree.ElementTree as et

from typing import Type


class SerializerInterface:
    def start_object(self, object_name: str, object_id: str):
        raise NotImplemented

    def add_property(self, name: str, value: str):
        raise NotImplemented

    def to_str(self):
        raise NotImplemented


class JsonSerializer(SerializerInterface):
    def __init__(self):
        self._current_object = None

    def start_object(self, object_name: str, object_id: str):
        self._current_object = {'id': object_id}

    def add_property(self, name: str, value: str):
        self._current_object[name] = value

    def to_str(self):
        return json.dumps(self._current_object)


class XmlSerializer(SerializerInterface):
    def __init__(self):
        self._element = None

    def start_object(self, object_name: str, object_id: str):
        self._element = et.Element(object_name, attrib={'id': object_id})

    def add_property(self, name: str, value: str):
        prop = et.SubElement(self._element, name)
        prop.text = value

    def to_str(self):
        return et.tostring(self._element, encoding='unicode')


class SerializerFactory:
    def __init__(self):
        self._creators = {}

    def register_format(self, format_: str, creator: Type[SerializerInterface]):
        self._creators[format_] = creator

    def get_serializer(self, format_: str) -> SerializerInterface:
        creator = self._creators.get(format_)
        if not creator:
            raise ValueError(format_)
        return creator()


factory = SerializerFactory()

factory.register_format('JSON', JsonSerializer)
factory.register_format('XML', XmlSerializer)


class SerializableInterface:
    def serialize(self, serializer: SerializerInterface):
        raise NotImplemented


class ObjectSerializer:
    @staticmethod
    def serialize(serializable: SerializableInterface, format_: str):
        serializer = factory.get_serializer(format_)
        serializable.serialize(serializer)
        return serializer.to_str()


class Song(SerializableInterface):
    def __init__(self, song_id: str, title: str, artist: str):
        self.song_id = song_id
        self.title = title
        self.artist = artist

    def serialize(self, serializer: SerializerInterface):
        serializer.start_object('song', self.song_id)
        serializer.add_property('title', self.title)
        serializer.add_property('artist', self.artist)


song = Song('1', 'Horse', 'Author')

print(ObjectSerializer.serialize(song, 'JSON'))

print(ObjectSerializer.serialize(song, 'XML'))

print(ObjectSerializer.serialize(song, 'some'))
