class DomainError(Exception):
    """Base class for all domain exceptions"""
    def __init__(self, message, code):
        self.message = message
        self.code = code
        super().__init__(message)


class OrderNotFound(DomainError):
    def __init__(self, order_number):
        super().__init__(
            f"Order {order_number} not found",
            "ORDER_NOT_FOUND"
        )


class InvalidOrderStatus(DomainError):
    def __init__(self, current_status, new_status):
        super().__init__(
            f"Cannot transition from {current_status} to {new_status}",
            "INVALID_STATUS_TRANSITION"
        )


class OrderCannotBeCancelled(DomainError):
    def __init__(self, order_number):
        super().__init__(
            f"Order {order_number} cannot be cancelled in its current state",
            "ORDER_CANNOT_BE_CANCELLED"
        )


class DriverCannotCancelOrder(DomainError):
    def __init__(self):
        super().__init__(
            "Drivers are not permitted to cancel orders",
            "DRIVER_CANCEL_FORBIDDEN"
        )


class NoAvailableDriver(DomainError):
    def __init__(self):
        super().__init__(
            "No available driver found at this time",
            "NO_AVAILABLE_DRIVER"
        )


class CartEmpty(DomainError):
    def __init__(self):
        super().__init__(
            "Your cart is empty",
            "CART_EMPTY"
        )


class MinimumOrderNotMet(DomainError):
    def __init__(self, minimum):
        super().__init__(
            f"Minimum order amount is {minimum}",
            "MINIMUM_ORDER_NOT_MET"
        )

class WrongDeliveryAddress(DomainError):
    def __init__(self, address):
        super().__init__(
            f"This {address} does not belongs to you",
            "WORONG_DELIVERY_ADDRESS"
        )

class NotValidAction(DomainError):
    def __init__(self, user_type,action):
        super().__init__(
            f"{user_type} can not change to {action} status ",
            "NOT_VALID_STATUS"
        )

class CanNotPerformAction(DomainError):
    def __init__(self,):
        super().__init__(
            f"You can not do more actions",
            "CAN_NOT_PERFORM_ACTIONS"
        )