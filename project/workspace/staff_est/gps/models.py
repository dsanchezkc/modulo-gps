# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from __future__ import unicode_literals

from django.contrib.gis.db import models

class Attributes(models.Model):
    description = models.CharField(max_length=4000)
    type = models.CharField(max_length=128)
    attribute = models.CharField(max_length=128)
    expression = models.CharField(max_length=4000)

    class Meta:
        managed = False
        db_table = 'attributes'

class Calendars(models.Model):
    name = models.CharField(max_length=128)
    attributes = models.CharField(max_length=4000)
    data = models.BinaryField()

    class Meta:
        managed = False
        db_table = 'calendars'

class Commands(models.Model):
    description = models.CharField(max_length=4000)
    type = models.CharField(max_length=128)
    textchannel = models.BooleanField()
    attributes = models.CharField(max_length=4000)

    class Meta:
        managed = False
        db_table = 'commands'

# class Databasechangelog(models.Model):
#     id = models.CharField(max_length=255)
#     author = models.CharField(max_length=255)
#     filename = models.CharField(max_length=255)
#     dateexecuted = models.DateTimeField()
#     orderexecuted = models.IntegerField()
#     exectype = models.CharField(max_length=10)
#     md5sum = models.CharField(max_length=35, blank=True, null=True)
#     description = models.CharField(max_length=255, blank=True, null=True)
#     comments = models.CharField(max_length=255, blank=True, null=True)
#     tag = models.CharField(max_length=255, blank=True, null=True)
#     liquibase = models.CharField(max_length=20, blank=True, null=True)
#     contexts = models.CharField(max_length=255, blank=True, null=True)
#     labels = models.CharField(max_length=255, blank=True, null=True)
#     deployment_id = models.CharField(max_length=10, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'databasechangelog'

class Databasechangeloglock(models.Model):
    id = models.IntegerField(primary_key=True)
    locked = models.BooleanField()
    lockgranted = models.DateTimeField(blank=True, null=True)
    lockedby = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'databasechangeloglock'


class DeviceAttribute(models.Model):
    deviceid = models.ForeignKey('Devices', models.DO_NOTHING, db_column='deviceid')
    attributeid = models.ForeignKey(Attributes, models.DO_NOTHING, db_column='attributeid')

    class Meta:
        managed = False
        db_table = 'device_attribute'


class DeviceCommand(models.Model):
    deviceid = models.ForeignKey('Devices', models.DO_NOTHING, db_column='deviceid')
    commandid = models.ForeignKey(Commands, models.DO_NOTHING, db_column='commandid')

    class Meta:
        managed = False
        db_table = 'device_command'


class DeviceDriver(models.Model):
    deviceid = models.ForeignKey('Devices', models.DO_NOTHING, db_column='deviceid')
    driverid = models.ForeignKey('Drivers', models.DO_NOTHING, db_column='driverid')

    class Meta:
        managed = False
        db_table = 'device_driver'


class DeviceGeofence(models.Model):
    deviceid = models.ForeignKey('Devices', models.DO_NOTHING, db_column='deviceid')
    geofenceid = models.ForeignKey('Geofences', models.DO_NOTHING, db_column='geofenceid')

    class Meta:
        managed = False
        db_table = 'device_geofence'


class DeviceMaintenance(models.Model):
    deviceid = models.ForeignKey('Devices', models.DO_NOTHING, db_column='deviceid')
    maintenanceid = models.ForeignKey('Maintenances', models.DO_NOTHING, db_column='maintenanceid')

    class Meta:
        managed = False
        db_table = 'device_maintenance'


class DeviceNotification(models.Model):
    deviceid = models.ForeignKey('Devices', models.DO_NOTHING, db_column='deviceid')
    notificationid = models.ForeignKey('Notifications', models.DO_NOTHING, db_column='notificationid')

    class Meta:
        managed = False
        db_table = 'device_notification'


class Devices(models.Model):
    name = models.CharField(max_length=128)
    uniqueid = models.CharField(unique=True, max_length=128)
    lastupdate = models.DateTimeField(blank=True, null=True)
    positionid = models.IntegerField(blank=True, null=True)
    groupid = models.ForeignKey('Groups', models.DO_NOTHING, db_column='groupid', blank=True, null=True)
    attributes = models.CharField(max_length=4000, blank=True, null=True)
    phone = models.CharField(max_length=128, blank=True, null=True)
    model = models.CharField(max_length=128, blank=True, null=True)
    contact = models.CharField(max_length=512, blank=True, null=True)
    category = models.CharField(max_length=128, blank=True, null=True)
    disabled = models.NullBooleanField()

    class Meta:
        managed = False
        db_table = 'devices'


class Drivers(models.Model):
    name = models.CharField(max_length=128)
    uniqueid = models.CharField(unique=True, max_length=128)
    attributes = models.CharField(max_length=4000)

    class Meta:
        managed = False
        db_table = 'drivers'

