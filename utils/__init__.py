from .utils import *


SOFTWARE_ENGINEERING = 'Інженерія програмного забезпечення'
COMPUTER_SCIENCE = "Комп'ютерні науки та інформаційні технології"
APPLIED_MATHEMATICS = 'Прикладна математика'
SYSTEM_ANALYSIS = 'Системний аналіз'


SPECIALTIES = [SOFTWARE_ENGINEERING, COMPUTER_SCIENCE, APPLIED_MATHEMATICS, SYSTEM_ANALYSIS]

STREAMS = [Stream(specialty, course) for specialty in SPECIALTIES for course in range(1, 7)]