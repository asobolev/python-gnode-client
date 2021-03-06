# Python G-Node Client
#
# Copyright (C) 2013  A. Stoewer
#                     A. Sobolev
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License (see LICENSE.txt).

from __future__ import print_function, absolute_import, division

import gnodeclient.util.declarative_models as dc
from gnodeclient.model.model_fields import Field, FQuantity, FDatafile, FParent, FChildren


class Model(dc.Model):
    """
    A base class for all defined models, that also provides some factory methods as well as some
    constants for all model names.

    Example:
    >>> signal = Model.create(Model.ANALOGSIGNAL)
    >>> signal.id = "id"
    """

    DOCUMENT = "document"
    SECTION = "section"
    PROPERTY = "property"
    VALUE = "value"
    BLOCK = "block"
    SEGMENT = "segment"
    EVENTARRAY = "eventarray"
    EVENT = "event"
    EPOCHARRAY = "epocharray"
    EPOCH = "epoch"
    RECORDINGCHANNELGROUP = "recordingchannelgroup"
    RECORDINGCHANNEL = "recordingchannel"
    UNIT = "unit"
    SPIKETRAIN = "spiketrain"
    SPIKE = "spike"
    ANALOGSIGNALARRAY = "analogsignalarray"
    ANALOGSIGNAL = "analogsignal"
    IRREGULARLYSAMPLEDSIGNAL = "irregularlysampledsignal"

    _MODEL_MAP = {}

    @classmethod
    def create(cls, type_name):
        """
        Creates an instance of the model class matching the type name.

        :param type_name: The name of the model class.

        :returns: An instance of the respective model class.
        :rtype: Model
        """
        return cls._MODEL_MAP[type_name]()

    @classmethod
    def exists(cls, type_name):
        """
        Check if a model name exists.

        :param type_name: The name of the model type.

        :returns: True if the model exists, False otherwise.
        :rtype: bool
        """
        return type_name in cls._MODEL_MAP

    @classmethod
    def get_location(cls, type_name):
        """
        Get the location prefix for a certain type.

        :param type_name: The name of the model type.

        :returns: The location prefix.
        :rtype: str
        """
        if type_name in (cls.DOCUMENT, cls.SECTION, cls.PROPERTY, cls.VALUE):
            return "/api/v1/metadata/" + type_name + "/"
        else:
            return "/api/v1/electrophysiology/" + type_name + "/"

    #
    # Fields
    #

    id          = Field(field_type=str)
    guid        = Field(field_type=str)
    resource_uri= Field(field_type=str)
    location    = Field(field_type=str)
    model       = Field(field_type=str)


class DocumentModel(Model):
    model       = Field(field_type=str, default=Model.DOCUMENT)
    author      = Field(field_type=str)
    date        = Field(field_type=str)
    version     = Field(field_type=str)
    repository  = Field(field_type=str)

    sections    = FChildren(type_info=Model.SECTION)


Model._MODEL_MAP[Model.DOCUMENT] = DocumentModel


class SectionModel(Model):
    model       = Field(field_type=str, default=Model.SECTION)
    name        = Field(field_type=str, obligatory=True)
    type        = Field(field_type=str)
    reference   = Field(field_type=str)
    description = Field(field_type=str)
    definition  = Field(field_type=str)
    link        = Field(field_type=str)
    include     = Field(field_type=str)
    repository  = Field(field_type=str)
    mapping     = Field(field_type=str)

    document      = FParent(type_info=Model.DOCUMENT)
    section     = FParent(type_info=Model.SECTION)
    sections    = FChildren(type_info=Model.SECTION)
    properties  = FChildren(type_info=Model.PROPERTY)
    blocks      = FChildren(type_info=Model.BLOCK)

Model._MODEL_MAP[Model.SECTION] = SectionModel


class PropertyModel(Model):
    model       = Field(field_type=str, default=Model.PROPERTY)
    name        = Field(field_type=str, obligatory=True)
    definition  = Field(field_type=str)
    mapping     = Field(field_type=str)
    dependency  = Field(field_type=str)
    dependencyvalue = Field(field_type=str)

    parent      = FParent(type_info=Model.SECTION, name_mapping="section")
    values      = FChildren(type_info=Model.VALUE, obligatory=True)

Model._MODEL_MAP[Model.PROPERTY] = PropertyModel


class ValueModel(Model):
    model       = Field(field_type=str, default=Model.VALUE)
    data        = Field(field_type=str, obligatory=True)
    uncertainty     = Field(field_type=str)
    unit            = Field(field_type=str)
    reference       = Field(field_type=str)
    definition      = Field(field_type=str)
    filename        = Field(field_type=str)
    encoder         = Field(field_type=str)
    checksum        = Field(field_type=str)

    parent          = FParent(type_info=Model.PROPERTY, name_mapping="property")