class Events(models.Model):
    type = models.CharField(max_length=128)
    servertime = models.DateTimeField()
    deviceid = models.ForeignKey(Devices, models.DO_NOTHING, db_column='deviceid', blank=True, null=True)
    positionid = models.IntegerField(blank=True, null=True)
    geofenceid = models.IntegerField(blank=True, null=True)
    attributes = models.CharField(max_length=4000, blank=True, null=True)
    maintenanceid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'events'


class Geofences(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=128, blank=True, null=True)
    area = models.CharField(max_length=4096)
    attributes = models.CharField(max_length=4000, blank=True, null=True)
    calendarid = models.ForeignKey(Calendars, models.DO_NOTHING, db_column='calendarid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'geofences'

class GroupAttribute(models.Model):
    groupid = models.ForeignKey('Groups', models.DO_NOTHING, db_column='groupid')
    attributeid = models.ForeignKey(Attributes, models.DO_NOTHING, db_column='attributeid')

    class Meta:
        managed = False
        db_table = 'group_attribute'

class GroupCommand(models.Model):
    groupid = models.ForeignKey('Groups', models.DO_NOTHING, db_column='groupid')
    commandid = models.ForeignKey(Commands, models.DO_NOTHING, db_column='commandid')

    class Meta:
        managed = False
        db_table = 'group_command'


class GroupDriver(models.Model):
    groupid = models.ForeignKey('Groups', models.DO_NOTHING, db_column='groupid')
    driverid = models.ForeignKey(Drivers, models.DO_NOTHING, db_column='driverid')

    class Meta:
        managed = False
        db_table = 'group_driver'


class GroupGeofence(models.Model):
    groupid = models.ForeignKey('Groups', models.DO_NOTHING, db_column='groupid')
    geofenceid = models.ForeignKey(Geofences, models.DO_NOTHING, db_column='geofenceid')

    class Meta:
        managed = False
        db_table = 'group_geofence'


class GroupMaintenance(models.Model):
    groupid = models.ForeignKey('Groups', models.DO_NOTHING, db_column='groupid')
    maintenanceid = models.ForeignKey('Maintenances', models.DO_NOTHING, db_column='maintenanceid')

    class Meta:
        managed = False
        db_table = 'group_maintenance'


class GroupNotification(models.Model):
    groupid = models.ForeignKey('Groups', models.DO_NOTHING, db_column='groupid')
    notificationid = models.ForeignKey('Notifications', models.DO_NOTHING, db_column='notificationid')

    class Meta:
        managed = False
        db_table = 'group_notification'

class Groups(models.Model):
    name = models.CharField(max_length=128)
    groupid = models.ForeignKey('self', models.DO_NOTHING, db_column='groupid', blank=True, null=True)
    attributes = models.CharField(max_length=4000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'groups'


class Maintenances(models.Model):
    name = models.CharField(max_length=4000)
    type = models.CharField(max_length=128)
    start = models.FloatField()
    period = models.FloatField()
    attributes = models.CharField(max_length=4000)

    class Meta:
        managed = False
        db_table = 'maintenances'


class Notifications(models.Model):
    type = models.CharField(max_length=128)
    attributes = models.CharField(max_length=4000, blank=True, null=True)
    web = models.NullBooleanField()
    mail = models.NullBooleanField()
    sms = models.NullBooleanField()
    always = models.BooleanField()
    calendarid = models.ForeignKey(Calendars, models.DO_NOTHING, db_column='calendarid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'notifications'


class Positions(models.Model):
    protocol = models.CharField(max_length=128, blank=True, null=True)
    deviceid = models.ForeignKey(Devices, models.DO_NOTHING, db_column='deviceid')
    servertime = models.DateTimeField()
    devicetime = models.DateTimeField()
    fixtime = models.DateTimeField()
    valid = models.BooleanField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    altitude = models.FloatField()
    speed = models.FloatField()
    course = models.FloatField()
    address = models.CharField(max_length=512, blank=True, null=True)
    attributes = models.CharField(max_length=4000, blank=True, null=True)
    accuracy = models.FloatField()
    network = models.CharField(max_length=4000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'positions'

class PositionsTraccar(models.Model):
    protocol = models.CharField(max_length=128, blank=True, null=True)
    deviceid = models.ForeignKey(Devices, models.DO_NOTHING, db_column='deviceid')  # Field name made lowercase.
    servertime = models.DateTimeField(db_column='servertime')  # Field name made lowercase.
    devicetime = models.DateTimeField(db_column='devicetime')  # Field name made lowercase.
    fixtime = models.DateTimeField(db_column='fixtime')  # Field name made lowercase.
    valid = models.BooleanField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    altitude = models.FloatField()
    speed = models.FloatField()
    course = models.FloatField()
    address = models.CharField(max_length=512, blank=True, null=True)
    attributes = models.CharField(max_length=4096)

    class Meta:
        managed = False
        db_table = 'positions'

    def __unicode__(self):
        return u"%s %s %s %s" % (self.id, self.deviceid, self.latitude, self.longitude)

class Servers(models.Model):
    registration = models.BooleanField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    zoom = models.IntegerField()
    map = models.CharField(max_length=128, blank=True, null=True)
    bingkey = models.CharField(max_length=128, blank=True, null=True)
    mapurl = models.CharField(max_length=512, blank=True, null=True)
    readonly = models.BooleanField()
    twelvehourformat = models.BooleanField()
    attributes = models.CharField(max_length=4000, blank=True, null=True)
    forcesettings = models.BooleanField()
    coordinateformat = models.CharField(max_length=128, blank=True, null=True)
    devicereadonly = models.NullBooleanField()
    limitcommands = models.NullBooleanField()
    poilayer = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'servers'

class Statistics(models.Model):
    capturetime = models.DateTimeField()
    activeusers = models.IntegerField()
    activedevices = models.IntegerField()
    requests = models.IntegerField()
    messagesreceived = models.IntegerField()
    messagesstored = models.IntegerField()
    attributes = models.CharField(max_length=4000)
    mailsent = models.IntegerField()
    smssent = models.IntegerField()
    geocoderrequests = models.IntegerField()
    geolocationrequests = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'statistics'


class UserAttribute(models.Model):
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='userid')
    attributeid = models.ForeignKey(Attributes, models.DO_NOTHING, db_column='attributeid')

    class Meta:
        managed = False
        db_table = 'user_attribute'


class UserCalendar(models.Model):
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='userid')
    calendarid = models.ForeignKey(Calendars, models.DO_NOTHING, db_column='calendarid')

    class Meta:
        managed = False
        db_table = 'user_calendar'


class UserCommand(models.Model):
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='userid')
    commandid = models.ForeignKey(Commands, models.DO_NOTHING, db_column='commandid')

    class Meta:
        managed = False
        db_table = 'user_command'


class UserDevice(models.Model):
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='userid')
    deviceid = models.ForeignKey(Devices, models.DO_NOTHING, db_column='deviceid')

    class Meta:
        managed = False
        db_table = 'user_device'

