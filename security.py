
#from werkzeug.security import safe_str_cmp
import hmac
from models.user import UserModel

#users = [User(1, 'bob', 'asdf')]
         
#username_mapping = {u.username: u for u in users}
#userid_mapping = {u.id : u for u in users}
def safe_str_cmp(a: str, b: str) -> bool:
     """This function compares strings in somewhat constant time. This
      requires that the length of at least one string is known in advance.

       Returns `True` if the two strings are equal, or `False` if they are not.
      """

     if isinstance(a, str):
        a = a.encode("utf-8")  # type: ignore
     if isinstance(b, str):
        b = b.encode("utf-8")  # type: ignore

     return hmac.compare_digest(a, b)
 
def authenticate(username, password):
#    user = username_mapping.get(username, None)
    user = UserModel.find_by_username(username)
    print("In authenticate")
    if user and safe_str_cmp(user.password, password):
        return user
def identity(payload):
    user_id = payload['identity']
    print("In identity")
#    return userid_mapping.get(user_id, None)
    return UserModel.find_by_id(user_id)