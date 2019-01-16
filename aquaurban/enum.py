import enum

class UserPermissionCode (enum.Enum):
	DUMMY 		= 0
	COMMON 		= 1
	SUPERVISOR 	= 2

class ActionCode (enum.Enum):
	LED_ON 	= 0
	LED_OFF = 1