class UserDriver(models.Model):
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='userid')
    driverid = models.ForeignKey(Drivers, models.DO_NOTHING, db_column='driverid')

    class Meta:
        managed = False
        db_table = 'user_driver'


class UserGeofence(models.Model):
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='userid')
    geofenceid = models.ForeignKey(Geofences, models.DO_NOTHING, db_column='geofenceid')

    class Meta:
        managed = False
        db_table = 'user_geofence'


class UserGroup(models.Model):
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='userid')
    groupid = models.ForeignKey(Groups, models.DO_NOTHING, db_column='groupid')

    class Meta:
        managed = False
        db_table = 'user_group'


class UserMaintenance(models.Model):
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='userid')
    maintenanceid = models.ForeignKey(Maintenances, models.DO_NOTHING, db_column='maintenanceid')

    class Meta:
        managed = False
        db_table = 'user_maintenance'


class UserNotification(models.Model):
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='userid')
    notificationid = models.ForeignKey(Notifications, models.DO_NOTHING, db_column='notificationid')

    class Meta:
        managed = False
        db_table = 'user_notification'

# class UserUser(models.Model):
#     userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='userid')
#     manageduserid = models.ForeignKey('Users', models.DO_NOTHING, db_column='manageduserid')
#
#     class Meta:
#         managed = False
#         db_table = 'user_user'

class Users(models.Model):
    name = models.CharField(max_length=128)
    email = models.CharField(unique=True, max_length=128)
    hashedpassword = models.CharField(max_length=128, blank=True, null=True)
    salt = models.CharField(max_length=128, blank=True, null=True)
    readonly = models.BooleanField()
    administrator = models.BooleanField()
    map = models.CharField(max_length=128, blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    zoom = models.IntegerField()
    twelvehourformat = models.BooleanField()
    attributes = models.CharField(max_length=4000, blank=True, null=True)
    coordinateformat = models.CharField(max_length=128, blank=True, null=True)
    disabled = models.NullBooleanField()
    expirationtime = models.DateTimeField(blank=True, null=True)
    devicelimit = models.IntegerField(blank=True, null=True)
    token = models.CharField(max_length=128, blank=True, null=True)
    userlimit = models.IntegerField(blank=True, null=True)
    devicereadonly = models.NullBooleanField()
    phone = models.CharField(max_length=128, blank=True, null=True)
    limitcommands = models.NullBooleanField()
    login = models.CharField(max_length=128, blank=True, null=True)
    poilayer = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
