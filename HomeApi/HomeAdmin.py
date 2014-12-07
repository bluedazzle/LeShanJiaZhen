from HomeApi.models import *
import json
from HomeApi.errorType import *


def add_homeitem_p(item_name):
    try:
        if len(HomeItem_P.objects.filter(item_name=item_name)) != 0:
            raise AlreadyExitError
        p = HomeItem_P(item_name=item_name)
        p.save()
        status = 1
    except AlreadyExitError:
        status = 6
    except Exception:
        status = 2
    return status


def del_homeitem_p(item_name):
    try:
        if len(HomeItem_P.objects.filter(item_name=item_name)) == 0:
            raise NoneExistError
        p = HomeItem_P.objects.get(item_name=item_name)
        p.delete()
        status = 1
    except NoneExistError:
        status = 7
    except Exception:
        status = 2
    return status


def change_homeitem_p(item_name, new_item_name):
    try:
        if len(HomeItem_P.objects.filter(item_name=item_name)) == 0:
            raise NoneExistError
        if len(HomeItem_P.objects.filter(item_name=new_item_name)) != 0:
            raise AlreadyExitError
        HomeItem_P.objects.get(item_name=item_name).update(item_name=new_item_name)
        status = 1
    except NoneExistError:
        status = 7
    except AlreadyExitError:
        status = 6
    except Exception:
        status = 2
    return status


def add_homeitem_o(item_name, parent_item):
    try:
        if len(HomeItem_O.objects.filter(item_name=item_name)) != 0:
            raise AlreadyExitError
        if len(HomeItem_P.objects.filter(item_name=parent_item)) == 0:
            raise NoneExistError
        p = HomeItem_O(item_name=item_name)
        p_parent = HomeItem_P.objects.get(item_name=parent_item)
        p.parent_item = p_parent
        p.save()
        status = 1
    except AlreadyExitError:
        status = 6
    except NoneExistError:
        status = 7
    except Exception:
        status = 2
    return status


def del_homeitem_o(item_name):
    try:
        if len(HomeItem_O.objects.filter(item_name=item_name)) == 0:
            raise NoneExistError
        p = HomeItem_O.objects.get(item_name=item_name)
        p.delete()
        status = 1
    except NoneExistError:
        status = 7
    except Exception:
        status = 2
    return status


def change_homeitem_o(item_name, new_item_name, parent_item):
    try:
        if len(HomeItem_O.objects.filter(item_name=item_name)) == 0:
            raise NoneExistError
        if len(HomeItem_O.objects.filter(item_name=new_item_name)) != 0:
            raise AlreadyExitError
        if len(HomeItem_P.objects.filter(item_name=parent_item)) == 0:
            raise NoneExistError
        p_parent = HomeItem_P.objects.get(item_name=parent_item)
        HomeItem_O.objects.filter(item_name=item_name).update(item_name=new_item_name, parent_item=p_parent)
        status = 1
    except NoneExistError:
        status = 7
    except AlreadyExitError:
        status = 6
    except Exception:
        status = 2
    return status


def add_homeitem(title, content, parent_item):
    try:
        if len(HomeItem.objects.filter(title=title)) != 0:
            raise AlreadyExitError
        if len(HomeItem_O.objects.filter(item_name=parent_item)) == 0:
            raise NoneExistError
        p_parent = HomeItem_O.objects.get(item_name=parent_item)
        p = HomeItem(title=title, content=content)
        p.parent_item = p_parent
        p.save()
        status = 1
    except AlreadyExitError:
        status = 6
    except NoneExistError:
        status = 7
    except Exception:
        status = 2
    return status


def del_homeitem(title):
    try:
        if len(HomeItem.objects.filter(title=title)) == 0:
            raise NoneExistError
        p = HomeItem.objects.get(title=title)
        p.delete()
        status = 1
    except NoneExistError:
        status = 7
    except Exception:
        status = 2
    return status


def change_homeitem(title, new_title, content, parent_item):
    try:
        if len(HomeItem.objects.filter(title=title)) == 0:
            raise NoneExistError
        if len(HomeItem.objects.filter(title=new_title)) != 0:
            raise AlreadyExitError
        if len(HomeItem_O.objects.filter(item_name=parent_item)) == 0:
            raise NoneExistError
        p_parent = HomeItem_O.objects.get(item_name=parent_item)
        HomeItem.objects.filter(title=title).update(title=new_title, content=content, parent_item=p_parent)
        status = 1
    except NoneExistError:
        status = 7
    except AlreadyExitError:
        status = 6
    except Exception:
        status = 2
    return status






