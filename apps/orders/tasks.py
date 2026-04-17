from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import logging

logger = logging.getLogger(__name__)


@shared_task
def broadcast_order_update(group_name, event_type, order_id, order_status, message):
    """
    Send a WebSocket message to a channel.
    """
    try:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": event_type,
                "order_id": order_id,
                "status": order_status,
                "message": message,
            }
        )
        logger.info(f"broadcast_order_update for group={group_name}")

    except Exception as exc:
        logger.error(f"broadcast_order_update failed for group={group_name}: {exc}")

@shared_task
def broadcast_new_order(group_name, event_type, order_id, message):
    """
    Send a WebSocket message to a channel.
    """
    try:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": event_type,
                "order_id": order_id,
                "message": message,
            }
        )
    except Exception as exc:
        logger.error(f"broadcast_order_update failed for group={group_name}: {exc}")
