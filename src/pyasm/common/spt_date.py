###########################################################
#
# Copyright (c) 2005, Southpaw Technology
#                     All Rights Reserved
#
# PROPRIETARY INFORMATION.  This software is proprietary to
# Southpaw Technology, and is not to be reproduced, transmitted,
# or disclosed in any way without written permission.
#
#
#
import tacticenv

__all__ = ['SPTDate']


from datetime import datetime, timedelta
from dateutil import parser
from dateutil.tz import *

TZLOCAL = tzlocal()
TZUTC = tzutc()
TZGMT = gettz('GMT')

class SPTDate(object):

    def now(cls):
        # utcnow is already converted to GMT
        date = datetime.utcnow()
        date = date.replace(tzinfo=TZGMT)
        date = cls.convert(date)
        return date
    now = classmethod(now)

    def today(cls):
        date = datetime.today()
        return cls.convert(date)
    today = classmethod(today)


    def start_of_today(cls):
        today = datetime.today()
        today = cls.convert(today)
        today = datetime(today.year, today.month, today.day)
        return today
    start_of_today = classmethod(start_of_today)


    def timedelta(cls, **kwargs):
        delta = timedelta(**kwargs)
        return delta
    timedelta = classmethod(timedelta)

    def parse(cls, expression):
        date = parser.parse(expression)
        date = cls.convert(date)
        return date
    parse = classmethod(parse)



    def convert_to_local(cls, date):
        '''convert a time to local time with timezone'''
        if not date:
            return None

        if isinstance(date, basestring):
            try:
                date = parser.parse(date)
            except:
                # This could be "now()", for example
                return date

        if date.tzinfo == None:
            # assume GMT
            date = date.replace(tzinfo=TZGMT)

        #NOTE: it errors out on time before epoch
        try:    
            local = date.astimezone(TZLOCAL)
        except:
            local = date.replace(tzinfo=None)

        return local
    convert_to_local = classmethod(convert_to_local)



    def convert_to_timezone(cls, date, timezone):
        '''convert a time to local time with timezone'''
        if not date:
            return None

        if isinstance(date, basestring):
            try:
                date = parser.parse(date)
            except:
                # This could be "now()", for example
                return date

        if date.tzinfo == None:
            # assume GMT
            date = date.replace(tzinfo=TZGMT)

        TZ = gettz(timezone)
        
        date = date.astimezone(TZ)
        return date
    convert_to_timezone = classmethod(convert_to_timezone)




    # convert to UTC, no timezone.  If no timezone is given in the date, use local
    def convert(cls, date, is_gmt=False):
        if date == "CURRENT_TIMESTAMP":
            date = datetime.utcnow()

        elif isinstance(date, basestring):
            # parse and convert 
            date = parser.parse(date)

        # set the timezone to UTC
        if not is_gmt and date.tzinfo == None:
            # assume local timezone if none is given
            date = date.replace(tzinfo=TZLOCAL)
        else:
            offset = date.utcoffset()
            if offset:
                date = date - date.utcoffset()
            date = date.replace(tzinfo=TZGMT)
        
        #FIXME: it errors out on time before epoch
        try:
            utc = date.astimezone(TZUTC)
        except Exception, e:
            naive = date.replace(tzinfo=None)
        else:
            naive = utc.replace(tzinfo=None)
        return naive

    convert = classmethod(convert)


    def add_gmt_timezone(cls, date):
        if isinstance(date, basestring):
            try:
                # do not use cls.parse ... it does a convert.
                date = parser.parse(date)
            except:
                # This could be "now()", for example
                return date

        date = date.replace(tzinfo=TZGMT)
        return date
    add_gmt_timezone = classmethod(add_gmt_timezone)


    def add_local_timezone(cls, date):
        if isinstance(date, basestring):
            try:
                # do not use cls.parse ... it does a convert.
                date = parser.parse(date)
            except:
                # This could be "now()", for example
                return date

        date = date.replace(tzinfo=TZLOCAL)
        return date
    add_local_timezone = classmethod(add_local_timezone)

    def add_timezone(cls, date, timezone):
        '''add an arbitrary timezone without affecting the value'''
        if isinstance(date, basestring):
            try:
                # do not use cls.parse ... it does a convert.
                date = parser.parse(date)
            except:
                # This could be "now()", for example
                return date
        new_tz = gettz(timezone)

        date = date.replace(tzinfo=new_tz)
        return date
    add_timezone = classmethod(add_timezone)


    def has_timezone(cls, date):
        err = False
        
        if isinstance(date, basestring):
            try:
                # do not use cls.parse ... it does a convert.
                date = parser.parse(date)
            except:
                # This could be "now()", for example
                err = True
                pass
        if err:
            return False
        else:
            return date.tzinfo != None
    has_timezone = classmethod(has_timezone)
 

    def get_display_date(cls, date):
        '''convert to local timezone'''
        pass



    def get_time_ago(cls, date):

        if isinstance(date, basestring):
            date = parser.parse(date)

        now = cls.now()

        diff = now - date

        # less than a minute
        if diff.seconds < 60:
            value = "%s seconds ago" % diff.seconds

        # less than an hour
        elif diff.seconds < 60 * 60:
            minutes = diff.seconds / 60
            if minutes == 1:
                value = "1 minute ago"
            else:
                value = "%s minutes ago" % minutes

        # less than a day
        elif diff.seconds < 60 * 60 * 24:
            hours = diff.seconds / 60 /60
            if hours == 1:
                value = "1 hour ago"
            else:
                value = "%s hours ago" % hours


        else:
            value = date.strftime("%b %d at %I:%m %p")

        return value

    get_time_ago = classmethod(get_time_ago)


if __name__ == '__main__':


    date = SPTDate.now() - timedelta(minutes=500.23)

    print SPTDate.get_time_ago(date)