Model._MODEL_MAP[Model.VALUE] = ValueModel


class BlockModel(Model):
    model       = Field(field_type=str, default=Model.BLOCK)
    name        = Field(field_type=str)
    index       = Field(field_type=int, default=0)
    description = Field(field_type=str)

    section                = FParent(type_info=Model.SECTION)
    recordingchannelgroups = FChildren(type_info=Model.RECORDINGCHANNELGROUP)
    segments               = FChildren(type_info=Model.SEGMENT)
    section               = FParent(type_info=Model.SECTION, name_mapping="metadata")

Model._MODEL_MAP[Model.BLOCK] = BlockModel


class SegmentModel(Model):
    model       = Field(field_type=str, default=Model.SEGMENT)
    name        = Field(field_type=str)
    index       = Field(default=0)

    block       = FParent(type_info=Model.BLOCK)

    analogsignals             = FChildren(type_info=Model.ANALOGSIGNAL)
    irregularlysampledsignals = FChildren(type_info=Model.IRREGULARLYSAMPLEDSIGNAL)
    analogsignalarrays        = FChildren(type_info=Model.ANALOGSIGNALARRAY)
    spiketrains               = FChildren(type_info=Model.SPIKETRAIN)
    spikes                    = FChildren(type_info=Model.SPIKE)
    events                    = FChildren(type_info=Model.EVENT)
    eventarrays               = FChildren(type_info=Model.EVENTARRAY)
    epochs                    = FChildren(type_info=Model.EPOCH)
    epocharrays               = FChildren(type_info=Model.EPOCHARRAY)
    section                  = FParent(type_info=Model.SECTION, name_mapping="metadata")

Model._MODEL_MAP[Model.SEGMENT] = SegmentModel


class EventArrayModel(Model):
    model       = Field(field_type=str, default=Model.EVENTARRAY)
    name        = Field(field_type=str)
    description = Field(field_type=str)

    labels      = FDatafile(obligatory=True)
    times       = FDatafile(obligatory=True)

    segment     = FParent(type_info=Model.SEGMENT)
    section    = FParent(type_info=Model.SECTION, name_mapping="metadata")

Model._MODEL_MAP[Model.EVENTARRAY] = EventArrayModel


class EventModel(Model):
    model       = Field(field_type=str, default=Model.EVENT)
    name        = Field(field_type=str)
    description = Field(field_type=str)
    label       = Field(obligatory=True, field_type=str, default="")

    time        = FQuantity(obligatory=True)

    segment     = FParent(type_info=Model.SEGMENT)
    section    = FParent(type_info=Model.SECTION, name_mapping="metadata")

Model._MODEL_MAP[Model.EVENT] = EventModel


class EpochArrayModel(Model):
    model       = Field(field_type=str, default=Model.EPOCHARRAY)
    name        = Field(field_type=str)
    description = Field(field_type=str)
    labels      = FDatafile(obligatory=True)

    times       = FDatafile(obligatory=True)
    durations   = FDatafile(obligatory=True)

    segment     = FParent(type_info=Model.SEGMENT)
    section    = FParent(type_info=Model.SECTION, name_mapping="metadata")

Model._MODEL_MAP[Model.EPOCHARRAY] = EpochArrayModel


class EpochModel(Model):
    model       = Field(field_type=str, default=Model.EPOCH)
    name        = Field(field_type=str)
    description = Field(field_type=str)
    label       = Field(obligatory=True, field_type=str, default="")

    time        = FQuantity(obligatory=True)
    duration    = FQuantity(obligatory=True)

    segment     = FParent(type_info=Model.SEGMENT)
    section    = FParent(type_info=Model.SECTION, name_mapping="metadata")

Model._MODEL_MAP[Model.EPOCH] = EpochModel


class RecordingChannelGroupModel(Model):
    model       = Field(field_type=str, default=Model.RECORDINGCHANNELGROUP)
    name        = Field(field_type=str)
    description = Field(field_type=str)

    block       = FParent(type_info=Model.BLOCK)
    units       = FChildren(type_info=Model.UNIT)
    recordingchannels   = FChildren(type_info=Model.RECORDINGCHANNEL)
    analogsignalarrays  = FChildren(type_info=Model.ANALOGSIGNALARRAY)
    section    = FParent(type_info=Model.SECTION, name_mapping="metadata")

Model._MODEL_MAP[Model.RECORDINGCHANNELGROUP] = RecordingChannelGroupModel


