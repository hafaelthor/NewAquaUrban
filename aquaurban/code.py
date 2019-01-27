import enum

class UserPermissionCode (enum.Enum):
	DUMMY 		= 0
	COMMON 		= 1
	SUPERVISOR 	= 2

class ActorCode (enum.Enum):
	LED		= 0
	FEEDER 	= 1

FEATURE_PERMISSION_TRESHOLD = {
	'bio': UserPermissionCode.DUMMY,
	'act': UserPermissionCode.COMMON
}