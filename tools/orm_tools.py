try:
    from api.models import IndividualUser, ProfessionalUser, CorporateUser
except ImportError as exception:
    print("%s - Please install the necessary libraries." % exception)
    sys.exit(0)

def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None

def user_exist(user_id):
    """
    Check if user exist in DB with specific user_id.
    Args:
        user_id - given user_id for checking if user exists.
    Returns:
        user(if exists)/error(if does not exist)
    """
    if get_or_none(IndividualUser, user_id=user_id):
        return IndividualUser.objects.get(user_id=user_id)
    elif get_or_none(ProfessionalUser, user_id=user_id):
        return ProfessionalUser.objects.get(user_id=user_id)
    elif get_or_none(CorporateUser, user_id=user_id):
        return CorporateUser.objects.get(user_id=user_id)
    else:
        return None