class RecordingChannelModel(Model):
    model       = Field(field_type=str, default=Model.RECORDINGCHANNEL)
    name        = Field(field_type=str)
    description = Field(field_type=str)
    index       = Field(field_type=int, default=0)

    recordingchannelgroups    = FChildren(type_info=Model.RECORDINGCHANNELGROUP, name_mapping="recordingchannelgroup")
    analogsignals             = FChildren(type_info=Model.ANALOGSIGNAL)
    irregularlysampledsignals = FChildren(type_info=Model.IRREGULARLYSAMPLEDSIGNAL)
    section                  = FParent(type_info=Model.SECTION, name_mapping="metadata")

Model._MODEL_MAP[Model.RECORDINGCHANNEL] = RecordingChannelModel


class UnitModel(Model):
    model       = Field(field_type=str, default=Model.UNIT)
    name        = Field(field_type=str)
    description = Field(field_type=str)

    recordingchannelgroup   = FParent(type_info=Model.RECORDINGCHANNELGROUP)
    spikes                  = FChildren(type_info=Model.SPIKE)
    spiketrains             = FChildren(type_info=Model.SPIKETRAIN)
    section                = FParent(type_info=Model.SECTION, name_mapping="metadata")

Model._MODEL_MAP[Model.UNIT] = UnitModel


class SpikeTrainModel(Model):
    model       = Field(field_type=str, default=Model.SPIKETRAIN)
    name        = Field(field_type=str)
    description = Field(field_type=str)

    t_start     = FQuantity(obligatory=True)
    t_stop      = FQuantity(obligatory=True)
    times       = FDatafile(obligatory=True)
    waveforms   = FDatafile()

    unit        = FParent(type_info=Model.UNIT)
    segment     = FParent(type_info=Model.SEGMENT)
    section    = FParent(type_info=Model.SECTION, name_mapping="metadata")

Model._MODEL_MAP[Model.SPIKETRAIN] = SpikeTrainModel


class SpikeModel(Model):
    model       = Field(field_type=str, default=Model.SPIKE)
    name        = Field(field_type=str)
    description = Field(field_type=str)

    time            = FQuantity(obligatory=True)
    left_sweep      = FQuantity()
    sampling_rate   = FQuantity()
    waveform        = FDatafile()

    unit        = FParent(type_info=Model.UNIT)
    segment     = FParent(type_info=Model.SEGMENT)
    section    = FParent(type_info=Model.SECTION, name_mapping="metadata")

Model._MODEL_MAP[Model.SPIKE] = SpikeModel


class AnalogsignalArrayModel(Model):
    model       = Field(field_type=str, default=Model.ANALOGSIGNALARRAY)
    name        = Field(field_type=str)
    description = Field(field_type=str)

    t_start         = FQuantity()
    sampling_rate   = FQuantity(obligatory=True)
    signal          = FDatafile(obligatory=True)

    segment                 = FParent(type_info=Model.SEGMENT)
    recordingchannelgroup   = FParent(type_info=Model.RECORDINGCHANNELGROUP)
    section                = FParent(type_info=Model.SECTION, name_mapping="metadata")

Model._MODEL_MAP[Model.ANALOGSIGNALARRAY] = AnalogsignalArrayModel


class AnalogsignalModel(Model):
    model       = Field(field_type=str, default=Model.ANALOGSIGNAL)
    name        = Field(field_type=str)
    description = Field(field_type=str)

    t_start         = FQuantity()
    sampling_rate   = FQuantity(obligatory=True)
    signal          = FDatafile(obligatory=True)

    segment          = FParent(type_info=Model.SEGMENT)
    recordingchannel = FParent(type_info=Model.RECORDINGCHANNEL)
    section         = FParent(type_info=Model.SECTION, name_mapping="metadata")

Model._MODEL_MAP[Model.ANALOGSIGNAL] = AnalogsignalModel


class IrregularlySampledSignalModel(Model):
    model       = Field(field_type=str, default=Model.IRREGULARLYSAMPLEDSIGNAL)
    name        = Field(field_type=str)
    description = Field(field_type=str)

    t_start     = FQuantity(obligatory=True)
    signal      = FDatafile(obligatory=True)
    times       = FDatafile(obligatory=True)

    segment          = FParent(type_info=Model.SEGMENT)
    recordingchannel = FParent(type_info=Model.RECORDINGCHANNEL)
    section         = FParent(type_info=Model.SECTION, name_mapping="metadata")

Model._MODEL_MAP[Model.IRREGULARLYSAMPLEDSIGNAL] = IrregularlySampledSignalModel
