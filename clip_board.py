



from collections import namedtuple
from functools import partial
from generics import compose
from f_generics import fcompose
from sources import lines_from
import re

pattern = rb'authen.+\(otp\)'
log_pattern = re.compile(
    rb"(?P<date>^[\w\d\: ]+\d{4})(?:: \[)"  # date
    rb"(?P<session>\d+)(?:\] )"  # session id
    rb"(?P<type>\w+ authen)(?: : id )"  # failed or passed authen attempt
    rb"(?P<id>\d+)(?:, )"  # ?
    rb"(?P<user>\S+)(?: in )"  # user id
    rb"(?P<customer>zmc|vgz|beh|unive)(?:, )"  # customer name
    rb"(?P<service>\w+)(?: \()"  # type of radius service
    rb"(?P<method>otp)(?:\))"  # authentication method - otp
)

log_struct = namedtuple('Log', 'date, session, type, id, user, customer, service, method')

source = lines_from('logs.txt')

logs = (log_struct(**re.match(log_pattern, log).groupdict()) for log in source if re.search(pattern, log))

filters = fcompose(
    lambda x: re.search(rb'authen.+\(otp\)', x),
)

maps = fcompose(
    lambda x: log_struct(**re.match(log_pattern, x).groupdict()),
)

print(list(logs))



