import errno

class UserUnsubscribet():
    """Вызывается, когда юзер пытается подписаться, хотя уже подписан"""
    pass
class UserSubscribet():
    """Вызывается, когда юзер пытается отписаться, хотя уже одписан"""
    pass
class UserSubscribNotFound():
    """Вызывается, когда юзер не найден в подписках"""
    pass
