from .models import Membership

def _get_membership(user, organization):
    if not user.is_authenticated or not organization:
        return None
    try:
        return Membership.objects.get(user=user, organization=organization)
    except Membership.DoesNotExist:
        return None

def is_organization_owner(user, organization):
    membership = _get_membership(user, organization)
    return membership.role == Membership.ROLE_OWNER if membership else False

def is_organization_admin(user, organization):
    membership = _get_membership(user, organization)
    return membership.role == Membership.ROLE_ADMIN if membership else False

def is_organization_member(user, organization):
    membership = _get_membership(user, organization)
    return membership is not None

def can_view_organization(user, organization):
    """
    All members (including guests) can view the organization details.
    """
    return is_organization_member(user, organization)

def can_manage_organization(user, organization):
    """
    Owners and Admins can manage organization resources.
    """
    membership = _get_membership(user, organization)
    if not membership:
        return False
    return membership.role in [Membership.ROLE_OWNER, Membership.ROLE_ADMIN]

def can_manage_members(user, organization):
    """
    Only Owners and Admins can manage members.
    """
    return can_manage_organization(user, organization)

def can_manage_billing(user, organization):
    """
    Typically limited to Owners and potentially specialized billing roles,
    but here we allow Owners and Admins for simplicity.
    """
    return can_manage_organization(user, organization)

def can_view_project(user, project):
    """
    Users can view a project if they own it directly OR if it belongs
    to an organization they are a member of.
    """
    if not user.is_authenticated:
        return False

    if project.user == user:
        return True

    if project.organization:
        return is_organization_member(user, project.organization)

    return False

def can_manage_project(user, project):
    """
    Users can manage a project if they own it directly OR if it belongs
    to an organization where they have management rights.
    """
    if not user.is_authenticated:
        return False

    if project.user == user:
        return True

    if project.organization:
        return can_manage_organization(user, project.organization)

    return False
